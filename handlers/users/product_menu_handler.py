from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization, savat
from loader import dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Regexp
from keyboards.default import amount_menu_uz, amount_menu_eng, products_menu_uz, products_menu_eng, menu_product_types_uz, menu_product_types_eng
from states.Customer_state import Customer_Form
from aiogram.dispatcher import FSMContext


   
@dp.message_handler(lambda message : message.text in [p.title for p in session.query(Product).all()], state=Customer_Form.product)
async def order_handler(message: types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    language = customer.language
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng"
    keyboard = amount_menu_uz if lang == "uz" else amount_menu_eng
    text = {
        "uz" : {
            "text" : "Miqdorini tanlang yoki kiriting",
            "price" : "Narx : ",    
    },
        "eng" : {
                "text" : "Выберите или введите количество" ,
                "price" : "Цена : "            
        } 
    }
    postfix = {
        "uz" : "so'm",
        "eng" : "UZS"
    }
    title = message.text
    await state.update_data({
        "product" : title,
        })
    product = session.query(Product).filter(Product.title == title).first()
    await Customer_Form.next()
    price = int(product.price)
    price = f"{price:,}".replace(',', ' ')
    print(price)
    caption = product.description
    caption += f"\n{text[lang]['price']} {price} {postfix[lang]} "
    await message.answer_photo(product.photo_id, caption=caption)
    await message.answer(text[lang]["text"], reply_markup=keyboard)


@dp.message_handler(Text(equals="📥Savat"), state=Customer_Form.product)
async def order_uz(message : types.Message, state : FSMContext):
    customer = session.query(Customer).filter(Customer.customer_id == message.from_user.id).first()
    products = customer.products
    if len(products) > 0:
        titles = [p.title for p in products]
        print(titles)
        btn_text = ["⬅️Ortga", "🔄Tozalash"]
        keyboard = ReplyKeyboardMarkup( row_width=1, resize_keyboard=True)
        keyboard.add(*(KeyboardButton(text=f"❌ {p.title}") for p in products))
        keyboard.row(*(KeyboardButton(text=f"{title}") for title in btn_text))

        # keyboard.add(*(KeyboardButton(f"🚖Buyurtma berish"),))

        text = "📥Savat\n\n"
        i = 1        
        total_price = 0
        records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id == customer.customer_id).all()
        for row in records:
            product = session.query(Product).filter(Product.product_id==row.product_id).first()
            text += f"<strong>{i}. {product.title}</strong>\n\n"
            i +=1
            total_price += int(row.amount) * int(product.price)
            price = format(int(product.price),",d").replace(',', ' ')
            amount_show = f"{int(row.amount) * int(product.price):,}".replace(',', ' ')
            text+= f"{row.amount} x {price} = {amount_show} so'm\n\n"
        total_price = f"{total_price:,}".replace(',', ' ')
        text += f"<strong>Umumiy: </strong> {total_price} so'm"    
        await message.answer(text, reply_markup=keyboard)
        await Customer_Form.savat.set()    

    else :
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
        await message.answer("🗑 Sizning savatingiz bo'sh, buyrutma berish uchun mahsulot tanlang", reply_markup=products_menu_uz)    


@dp.message_handler(Text(equals="📥Корзина"), state=Customer_Form.product)
async def order_eng(message : types.Message, state : FSMContext):
    customer = session.query(Customer).filter(Customer.customer_id == message.from_user.id).first()
    products = customer.products
    if len(products) != 0:
        titles = [p.title for p in products]
        print(titles)
        btn_text = ["⬅️Назад", "🔄Очистить"]
        keyboard = ReplyKeyboardMarkup( row_width=1, resize_keyboard=True)
        keyboard.add(*(KeyboardButton(text=f"❌ {p.title}") for p in products))
        keyboard.row(*(KeyboardButton(text=f"{title}") for title in btn_text))
        # keyboard.add(*(KeyboardButton(f"🚖Place an order"),))
        text = "📥Корзина\n\n"
        i = 1        
        total_price = 0
        records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id == customer.customer_id).all()
        for row in records:
            product = session.query(Product).filter(Product.product_id==row.product_id).first()
            text += f"<strong>{i}. {product.title}</strong>\n\n"
            i +=1
            total_price += int(row.amount) * int(product.price)
            price = format(int(product.price),",d").replace(',', ' ')
            amount_show = f"{int(row.amount) * int(product.price):,}".replace(',', ' ')
            text+= f"{row.amount} x {price} = {amount_show} UZS\n\n"
        total_price = f"{total_price:,}".replace(',', ' ')
        text += f"<strong>Общий: </strong> {total_price} UZS"    
    
        await message.answer(text, reply_markup=keyboard)    
        await Customer_Form.savat.set()    

    else :
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
        await message.answer("🗑 Ваша корзина пуста, чтобы сделать заказ выберите продукты", reply_markup=products_menu_eng)    

@dp.message_handler(Text(equals="⬅️Назад"), state=Customer_Form.product)
async def ortga_main_menu(message : types.Message, state : FSMContext):
    text = "😃 Привет, оформим вместе заказ?"    
    keyboard = menu_product_types_eng
    await message.answer(text, reply_markup=keyboard)
    await state.reset_state()

@dp.message_handler(Text(equals="⬅️Ortga"), state=Customer_Form.product)
async def ortga_main_menu(message : types.Message, state : FSMContext):
    text = "Juda yaxshi birgalikda buyurtma beramizmi? 😃"    
    keyboard = menu_product_types_uz
    await message.answer(text, reply_markup=keyboard)
    await state.reset_state()


@dp.message_handler(lambda message : message.text.isdigit(), state=Customer_Form.amount)
async def order_handler(message: types.Message, state : FSMContext):
    user_id = message.from_user.id
    amount = message.text
    print("amount kirildi.")
    await state.update_data({
        "amount" : amount,
        })
    data = await state.get_data()
    product_title = data.get("product")
    amount = data.get("amount")
    amount = int(amount)
    product = session.query(Product).filter(Product.title == product_title).first()
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    if product in customer.products:
        customer.products.remove(product)
        session.commit()
    customer_savat = savat.insert().values(customer_id=customer.customer_id, product_id=product.product_id, amount=amount)
    session.execute(customer_savat)
    session.commit()
    text = {
        "uz" : "Mahsulot tanlang",
        "eng" : "Выберите продукт",
    }
    # O'zgardi keyboard uchun
    products = session.query(Product).all()
    titles = [p.title for p in products]
    if lang == "uz":
        titles.append("⬅️Ortga")
    else:
        titles.append("⬅️Назад")    
    products_menu_uz = ReplyKeyboardMarkup(
    keyboard = [
            [
                KeyboardButton(text="📥Savat"),
                KeyboardButton(text="🚖Buyurtma berish")
            ],
        ],
        row_width=2,
        resize_keyboard=True
    )
    products_menu_uz.add(*(KeyboardButton(text=title) for title in titles))
    products_menu_eng = ReplyKeyboardMarkup(
    keyboard = [
            [
                KeyboardButton(text="📥Корзина"),
                KeyboardButton(text="🚖Оформить заказ")
            ],
        ],
        row_width=2,
        resize_keyboard=True
    )
    products_menu_eng.add(*(KeyboardButton(text=title) for title in titles))
    keyboard = products_menu_uz if lang == "uz" else products_menu_eng
    await message.answer(text[lang], reply_markup=keyboard)
    await state.reset_state()
    await Customer_Form.product.set()
        


@dp.message_handler(Text(equals="⬅️Назад", ignore_case=True), state=Customer_Form.amount)
async def ortga_product_list(message : types.Message, state : FSMContext):
    await state.reset_state()
    await Customer_Form.product.set()
    products = session.query(Product).all()
    titles = [p.title for p in products]
    titles.append("⬅️Назад")
    products_menu_eng = ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text="📥Корзина"),
                KeyboardButton(text="🚖Оформить заказ")
            ],
        ],
        row_width=2,
        resize_keyboard=True
    )
    products_menu_eng.add(*(KeyboardButton(text=title) for title in titles))
    await message.answer("Выберите продукт", reply_markup=products_menu_eng)        


@dp.message_handler(Text(equals="⬅️Ortga", ignore_case=True), state=Customer_Form.amount)
async def ortga_product_list(message : types.Message, state : FSMContext):
    print("Ortga")
    await state.reset_state()
    await Customer_Form.product.set()
    # O'zgardi keyboard uchun
    products = session.query(Product).all()
    titles = [p.title for p in products]
    titles.append("⬅️Ortga")
    products_menu_uz = ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text="📥Savat"),
                KeyboardButton(text="🚖Buyurtma berish")
            ],
        ],
        row_width=2,
        resize_keyboard=True
    )
    products_menu_uz.add(*(KeyboardButton(text=title) for title in titles))
    await message.answer("Mahsulot tanlang", reply_markup=products_menu_uz)        




@dp.message_handler(Text(equals="📥Корзина", ignore_case=True), state=Customer_Form.amount)
async def order_eng2(message : types.Message, state : FSMContext):
    customer = session.query(Customer).filter(Customer.customer_id == message.from_user.id).first()
    products = customer.products
    if len(products) > 0:
        titles = [p.title for p in products]
        print(titles)
        btn_text = ["⬅️Назад", "🔄Очистить"]
        keyboard = ReplyKeyboardMarkup( row_width=1, resize_keyboard=True)
        keyboard.add(*(KeyboardButton(text=f"❌ {p.title}") for p in products))
        keyboard.row(*(KeyboardButton(text=f"{title}") for title in btn_text))
        # keyboard.add(*(KeyboardButton(f"🚖Palce an order"),))

        text = "📥Корзина\n\n"
        i = 1        
        total_price = 0
        records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id == customer.customer_id).all()
        for row in records:
            product = session.query(Product).filter(Product.product_id==row.product_id).first()
            text += f"<strong>{i}. {product.title}</strong>\n\n"
            i +=1
            total_price += int(row.amount) * int(product.price)
            price = format(int(product.price),",d").replace(',', ' ')
            amount_show = f"{int(row.amount) * int(product.price):,}".replace(',', ' ')
            text+= f"{row.amount} x {price} = {amount_show} UZS\n\n"
        total_price = f"{total_price:,}".replace(',', ' ')
        text += f"<strong>Общий: </strong> {total_price} UZS" 
        
        await Customer_Form.savat.set()

        await message.answer(text, reply_markup=keyboard)        
    else :
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
        await message.answer("🗑 Ваша корзина пуста, чтобы сделать заказ выберите продукты", reply_markup=products_menu_eng)    
        await Customer_Form.product.set()


@dp.message_handler(Text(equals="📥Savat", ignore_case=True), state=Customer_Form.amount)
async def order_uz2(message : types.Message, state : FSMContext):
    customer = session.query(Customer).filter(Customer.customer_id == message.from_user.id).first()
    products = customer.products
    if len(products) > 0:
        titles = [p.title for p in products]
        print(titles)
        btn_text = ["⬅️Ortga", "🔄Tozalash"]
        keyboard = ReplyKeyboardMarkup( row_width=1, resize_keyboard=True)
        keyboard.add(*(KeyboardButton(text=f"❌ {p.title}") for p in products))
        keyboard.row(*(KeyboardButton(text=f"{title}") for title in btn_text))
        # keyboard.add(*(KeyboardButton(f"🚖Buyurtma berish"),))
        text = "📥Savat\n\n"
        i = 1        
        total_price = 0
        records = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id == customer.customer_id).all()
        for row in records:
            product = session.query(Product).filter(Product.product_id==row.product_id).first()
            text += f"<strong>{i}. {product.title}</strong>\n\n"
            i +=1
            total_price += int(row.amount) * int(product.price)
            price = format(int(product.price),",d").replace(',', ' ')
            amount_show = f"{int(row.amount) * int(product.price):,}".replace(',', ' ')
            text+= f"{row.amount} x {price} = {amount_show} so'm\n\n"
        total_price = f"{total_price:,}".replace(',', ' ')
        text += f"<strong>Umumiy: </strong> {total_price} so'm"    
        await Customer_Form.savat.set()

        await message.answer(text, reply_markup=keyboard)
    else :
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
        await message.answer("🗑 Sizning savatingiz bo'sh, buyrutma berish uchun mahsulot tanlang", reply_markup=products_menu_uz)    
        await Customer_Form.product.set()

  
@dp.message_handler(Regexp(r"^🔄Tozalash$"),  state=Customer_Form.savat)
async def order_handler(message: types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    customer.products.clear()
    session.commit()
    text = "Juda yaxshi birgalikda buyrutma beramizmi? 😃"
    print(f"{customer.username} savatini tozaladi {customer.products}")
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
    await Customer_Form.product.set()

  
@dp.message_handler(Regexp(r"^🔄Очистить$"),  state=Customer_Form.savat)
async def order_handler(message: types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    customer.products.clear()
    session.commit()
    text = "😃 Привет, оформим вместе заказ?"
    print(f"{customer.username} cleared his savat {customer.products}")
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
    await message.answer(text, reply_markup=products_menu_eng)
    await Customer_Form.product.set()
  
@dp.message_handler(lambda message : message.text in ["❌ " + p.title for p in session.query(Product).all()], state=Customer_Form.savat)
async def order_handler(message: types.Message, state : FSMContext):
    user_id = message.from_user.id
    title = message.text.replace("❌ ", "")    
    print("title: ", title)
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    language = customer.language
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng"
    text  = {
        "uz" : "Juda yaxshi birgalikda buyrutma beramizmi? 😃",
        "eng" : "😃 Привет, оформим вместе заказ?",
    } 
    products = session.query(Product).all()
    titles = [p.title for p in products]
    if lang == "uz":
        titles.append("⬅️Ortga")
    else :
        titles.append("⬅️Назад")
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
    products_menu_uz.add(*(KeyboardButton(title) for title in titles))
    products_menu_eng.add(*(KeyboardButton(title) for title in titles))
    keyboard = products_menu_uz if lang == "uz" else products_menu_eng
    product = session.query(Product).filter(Product.title == title).first()
    print(product in customer.products)
    customer.products.remove(product) 
    session.commit()        
    await message.answer(text[lang], reply_markup=keyboard)
    await Customer_Form.product.set()