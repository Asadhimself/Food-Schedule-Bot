from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ChatType
from aiogram.utils.markdown import hbold, hitalic, quote_html

from keyboards.inline.days import days
from keyboards.inline.schedule import schedule  # , back_callback
from loader import dp, db
from states.what_to_eat import FindMeFood


@dp.message_handler(Text("🗓 Расписание на сегодня"))
@dp.message_handler(Command("today"), state='*', chat_type=[ChatType.PRIVATE])
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
        today = await db.send_food(when, day, user)
        text = "".join([hbold(f"⌛️ {day} / {when}:\n\n"),
                        hitalic(f"🥣 {quote_html(today)}\n\n"),
                        hbold("Приятного вам аппетита 🍽❤\n\n"),
                        "➡️Для просмотра другого дня нажмите /today"
                        ])
        await call.message.edit_text(text=text)
        edit_params = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Изменить время 🔄🕟", callback_data=f"edit:time:{when}:{day}"),
                    InlineKeyboardButton(text="Изменить еду 🔄🍜", callback_data=f"edit:food:{when}:{day}"),
                ]
            ]
        )
        await call.message.edit_reply_markup(reply_markup=edit_params)
        await state.finish()

# @dp.callback_query_handler(back_callback.filter(action="back"), state='*')
# async def go_back(call: CallbackQuery, state: FSMContext):
#     await call.message.edit_text(f"{call.data}\nВыберите тип перекуса:")
#     await call.message.edit_reply_markup(reply_markup=schedule)
#     await state.reset_state(with_data=False)
