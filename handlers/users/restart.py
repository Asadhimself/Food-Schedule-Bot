from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("restart"), state='*')
async def restart_bot(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Обнулил процессы. . .")