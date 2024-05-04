from telegram import ReplyKeyboardRemove, Update
from src.llm.chains import cancel_chain
from src.bot_utils.language import languages


async def send_cancel_message(update: Update):
    cancel_reply = cancel_chain.invoke(
        {
            "user_name": update.message.from_user.first_name,
            "user_language": languages[update.message.from_user.language_code],
        }
    )
    await update.message.reply_text(cancel_reply, reply_markup=ReplyKeyboardRemove())
