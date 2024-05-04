from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from src.handler.cancel_handler import handle_cancel
from src.handler.start_handler import handle_start
from src.handler.text_handler import handle_text
from src.logger.logger import logger


def start_bot(bot_token: str):
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )
    application.add_handler(CommandHandler("cancel", handle_cancel))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
