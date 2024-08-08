from typing import List
from ...logger.logger import logger
from astrogpt.llm.chains import menu_chain, joke_chain
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.llm.parsers import Decision, AdviceParser

from astrogpt.models.user import User
from astrogpt.bot_utils.reply_chat import ReplyChat
from sqlalchemy.orm import Session
from astrogpt.llm.parsers import MenuDecision


from astrogpt.handler.subscribe_handler import handle_subscribe
from astrogpt.handler.unsubscribe_handler import handle_unsubscribe
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.language import get_language

from astrogpt.db_utils.add_message import add_message
from astrogpt.handler.llm_handlers.utils import ActionResult
from astrogpt.handler.llm_handlers.handle_collect_data_data_with_llm import (
    handle_collect_data_data_with_llm,
)
from astrogpt.llm.chains import advice_chain
from astrogpt.db_utils.get_last_advices import get_last_advices
from astrogpt.db_utils.get_last_daily_forecasts import get_last_forecasts
from astrogpt.db_utils.add_advice import add_advice
from astrogpt.db_utils.add_joke import add_joke
from astrogpt.db_utils.get_jokes import get_jokes


def replace_none_with_missing(text: str | None) -> str:
    return text if text is not None else "MISSING"


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

            logger.info(
                "User %s menu decision %s %s",
                user_id,
                reply.decision,
                reply.decision_context,
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
            elif reply.decision == Decision.trigger_joke_about_astrology_generator:
                joke_example = get_jokes(session, count=3)
                joke = joke_chain.invoke(
                    {
                        "user_name": user_name,
                        "user_birthday": replace_none_with_missing(
                            user.date_of_birth_text
                        ),
                        "joke_examples": "\n\n".join(joke_example),
                        "user_language": user_language,
                        "user_input": user_input,
                    }
                )
                add_joke(session=session, joke=joke)
                previous_actions.append(ActionResult(action="Joke", result=joke))
            elif reply.decision == Decision.trigger_situational_advice_generator:
                advice: AdviceParser = advice_chain.invoke(
                    {
                        "user_name": user_name,
                        "user_birthday": replace_none_with_missing(
                            user.date_of_birth_text
                        ),
                        "user_language": user_language,
                        "user_input": user_input,
                        "previous_conversation": previous_conversation,
                        "previous_forecast": get_last_forecasts(session, user_id),
                        "previous_advice": get_last_advices(session, user_id),
                        "user_subscription": "yes" if user.daily_forecast else "no",
                    }
                )
                logger.info(
                    "User %s advice %s; %s; %s",
                    user_id,
                    advice.astrological_advice,
                    advice.situation,
                    advice.clarification,
                )
                if advice.clarification is not None:
                    previous_actions.append(
                        ActionResult(
                            action="Provide Advice",
                            result="Clarification needed: " + advice.clarification,
                        )
                    )
                else:
                    add_advice(
                        session=session,
                        user_id=user_id,
                        advice=advice.astrological_advice,
                        situation=advice.situation,
                    )
                    previous_actions.append(
                        ActionResult(
                            action="Provide Advice",
                            result=advice.astrological_advice,
                        )
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
