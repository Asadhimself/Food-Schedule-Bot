from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.add_user(message.from_user.full_name, message.from_user.username, message.from_user.id)
        await db.set_private_table(message.from_user.id)
        await message.answer(f"Привет, {message.from_user.full_name}!")
    except Exception as err:
        await bot.send_message(ADMINS[0], f"{err.__class__.__name__}: {err} \n"
                                          f"Пользователь: {message.from_user}")
