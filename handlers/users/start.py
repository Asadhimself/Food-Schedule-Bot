from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_menu import main_menu
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.add_user(message.from_user.full_name, message.from_user.username, message.from_user.id)
        await db.set_private_table(message.from_user.id)
        await message.answer(f"👋Привет, {message.from_user.full_name}!\n"
                             f"Я уже создал для вас ваше личное расписание!🗓\n\n"
                             f"Проверить его вы можете по команде /today\n\n"
                             f"И получить справку о боте по команде /help",
                             reply_markup=main_menu)
    except:
        await message.answer(f"👋 Привет, {message.from_user.full_name}!\n"
                             f"Я вас помню. С возвращением ❤️", reply_markup=main_menu)
