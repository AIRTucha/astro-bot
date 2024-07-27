from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from astrogpt.bot_utils.send_cancel_message import send_cancel_message
from astrogpt.bot_utils.send_critical_error import send_critical_error
from astrogpt.bot_utils.reply_chat import ReplyChat


async def handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = ReplyChat(update)
    try:
        await send_cancel_message(chat)
    except Exception as e:
        await send_critical_error(chat, str(e))
