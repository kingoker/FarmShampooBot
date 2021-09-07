from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization
from loader import dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from keyboards.default import products_menu_uz, products_menu_eng
from states.Customer_state import Customer_Form
from database.database import session, Customer, Product, Organization, savat


@dp.message_handler(Text(equals="🛍Заказать", ignore_case=True))
async def order_handler(message: types.Message):
    user_id = message.from_user.id
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
    await message.answer("💫 С чего начнём?", reply_markup=products_menu_eng) # productlar ro'yxatini chiqar
    await Customer_Form.product.set()



@dp.message_handler(Text(equals="🛍Buyurtma berish", ignore_case=True))
async def order_handler(message: types.Message):
    user_id = message.from_user.id
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
    await message.answer("💫 Nimadan boshlaymiz?", reply_markup=products_menu_uz) # productlar ro'yxatini chiqar
    await Customer_Form.product.set()

    