from typing import List
from ...logger.logger import logger
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.models.user import User
from astrogpt.bot_utils.reply_chat import ReplyChat
from sqlalchemy.orm import Session
from astrogpt.db_utils.get_messages import get_messages
from astrogpt.bot_utils.language import get_language
from astrogpt.db_utils.add_message import add_message
from astrogpt.handler.llm_reasoning.action_result import ActionResult
from astrogpt.handler.llm_reasoning.collect_data import (
    collect_data,
)
from astrogpt.db_utils.update_user import (
    update_user_daily_forecast_subscription,
)
from astrogpt.handler.llm_reasoning.select_action import select_action
from astrogpt.handler.llm_reasoning.generate_joke import generate_joke
from astrogpt.handler.llm_reasoning.generate_advice import generate_advice
from astrogpt.handler.llm_reasoning.get_daily_forecast import get_daily_forecast
from astrogpt.llm.parsers import MenuActions


async def handle_main_menu(
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
    user_id = chat.get_user_id()

    previous_actions: List[object] = []
    handled_actions = set()

    while len(previous_actions) < 7:
        try:
            selected_action = await select_action(chat, user, previous_actions, session)

            if selected_action.selected_action in handled_actions:
                previous_actions.append(
                    ActionResult(
                        action="Select Next Actions",
                        result=f"Action {selected_action.selected_action} already handled, select another if there are any left or reply to user with result",
                    ),
                )
                continue

            handled_actions.add(selected_action.selected_action)

            logger.info("User %s selected action %s", user_id, selected_action)

            previous_actions.append(
                ActionResult(
                    "Select Next Actions",
                    str(selected_action),
                ),
            )
            if selected_action.selected_action == MenuActions.update_user_data:
                try:
                    actions = await collect_data(
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

            elif selected_action.selected_action == MenuActions.subscribe:
                update_user_daily_forecast_subscription(session, user.id, True)
                previous_actions.append(
                    ActionResult(action="Subscribe", result="Subscribed Successfully")
                )
            elif selected_action.selected_action == MenuActions.unsubscribe:
                update_user_daily_forecast_subscription(session, user.id, False)
                previous_actions.append(
                    ActionResult(action="Unsubscribe", result="Subscription Canceled")
                )
            elif (
                selected_action.selected_action == MenuActions.get_joke_about_astrology
            ):
                action_results = await generate_joke(chat, session)
                previous_actions += action_results
            elif selected_action.selected_action == MenuActions.get_situational_advice:
                action_results = await generate_advice(chat, user, session)
                previous_actions += action_results
            elif selected_action.selected_action == MenuActions.get_daily_forecast:
                action_results = await get_daily_forecast(
                    session=session, user=user, chat=chat
                )
                previous_actions += action_results
            else:
                break
        except Exception as e:
            previous_actions.append(
                ActionResult(action="Critical Error", result="Failed due to " + str(e))
            )
            return previous_actions

    return previous_actions
