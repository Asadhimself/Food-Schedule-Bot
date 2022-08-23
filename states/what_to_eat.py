from aiogram.dispatcher.filters.state import StatesGroup, State


class FindMeFood(StatesGroup):
    EnterDay = State()
    EnterWhen = State()