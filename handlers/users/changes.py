from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.edit import edit_callback
from loader import dp, db


@dp.callback_query_handler(edit_callback.filter(action="time"))
async def edit_food(call: CallbackQuery, callback_data: dict):
    await call.answer("Эта функция пока что недоступна!", show_alert=True)


@dp.callback_query_handler(edit_callback.filter(action="food"))
async def edit_food(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=10)
    info = callback_data
    await call.message.answer(f"Изменения на {info['schedule_day']} / {info['schedule_when']}:\n\n"
                              "Хорошо! пришлите сообщение и я поменяю на него в вашем графике")
    await state.set_state("changes")
    await state.update_data(day=info['schedule_day'])
    await state.update_data(when=info['schedule_when'])


@dp.message_handler(state="changes")
async def set_changes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            day, when = data.get("day"), data.get("when")
            today_old = await db.send_food(when, day, message.chat.id)
            await message.answer(f"Изменения в {day} / {when}\n\n"
                                 f"Старая запись: {today_old}\n"
                                 f"Новая запись: {message.text}")
            await db.change_food(when, day, message.chat.id, message.text)
        except Exception as err:
            await message.answer(f"{err.__class__.__name__}: {err}")
        await state.finish()

