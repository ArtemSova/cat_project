# reply_kbrd
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Все котики"),
            KeyboardButton(text="Новый котик"),
        ],
        [
            KeyboardButton(text="Создать/изменить пароль для сайта"),
        ],
    ],
    resize_keyboard=True,                        # нормальный размер кнопок
    input_field_placeholder="Выберите команду",  # текст в поле ввода
)
