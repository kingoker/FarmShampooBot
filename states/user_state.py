from aiogram.dispatcher.filters.state import StatesGroup, State

class Personal(StatesGroup):
	language = State()
	phone = State()
	code = State()
	name = State()

