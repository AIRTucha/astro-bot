from src.logger.logger import logger
from telegram import Update
from src.bot_utils.send_text import send_text
from src.bot_utils.update_get_user_data import get_user_id
from src.bot_utils.language import get_error_message


async def send_critical_error(update: Update, error: str) -> None:
    user_id = get_user_id(update)
    logger.error("User %s, got critical error %s", user_id, error)
    error_message = get_error_message(update)
    await send_text(update, error_message)
