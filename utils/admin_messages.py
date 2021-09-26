from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization, savat
from loader import dp, bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Regexp
from aiogram.types.message import ContentTypes
from keyboards.default import amount_menu_uz, amount_menu_eng, products_menu_uz, products_menu_eng, menu_product_types_uz, menu_product_types_eng
from states.Customer_state import Customer_Form
from aiogram.dispatcher import FSMContext
from utils.misc.show_gmap import show
from data.config import  PAYMENTS_PROVIDER_TOKEN, ADMINS



async def admin_send_message(message, customer, pickup=False, delivery=False, paid=False, cash=False, location=False):
	if customer.yuborish_turi == "🚖Доставка":
		admin_text = f"<strong>🚖 Новый заказ</strong> – Доставка:\n"
	else:
		admin_text = f"🏃 <strong>Новый заказ</strong> – Самовывоз:\n"
	total_price = 0
	admin_text += f"<strong>Юзер</strong>:@{message.from_user.username}\n"
	admin_text += f"<strong>Имя</strong>:{customer.username}\n"
	admin_text += f"<strong>Номер телефона</strong>: {customer.phone}\n"
	admin_text += f"<strong>Язык</strong>: {customer.language}\n"
	i = 0
	records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id == customer.customer_id).all()
	for row in records:
		product = session.query(Product).filter(Product.product_id==row.product_id).first()
		i +=1
		admin_text += f"<strong>{i}. {product.title}</strong>\n\n"
		total_price += int(row.amount) * int(product.price)
		price = format(int(product.price),",d").replace(',', ' ')
		amount_show = f"{int(row.amount) * int(product.price):,}".replace(',', ' ')
		admin_text+= f"{row.amount} x {price} = {amount_show} UZS\n\n"
	total_price = f"{total_price:,}".replace(',', ' ')
	admin_text += f"<strong>Сумма оплаты: </strong> {total_price} UZS\n"
	if cash:
		admin_text += f"<strong>Cпособ оплаты</strong>: Наличные\n"
	if not paid:
		admin_text += f"<strong>Оплачено</strong>: ⛔\n"
	else:
		admin_text += f"<strong>Оплачено</strong>: ✅\n"
	if location:
		admin_text += f"<strong>Адрес</strong>: {show(customer.latitude, customer.longitude)}\n" 	
	admin_text += f"<strong>Время: </strong> {customer.time}\n"
	admin_text += f"<strong>Комментарии</strong>:{customer.comment}"
	for admin in ADMINS:
		try:
			await dp.bot.send_message(admin, admin_text)

		except Exception as err:
			logging.exception(err)

