from ..logger.logger import logger
from astrogpt.models.user import User
from astrogpt.bot_utils.chat import Chat
from astrogpt.bot_utils.reply_chat import ReplyChat
from astrogpt.bot_utils.language import get_language, lang_codes
from astrogpt.llm.chains import parse_user_language_chain

from astrogpt.bot_utils.send_daily_forecast import send_daily_forecast
from astrogpt.bot_utils.send_command_explanation_message import (
    send_command_explanation_message,
)
from astrogpt.db_utils.update_user import update_user_language


from sqlalchemy.orm import Session


class UserLanguageParsingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


async def handle_prase_user_language(
    session: Session,
    user: User,
    chat: Chat,
) -> None:
    user_name = chat.get_user_name()
    user_input = chat.get_message_text()
    user_language = get_language(chat)
    user_id = chat.get_user_id()

    reply = parse_user_language_chain.invoke(
        {
            "user_name": user_name,
            "user_input": user_input,
            "user_language": user_language,
            "supported_languages": [lang for lang in lang_codes],
        }
    )
    if reply.extraction_error:
        logger.error(
            "User extraction error %s %s %s",
            user_id,
            user_input,
            reply.extraction_error,
        )
        raise UserLanguageParsingError(reply.extraction_error)
        # await chat.send_text(reply.extraction_error)
    else:
        logger.info(
            "User user language input %s %s %s",
            user_id,
            user_input,
            reply.language,
        )
        lang_code = lang_codes.get(reply.language)
        if lang_code is None:
            logger.error("User language not supported %s %s", user_id, reply.language)
            raise UserLanguageParsingError(f"Language - {reply.language} not supported")
            # await chat.send_text("Language not supported")
        update_user_language(session, user, lang_code)
        logger.info("User %s user language updated as %s", user_id, reply.language)
        # await send_daily_forecast(user, chat)
        # await send_command_explanation_message(chat)
