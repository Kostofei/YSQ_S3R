from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from data_file.answers_list import answers, answers_extended


answer_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=answers[str(i)]) for i in range(1, 3)],
        [KeyboardButton(text=answers[str(i)]) for i in range(3, 5)],
        [KeyboardButton(text=answers[str(i)]) for i in range(5, 7)],
    ],
    resize_keyboard=False,
)

answer_keyboard_extended = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=answers[str(i)]) for i in range(1, 3)],
        [KeyboardButton(text=answers[str(i)]) for i in range(3, 5)],
        [KeyboardButton(text=answers[str(i)]) for i in range(5, 7)],
        [KeyboardButton(text='Назад')],
    ],
    resize_keyboard=False,
)

del_keyboard = ReplyKeyboardRemove()


