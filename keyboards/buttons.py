from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

balance = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Balance")]
], resize_keyboard=True,one_time_keyboard=True)
