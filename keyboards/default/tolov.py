from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


tolov_uz = ReplyKeyboardMarkup(
	row_width=2,
	resize_keyboard=True,
	one_time_keyboard=True
	)
tolov_uz.add(*(KeyboardButton(text=text) for text in ["💴 Naqd pul", "💴 Payme", "⬅️Ortga"]))



tolov_eng = ReplyKeyboardMarkup(
	row_width=2,
	resize_keyboard=True,
	one_time_keyboard=True

	)
tolov_eng.add(*(KeyboardButton(text=text) for text in ["💴 Наличные", "💴 Payme","⬅️Назад"]))
