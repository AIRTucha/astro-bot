from typing import List
from ...logger.logger import logger
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.llm.parsers import AdviceParser, AdviceResult

from astrogpt.models.user import User
from astrogpt.bot_utils.reply_chat import ReplyChat
from sqlalchemy.orm import Session
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.language import get_language
from astrogpt.handler.llm_reasoning.action_result import ActionResult
from astrogpt.llm.chains import advice_chain
from astrogpt.db_utils.get_last_advices import get_last_advices
from astrogpt.db_utils.get_last_daily_forecasts import get_last_forecasts
from astrogpt.db_utils.add_advice import add_advice
from astrogpt.handler.llm_reasoning.replace_none_with_missing import (
    replace_none_with_missing,
)
from astrogpt.handler.llm_reasoning.format_list import format_list


async def generate_advice(
    chat: ReplyChat,
    user: User,
    session: Session,
) -> List[ActionResult]:
    try:
        user_name = chat.get_user_name()
        user_input = chat.get_message_text()
        user_language = get_language(chat)
        user_id = chat.get_user_id()
        messages = get_messages(session, user_id)
        messages_str = format_list(messages)
        user_birthday = replace_none_with_missing(user.date_of_birth_text)
        last_forecasts = get_last_forecasts(session, user_id)
        last_forecasts_str = format_list(last_forecasts)
        last_advices = get_last_advices(session, user_id)
        last_advices_str = format_list(last_advices)

        advice: AdviceParser = advice_chain.invoke(
            {
                "user_name": user_name,
                "user_birthday": user_birthday,
                "user_language": user_language,
                "user_input": user_input,
                "previous_conversation": messages_str,
                "previous_forecast": last_forecasts_str,
                "previous_advice": last_advices_str,
                "user_subscription": "yes" if user.daily_forecast else "no",
            }
        )

        if advice.advice_result == AdviceResult.clarification:
            return [
                ActionResult(
                    action="Advice Generation Error",
                    result="Clarification needed: " + advice.result_description,
                )
            ]

        else:
            add_advice(
                session=session,
                user_id=user_id,
                advice=advice.result_description,
                situation=advice.situation,
            )
            return [
                ActionResult(
                    action="Advice Generated",
                    result=advice.result_description,
                )
            ]
    except Exception as e:
        return [
            ActionResult(
                action="Advice Generation Error", result="Failed due to " + str(e)
            )
        ]
