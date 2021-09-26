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
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

        hour_plus = (
            ('+', 'h++'),
            ('+', 's++'),
        
        )
        clock_values = (

            ('12', '12'),
            ('00', '00'),
        
            )
        hour_minus = (
            ('-', 'h--'),
            ('-', 's--'),
        
            )
        text_keyboard = {
                "uz" : "✅ Tasdiqlash",
                "eng" : "✅ Подтвердить"
            }
        row_btns1 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in hour_plus)
        row_btns2 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in clock_values)
        row_btns3 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in hour_minus)
        row_btns4 = (types.InlineKeyboardButton(text_keyboard[lang], callback_data="✅"), )


        keyboard_markup.row(*(row_btns1))
        keyboard_markup.row(*(row_btns2))
        keyboard_markup.row(*(row_btns3))
        keyboard_markup.row(*(row_btns4))

        await message.answer(text[lang], reply_markup=keyboard_markup)
        await Customer_Form.time.set()

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
