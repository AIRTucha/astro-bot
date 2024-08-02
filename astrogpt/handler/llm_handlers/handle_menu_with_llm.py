from typing import List
from ...logger.logger import logger
from astrogpt.llm.chains import menu_chain, reply_user_input_chain
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.llm.parsers import Decision

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

from astrogpt.bot_utils.send_reply_to_user import send_reply_to_user
from astrogpt.db_utils.add_message import add_message
from astrogpt.handler.llm_handlers.utils import ActionResult
from astrogpt.handler.llm_handlers.handle_collect_data_data_with_llm import (
    handle_collect_data_data_with_llm,
)


async def handle_menu_with_llm(
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
    user_name = chat.get_user_name()
    user_input = chat.get_message_text()
    user_id = chat.get_user_id()
    user_birthday = user.date_of_birth_text
    messages = get_messages(session, user_id)

    messages.reverse()

    previous_conversation = "\n".join([str(message) for message in messages])

    previous_actions: List[object] = []
    previous_actions_str = ""

    while len(previous_actions) < 7:
        user_language = get_language(chat)
        try:
            reply: MenuDecision = menu_chain.invoke(
                {
                    "user_name": user_name,
                    "user_birthday": user_birthday,
                    "user_input": user_input,
                    "previous_conversation": previous_conversation,
                    "actions_taken": previous_actions_str,
                    "user_language": user_language,
                    "user_subscription": "yes" if user.daily_forecast else "no",
                }
            )

            logger.info(
                "User %s menu decision %s %s",
                user_id,
                reply.decision,
                reply.decision_details,
            )

            previous_actions.append(reply)
            if reply.decision == Decision.update_user_data:
                try:
                    actions = await handle_collect_data_data_with_llm(
                        chat,
                        user,
                        session,
                    )
                    previous_actions += actions

                except Exception as e:
                    previous_actions.append(
                        ActionResult(
                            action="Data update",
                            result="Exception failed due to " + str(e),
                        )
                    )

            elif reply.decision == Decision.subscribe:
                await handle_subscribe(session, chat, user)

                previous_actions.append(
                    ActionResult(action="Subscribe", result="Subscribed Successfully")
                )
            elif reply.decision == Decision.unsubscribe:
                await handle_unsubscribe(session, chat, user)
                previous_actions.append(
                    ActionResult(action="Unsubscribe", result="Subscription Canceled")
                )
            else:
                break
        except Exception as e:
            previous_actions.append(
                ActionResult(action="Critical Error", result="Failed due to " + str(e))
            )
        finally:
            previous_actions_str = "\n".join(
                [str(action) for action in previous_actions]
            )

    return previous_actions
