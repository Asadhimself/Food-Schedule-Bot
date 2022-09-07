from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db


@dp.message_handler(Text("🔎 Поисковик калорий"))
@dp.message_handler(Command("calories"), state='*')
async def send_inline_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Для входа в режим поиска введите юзернейм бота✍️:\n"
                              "<code>@eat_with_me_bot</code>\n\n"
                              "Вы можете вызвать поисковик в любом другом чате 🌐\n\n"
                              "Так же для входа в инлайн режим можете кликнуть по кнопке ниже↙️",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [
                                 InlineKeyboardButton(text="Войти в инлайн режим", switch_inline_query_current_chat=""),
                                 InlineKeyboardButton(text="Инлайн режим в другом чате",
                                                      switch_inline_query=""),
                             ]
                         ]))


@dp.inline_handler(text="")
async def empty_query(query: types.InlineQuery):
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="unknown",
                title="Введите какой-то запрос🗑. Помощь в запросе:",
                input_message_content=types.InputTextMessageContent(
                    message_text="Для входа в режим поиска введите юзернейм бота✍️:\n"
                                 "<code>@eat_with_me_bot</code>\n\n"
                                 "Вы можете вызвать поисковик в любом другом чате 🌐\n\n"
                                 "Так же для входа в инлайн режим можете кликнуть по кнопке ниже↙️",
                    parse_mode="HTML"
                ),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Пример запроса 🆘",
                            switch_inline_query_current_chat="Баранина")
                    ]
                ]
                )
            )
        ],
        cache_time=5
    )


@dp.inline_handler()
async def some_query(query: types.InlineQuery):
    # то, что вводит пользователь в инлайн режиме
    user_input = query.query.lower()
    # username всех пользователей из базы
    records = await db.get_all_products()
    inline_queries = []
    for num, item in enumerate(records, start=1):
        if user_input.lower() in item["product_name"].lower():
            res = types.InlineQueryResultArticle(
                id=str(num),
                title=f"{item['product_name']}",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"🍲 <b>{item['product_name']}</b>:\n"
                                 f"💪 <i>Калории:</i> {item['calories']}\n"
                                 f"🥚 <i>Белки:</i> {item['proteins']}\n"
                                 f"🥩 <i>Жиры:</i> {item['fats']}\n"
                                 f"🍞 <i>Углеводы:</i> {item['carbohydronates']}")
            )
            inline_queries.append(res)

    await query.answer(
        results=inline_queries[:50]
    )
