from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


back_menu_uz = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton("⬅️Ortga")],
	],
	resize_keyboard=True
)


back_menu_eng = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton("⬅️Назад")],
	],
	resize_keyboard=True
)

edit_settings_menu_eng = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="Изменить Имя"),
			KeyboardButton(text="Изменить номер"),
		],
		[
            KeyboardButton(text="🇷🇺 Выберите язык"),
        ],            
        [
            KeyboardButton("⬅️Назад")
        ],
		
	], 
	resize_keyboard=True
	)
edit_settings_menu_uz = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Ismni o'zgartirish"),
                KeyboardButton(text="Raqamni o'zgartirish"),
            ],
            [
                KeyboardButton(text="🇺🇿 Tilni tanlang"),
            ],            
            [
                KeyboardButton("⬅️Ortga")
            ],
        ], 
        resize_keyboard=True
    )
