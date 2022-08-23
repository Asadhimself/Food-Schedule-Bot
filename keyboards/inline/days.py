from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


days = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Понедельник", callback_data="Понедельник"),
            InlineKeyboardButton(text="Вторник", callback_data="Вторник"),
        ],
        [
            InlineKeyboardButton(text="Cреда", callback_data="Среда"),
            InlineKeyboardButton(text="Четверг", callback_data="Четверг"),
        ],
        [
            InlineKeyboardButton(text="Пятница", callback_data="Пятница"),
            InlineKeyboardButton(text="Суббота", callback_data="Суббота"),
        ],
        [
            InlineKeyboardButton(text="Воскресенье", callback_data="days:Воскресенье")
        ]
    ]
)
