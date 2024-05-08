from telegram import Update
from src.llm.chains import unexpected_input_reply_chain

from src.bot_utils.update_get_user_data import get_user_first_name
from src.bot_utils.language import get_language
from src.bot_utils.send_text import send_text
from src.bot_utils.update_get_message_data import get_message_text


async def send_unexpected_input_reply(update: Update):
    user_name = get_user_first_name(update)
    user_language = get_language(update)
    await send_text(
        update,
        unexpected_input_reply_chain.invoke(
            {
                "user_name": user_name,
                "user_language": user_language,
                "user_input": get_message_text(update),
            }
        ),
    )
