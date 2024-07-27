from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from astrogpt.models.engine import engine
from sqlalchemy.orm import Session
from astrogpt.logger.logger import logger
from astrogpt.db_utils.get_user import get_user_from_chat
from astrogpt.db_utils.create_user import create_user
from astrogpt.bot_utils.send_welcome_message import (
    send_welcome_message,
    send_welcome_again_message,
)
from astrogpt.bot_utils.send_critical_error import send_critical_error
from astrogpt.bot_utils.send_command_explanation_message import (
    send_command_explanation_message,
)

from astrogpt.bot_utils.reply_chat import ReplyChat


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = ReplyChat(update)
    try:
        with Session(engine) as session:
            user = get_user_from_chat(session, chat)
            user_id = chat.get_user_id()
            if user is None:
                logger.info("User %s id created", user_id)
                create_user(session, chat)

            logger.info("User %s started the bot", user_id)
            if user is None or user.date_of_birth_text is None:
                await send_welcome_message(chat)
            else:
                await send_welcome_again_message(user, chat)
                await send_command_explanation_message(chat)

    except Exception as e:
        await send_critical_error(chat, str(e))
