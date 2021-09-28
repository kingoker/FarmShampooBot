from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization, savat
from loader import dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Regexp
from keyboards.default import tolov_uz, tolov_eng, amount_menu_uz, amount_menu_eng, products_menu_uz, products_menu_eng, menu_product_types_uz, menu_product_types_eng
from states.Customer_state import Customer_Form
from aiogram.dispatcher import FSMContext
from utils.misc.get_distance import calc_distance
from utils.misc.show_gmap import show
from utils import admin_send_message, mahsulot_yuborish
from data.config import ADMINS, OFFICE_LOCATION




@dp.message_handler(lambda message : message.text in ["💴 Naqd pul", "💴 Payme", "💴 Наличные", "⬅️Ortga", "⬅️Назад"], state=Customer_Form.tolov_turi)
async def picking_tolov_turi(message : types.Message, state : FSMContext):
  user_id = message.from_user.id
  customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
  lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
  if message.text == "💴 Naqd pul":
    print("'Naqd pul' bosildi")
    await state.update_data({
      "tolov_turi" : "💴 Наличные",
      })    

    await admin_send_message(message, customer, pickup=True, cash=True)
    await state.reset_state()
    text = {
      "uz" : "Xaridingiz uchun rahmat.",
      "eng" : "Спасибо за покупку.",
    }
    customer.latitude = None
    customer.longitude = None
    customer.products.clear()
    session.commit()
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
    await message.answer(text[lang], reply_markup=keyboard)

  elif message.text == "💴 Наличные":
    print("'Наличные'' bosildi")
    await state.update_data({
      "tolov_turi" : "💴 Наличные",
      })    

    await admin_send_message(message, customer, pickup=True, cash=True)
    await state.reset_state()
    text = {
      "uz" : "Xaridingiz uchun rahmat.",
      "eng" : "Спасибо за покупку.",
    }
    customer.latitude = None
    customer.longitude = None  
    customer.products.clear()
    session.commit()  
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
    await message.answer(text[lang], reply_markup=keyboard)


  elif message.text == "💴 Payme":
    print("'Payme'")
    k_text = {"uz" : "⬅️Ortga", "eng" : "⬅️Назад",}
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*(KeyboardButton(k_text[lang]),))
    records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id==customer.customer_id).all()
    if lang == "uz":
      description = "To'lov qilish uchun quyidagi tugmani bosing."
    else :
      description = "Нажмите кнопку ниже, чтобы заплатить."    
    await mahsulot_yuborish(message, description, records, customer)
    await state.reset_state()

  elif message.text in ["⬅️Ortga", "⬅️Назад"]:
    print(message.text)
    text = {
      "uz" : "Bosh menyu",
      "eng" : "Главное меню"
    }
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
    await state.reset_state()
    await message.answer(text[lang], reply_markup=keyboard)

