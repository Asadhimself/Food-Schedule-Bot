from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("commands", "Вывести справку"),
            types.BotCommand("today", "Вывести расписание на день"),
            types.BotCommand("calories", "Режим поиска"),
            types.BotCommand("restart", "Сбросить процессы"),
        ]
    )
