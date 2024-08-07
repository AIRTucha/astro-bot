from typing import List
from ...logger.logger import logger
from astrogpt.llm.chains import collect_user_data_chain
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.llm.parsers import Decision
from astrogpt.bot_utils.language import get_language, lang_codes
from astrogpt.models.user import User
from astrogpt.models.messages import Message
from astrogpt.bot_utils.reply_chat import ReplyChat
from astrogpt.bot_utils.send_critical_error import send_critical_error
from sqlalchemy.orm import Session
from astrogpt.llm.parsers import CollectDataParser
from astrogpt.bot_utils.send_unexpected_input_reply import send_unexpected_input_reply

from astrogpt.db_utils.update_user import update_user_birthday
from astrogpt.handler.subscribe_handler import handle_subscribe
from astrogpt.handler.unsubscribe_handler import handle_unsubscribe
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.send_unexpected_input_reply import send_unexpected_input_reply
from astrogpt.bot_utils.language import get_language
from dataclasses import dataclass
from astrogpt.bot_utils.send_reply_to_user import send_reply_to_user
from astrogpt.db_utils.add_message import add_message
from astrogpt.handler.llm_handlers.utils import ActionResult
from astrogpt.db_utils.update_user import (
    update_user_birthday,
    update_user_language,
)


def replace_none_with_missing(text: str | None) -> str:
    return text if text is not None else "MISSING"


async def handle_collect_data_data_with_llm(
    chat: ReplyChat,
    user: User,
    session: Session,
) -> List[object]:
    add_message(
        session=session,
        user_id=user.id,
        message=chat.get_message_text(),
        from_user=True,
    )
    user_input = chat.get_message_text()
    user_id = chat.get_user_id()
    user_language = get_language(chat)
    messages = get_messages(session, user_id)

    messages.reverse()

    previous_conversation = "\n".join([str(message) for message in messages])

    actions_taken: List[object] = []

    data_collected: CollectDataParser = collect_user_data_chain.invoke(
        {
            "user_name": user.name,
            "user_input": user_input,
            "previous_conversation": previous_conversation,
            "user_language": user_language,
            "user_birthday": replace_none_with_missing(user.date_of_birth_text),
            "user_language": user_language,
            "user_input": user_input,
            "previous_conversation": previous_conversation,
            "user_subscription": "yes" if user.daily_forecast else "no",
        }
    )

    logger.info("Data collected %s", data_collected)
    actions_taken.append(
        ActionResult(
            action="User data parsing",
            result=data_collected.parsing_feedback,
        )
    )

    if data_collected.birthday_text is not None:
        update_user_birthday(session, user, data_collected.birthday_text)
        actions_taken.append(
            ActionResult(action="Update birthday", result="Updated Successfully")
        )

    if data_collected.language is not None:
        lang_code = lang_codes.get(data_collected.language)
        if lang_code is None:
            logger.error(
                "User language not supported %s %s", user_id, data_collected.language
            )
            actions_taken.append(
                ActionResult(
                    action="Update language",
                    result=f"Language - {data_collected.language} not supported",
                )
            )
        else:
            update_user_language(session, user, lang_code)
            actions_taken.append(
                ActionResult(
                    action="Update language",
                    result="Updated Successfully",
                )
            )

    chat.refresh_state(session)

    return actions_taken
