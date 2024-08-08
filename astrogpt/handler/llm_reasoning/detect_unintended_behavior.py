from typing import List

from astrogpt.models.user import User
from sqlalchemy.orm import Session
from astrogpt.logger.logger import logger

from astrogpt.models.user import User

from astrogpt.bot_utils.reply_chat import ReplyChat
from astrogpt.llm.chains import unintended_behavior_detection_chain
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.db_utils.get_last_warnings import get_warnings
from astrogpt.llm.parsers import UnintendedBehaviorDetector
from astrogpt.db_utils.add_warning import add_warning
from astrogpt.handler.llm_reasoning.action_result import ActionResult
from astrogpt.models.warning import WarningType


async def detect_unintended_behavior(
    chat: ReplyChat, user: User, session: Session
) -> List[object]:

    warnings = get_warnings(session, user.id)

    if len(warnings) >= 5:
        raise Exception("User has reached the maximum number of warnings")

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
    if (
        unintendedBehaviorDetector.confidence > 0.75
        and unintendedBehaviorDetector.warning is not None
    ):
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
        return []
