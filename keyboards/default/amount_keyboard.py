from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


amount_menu_uz = ReplyKeyboardMarkup(
	row_width=3,
	resize_keyboard=True
	)
amount_menu_uz.add(*(KeyboardButton(text=num) for num in ['1', '2', '3', '4', '5', '6', '7', '8', '9', "📥Savat", "⬅️Ortga"]))



amount_menu_eng = ReplyKeyboardMarkup(
	row_width=3,
	resize_keyboard=True
	)
amount_menu_eng.add(*(KeyboardButton(text=num) for num in ['1', '2', '3', '4', '5', '6', '7', '8', '9', "📥Kорзина", "⬅️Назад"]))
