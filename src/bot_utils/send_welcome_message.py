from telegram import ReplyKeyboardRemove, KeyboardButton, Update
from src.llm.chains import welcome_chain, welcome_again_chain
from src.bot_utils.language import languages


async def send_welcome_message(update: Update):
    KeyboardButton(
        text="🌐 Change language",
    )
    await update.message.reply_text(
        welcome_chain.invoke(
            {
                "user_name": update.message.from_user.first_name,
                "user_language": languages[update.message.from_user.language_code],
            }
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


async def send_welcome_again_message(update: Update):
    KeyboardButton(
        text="🌐 Change language",
    )
    await update.message.reply_text(
        welcome_again_chain.invoke(
            {
                "user_name": update.message.from_user.first_name,
                "user_language": languages[update.message.from_user.language_code],
            }
        ),
        reply_markup=ReplyKeyboardRemove(),
    )
