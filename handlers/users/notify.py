# import asyncio
# import aioschedule
# from aiogram.dispatcher.filters import Command
#
# from loader import bot, dp
#
#
# @dp.message_handler(Command("schedule"))
# async def choose_your_dinner():
#     await bot.send_message(chat_id=289241304, text="Я сработал")
#
# async def scheduler():
#     aioschedule.every().day.at("02:10").do(choose_your_dinner)
#
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)
#
#
#     # if __name__ == '__main__':
#     #     executor.start_polling(on_startup=on_startup)
