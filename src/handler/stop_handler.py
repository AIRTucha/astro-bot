from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from src.llm.chains import (
    unsubscribed_chain,
)
from ..logger.logger import logger

from src.models.engine import engine
from src.models.user import User
from sqlalchemy.orm import Session
from src.db_utils.get_user import get_user_from_chat
from src.bot_utils.language import get_language, get_subscribe
from src.bot_utils.send_critical_error import send_critical_error
from src.models.user import User
from src.db_utils.update_user import (
    update_user_daily_forecast_subscription,
)

from src.bot_utils.chat import Chat
from src.bot_utils.reply_chat import ReplyChat


async def stop_handler(update: Update, context: ContextTypes) -> None:
    chat = ReplyChat(update)

    with Session(engine) as session:
        user = get_user_from_chat(session, chat)
        if user is None:
            await send_critical_error(chat, "User not found")
            return
        update_user_daily_forecast_subscription(session, user.id, False)
    logger.info("User %s stopped bot with '%s'", user.id, chat.message.text)
