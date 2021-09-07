from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization
from loader import dp
from states.product_del_state import Product_del_State
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=["product_delete"])
async def bot_help(message: types.Message):
    await message.answer("Product ni o'chirishingiz uchun uning title ini kiriting: ")
    await Product_del_State.title.set()


@dp.message_handler(state=Product_del_State.title)
async def title_input(message: types.Message, state : FSMContext):
    title = message.text
    await state.update_data({
        "title" : title,
        })
    product = session.query(Product).filter(Product.title == title).first()

    if product is not None:
        session.delete(product)
        session.commit()
        await message.answer("Product o'chirildi")
    else:
        await message.answer("Bunday product mavjud emas!")

    await state.reset_state()
