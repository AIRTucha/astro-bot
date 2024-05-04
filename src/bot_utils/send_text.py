from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from typing import List
from src.logger.logger import logger


async def send_text(update: Update, text: str, *button_texts: str) -> None:
    if update.message is None:
        logger.error("Update message is None")
        return
    if len(button_texts) == 0:
        await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    else:
        keyboard = [[KeyboardButton(text) for text in button_texts]]
        await update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
