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


async def unsubscribe_handler(update: Update, context: ContextTypes) -> None:
    chat = ReplyChat(update)

    with Session(engine) as session:
        user = get_user_from_chat(session, chat)
        if user is None:
            await send_critical_error(chat, "User not found")
            return
        await handle_unsubscribe(session, chat, user)
    logger.info("User %s unsubscribed", user.id)


async def handle_unsubscribe(session: Session, chat: Chat, user: User) -> None:
    update_user_daily_forecast_subscription(session, user.id, False)
    unsubscribed_message_reply = unsubscribed_chain.invoke(
        {
            "user_name": user.name,
            "user_language": get_language(chat),
        }
    )
    await chat.send_text(unsubscribed_message_reply, get_subscribe(chat))
