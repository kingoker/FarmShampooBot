from aiogram.dispatcher.filters.state import StatesGroup, State

class Customer_Form(StatesGroup):
	product = State()
	amount = State()
	time = State()
	comment = State()
	savat = State()
	# location = State()
	pickup = State()
	tolov_turi = State()
	comment = State()
	yuborish_turi = State()
	delivery = State()
	location = State()
	payment = State()

