from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menuStart = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="🇺🇿O'zbekcha"),
		],
		[
			KeyboardButton(text="🇷🇺Русский")
		]
	], 
	one_time_keyboard=True,
	resize_keyboard=True
	)