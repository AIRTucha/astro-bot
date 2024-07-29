from ..logger.logger import logger
from astrogpt.models.user import User
from astrogpt.bot_utils.chat import Chat
from astrogpt.bot_utils.reply_chat import ReplyChat
from astrogpt.bot_utils.language import get_language
from astrogpt.llm.chains import parse_birthday_chain

from astrogpt.bot_utils.send_daily_forecast import send_daily_forecast
from astrogpt.bot_utils.send_command_explanation_message import (
    send_command_explanation_message,
)
from astrogpt.db_utils.update_user import update_user_birthday


from sqlalchemy.orm import Session


class BirthdayParsingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


async def handle_birthday_input(
    session: Session,
    user: User,
    chat: Chat,
) -> None:
    logger.info("Handling birthday input")
    user_name = chat.get_user_name()
    user_input = chat.get_message_text()
    user_language = get_language(chat)
    user_id = chat.get_user_id()

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
        raise BirthdayParsingError(reply.extraction_error)
    else:
        logger.info(
            "User birthday input %s %s %s",
            user_id,
            user_input,
            reply.birthday_text,
        )
        update_user_birthday(session, user, reply.birthday_text)
        logger.info("User %s birthday updated as %s", user_id, reply.birthday_text)
        await send_daily_forecast(user, chat)
        await send_command_explanation_message(chat)
