from src.logger.logger import logger
from telegram import Update, ReplyKeyboardRemove
from src.bot_utils.language import error_messages, languages


async def send_critical_error(update: Update, error: str) -> None:
    logger.error("User %s, got critical error %s", update.message.from_user.id, error)
    error_message = error_messages[languages[update.message.from_user.language_code]]
    await update.message.reply_text(error_message, reply_markup=ReplyKeyboardRemove())
