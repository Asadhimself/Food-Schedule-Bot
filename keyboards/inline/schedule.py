from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


schedule = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Завтрак", callback_data="Завтрак"),
            InlineKeyboardButton(text="Утренний перекус", callback_data="Утренний перекус"),
        ],
        [
            InlineKeyboardButton(text="Обед", callback_data="Обед"),
        ],
        [
            InlineKeyboardButton(text="Вечерний перекус", callback_data="Вечерний перекус"),
            InlineKeyboardButton(text="Ужин", callback_data="Ужин"),
        ],
    ]
)
