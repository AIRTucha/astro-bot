from telegram import Update
from src.llm.chains import cancel_chain
from src.bot_utils.language import get_language
from src.bot_utils.send_text import send_text
from src.bot_utils.update_get_user_data import get_user_first_name


async def send_cancel_message(update: Update):
    user_name = get_user_first_name(update)
    user_language = get_language(update)
    cancel_reply = cancel_chain.invoke(
        {
            "user_name": user_name,
            "user_language": user_language,
        }
    )
    await send_text(update, cancel_reply)
