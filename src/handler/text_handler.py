from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import (
    ContextTypes,
)
from src.llm.chains import (
    parse_birthday_chain,
    subscribed_chain,
    unsubscribed_chain,
)
from ..logger.logger import logger

from src.models.engine import engine
from src.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.handler.start_handler import handle_start
from src.bot_utils.send_prediction import send_prediction
from src.db_utils.update_user import update_user_birthday
from src.db_utils.get_user import get_user_from_update
from src.bot_utils.language import languages, subscribe, unsubscribe
from src.bot_utils.send_critical_error import send_critical_error
from src.models.user import User
from src.db_utils.update_user import (
    update_user_birthday,
    update_user_daily_forecast_subscription,
)


async def handle_birthday_input(
    session: Session,
    user: User,
    update: Update,
) -> None:
    reply = parse_birthday_chain.invoke(
        {
            "user_name": user.name,
            "user_input": update.message.text,
            "user_language": languages[update.message.from_user.language_code],
        }
    )
    print("reply", reply)
    if reply.extraction_error:
        logger.error(
            "User extraction error %s %s %s",
            user.id,
            update.message.text,
            reply.extraction_error,
        )
        await update.message.reply_text(
            reply.extraction_error, reply_markup=ReplyKeyboardRemove()
        )
    else:
        logger.info(
            "User birthday input %s %s %s",
            user.id,
            update.message.text,
            reply.birthday_text,
        )
        update_user_birthday(session, user.id, reply.birthday_text)
        await send_prediction(update, reply.birthday_text)


def is_message_subscribe(update: Update) -> bool:
    return (
        subscribe[update.message.from_user.language_code].lower()
        == update.message.text.lower()
    )


def is_message_unsubscribe(update: Update) -> bool:
    return (
        unsubscribe[update.message.from_user.language_code].lower()
        == update.message.text.lower()
    )


async def handle_subscribe(session: Session, update: Update, user: User) -> None:
    update_user_daily_forecast_subscription(session, user.id, True)
    subscribed_message_reply = subscribed_chain.invoke(
        {
            "user_name": user.name,
            "user_language": languages[update.message.from_user.language_code],
        }
    )
    await update.message.reply_text(
        subscribed_message_reply,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(unsubscribe[update.message.from_user.language_code])]
            ]
        ),
    )


async def handle_unsubscribe(session: Session, update: Update, user: User) -> None:
    update_user_daily_forecast_subscription(session, user.id, False)
    unsubscribed_message_reply = unsubscribed_chain.invoke(
        {
            "user_name": user.name,
            "user_language": languages[update.message.from_user.language_code],
        }
    )
    await update.message.reply_text(
        unsubscribed_message_reply,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(subscribe[update.message.from_user.language_code])]
            ]
        ),
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("User input %s", update.message.from_user.id)
    try:
        with Session(engine) as session:
            user = get_user_from_update(session, update)
            if user is None:
                logger.info("User does to exist %s", update.message.from_user.id)
                await handle_start(session, update, context)
            else:
                if user.date_of_birth_text is None:
                    await handle_birthday_input(session, user, update)
                else:
                    if is_message_subscribe(update):
                        logger.info(
                            "User subscribed %s %s",
                            update.message.from_user.id,
                            user.daily_forecast,
                        )
                        await handle_subscribe(session, update, user)
                    elif is_message_unsubscribe(update):
                        logger.info(
                            "User unsubscribed %s %s",
                            update.message.from_user.id,
                            user.daily_forecast,
                        )
                        await handle_unsubscribe(session, update, user)
                    else:
                        print("user.date_of_birth_text", user.date_of_birth_text)
                        await send_prediction(update, user.date_of_birth_text)
    except Exception as e:
        await send_critical_error(update, str(e))
