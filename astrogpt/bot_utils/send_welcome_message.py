from astrogpt.llm.chains import welcome_chain

from astrogpt.bot_utils.language import get_language

from astrogpt.bot_utils.chat import Chat


async def send_welcome_message(chat: Chat):
    user_name = chat.get_user_name()
    user_language = get_language(chat)
    await chat.send_text(
        welcome_chain.invoke(
            {
                "user_name": user_name,
                "user_language": user_language,
            }
        ),
    )
