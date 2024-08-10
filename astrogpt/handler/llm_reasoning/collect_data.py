from typing import List
from ...logger.logger import logger
from astrogpt.llm.chains import collect_user_data_chain
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.language import get_language, lang_codes
from astrogpt.models.user import User
from astrogpt.bot_utils.reply_chat import ReplyChat
from sqlalchemy.orm import Session
from astrogpt.llm.parsers import CollectDataParser

from astrogpt.db_utils.update_user import update_user_birthday
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.language import get_language

from astrogpt.db_utils.add_message import add_message
from astrogpt.handler.llm_reasoning.action_result import ActionResult
from astrogpt.db_utils.update_user import (
    update_user_birthday,
    update_user_language,
)


def replace_none_with_missing(text: str | None) -> str:
    return text if text is not None else "MISSING"


async def collect_data(
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

    if not data_collected.is_data_about_user:
        actions_taken.append(
            ActionResult(
                action="Data extraction",
                result="It is not clear if data is about the user, clarification is needed",
            )
        )
        return actions_taken

    if data_collected.user_birthday_text is not None:
        update_user_birthday(session, user, data_collected.user_birthday_text)
        actions_taken.append(
            ActionResult(
                action="Update birthday",
                result=f"Successfully updated to {data_collected.user_birthday_text}",
            )
        )

    if data_collected.language is not None:
        lang_code = lang_codes.get(data_collected.language.lower())
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
