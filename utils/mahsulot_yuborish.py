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
from utils import admin_send_message
from data.config import  PAYMENTS_PROVIDER_TOKEN, ADMINS


async def mahsulot_yuborish(message, description, records, customer):
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    prices = []
    total = 0
    for row in records:
        product = session.query(Product).filter(Product.product_id==row.product_id).first()
        prices.append(types.LabeledPrice(label= f"{product.title}", amount=int(product.price)*int(row.amount)*100))
    text = {
    "uz" : "⬅️Ortga",
    "eng" : "⬅️Назад",
  }
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*(KeyboardButton(text[lang]), ))
    await message.answer("💴 Payme", reply_markup=keyboard)     
    await bot.send_invoice(message.chat.id, title=f"{customer.username}'s products",
                       description=description,
                       provider_token=PAYMENTS_PROVIDER_TOKEN,
                       currency='uzs',
                       photo_url='https://visualmodo.com/wp-content/uploads/2019/01/PayPal-Payment-Requests-Usage-Guide.png',
                       photo_height=512,
                       photo_width=512,
                       photo_size=512,
                       prices=prices,
                       start_parameter='products',
                       payload='Test',
                       )
