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
from utils import admin_send_message, mahsulot_yuborish
from data.config import  PAYMENTS_PROVIDER_TOKEN, ADMINS


@dp.message_handler(lambda message:message.text=="⬅️Ortga", state=Customer_Form.delivery)
async def back_uz(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
    customer.products.clear()
    session.commit()
    text = "Bosh menyu"
    await state.reset_state()
    await message.answer(text, reply_markup=menu_product_types_uz)


@dp.message_handler(lambda message:message.text=="⬅️Назад", state=Customer_Form.delivery)
async def back_eng(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
    customer.products.clear()
    session.commit()
    text = "Главное меню"
    await state.reset_state()
    await message.answer(text, reply_markup=menu_product_types_eng)




@dp.message_handler(state=Customer_Form.delivery)
async def delivery(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id==customer.customer_id).all()
    if lang == "uz":
        description = "To'lov qilish uchun quyidagi tugmani bosing."
    else :
        description = "Нажмите кнопку ниже, чтобы заплатить."    
    await mahsulot_yuborish(message, description, records, customer)
    await state.reset_state()



@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    print(customer.products)
    customer.products.clear()
    await admin_send_message(message=message, customer=customer, paid=True)
    customer.latitude = None
    customer.longitude = None
    session.commit()    
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    text = {"uz":"Xaridingiz uchun rahmat.", "eng" : "Спасибо за покупку."}
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng    
    await message.answer(text[lang],reply_markup=keyboard)
