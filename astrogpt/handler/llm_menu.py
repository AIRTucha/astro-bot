from typing import List
from ..logger.logger import logger
from astrogpt.llm.chains import menu_chain
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.llm.parsers import Decision
from astrogpt.handler.handle_birthday_input import handle_birthday_input
from astrogpt.models.user import User
from astrogpt.models.messages import Message
from astrogpt.bot_utils.reply_chat import ReplyChat
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


async def handle_menu_with_llm(
    chat: ReplyChat,
    user: User,
    session: Session,
) -> None:
    user_name = chat.get_user_name()
    user_input = chat.get_message_text()
    user_id = chat.get_user_id()
    user_birthday = user.date_of_birth_text
    user_language = get_language(chat)
    messages = get_messages(session, user_id)
    previous_conversation = "\n".join([str(message) for message in messages])

    previous_actions: List[MenuDecision] = []

    while len(previous_actions) < 5:

        previous_actions_str = "\n".join([str(action) for action in previous_actions])
        reply: MenuDecision = menu_chain.invoke(
            {
                "user_name": user_name,
                "user_birthday": user_birthday,
                "user_input": user_input,
                "previous_conversation": previous_conversation,
                "previous_actions": previous_actions_str,
                "user_language": user_language,
            }
        )
        logger.info(
            "User %s menu decision %s %s",
            user_id,
            reply.decision,
            reply.decision_details,
        )

        previous_actions.append(reply)

        if reply.decision == Decision.update_birth_day:
            await handle_birthday_input(session, user, chat)
        elif reply.decision == Decision.send_daily_forecast:
            await send_daily_forecast(user, chat)
        elif reply.decision == Decision.subscribe:
            await handle_subscribe(session, chat, user)
        elif reply.decision == Decision.unsubscribe:
            await handle_unsubscribe(session, chat, user)
        elif reply.decision == Decision.unclear_user_input:
            await send_unexpected_input_reply(chat)
        else:
            await send_critical_error(chat)

        return
