from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold, hitalic, quote_html

from keyboards.inline.confirm_call import confirm_callback
from keyboards.inline.edit import edit_callback
from loader import dp, db


@dp.callback_query_handler(edit_callback.filter(action="time"))
async def edit_food(call: CallbackQuery, callback_data: dict):
    await call.answer("Эта функция пока что недоступна...😓", show_alert=True)


@dp.callback_query_handler(edit_callback.filter(action="food"))
async def edit_food(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=10)
    info = callback_data
    await call.message.answer(f"⏳ Изменения в {info['schedule_day']} / {info['schedule_when']}:\n\n"
                              "Хорошо! пришлите сообщение и я поменяю на него в вашем графике 🦾")
    await state.set_state("changes")
    await state.update_data(day=info['schedule_day'])
    await state.update_data(when=info['schedule_when'])


@dp.message_handler(state="changes")
async def set_changes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            day, when = data.get("day"), data.get("when")
            today_old = await db.send_food(when, day, message.chat.id)
            confirm = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Подтвердить изменения",
                                         callback_data=f"action:yes:{day}:{when}:{'+'.join(message.text.split())}"),
                    InlineKeyboardButton(text="❌ Отменить изменения", callback_data="action:no:no:no:no")
                ]
            ])
            text = [hbold(f"⏳ Изменения в {day} / {when}\n\n"),
                    hitalic(f"❌ Старая запись: {quote_html(today_old)}\n"),
                    hitalic(f"✅ Новая запись: {quote_html(message.text)}\n\n"),
                    (f"🙏 Для просмотра другого дня нажмите /today")]
            await message.answer(text="".join(text),
                                 reply_markup=confirm)
        except Exception as err:
            await message.answer(f"{err.__class__.__name__}: {err}")
        await state.finish()


@dp.callback_query_handler(confirm_callback.filter(conf="yes"))
async def conf_yes(call: CallbackQuery, callback_data: dict):
    info = callback_data
    food = " ".join(info['food'].split("+"))
    await db.change_food(info['when'], info['day'], call.from_user.id, food)
    await call.message.edit_text("Изменения успешно внесены! 🧷\n\n"
                                 "Посмотреть другой день /today")
    await call.message.edit_reply_markup()


@dp.callback_query_handler(confirm_callback.filter(conf="no"))
async def conf_no(call: CallbackQuery):
    await call.message.edit_text("Хорошо. Оставил старую запись 😌\n\n"
                                 "Посмотреть другой день /today")
    await call.message.edit_reply_markup()