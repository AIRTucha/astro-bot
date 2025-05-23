from typing import List
from ...logger.logger import logger
from astrogpt.llm.chains import menu_chain, joke_chain
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.llm.parsers import MenuActions, AdviceParser

from astrogpt.models.user import User
from astrogpt.bot_utils.reply_chat import ReplyChat
from sqlalchemy.orm import Session
from astrogpt.llm.parsers import SelectedAction


from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.language import get_language

from astrogpt.handler.llm_reasoning.action_result import ActionResult

from astrogpt.db_utils.get_last_daily_forecasts import get_last_forecasts
from astrogpt.handler.llm_reasoning.replace_none_with_missing import (
    replace_none_with_missing,
)
from astrogpt.handler.llm_reasoning.action_result import ActionResult
from astrogpt.handler.llm_reasoning.format_list import format_list


async def select_action(
    chat: ReplyChat,
    user: User,
    previous_actions: List[ActionResult],
    session: Session,
) -> SelectedAction:
    user_name = chat.get_user_name()
    user_input = chat.get_message_text()
    user_id = chat.get_user_id()
    messages = get_messages(session, user_id, 7)
    previous_conversation = format_list(messages)
    previous_actions_str = format_list(previous_actions)
    user_language = get_language(chat)
    return menu_chain.invoke(
        {
            "processing_steps": previous_actions_str,
            "user_name": user_name,
            "user_birthday": replace_none_with_missing(user.date_of_birth_text),
            "user_language": user_language,
            "user_input": user_input,
            "previous_conversation": previous_conversation,
            "previous_forecast": get_last_forecasts(session, user_id),
            "user_subscription": "yes" if user.daily_forecast else "no",
        }
    )
