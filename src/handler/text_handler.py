from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from src.llm.chains import (
    parse_birthday_chain,
    subscribed_chain,
    unsubscribed_chain,
)
from ..logger.logger import logger
from src.bot_utils.send_text import send_text

from src.models.engine import engine
from src.models.user import User
from sqlalchemy.orm import Session
from src.handler.start_handler import handle_start
from src.bot_utils.send_daily_forecast import send_daily_forecast
from src.db_utils.update_user import update_user_birthday
from src.db_utils.get_user import get_user_from_update
from src.bot_utils.language import get_language, get_subscribe, get_unsubscribe
from src.bot_utils.send_critical_error import send_critical_error
from src.models.user import User
from src.db_utils.update_user import (
    update_user_birthday,
    update_user_daily_forecast_subscription,
)
from src.bot_utils.update_get_user_data import get_user_id, get_user_first_name
from src.bot_utils.update_get_message_data import get_message_text
from src.bot_utils.send_unexpected_input_reply import send_unexpected_input_reply


async def handle_birthday_input(
    session: Session,
    user: User,
    update: Update,
) -> None:
    user_name = get_user_first_name(update)
    user_input = get_message_text(update)
    user_language = get_language(update)
    user_id = get_user_id(update)

    reply = parse_birthday_chain.invoke(
        {
            "user_name": user_name,
            "user_input": user_input,
            "user_language": user_language,
        }
    )
    if reply.extraction_error:
        logger.error(
            "User extraction error %s %s %s",
            user_id,
            user_input,
            reply.extraction_error,
        )
        await send_text(update, reply.extraction_error)
    else:
        logger.info(
            "User birthday input %s %s %s",
            user_id,
            user_input,
            reply.birthday_text,
        )
        update_user_birthday(session, user.id, reply.birthday_text)
        await send_daily_forecast(user, update, reply.birthday_text)


def is_message_subscribe(update: Update) -> bool:
    return get_subscribe(update).lower() == get_message_text(update).lower()


def is_message_unsubscribe(update: Update) -> bool:
    return get_unsubscribe(update).lower() == get_message_text(update).lower()


async def handle_subscribe(session: Session, update: Update, user: User) -> None:
    user_name = get_user_first_name(update)
    user_language = get_language(update)
    update_user_daily_forecast_subscription(session, user.id, True)
    subscribed_message_reply = subscribed_chain.invoke(
        {
            "user_name": user_name,
            "user_language": user_language,
        }
    )
    await send_text(update, subscribed_message_reply, get_unsubscribe(update))


async def handle_unsubscribe(session: Session, update: Update, user: User) -> None:
    update_user_daily_forecast_subscription(session, user.id, False)
    unsubscribed_message_reply = unsubscribed_chain.invoke(
        {
            "user_name": user.name,
            "user_language": get_language(update),
        }
    )
    await send_text(update, unsubscribed_message_reply, get_unsubscribe(update))


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = get_user_id(update)
    user_input = get_message_text(update)

    logger.info("User input %s: %s", user_id, user_input)
    try:
        with Session(engine) as session:
            user = get_user_from_update(session, update)
            if user is None:
                logger.info("User does to exist %s", user_id)
                await handle_start(update, context)
            else:
                if user.date_of_birth_text is None:
                    await handle_birthday_input(session, user, update)
                else:
                    if is_message_subscribe(update):
                        logger.info(
                            "User subscribed %s %s",
                            user_id,
                            user.daily_forecast,
                        )
                        await handle_subscribe(session, update, user)
                    elif is_message_unsubscribe(update):
                        logger.info(
                            "User unsubscribed %s %s",
                            user_id,
                            user.daily_forecast,
                        )
                        await handle_unsubscribe(session, update, user)
                    else:
                        await send_unexpected_input_reply(update)
    except Exception as e:
        await send_critical_error(update, str(e))
