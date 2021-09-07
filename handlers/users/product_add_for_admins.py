from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization
from loader import dp
from states.product_state import Product_State
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")
    
    await message.answer("\n".join(text))

@dp.message_handler(commands=["product_add"])
async def bot_help(message: types.Message):
    await message.answer("Product qo'shishingiz mumkin, title kiriting: ")
    await Product_State.title.set()


@dp.message_handler(state=Product_State.title)
async def bot_help(message: types.Message, state : FSMContext):
    title = message.text
    await state.update_data({
        "title" : title,
        })
    await message.answer("product rasmini yuboring : ")
    await Product_State.image_id.set()


@dp.message_handler(content_types=["photo"],state=Product_State.image_id)
async def bot_help(message: types.Message, state : FSMContext):
    image_id = message.photo[-1].file_id
    print(image_id)
    await state.update_data({
        "image_id" : image_id,
        })
    await message.answer("productga description yuboring : ")
    await Product_State.description.set()


@dp.message_handler(state=Product_State.description)
async def bot_help(message: types.Message, state : FSMContext):
    description = message.text
    await state.update_data({
        "description" : description,
        })
    await message.answer("product narxini yuboring : ")
    await Product_State.price.set()

@dp.message_handler(state=Product_State.price)
async def bot_help(message: types.Message, state : FSMContext):
    try :
        price = message.text
        await state.update_data({
            "price" : price,
            })
        data = await state.get_data()
        title = data.get("title")
        image_id = data.get("image_id")
        description = data.get("description")
        price = data.get("price")
        test = int(price)
        product = Product(title=title, description=description, photo_id=image_id, price=price)
        session.add(product)
        session.commit()
        print("commited")
        await state.reset_state()
        await message.answer("product yuklandi : ")
    except ValueError:
        await message.answer("Iltimos faqat sonlar kiriting.")    
