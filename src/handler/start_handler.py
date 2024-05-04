from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from src.models.engine import engine
from sqlalchemy.orm import Session
from src.logger.logger import logger
from src.db_utils.get_user import get_user_from_update
from src.db_utils.create_user import create_user
from src.bot_utils.send_welcome_message import (
    send_welcome_message,
    send_welcome_again_message,
)
from src.bot_utils.send_critical_error import send_critical_error


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with Session(engine) as session:
            user = get_user_from_update(session, update)

            if user is None:
                logger.info("User %s id created", update.message.from_user.id)
                create_user(session, update)

            logger.info("User %s started the bot", update.message.from_user.id)
            if user.date_of_birth_text is None:
                await send_welcome_message(update)
            else:
                await send_welcome_again_message(update)
    except Exception as e:
        await send_critical_error(update, str(e))
