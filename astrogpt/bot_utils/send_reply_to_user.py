from typing import List
from ..logger.logger import logger
from astrogpt.llm.chains import reply_user_input_chain
from astrogpt.db_utils.get_messages import get_messages

from astrogpt.models.user import User
from astrogpt.bot_utils.chat import Chat

from sqlalchemy.orm import Session

from astrogpt.db_utils.get_messages import get_messages

from astrogpt.bot_utils.language import get_language


from astrogpt.db_utils.add_message import add_message


async def send_reply_to_user(
    session: Session,
    chat: Chat,
    user: User,
    actions_taken: List[object],
    user_input: str = "",
) -> None:
    user_name = chat.get_user_name()
    messages = get_messages(session, user.id)
    previous_conversation_str = "\n".join([str(message) for message in messages])
    actions_taken_str = "\n".join([str(action) for action in actions_taken])
    user_language = get_language(chat)
    logger.info(
        "User lang %s",
        user_language,
    )

    user_message = reply_user_input_chain.invoke(
        {
            "user_name": user_name,
            "user_input": user_input,
            "previous_conversation": previous_conversation_str,
            "actions_taken": actions_taken_str,
            "user_language": user_language,
        }
    )
    await chat.send_text(user_message)
    add_message(
        session=session,
        user_id=user.id,
        message=user_message,
        from_user=False,
    )
