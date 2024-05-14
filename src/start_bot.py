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
from src.models.engine import engine
from sqlalchemy.orm import Session
from src.db_utils.get_users_for_forecast import get_users_for_forecast


class Bot:
    def __init__(self, bot_token: str) -> None:
        self.application = (
            Application.builder()
            .token(bot_token)
            .read_timeout(20000)
            .write_timeout(20000)
            .build()
        )

    async def start(self):

        self.application.add_handler(CommandHandler("start", handle_start))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
        )
        self.application.add_handler(CommandHandler("cancel", handle_cancel))

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

        # await self.application.bot.send_message(chat_id=63033311, text="Bot started!")

    async def stop(self):
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()

    async def send_daily_forecast(self):
        with Session(engine) as session:
            users = await get_users_for_forecast(session)
            for user in users:
                logger.info("Sending daily forecast to user %s", user.name)

                # await send_daily_forecast(user)
        # await update.message.reply_text("Daily forecast sent!")
