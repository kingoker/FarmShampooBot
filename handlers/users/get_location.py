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
import requests 

@dp.message_handler(content_types=['location'], state=Customer_Form.location)
async def get_location(message : types.Message, state : FSMContext):
    print(message.location.latitude) 
    print(message.location.longitude) 

    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    await state.update_data({
        "location" : message,
        })  
    text = {
        "uz" : "Yetkazib berish hududidan tashqarida.",
        "eng" : "Вне зоны доставки.",
    }
    customer.latitude = message.location.latitude
    customer.longitude = message.location.longitude
    session.commit()
    r = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={message.location.latitude}&lon={message.location.longitude}&format=json")
    # res = json.loads(r)
    r = r.json()

    print(r["address"])
    try :
        address = r["address"]["city"]
    except KeyError:
        address = "Error"    
    print(address)     
    if address  != "Toshkent":# To'g'rila
        await message.answer(text[lang])
        
    else:
        text = {
        "uz" : "Buyurtmani qabul qilish uchun qulay vaqtni va izohni yozing yozing:",
        "eng" : "Укажите удобное для вас время получения заказа и ваши комментарии:",
        }
        k_text = {"uz" : "⬅️Ortga", "eng" : "⬅️Назад",}
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*(KeyboardButton(k_text[lang]),))
        await message.answer(text[lang], reply_markup=keyboard)
        await Customer_Form.delivery.set()

@dp.message_handler(lambda message:message.text=="⬅️Ortga", state=Customer_Form.location)
async def back_uz(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
    customer.products.clear()
    session.commit()
    text = "Bosh menyu"
    await state.reset_state()
    await message.answer(text, reply_markup=menu_product_types_uz)


@dp.message_handler(lambda message:message.text=="⬅️Назад", state=Customer_Form.location)
async def back_eng(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
    customer.products.clear()
    session.commit()
    text = "Главное меню"
    await state.reset_state()
    await message.answer(text, reply_markup=menu_product_types_eng)
