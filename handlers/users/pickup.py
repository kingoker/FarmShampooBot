from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization, savat
from loader import dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Regexp
from keyboards.default import tolov_uz, tolov_eng, amount_menu_uz, amount_menu_eng, products_menu_uz, products_menu_eng, menu_product_types_uz, menu_product_types_eng
from states.Customer_state import Customer_Form
from aiogram.dispatcher import FSMContext
from utils.misc.get_distance import calc_distance
from utils.misc.show_gmap import show
from utils import admin_send_message
from data.config import ADMINS, OFFICE_LOCATION



@dp.message_handler(lambda message : message.text == "⬅️Ortga", state=Customer_Form.pickup)
async def ortga_comment_input_uz(message : types.Message, state : FSMContext):
	user_id = message.from_user.id
	customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
	customer.products.clear()
	session.commit()
	products = session.query(Product).all()
	titles = [p.title for p in products]
	titles.append("⬅️Ortga")
	products_menu_uz = ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton("📥Savat"),
				KeyboardButton("🚖Buyurtma berish"),
			],
		],
		row_width=2,
		resize_keyboard=True,
		)
	products_menu_uz.add(*(KeyboardButton(title) for title in titles))
	await message.answer("Mahsulot tanlang", reply_markup=products_menu_uz)
	await Customer_Form.product.set()



@dp.message_handler(lambda message : message.text == "⬅️Назад", state=Customer_Form.pickup)
async def ortga_comment_input_eng(message : types.Message, state : FSMContext):
	user_id = message.from_user.id
	customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
	customer.products.clear()
	session.commit()
	products = session.query(Product).all()
	titles = [p.title for p in products]
	titles.append("⬅️Назад")
	products_menu_eng = ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton("📥Корзина"),
				KeyboardButton("🚖Оформить заказ"),
			],
		],
		row_width=2,
		resize_keyboard=True,
		)
	products_menu_eng.add(*(KeyboardButton(title) for title in titles))
	await message.answer("Выберите продукт", reply_markup=products_menu_eng)
	await Customer_Form.product.set()
	





@dp.message_handler(state=Customer_Form.pickup)
async def comment_input(message : types.Message, state : FSMContext):
	comment = message.text
	user_id = message.from_user.id
	customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
	customer.comment = comment
	lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
	text = {
		"uz" : {
			"guide" : "Ofisimiz telefon raqamlari :\n+998 (95) 177-38-98\n+998 (97) 700-92-21\n+998 (90) 941-52-00.\nQiziqishingiz uchun rahmat!",
		},
		"eng" : {
			"guide" : "Номера телефонов наших офисов :\n+998 (95) 177-38-98\n+998 (97) 700-92-21\n+998 (90) 941-52-00.\nСпасибо за Ваш интерес!",
		},
	} 
	keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
	await message.answer_location(latitude=OFFICE_LOCATION[0], longitude=OFFICE_LOCATION[1])
	await message.answer(text[lang]["guide"], reply_markup=keyboard)
	products = customer.products
	data = await state.get_data()
	tolov_turi = data.get("tolov_turi")
	if tolov_turi:
		await admin_send_message(message, customer, pickup=True, cash=True)
	else:	
		await admin_send_message(message, customer, pickup=True)
	
	customer.products.clear()
	session.commit()

	await state.reset_state()
