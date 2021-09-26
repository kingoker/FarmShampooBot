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
from utils.admin_messages import admin_send_message
from data.config import ADMINS, OFFICE_LOCATION


@dp.message_handler(lambda message : message.text in ["⬅️Назад", "⬅️Ortga"], state=Customer_Form.comment)
async def back_from_comment(message : types.Message, state : FSMContext):
	user_id = message.from_user.id
	customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
	customer.products.clear()
	session.commit()
	lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
	text = {
		"uz" : "Bosh menyu",
		"eng" : "Главное меню"
	}
	await state.reset_state()
	keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
	await message.answer(text[lang], reply_markup=keyboard)


@dp.message_handler(lambda message : message.text not in ["⬅️Назад", "⬅️Ortga"], state=Customer_Form.comment)
async def comment_input(message : types.Message, state : FSMContext):
	user_id = message.from_user.id
	customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
	lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
	comment = message.text
	customer.comment = comment
	session.commit()
	# await state.update_data({
	# 	"comment" : comment,
	# 	})
	# ikki tilga to'g'rila
	keyboard = tolov_uz if lang == "uz" else tolov_eng
	text = {
		'uz': 'To\'lov turini tanlang!',
		'eng': 'Выберите вариант оплаты',
	}
	await message.answer(text[lang], reply_markup=keyboard)
	await Customer_Form.tolov_turi.set()
