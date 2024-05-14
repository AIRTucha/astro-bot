from telegram import Update
from src.llm.chains import cancel_chain
from src.bot_utils.language import get_language
from src.bot_utils.chat import Chat


async def send_cancel_message(chat: Chat):
    user_name = chat.get_user_name()
    user_language = get_language(chat)
    cancel_reply = cancel_chain.invoke(
        {
            "user_name": user_name,
            "user_language": user_language,
        }
    )
    await chat.send_text(cancel_reply)
