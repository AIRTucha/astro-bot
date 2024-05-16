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
from src.bot_utils.bot_chat import BotChat
from src.bot_utils.send_daily_forecast import send_daily_forecast


class Bot:
    def __init__(self, bot_token: str) -> None:
        self.application = (
            Application.builder()
            .token(bot_token)
            .read_timeout(20000)
            .write_timeout(20000)
            .build()
        )
        self.application.bot

    async def start(self):

        self.application.add_handler(CommandHandler("start", handle_start))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
        )
        self.application.add_handler(CommandHandler("cancel", handle_cancel))

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

        # await self.application.bot.send_https://scontent.ffra2-1.fna.fbcdn.net/v/t39.30808-6/440389240_857552689750682_6349401513829990214_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=5f2048&_nc_ohc=JsGFdY6t_BcQ7kNvgEmA-zy&_nc_ht=scontent.ffra2-1.fna&oh=00_AYD4X320t3o9xoiHc9YziBW_0oeMMwDquOZS1g-mLrZT5g&oe=66443E52message(chat_id=63033311, text="Bot started!")

    async def stop(self):
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()

    async def send_daily_forecast(self):
        with Session(engine) as session:
            users = await get_users_for_forecast(session)
            for user in users:
                logger.info("Sending daily forecast to user %s", user.name)
                botChat = BotChat(self.application.bot, user)

                await send_daily_forecast(user, botChat)
