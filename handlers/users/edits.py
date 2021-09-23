from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization
from loader import dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text, Regexp
from keyboards.default import edit_settings_menu_eng, menuStart, edit_settings_menu_uz, back_menu_uz, back_menu_eng, menu_product_types_uz, menu_product_types_eng
from states.user_edit_state import Personal_edit
from aiogram.dispatcher import FSMContext
from random import randint
from utils.send_sms import send_sms





PHONE_NUM = r'^[\+][0-9]{3}[0-9]{3}[0-9]{6}$'

@dp.message_handler(Text(equals="⚙️Sozlamalar", ignore_case=True))
async def order_handler(message: types.Message):
    await message.answer("⚙️Sozlamalar", reply_markup=edit_settings_menu_uz)


@dp.message_handler(Text(equals="⚙️Настройки", ignore_case=True))
async def order_handler(message: types.Message):
    await message.answer("⚙️Настройки", reply_markup=edit_settings_menu_eng)



@dp.message_handler(Text(equals="Изменить ФИО", ignore_case=True))
async def order_handler(message: types.Message):
    await message.answer("Введите ваше имя", reply_markup=back_menu_eng)
    await Personal_edit.name.set()
    

@dp.message_handler(Text(equals="Ismni o'zgartirish", ignore_case=True))
async def order_handler(message: types.Message):
    await message.answer("Ismingizni kiriting", reply_markup=back_menu_uz)
    await Personal_edit.name.set()



@dp.message_handler(Text(equals="⬅️Назад", ignore_case=True), state=Personal_edit.name)
async def edit_handler(message: types.Message, state : FSMContext):
    await state.reset_state()
    await message.answer("⚙️Настройки", reply_markup=edit_settings_menu_eng)
    


@dp.message_handler(Text(equals="⬅️Ortga", ignore_case=True), state=Personal_edit.name)
async def edit_handler(message: types.Message, state : FSMContext):
    await state.reset_state()
    await message.answer("⚙️Sozlamalar", reply_markup=edit_settings_menu_uz)
    


@dp.message_handler(state=Personal_edit.name)
async def edit_name_handler(message: types.Message, state : FSMContext):
    user_id = message.from_user.id
    name = message.text
    await state.update_data({
        "name" : name,
        })
    await state.reset_state()
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    customer.username = f"{name}"
    session.commit()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    if lang == "uz":
        await message.answer("⚙️Sozlamalar", reply_markup=edit_settings_menu_uz)
    else :
        await message.answer("⚙️Настройки", reply_markup=edit_settings_menu_eng)



@dp.message_handler(Text(equals="Изменить номер", ignore_case=True))
async def edit_phone_handler(message: types.Message):
    await message.answer("📱 Отправьте ваш номер телефона.\nОтправьте номер телефона для звонков в формате:\n+ 998 ** *** ****", reply_markup=back_menu_eng)
    await Personal_edit.phone.set()


@dp.message_handler(Text(equals="Raqamni o'zgartirish", ignore_case=True))
async def edit_phone_handler(message: types.Message):
    await message.answer("📱 Raqamni +998 ** *** ** ** shaklida yuboring.", reply_markup=back_menu_uz)
    await Personal_edit.code.set()



@dp.message_handler(Regexp(PHONE_NUM), state=Personal_edit.code)
async def edit_handler(message: types.Message, state : FSMContext):
    user_id = message.from_user.id
    phone = message.text

    code = randint(100000, 999999)
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    await state.update_data({
        "code" : code,
        })
    await state.update_data({
        "phone" : phone,
        })
    
    text = {
        "uz" : "Kod jo'natildi. Akkauntni aktiv holga keltirish uchun kodni jo'nating.",
        "eng": "Присылается смс-код. Пожалуйста, введите отправленный вам код.",
    }
    sms_text = {
        "uz" : f"Sizning aktivatsiya kodingiz : {code}.",
        "eng": f"Ваш код активации: {code}."
    }
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    send_text = text[lang] # sms uchun text
    print(sms_text)
    sms = send_sms(sms_text[lang], phone)
    
    # sms = client.messages \
    #                 .create(
    #                      body=sms_text[lang],
    #                      from_='+1 989 310 7966',
    #                      to=phone
    #     )
    keyboard = back_menu_uz if lang == "uz" else back_menu_eng
    await message.answer(text[lang], reply_markup=keyboard)
    await Personal_edit.phone.set()

    


@dp.message_handler(Text(equals="⬅️Ortga", ignore_case=True), state=Personal_edit.code)
async def edit_handler(message: types.Message, state : FSMContext):
    await state.reset_state()
    await message.answer("⚙️Sozlamalar", reply_markup=edit_settings_menu_uz)


@dp.message_handler(Text(equals="⬅️Назад", ignore_case=True), state=Personal_edit.code)
async def edit_handler(message: types.Message, state : FSMContext):
    await state.reset_state()
    await message.answer("⚙️Настройки", reply_markup=edit_settings_menu_eng)


@dp.message_handler(lambda message : message.text is not None, state=Personal_edit.code)
async def phone_input_incorrect(message : types.Message, state : FSMContext):
    text = {
            "uz" :{ 
            "guide" : "Iltimos, yaroqli telefon raqamini kiriting."
            },
            "eng" : {
            "guide" : "Пожалуйста введите правильный номер телефона.",
            },
        }
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()    
    language = customer.language
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng" 
    keyboard = back_menu_uz if lang == "uz" else back_menu_eng
    await message.answer(text[lang]['guide'], reply_markup=keyboard)



# Phone number larni tekshirish code orqali


@dp.message_handler(Text(equals="⬅️Ortga", ignore_case=True), state=Personal_edit.phone)
async def edit_handler(message: types.Message, state : FSMContext):
    await state.reset_state()
    await message.answer("⚙️Sozlamalar", reply_markup=edit_settings_menu_uz)            


@dp.message_handler(Text(equals="⬅️Назад", ignore_case=True), state=Personal_edit.phone)
async def edit_handler(message: types.Message, state : FSMContext):
    await state.reset_state()
    await message.answer("⚙️Настройки", reply_markup=edit_settings_menu_eng)



@dp.message_handler(lambda message : message.text is not None, state=Personal_edit.phone)
async def edit_handler(message: types.Message, state : FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    keyboard = back_menu_uz if lang == "uz" else back_menu_eng
    code = data.get("code")
    try :
        isauthenticated = code == int(message.text)

    except :
        isauthenticated = False
    
    text = {
        "uz" : "Notog'ri kod kiritildi.",
        "eng" : "Неверный код.",
    }

    if isauthenticated and lang == "uz": 
        customer.phone = data.get("phone")
        session.commit()  
        await state.reset_state()        
        await message.answer("⚙️Sozlamalar", reply_markup=edit_settings_menu_uz)
    elif isauthenticated and lang == "eng":
        customer.phone = data.get("phone")
        session.commit()  
        await state.reset_state()        
        await message.answer("⚙️Настройки", reply_markup=edit_settings_menu_eng)
    else:
        await message.answer(text[lang], reply_markup=keyboard)
                

@dp.message_handler(Text(equals="🇺🇿 Tilni tanlang", ignore_case=True))
async def edit_language(message : types.Message):
    await message.answer("🇺🇿 Tilni tanlang", reply_markup=menuStart) 
    await Personal_edit.language.set()               


@dp.message_handler(Text(equals="🇷🇺 Выберите язык", ignore_case=True))
async def edit_language(message : types.Message):
    await message.answer("🇷🇺 Выберите язык", reply_markup=menuStart)                
    await Personal_edit.language.set()



@dp.message_handler(Text(equals="🇺🇿O'zbekcha", ignore_case=True), state=Personal_edit.language)
async def edit_language(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    language = message.text
    customer.language = language
    session.commit()
    await state.reset_state()
    await message.answer("⚙️Sozlamalar", reply_markup=edit_settings_menu_uz)                



@dp.message_handler(Text(equals="🇷🇺Русский", ignore_case=True), state=Personal_edit.language)
async def edit_language(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.customer_id == user_id).first()
    language = message.text
    customer.language = language
    session.commit()
    await state.reset_state()
    await message.answer("⚙️Настройки", reply_markup=edit_settings_menu_eng)


@dp.message_handler(Text(equals="⬅️Ortga", ignore_case=True))
async def ortga(message : types.Message):
    text = "Bosh menu"
    keyboard = menu_product_types_uz 
    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(Text(equals="⬅️Назад", ignore_case=True))
async def ortga(message : types.Message):
    text = "Главное меню"
    keyboard = menu_product_types_eng 
    await message.answer(text, reply_markup=keyboard)    