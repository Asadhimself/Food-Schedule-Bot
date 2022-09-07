from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.callback_data import CallbackData
#
# back_callback = CallbackData("do", "action")

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
        # [
        #     InlineKeyboardButton(text="Выбрать другой день", callback_data="do:back")
        # ]
    ]
)
