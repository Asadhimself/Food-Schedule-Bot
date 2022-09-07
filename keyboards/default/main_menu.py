from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔎 Поисковик калорий"),
            KeyboardButton(text="🗓 Расписание на сегодня")
        ],
        [
            KeyboardButton(text="🆘 Помощь в боте")
        ],
        [
            KeyboardButton(text="📞 Обратная связь")
        ]
    ],
    resize_keyboard=True
)