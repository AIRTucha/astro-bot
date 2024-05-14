from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from src.models.engine import engine
from sqlalchemy.orm import Session
from src.logger.logger import logger
from src.db_utils.get_user import get_user_from_chat
from src.db_utils.create_user import create_user
from src.bot_utils.send_welcome_message import (
    send_welcome_message,
    send_welcome_again_message,
)
from src.bot_utils.send_critical_error import send_critical_error
from src.bot_utils.chat import Chat

from src.bot_utils.reply_chat import ReplyChat


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
    except Exception as e:
        await send_critical_error(chat, str(e))
