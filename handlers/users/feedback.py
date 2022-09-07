from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp


@dp.message_handler(Text("📞 Обратная связь"))
async def send_feedback(message: types.Message):
    await message.answer("Постараемся вам ответить как можно скорее:\n"
                         "@asadhimself - разработчик бота\n")