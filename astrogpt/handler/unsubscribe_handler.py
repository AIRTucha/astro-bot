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
from astrogpt.bot_utils.language import get_language
from astrogpt.models.user import User
from astrogpt.db_utils.update_user import (
    update_user_daily_forecast_subscription,
)

from astrogpt.bot_utils.chat import Chat
from astrogpt.bot_utils.reply_chat import ReplyChat
from astrogpt.db_utils.create_user import create_user


async def unsubscribe_handler(update: Update, context: ContextTypes) -> None:
    chat = ReplyChat(update)

    with Session(engine) as session:
        user = get_user_from_chat(session, chat)
        if user is None:
            create_user(session, chat)
            await unsubscribe_handler(update, context)
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
    # await chat.send_text(unsubscribed_message_reply)
