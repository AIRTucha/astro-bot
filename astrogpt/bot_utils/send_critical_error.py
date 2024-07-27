from astrogpt.logger.logger import logger
from astrogpt.bot_utils.language import get_error_message
from astrogpt.bot_utils.chat import Chat


async def send_critical_error(chat: Chat, error: str) -> None:
    try:
        user_id = chat.get_user_id()
        logger.error("User %s, got critical error %s", user_id, error)
        error_message = get_error_message(chat)
        await chat.send_text(error_message)
    except Exception as e:
        logger.error("Error in send_critical_error %s", str(e))
