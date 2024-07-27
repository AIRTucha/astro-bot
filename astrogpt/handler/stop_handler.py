from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from astrogpt.llm.chains import (
    unsubscribed_chain,
)
from ..logger.logger import logger

from astrogpt.models.engine import engine
from astrogpt.models.user import User
from sqlalchemy.orm import Session
from astrogpt.db_utils.get_user import get_user_from_chat
from astrogpt.bot_utils.language import get_language, get_subscribe
from astrogpt.bot_utils.send_critical_error import send_critical_error
from astrogpt.models.user import User
from astrogpt.db_utils.update_user import (
    update_user_daily_forecast_subscription,
)

from astrogpt.bot_utils.chat import Chat
from astrogpt.bot_utils.reply_chat import ReplyChat


async def stop_handler(update: Update, context: ContextTypes) -> None:
    chat = ReplyChat(update)

    with Session(engine) as session:
        user = get_user_from_chat(session, chat)
        if user is None:
            await send_critical_error(chat, "User not found")
            return
        update_user_daily_forecast_subscription(session, user.id, False)
    logger.info("User %s stopped bot with '%s'", user.id, chat.message.text)
