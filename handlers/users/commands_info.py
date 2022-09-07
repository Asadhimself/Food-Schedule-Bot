from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from loader import dp


@dp.message_handler(Text("🆘 Помощь в боте"))
@dp.message_handler(Command("commands"), state='*')
async def send_commands(message: types.Message):
    await message.answer("\n".join(["Список команд: ",
                                    "/start - Начать диалог 💬",
                                    "/help - Получить помощь в пользовании бота 🆘",
                                    "/about - Получить справку о боте 📓",
                                    "/calories - Поиск калорийности продуктов 🔍",
                                    "/today - Вызвать расписание на сегодня 🗓",
                                    "/restart - В случае возникновения ошибок. Перезапускает все процессы 🔁",
                                    "/menu - Вызвать главное меню 📢",
                                    "/commands - Вызвать полный список доступных команд 🖥"]))
