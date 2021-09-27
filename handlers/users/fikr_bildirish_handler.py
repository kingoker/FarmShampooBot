from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from keyboards.default import products_menu_uz, products_menu_eng, menu_product_types_uz, menu_product_types_eng
from states.Customer_state import Customer_Form
from database.database import session, Customer, Product, Organization, savat
from data.config import OFFICE_LOCATION, ADMINS
from aiogram.types import ReplyKeyboardRemove
from states.fikr_bildirish_state import Customer_Fikr
@dp.message_handler(Text(equals="✍️Fikr bildirish", ignore_case=True))
async def order_handler(message: types.Message):
    titles = ["Hammasi yoqadi ⭐️⭐️⭐️⭐️⭐️", "Yaxshi ⭐️⭐️⭐️⭐️", "Yoqmadi ⭐️⭐️⭐️", "Yomon ⭐️⭐️", "Juda yomon ⭐️", "⬅️Ortga"]
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*(KeyboardButton(text) for text in titles))
    await message.answer(message.text, reply_markup=keyboard)
    await Customer_Fikr.baho.set()    



@dp.message_handler(Text(equals="✍️Оставить отзыв", ignore_case=True))
async def order_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    titles = ["Все понравилось ⭐️⭐️⭐️⭐️⭐️", "Нормально ⭐️⭐️⭐️⭐️", "Удовлетворительно ⭐️⭐️⭐️", "Не понравилось ⭐️⭐️", "Хочу пожаловатся ⭐️", "⬅️Назад"]
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*(KeyboardButton(text) for text in titles))
    await message.answer(message.text, reply_markup=keyboard)
    await Customer_Fikr.baho.set()    
    
@dp.message_handler(lambda message : message.text in ["⬅️Ortga", "⬅️Назад"], state=Customer_Fikr.baho)
async def ortga(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
    await message.answer(message.text, reply_markup=keyboard)
    await state.reset_state()

@dp.message_handler(lambda message : message.text in ["Все понравилось ⭐️⭐️⭐️⭐️⭐️", "Нормально ⭐️⭐️⭐️⭐️", "Удовлетворительно ⭐️⭐️⭐️", "Не понравилось ⭐️⭐️", "Хочу пожаловатся ⭐️", "Hammasi yoqadi ⭐️⭐️⭐️⭐️⭐️", "Yaxshi ⭐️⭐️⭐️⭐️", "Yoqmadi ⭐️⭐️⭐️", "Yomon ⭐️⭐️", "Juda yomon ⭐️"], state=Customer_Fikr.baho) 
async def baho_qoyish(message : types.Message, state : FSMContext):
    await state.update_data({
        "baho" : message.text,
        })   
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    text = {"uz" : "Fikr - mulohazangizni xabar xabar shaklida qoldiring.", "eng" : "Оставьте отзыв в виде сообщения."}
    await message.answer(text[lang], reply_markup=ReplyKeyboardRemove())
    await Customer_Fikr.comment.set()


@dp.message_handler(state=Customer_Fikr.baho)
async def nothing(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    text = {"uz" : "😃 Juda yaxshi birgalikda buyurtma beramizmi?", "eng" : "😃 Привет, оформим вместе заказ?"}
    await state.reset_state()
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
    await message.answer(text[lang], reply_markup=keyboard)

@dp.message_handler(state=Customer_Fikr.comment)
async def fikr(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    text = {"eng" : "Спасибо за ваш отзыв!", "uz" : "Fikr -mulohazangiz uchun tashakkur!"}      
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
    await message.answer(text[lang], reply_markup=keyboard)
    await state.update_data({
        "comment" : message.text,
        })
    data = await state.get_data()
    baho = data.get("baho")
    comment = data.get("comment")
    await state.reset_state()
    for admin in ADMINS:
        await bot.send_message(admin ,text=f"Оценка и отзывы, которые {customer.username} оставил для улучшения нашего сервиса:\n{baho}\n{comment}")

