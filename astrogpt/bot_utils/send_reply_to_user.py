from typing import List
from ..logger.logger import logger
from astrogpt.llm.chains import menu_chain, reply_user_input_chain
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.llm.parsers import Decision

from astrogpt.models.user import User
from astrogpt.models.messages import Message
from astrogpt.bot_utils.chat import Chat
from astrogpt.bot_utils.send_critical_error import send_critical_error
from sqlalchemy.orm import Session
from astrogpt.llm.parsers import MenuDecision
from astrogpt.bot_utils.send_unexpected_input_reply import send_unexpected_input_reply

from astrogpt.bot_utils.send_daily_forecast import send_daily_forecast
from astrogpt.db_utils.update_user import update_user_birthday
from astrogpt.handler.subscribe_handler import handle_subscribe
from astrogpt.handler.unsubscribe_handler import handle_unsubscribe
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.send_unexpected_input_reply import send_unexpected_input_reply
from astrogpt.bot_utils.language import get_language
from dataclasses import dataclass

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
