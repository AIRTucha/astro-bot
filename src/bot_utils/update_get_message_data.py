from telegram import Update
from src.logger.logger import logger


def get_message_text(update: Update) -> str:
    if update.message is None or update.message.text is None:
        logger.error("Update message is None")
        return "UNKNOWN_MESSAGE_TEXT"
    return update.message.text
