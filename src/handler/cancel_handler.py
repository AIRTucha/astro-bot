from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from ..logger.logger import logger
from src.bot_utils.send_cancel_message import send_cancel_message
from src.bot_utils.send_critical_error import send_critical_error


async def handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logger.info("User %s canceled the conversation.", update.message.from_user.id)
        await send_cancel_message(update)

    except Exception as e:
        await send_critical_error(update, str(e))
