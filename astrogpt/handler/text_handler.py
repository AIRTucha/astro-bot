from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from ..logger.logger import logger
from typing import List
from astrogpt.models.engine import engine
from astrogpt.models.user import User
from sqlalchemy.orm import Session

from astrogpt.bot_utils.send_welcome_message import (
    send_welcome_message,
)

from astrogpt.bot_utils.send_daily_forecast import send_daily_forecast
from astrogpt.db_utils.update_user import update_user_birthday
from astrogpt.handler.subscribe_handler import handle_subscribe
from astrogpt.handler.unsubscribe_handler import handle_unsubscribe
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.send_unexpected_input_reply import send_unexpected_input_reply
from astrogpt.db_utils.get_user import get_user_from_chat
from astrogpt.bot_utils.language import get_language, get_subscribe, get_unsubscribe
from astrogpt.bot_utils.send_critical_error import send_critical_error
from astrogpt.bot_utils.send_command_explanation_message import (
    send_command_explanation_message,
)
from astrogpt.models.user import User
from astrogpt.db_utils.update_user import (
    update_user_birthday,
)

from astrogpt.bot_utils.send_unexpected_input_reply import send_unexpected_input_reply
from astrogpt.bot_utils.chat import Chat
from astrogpt.bot_utils.reply_chat import ReplyChat
from astrogpt.handler.llm_handlers.handle_menu_with_llm import handle_menu_with_llm

from astrogpt.handler.llm_handlers.handle_collect_data_data_with_llm import (
    handle_collect_data_data_with_llm,
)
from astrogpt.bot_utils.send_reply_to_user import send_reply_to_user
from astrogpt.db_utils.create_user import create_user
from astrogpt.llm.chains import unintended_behavior_detection_chain
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.db_utils.get_last_warnings import get_warnings
from astrogpt.llm.parsers import UnintendedBehaviorDetector
from astrogpt.db_utils.add_warning import add_warning
from astrogpt.handler.llm_handlers.utils import ActionResult


def is_message_subscribe(chat: Chat) -> bool:
    return get_subscribe(chat).lower() == chat.get_message_text().lower()


def is_message_unsubscribe(chat: Chat) -> bool:
    return get_unsubscribe(chat).lower() == chat.get_message_text().lower()


async def handle_text_input_with_llm(
    chat: ReplyChat, user: User, session: Session
) -> List[object]:

    warnings = get_warnings(session, user.id)

    if len(warnings) > 5:
        return []

    user_input = chat.get_message_text()

    message = get_messages(session, user.id, 3)

    unintendedBehaviorDetector: UnintendedBehaviorDetector = (
        unintended_behavior_detection_chain.invoke(
            {
                "user_input": user_input,
                "previous_conversation": "\n\n".join([str(m) for m in message]),
                "previous_warnings": "\n\n".join([str(w) for w in warnings]),
            }
        )
    )

    logger.info("Unintended behavior detected %s", unintendedBehaviorDetector)
    if unintendedBehaviorDetector.warning is not None:
        add_warning(
            session,
            user.id,
            unintendedBehaviorDetector.warning,
            unintendedBehaviorDetector.warning_explanation,
        )

        if len(warnings) > 3:
            return [
                ActionResult(
                    "Warning detected",
                    f"Warning: {unintendedBehaviorDetector.warning}, Explanation: {unintendedBehaviorDetector.warning_explanation}, You have reached the maximum number of warnings, your account will be blocked",
                )
            ]
        else:
            return [
                ActionResult(
                    "Warning detected",
                    f"Warning: {unintendedBehaviorDetector.warning}, Explanation: {unintendedBehaviorDetector.warning_explanation}, Warning count: {len(warnings) + 1} out of 3",
                )
            ]
    else:
        actions_taken = await handle_menu_with_llm(chat, user, session)
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
