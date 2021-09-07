from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization, savat
from loader import dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Regexp
from keyboards.default import amount_menu_uz, amount_menu_eng, products_menu_uz, products_menu_eng, menu_product_types_uz, menu_product_types_eng
from states.Customer_state import Customer_Form
from aiogram.dispatcher import FSMContext
from utils.misc.get_distance import calc_distance
from utils.misc.show_gmap import show
from data.config import ADMINS, OFFICE_LOCATION



@dp.message_handler(Text(equals="🚖Оформить заказ"), state=Customer_Form.product)
async def order_place_eng(message : types.Message, state : FSMContext):
	print("🚖Оформить заказ")
	user_id = message.from_user.id
	customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
	products = customer.products
	if len(products) > 0:	
		keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
		text = ["🚖Доставка", "🏃Самовывоз"]
		keyboard.row(*(KeyboardButton(t) for t in text))
		keyboard.add(*(KeyboardButton("⬅️Назад"),))
		await message.answer("🚖Оформить заказ", reply_markup=keyboard)
	else:
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
		await message.answer("🗑 Ваша корзина пуста, чтобы сделать заказ выберите продукты", reply_markup=products_menu_eng)
			



@dp.message_handler(Text(equals="🚖Buyurtma berish"), state=Customer_Form.product)
async def order_place_uz(message : types.Message, state : FSMContext):
	print("🚖Yetkazib berish")
	user_id = message.from_user.id
	customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
	products = customer.products
	if len(products) > 0:	
		keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
		text = ["🚖Yetkazib berish", "🏃Olib ketish"]
		keyboard.row(*(KeyboardButton(t) for t in text))
		keyboard.add(*(KeyboardButton("⬅️Ortga"),))
		await message.answer("🚖Buyurtma berish", reply_markup=keyboard)

	else:
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
		await message.answer("🗑 Sizning savatingiz bo'sh", reply_markup=products_menu_uz)
	
@dp.message_handler(lambda message : message.text in ["🚖Yetkazib berish", "🚖Доставка"], state=Customer_Form.product)
async def order_place_eng(message : types.Message, state : FSMContext):
	lang = "uz" if message.text == "🚖Yetkazib berish" else "eng"
	text = {
		"uz" : {
			"keyboard" : ["📍Geomanzilingizni yuborish", "⬅️Ortga"],
			"guide" : "Iltimos yetkazib berish manzilini quyidagi, \"📍 Geomanzilimni yuborish\" tugmasi orqali jo'nating."
		},
		"eng" : {
			"keyboard" : ["📍Отправить мое местоположение", "⬅️Назад"],
			"guide" : "Отправьте местоположение. Чтобы отправить местоположение, нажмите \"📍Отправить мое местоположение \""
		},
	} 
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*(KeyboardButton(text[lang]["keyboard"][0], request_location=True),))
	keyboard.add(*(KeyboardButton(text[lang]["keyboard"][1],),))
	await Customer_Form.location.set()
	await message.answer(text[lang]['guide'], reply_markup=keyboard)
	print("location state ga kirdi")


	
@dp.message_handler(lambda message : message.text in ["🏃Olib ketish", "🏃Самовывоз"], state=Customer_Form.product)
async def order_place_eng(message : types.Message, state : FSMContext):
	# user_id = message.from_user.id
	# customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
	lang = "uz" if message.text == "🏃Olib ketish" else "eng"
	text = {
		"uz" : "Buyurtmani qabul qilish uchun qulay vaqtni va izohni yozing yozing:",
		"eng" : "Укажите удобное для вас время получения заказа и ваши комментарии:",
	}
	k_text = {"uz" : "⬅️Ortga", "eng" : "⬅️Назад",}
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*(KeyboardButton(k_text[lang]),))
	await message.answer(text[lang], reply_markup=keyboard)
	await Customer_Form.pickup.set()

	
@dp.message_handler(lambda message:message.text == "⬅️Ortga" , state=Customer_Form.delivery)
async def ortga(message : types.Message, state : FSMContext):
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

@dp.message_handler(lambda message:message.text == "⬅️Назад" , state=Customer_Form.delivery)
async def ortga_eng(message : types.Message, state : FSMContext):
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
	
































	# text = {
	# 	"uz" : {
	# 		"guide" : "Ofisimiz telefon raqami : +123456789.\nQiziqishingiz uchun rahmat!",
	# 	},
	# 	"eng" : {
	# 		"guide" : "Our office number : +123456789.\nThanks for your interests for our service!",
	# 	},
	# } 
	# keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
	# await message.answer_location(latitude=OFFICE_LOCATION[0], longitude=OFFICE_LOCATION[1])
	# await message.answer(text[lang]["guide"], reply_markup=keyboard)
	# products = customer.products	
	# admin_text = f"<strong>{customer.username}</strong> quyidagi mahsulotlarni olib ketish orqali sotib olmoqchi:"
	# total_price = 0
	# i = 0
	# records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id == customer.customer_id).all()
	# for row in records:
	# 	product = session.query(Product).filter(Product.product_id==row.product_id).first()
	# 	i +=1
	# 	admin_text += f"<strong>{i}. {product.title}</strong>\n\n"
	# 	total_price += int(row.amount) * int(product.price)
	# 	price = format(int(product.price),",d").replace(',', ' ')
	# 	amount_show = f"{int(row.amount) * int(product.price):,}".replace(',', ' ')
	# 	admin_text+= f"{row.amount} x {price} = {amount_show} so'm\n\n"
	# total_price = f"{total_price:,}".replace(',', ' ')
	# admin_text += f"<strong>Umumiy: </strong> {total_price} so'm\n"
	# admin_text += f"{customer.username} bilan bog'lanish tili {customer.language}\nTelefon raqam: {customer.phone}."

	# for admin in ADMINS:
	# 	try:
	# 		await dp.bot.send_message(admin, admin_text)

	# 	except Exception as err:
	# 		logging.exception(err)

	# await state.reset_state()



			