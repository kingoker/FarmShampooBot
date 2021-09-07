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



@dp.message_handler(lambda message:message.text=="⬅️Ortga", state=Customer_Form.delivery)
async def back_uz(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
    customer.products.clear()
    session.commit()
    text = "Bosh menyu"
    await message.answer(text, reply_markup=menu_product_types_uz)


@dp.message_handler(lambda message:message.text=="⬅️Назад", state=Customer_Form.delivery)
async def back_eng(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
    customer.products.clear()
    session.commit()
    text = "Главное меню"
    await message.answer(text, reply_markup=menu_product_types_eng)




@dp.message_handler(state=Customer_Form.delivery)
async def delivery(message : types.Message, state : FSMContext):
    comment = message.text
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id==user_id).first()
    customer.comment = comment
    session.commit()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id==customer.customer_id).all()
    prices = []
    total = 0
    if lang == "uz":
        description = "To'lov qilish uchun quyidagi tugmani bosing."
    else :
        description = "Нажмите кнопку ниже, чтобы заплатить."    
    for row in records:
        product = session.query(Product).filter(Product.product_id==row.product_id).first()
        prices.append(types.LabeledPrice(label= f"{product.title}", amount=int(product.price)*int(row.amount)*100))
   
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
    await state.reset_state()



@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    print(customer)
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    admin_text = f"<strong>🚖 Новый заказ</strong> – Доставка:\n"
    admin_text += f"Юзер: @{message.from_user.username}\n"
    admin_text += f"Имя: {customer.username}\n"
    admin_text += f"Номер телефона: {customer.phone}\n\n"
    i = 1        
    total_price = 0
    records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id == customer.customer_id).all()
    for row in records:
        product = session.query(Product).filter(Product.product_id==row.product_id).first()
        admin_text += f"<strong>{i}. {product.title}</strong>\n\n"
        i +=1
        total_price += int(row.amount) * int(product.price)
        price = format(int(product.price),",d").replace(',', ' ')
        amount_show = f"{int(row.amount) * int(product.price):,}".replace(',', ' ')
        admin_text+= f"{row.amount} x {price} = {amount_show} UZS\n\n"
    total_price = f"{total_price:,}".replace(',', ' ')
    admin_text += f"<strong>Оплата</strong>: Картой\n"
    admin_text += f"<strong>Сумма оплаты</strong>: {total_price} UZS\n"
    admin_text += f"<strong>Оплачено</strong>: ✅\n"
    admin_text += f"<strong>Комментарии</strong>: {customer.comment}\n"
    admin_text += f"<strong>Адрес</strong>: {show(customer.latitude, customer.longitude)}\n" 
    admin_text += f"<strong>Язык</strong>: {customer.language}"
    customer.products.clear()
    session.commit()
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, admin_text)

        except Exception as err:
            logging.exception(err)

    text = {"uz":"Xaridingiz uchun rahmat.", "eng" : "Спасибо за покупку."}
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng    
    await message.answer(text[lang],reply_markup=keyboard)
