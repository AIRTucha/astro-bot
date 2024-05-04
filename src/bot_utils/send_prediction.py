from telegram import ReplyKeyboardMarkup, KeyboardButton, Update

from src.llm.chains import prediction_chain
from src.bot_utils.language import languages, subscribe


async def send_prediction(update: Update, birthday_text: str) -> None:
    prediction = prediction_chain.invoke(
        {
            "user_name": update.message.from_user.first_name,
            "birth_day": birthday_text,
            "user_language": languages[update.message.from_user.language_code],
        }
    )
    await update.message.reply_text(
        prediction,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(subscribe[update.message.from_user.language_code])]
            ]
        ),
    )
