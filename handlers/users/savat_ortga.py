from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization, savat
from loader import dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Regexp
from keyboards.default import amount_menu_uz, amount_menu_eng, products_menu_uz, products_menu_eng, menu_product_types_uz, menu_product_types_eng
from states.Customer_state import Customer_Form
from aiogram.dispatcher import FSMContext

@dp.message_handler(Text(equals="⬅️Назад"), state=Customer_Form.savat)
async def ortga_main_menu(message : types.Message, state : FSMContext):
    text = "😃 Привет, оформим вместе заказ?"    
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
    # keyboard = menu_product_types_eng
    await message.answer(text, reply_markup=products_menu_eng)
    await state.reset_state()
    await Customer_Form.product.set()

@dp.message_handler(Text(equals="⬅️Ortga"), state=Customer_Form.savat)
async def ortga_main_menu(message : types.Message, state : FSMContext):
    text = "Juda yaxshi birgalikda buyurtma beramizmi? 😃"    
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
    await message.answer(text, reply_markup=products_menu_uz)
    await state.reset_state()
    await Customer_Form.product.set()

    # keyboard = menu_product_types_uz
    # await message.answer(text, reply_markup=keyboard)
    # await state.reset_state()
