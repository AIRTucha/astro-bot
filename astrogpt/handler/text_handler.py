from typing import List

from astrogpt.models.user import User
from sqlalchemy.orm import Session
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from astrogpt.logger.logger import logger
from astrogpt.bot_utils.send_critical_error import send_critical_error

from astrogpt.models.user import User

from astrogpt.bot_utils.reply_chat import ReplyChat
from astrogpt.handler.llm_reasoning.handle_main_menu import handle_main_menu

from astrogpt.bot_utils.send_reply_to_user import send_reply_to_user
from astrogpt.db_utils.create_user import create_user
from astrogpt.models.engine import engine
from astrogpt.db_utils.get_user import get_user_from_chat
from astrogpt.bot_utils.send_welcome_message import send_welcome_message
from astrogpt.handler.llm_reasoning.detect_unintended_behavior import (
    detect_unintended_behavior,
)


async def handle_text_input_with_llm(
    chat: ReplyChat, user: User, session: Session
) -> List[object]:
    warning_actions = await detect_unintended_behavior(chat, user, session)

    if len(warning_actions) > 0:
        return warning_actions
    else:
        actions_taken = await handle_main_menu(chat, user, session)
        return actions_taken


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = ReplyChat(update)
    user_id = chat.get_user_id()
    user_input = chat.get_message_text()

    logger.info("User input %s: %s", user_id, user_input)
    try:
        with Session(engine) as session:
            user = get_user_from_chat(session, chat)
            if user is None:
                logger.info("User does to exist %s", user_id)
                create_user(session, chat)
                await send_welcome_message(chat)
                await handle_text(update, context)
                return
            chat.refresh_state(session)

            actions_take = await handle_text_input_with_llm(chat, user, session)

            if len(actions_take) == 0:
                await send_critical_error(chat, "No actions taken")
                return

            logger.info("Actions taken %s", actions_take)

            await send_reply_to_user(
                session=session,
                chat=chat,
                user=user,
                actions_taken=actions_take,
                user_input=user_input,
            )

    except Exception as e:
        await send_critical_error(chat, str(e))
