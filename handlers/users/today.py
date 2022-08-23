from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.days import days
from keyboards.inline.edit import edit_callback
from keyboards.inline.schedule import schedule
from loader import dp, db
from states.what_to_eat import FindMeFood


@dp.message_handler(Command("today"))
async def day_command(message: types.Message):
    await message.answer("Выберите день:", reply_markup=days)
    await FindMeFood.EnterDay.set()


@dp.callback_query_handler(state=FindMeFood.EnterDay)
async def set_day(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"{call.data}\nВыберите тип перекуса:")
    await call.message.edit_reply_markup(reply_markup=schedule)
    await state.update_data(day=call.data)
    await FindMeFood.next()


@dp.callback_query_handler(state=FindMeFood.EnterWhen)
async def find_food(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=10)
    await state.update_data(when=call.data)
    async with state.proxy() as data:
        day = data.get("day")
        when = data.get("when")
        user = call.message.chat.id
        today = await db.send_food(when, day)
        await call.message.edit_text(f"{day} / {when}:\n"
                                     f"{today}\n"
                                     "Приятного вам аппетита ")
        edit_params = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Изменить время", callback_data=f"edit:time:{day}:{when}"),
                    InlineKeyboardButton(text="Изменить еду", callback_data=f"edit:food:{day}:{when}"),
                ]
            ]
        )
        await call.message.edit_reply_markup(reply_markup=edit_params)
        await state.finish()


@dp.callback_query_handler(edit_callback.filter(action="time"))
async def edit_food(call: CallbackQuery, callback_data: dict):
    print(callback_data)
    await call.answer("Эта функция пока что недоступна!", show_alert=True)


@dp.callback_query_handler(edit_callback.filter(action="food"))
async def edit_food(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=10)
    await call.message.answer("Хорошо! пришлите сообщение и я поменяю на него в вашем графика")
