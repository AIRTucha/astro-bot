from src.llm.chains import (
    command_explanation_chain,
)
from src.bot_utils.language import get_language
from src.bot_utils.chat import Chat


async def send_command_explanation_message(chat: Chat):
    user_name = chat.get_user_name()
    user_language = get_language(chat)

    command_explanation_message = command_explanation_chain.invoke(
        {
            "user_name": user_name,
            "user_language": user_language,
        }
    )
    await chat.send_text(
        command_explanation_message,
    )
