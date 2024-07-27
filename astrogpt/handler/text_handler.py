from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from astrogpt.llm.chains import (
    parse_birthday_chain,
)
from ..logger.logger import logger

from astrogpt.models.engine import engine
from astrogpt.models.user import User
from sqlalchemy.orm import Session
from astrogpt.handler.start_handler import handle_start
from astrogpt.bot_utils.send_daily_forecast import send_daily_forecast
from astrogpt.db_utils.update_user import update_user_birthday
from astrogpt.db_utils.get_user import get_user_from_chat
from astrogpt.bot_utils.language import get_language, get_subscribe, get_unsubscribe
from astrogpt.bot_utils.send_critical_error import send_critical_error
from astrogpt.bot_utils.send_command_explanation_message import (
    send_command_explanation_message,
)
from astrogpt.models.user import User
from astrogpt.db_utils.update_user import (
    update_user_birthday,
)

from astrogpt.bot_utils.send_unexpected_input_reply import send_unexpected_input_reply
from astrogpt.bot_utils.chat import Chat
from astrogpt.bot_utils.reply_chat import ReplyChat

from astrogpt.handler.subscribe_handler import handle_subscribe
from astrogpt.handler.unsubscribe_handler import handle_unsubscribe


async def handle_birthday_input(
    session: Session,
    user: User,
    chat: Chat,
) -> None:
    user_name = chat.get_user_name()
    user_input = chat.get_message_text()
    user_language = get_language(chat)
    user_id = chat.get_user_id()

    reply = parse_birthday_chain.invoke(
        {
            "user_name": user_name,
            "user_input": user_input,
            "user_language": user_language,
        }
    )
    if reply.extraction_error:
        logger.error(
            "User extraction error %s %s %s",
            user_id,
            user_input,
            reply.extraction_error,
        )
        await chat.send_text(reply.extraction_error)
    else:
        logger.info(
            "User birthday input %s %s %s",
            user_id,
            user_input,
            reply.birthday_text,
        )
        update_user_birthday(session, user, reply.birthday_text)
        logger.info("User %s birthday updated as %s", user_id, reply.birthday_text)
        await send_daily_forecast(user, chat)
        await send_command_explanation_message(chat)


def is_message_subscribe(chat: Chat) -> bool:
    return get_subscribe(chat).lower() == chat.get_message_text().lower()


def is_message_unsubscribe(chat: Chat) -> bool:
    return get_unsubscribe(chat).lower() == chat.get_message_text().lower()


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = ReplyChat(update)
    user_id = chat.get_user_id()
    user_input = chat.get_message_text()

    logger.info("User input %s: %s", user_id, user_input)
    try:
        with Session(engine) as session:
            user = get_user_from_chat(session, chat)
            if user is None:
                logger.info("User does to exist %s", user_id)
                await handle_start(update, context)
            else:
                if user.date_of_birth_text is None:
                    logger.info("Birthday input %s", user_id)
                    await handle_birthday_input(session, user, chat)
                else:
                    if is_message_subscribe(chat):
                        logger.info(
                            "User subscribed %s %s",
                            user_id,
                            user.daily_forecast,
                        )
                        await handle_subscribe(session, chat, user)
                    elif is_message_unsubscribe(chat):
                        logger.info(
                            "User unsubscribed %s %s",
                            user_id,
                            user.daily_forecast,
                        )
                        await handle_unsubscribe(session, chat, user)
                    else:
                        await send_unexpected_input_reply(chat)
    except Exception as e:
        await send_critical_error(chat, str(e))
