from aiogram.dispatcher.filters.state import StatesGroup, State

class Customer_Form(StatesGroup):
	product = State()
	amount = State()
	time = State()
	comment = State()
	savat = State()
	# location = State()
	pickup = State()
	delivery = State()
	location = State()
	payment = State()

