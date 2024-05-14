from src.llm.chains import unexpected_input_reply_chain

from src.bot_utils.language import get_language

from src.bot_utils.chat import Chat


async def send_unexpected_input_reply(chat: Chat):
    user_name = chat.get_user_name()
    user_language = get_language(chat)
    await chat.send_text(
        unexpected_input_reply_chain.invoke(
            {
                "user_name": user_name,
                "user_language": user_language,
                "user_input": chat.get_message_text(),
            }
        ),
    )
