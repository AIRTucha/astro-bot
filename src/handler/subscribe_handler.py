from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from src.llm.chains import (
    subscribed_chain,
)
from ..logger.logger import logger

from src.models.engine import engine
from src.models.user import User
from sqlalchemy.orm import Session
from src.db_utils.get_user import get_user_from_chat
from src.bot_utils.language import get_language
from src.models.user import User
from src.db_utils.update_user import (
    update_user_daily_forecast_subscription,
)
from src.bot_utils.chat import Chat
from src.bot_utils.reply_chat import ReplyChat
from src.db_utils.create_user import create_user


async def subscribe_handler(update: Update, context: ContextTypes) -> None:
    chat = ReplyChat(update)

    with Session(engine) as session:
        user = get_user_from_chat(session, chat)
        if user is None:
            create_user(session, chat)
            await subscribe_handler(update, context)
            return
        await handle_subscribe(session, chat, user)
        logger.info("User %s subscribed", user.id)


async def handle_subscribe(session: Session, chat: Chat, user: User) -> None:
    user_name = chat.get_user_name()
    user_language = get_language(chat)
    update_user_daily_forecast_subscription(session, user.id, True)
    subscribed_message_reply = subscribed_chain.invoke(
        {
            "user_name": user_name,
            "user_language": user_language,
        }
    )
    await chat.send_text(subscribed_message_reply)
