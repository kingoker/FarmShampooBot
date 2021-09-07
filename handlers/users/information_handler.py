from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization
from loader import dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from keyboards.default import products_menu_uz, products_menu_eng
from states.Customer_state import Customer_Form
from database.database import session, Customer, Product, Organization, savat
from data.config import OFFICE_LOCATION

@dp.message_handler(Text(equals="ℹ️Информация", ignore_case=True))
async def order_handler(message: types.Message):
    text = "Официальный дистрибьютор Merz Pharmaceuticals GmbH в Узбекистане.\nТелефоны:\n+998 (95)177-38-98\n+998 (97) 700-92-21\n+998 (90) 941-52-00"
    await message.answer(text) # productlar ro'yxatini chiqar
    await message.answer_location(latitude=OFFICE_LOCATION[0], longitude=OFFICE_LOCATION[1])


@dp.message_handler(Text(equals="ℹ️Ma'lumot", ignore_case=True))
async def order_handler(message: types.Message):
    text = "Merz Pharmaceuticals GmbH kompaniyasining O'zbekistondagi rasmiy distribyutori. .\nTelefon raqamlarimiz:\n+998 (95)177-38-98\n+998 (97) 700-92-21\n+998 (90) 941-52-00"
    await message.answer(text) # productlar ro'yxatini chiqar
    await message.answer_location(latitude=OFFICE_LOCATION[0], longitude=OFFICE_LOCATION[1])

    
    