from src.logger.logger import logger
from src.bot_utils.language import get_error_message
from src.bot_utils.chat import Chat


async def send_critical_error(chat: Chat, error: str) -> None:
    user_id = chat.get_user_id()
    logger.error("User %s, got critical error %s", user_id, error)
    error_message = get_error_message(chat)
    await chat.send_text(error_message)
