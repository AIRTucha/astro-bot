from typing import List
from ..logger.logger import logger
from astrogpt.llm.chains import thinking_chain
from astrogpt.db_utils.get_messages import get_messages

from astrogpt.models.user import User
from astrogpt.bot_utils.chat import Chat

from sqlalchemy.orm import Session

from astrogpt.db_utils.get_messages import get_messages

from astrogpt.bot_utils.language import get_language


from astrogpt.db_utils.add_message import add_message


async def send_thinking_message(
    session: Session,
    chat: Chat,
    user: User,
) -> None:
    user_name = chat.get_user_name()
    messages = get_messages(session, user.id)
    previous_conversation_str = "\n".join([str(message) for message in messages])
    user_language = get_language(chat)
    logger.info(
        "User lang %s",
        user_language,
    )

    user_message = thinking_chain.invoke(
        {
            "user_name": user_name,
            "previous_conversation": previous_conversation_str,
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
