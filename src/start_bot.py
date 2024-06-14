from http import HTTPStatus
from typing import Any
from fastapi import Response
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

import os
import asyncio


async def error_handler(update: Update) -> None:
    logger.error("Update %s caused error %s", update.to_dict())


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
        self.application.add_error_handler(error_handler)

        await self.application.initialize()
        await self.application.start()

        if os.getenv("WEBHOOK_ENABLED") != "true":
            await self.application.updater.start_polling()
        else:
            logger.info("Setting webhook")
            await self.application.bot.set_webhook(
                "https://backend-fb37jnmkpa-ez.a.run.app/tg_webhook"
            )

    async def stop(self):
        if os.getenv("WEBHOOK_ENABLED") != "true":
            await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()

    async def send_daily_forecast(self):
        with Session(engine) as session:
            while True:
                users = await get_users_for_forecast(session)
                if len(users) == 0:
                    logger.info("All forecasts sent for today. Exiting...")
                    break
                async with asyncio.TaskGroup() as tg:
                    for user in users:
                        logger.info("Sending daily forecast to user %s", user.name)
                        botChat = BotChat(self.application.bot, user)

                        tg.create_task(send_daily_forecast(user, botChat))

    async def process_update(self, update: Any) -> Response:
        update = Update.de_json(update, self.application.bot)
        await self.application.process_update(update)
        return Response(status_code=HTTPStatus.OK)
