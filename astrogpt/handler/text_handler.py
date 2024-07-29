from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from astrogpt.llm.chains import parse_birthday_chain, menu_chain
from ..logger.logger import logger

from astrogpt.models.engine import engine
from astrogpt.models.user import User
from sqlalchemy.orm import Session
from astrogpt.handler.start_handler import handle_start

from astrogpt.handler.handle_birthday_input import handle_birthday_input
from astrogpt.bot_utils.send_daily_forecast import send_daily_forecast
from astrogpt.db_utils.update_user import update_user_birthday
from astrogpt.handler.subscribe_handler import handle_subscribe
from astrogpt.handler.unsubscribe_handler import handle_unsubscribe
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.send_unexpected_input_reply import send_unexpected_input_reply
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
from astrogpt.handler.llm_menu import handle_menu_with_llm


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
                chat.refresh_state(session)
                if user.date_of_birth_text is None:
                    logger.info("Birthday input %s", user_id)
                    await handle_birthday_input(session, user, chat)
                    logger.info("OK")
                else:
                    await handle_menu_with_llm(chat, user, session)

    except Exception as e:
        await send_critical_error(chat, str(e))
