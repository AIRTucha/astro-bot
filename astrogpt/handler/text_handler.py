from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from ..logger.logger import logger

from astrogpt.models.engine import engine
from astrogpt.models.user import User
from sqlalchemy.orm import Session

from astrogpt.bot_utils.send_welcome_message import (
    send_welcome_message,
)

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
from astrogpt.handler.llm_handlers.handle_menu_with_llm import handle_menu_with_llm

from astrogpt.handler.llm_handlers.handle_collect_data_data_with_llm import (
    handle_collect_data_data_with_llm,
)
from astrogpt.bot_utils.send_reply_to_user import send_reply_to_user
from astrogpt.db_utils.create_user import create_user


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
                create_user(session, chat)
                await send_welcome_message(chat)
                await handle_text(update, context)
                return

            chat.refresh_state(session)
            actions_take = await handle_menu_with_llm(chat, user, session)
            await send_reply_to_user(
                session=session,
                chat=chat,
                user=user,
                actions_taken=actions_take,
                user_input=user_input,
            )

    except Exception as e:
        await send_critical_error(chat, str(e))
