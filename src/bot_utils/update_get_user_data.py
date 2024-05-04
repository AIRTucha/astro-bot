from telegram import Update

from src.logger.logger import logger


def get_user_first_name(update: Update) -> str:
    if update.message is None or update.message.from_user is None:
        logger.error("Update message is None")
        return "UNKNOWN_FIRST_NAME"
    return update.message.from_user.first_name


def get_user_last_name(update: Update) -> str:
    if (
        update.message is None
        or update.message.from_user is None
        or update.message.from_user.last_name is None
    ):
        logger.error("Update message is None")
        return "UNKNOWN_LAST_NAME"
    return update.message.from_user.last_name


def get_user_id(update: Update) -> int:
    if update.message is None or update.message.from_user is None:
        logger.error("Update message is None")
        return -1
    return update.message.from_user.id
