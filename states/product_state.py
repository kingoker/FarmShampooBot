from aiogram.dispatcher.filters.state import StatesGroup, State

class Product_State(StatesGroup):
	title = State()
	image_id = State()
	description = State()
	price = State()

