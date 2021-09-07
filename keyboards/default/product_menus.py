from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


products_menu_uz = ReplyKeyboardMarkup(
	keyboard = [
	[
		KeyboardButton(text="📥Savat"),
		KeyboardButton(text="🚖Buyrtuma berish")
	],
	],
	row_width=2,
	resize_keyboard=True
	)





products_menu_eng = ReplyKeyboardMarkup(
	keyboard = [
	[
		KeyboardButton(text="📥Basket"),
		KeyboardButton(text="🚖Place an order")
	],
	],
	row_width=2,
	resize_keyboard=True
	)


