from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# menu_product_types_eng = ReplyKeyboardMarkup

menu_product_types_eng = ReplyKeyboardMarkup(
	resize_keyboard=True
	)
menu_product_types_eng.add(*(KeyboardButton("🛍Заказать"),))
menu_product_types_eng.row(*(KeyboardButton(text) for text in ["✍️Оставить отзыв", "☎️Связаться с нами"]))
menu_product_types_eng.row(*(KeyboardButton(text) for text in ["ℹ️Информация", "⚙️Настройки"]))



menu_product_types_uz = ReplyKeyboardMarkup(
	resize_keyboard=True
	)
menu_product_types_uz.add(*(KeyboardButton("🛍Buyurtma berish"),))
menu_product_types_uz.row(*(KeyboardButton(text) for text in ["✍️Fikr bildirish", "☎️Biz bilan aloqa"]))
menu_product_types_uz.row(*(KeyboardButton(text) for text in ["ℹ️Ma'lumot", "⚙️Sozlamalar"]))

