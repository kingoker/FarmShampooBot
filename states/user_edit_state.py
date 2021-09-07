from aiogram.dispatcher.filters.state import StatesGroup, State

class Personal_edit(StatesGroup):
	language = State()
	phone = State()
	code = State()
	name = State()

