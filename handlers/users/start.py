from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from keyboards.default import phone_uz, phone_eng, menuStart, menu_product_types_eng, menu_product_types_uz
from aiogram.dispatcher import FSMContext
from states.user_state import Personal
from random import randint
from aiogram.dispatcher.filters import Regexp
from database.database import session, Customer
from aiogram.types import ReplyKeyboardRemove

# from twilio.rest import Client
# from data.config import auth_token, account_sid
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# client = Client(account_sid, auth_token)

PHONE_NUM = r'^[\+][0-9]{3}[0-9]{3}[0-9]{6}$'


# print(message.sid)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    custumer = session.query(Customer).filter(Customer.customer_id == message.from_user.id).first()
    if custumer is None:
        await message.answer(
            f"Keling avvaliga xizmat ko'rsatish tilini tanlab olaylik. \n\nСначала выберем язык обслуживания.",
            reply_markup=menuStart)
        print(message.from_user)
        await Personal.language.set()
    else:
        print(message.from_user.id)
        lang = "uz" if custumer.language == "🇺🇿O'zbekcha" else "eng"
        text = {
            "uz": "😃 Juda yaxshi birgalikda buyurtma beramizmi?",
            "eng": "😃 Привет, оформим вместе заказ?",
        }
        keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
        await message.answer(text[lang], reply_markup=keyboard)


@dp.message_handler(state=Personal.language)
async def language_choose(message: types.Message, state: FSMContext):
    language = message.text
    await state.update_data({
        'language': language,
    })

    text = {
        "uz": {
            "guide": "Telefon raqamingiz qanday ? Telefon raqamingizni jo'natish uchun quyidagi \"Raqamni jo'natish\" tugmasini bosing."
        },
        "eng": {
            "guide": "Какой у тебя номер телефона? Для отправки номера телефона нажмите кнопку \"Отправить номер телефона \" ниже."
        },
        "except": {
            "error": "Iltimos yaroqli tilni tanlang!\n\nПожалуйста, введите правильный язык!"
        }
    }
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng" if language == "🇷🇺Русский" else "except"
    if lang != "except":
        send_text2 = text[lang]["guide"]
        keyboard = phone_uz if lang == "uz" else phone_eng
        await message.answer(send_text2, reply_markup=keyboard)
        await Personal.next()
    else:
        await message.answer(text[lang]["error"])


@dp.message_handler(Regexp(PHONE_NUM), state=Personal.phone)
async def phone_input_text(message: types.Message, state: FSMContext):
    contact = message.text
    print(contact)
    await state.update_data({
        "phone": contact,
    })
    # text = {
    #     "uz": "Kod jo'natildi. Akkauntni aktiv holga keltirish uchun kodni jo'nating.",
    #     "eng": "Присылается смс-код. Пожалуйста, введите отправленный вам код.",
    # }
    # code = randint(100000, 999999)
    # await state.update_data({
    #     "code" : code,
    #     })
    # sms_text = {
    #     "uz" : f"Sizning aktivatsiya kodingiz : {code}",
    #     "eng": f"Ваш код активации: {code}."
    # }
    language = await state.get_data()
    language = language.get('language')
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng"
    # send_text = text[lang] # sms uchun text
    # print(sms_text[lang])
    # phone_number = contact
    # sms = client.messages \
    #                 .create(
    #                      body=sms_text[lang],
    #                      from_='+1 408 872 8929',
    #                      to=f"+{phone_number}"
    #                  )
    # telefon_text = {
    #     "uz" : ["Telefon raqamni o'zgartirish", "Kodni qayta jo'natish"],
    #     "eng" : ["Сменить номер телефона", "Отправить код еще раз"],
    # }
    # keyboard = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(telefon_text[lang][0])],[types.KeyboardButton(telefon_text[lang][1])]], resize_keyboard=True)
    # await message.answer(send_text, reply_markup=keyboard)
    send_text = {
        "uz": "Ismingizni kiriting:",
        "eng": "Введите ваше имя:"
    }
    await message.answer(send_text[lang], reply_markup=ReplyKeyboardRemove())
    await Personal.name.set()


@dp.message_handler(state=Personal.phone, content_types=["contact"])
async def phone_input(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    print(contact)
    await state.update_data({
        "phone": contact,
    })
    # text = {
    #     "uz": "Kod jo'natildi. Akkauntni aktiv holga keltirish uchun kodni jo'nating.",
    #     "eng": "Присылается смс-код. Пожалуйста, введите отправленный вам код.",
    # }
    # code = randint(100000, 999999)
    # await state.update_data({
    #     "code" : code,
    #     })
    # sms_text = {
    #     "uz" : f"Sizning aktivatsiya kodingiz : {code}",
    #     "eng": f"Ваш код активации: {code}."
    # }
    language = await state.get_data()
    language = language.get('language')
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng"
    # send_text = text[lang] # sms uchun text
    # print(sms_text[lang])
    # phone_number = contact
    # sms = client.messages \
    #                 .create(
    #                      body=sms_text[lang],
    #                      from_='+1 408 872 8929',
    #                      to=f"+{phone_number}"
    #                  )
    # telefon_text = {
    #     "uz" : ["Telefon raqamni o'zgartirish", "Kodni qayta jo'natish"],
    #     "eng" : ["Сменить номер телефона", "Отправить код еще раз"],
    # }
    # keyboard = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(telefon_text[lang][0])],[types.KeyboardButton(telefon_text[lang][1])]], resize_keyboard=True)
    # await message.answer(send_text, reply_markup=keyboard)
    send_text = {
        "uz": "Ismingizni kiriting:",
        "eng": "Введите ваше имя:"
    }
    await message.answer(send_text[lang], reply_markup=ReplyKeyboardRemove())
    await Personal.name.set()


@dp.message_handler(lambda message: message.text is not None, state=Personal.phone)
async def phone_input_incorrect(message: types.Message, state: FSMContext):
    text = {
        "uz": {
            "guide": "Telefon raqamingiz qanday ? Telefon raqamingizni jo'natish uchun quyidagi \"Raqamni jo'natish\" tugmasini bosing."
        },
        "eng": {
            "guide": "Какой у тебя номер телефона? Для отправки номера телефона нажмите кнопку \"Отправить номер телефона \" ниже."
        },
    }
    language = await state.get_data()
    language = language.get('language')
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng"
    keyboard = phone_uz if lang == "uz" else phone_eng
    await message.answer(text[lang]['guide'], reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Kodni qayta jo'natish", state=Personal.code)
async def resend_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data.get("phone")
    text = "Kod jo'natildi. Akkauntni aktiv holga keltirish uchun kodni jo'nating."
    code = randint(100000, 999999)
    await state.update_data({
        "code": code,
    })
    sms_text = f"Sizning aktivatsiya kodingiz : {code}"
    print(sms_text)
    sms = client.messages \
        .create(
        body=sms_text,
        from_='+1 408 872 8929',
        to=f"+{phone_number}"
    )
    telefon_text = ["Telefon raqamni o'zgartirish", "Kodni qayta jo'natish"]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(telefon_text[0])], [types.KeyboardButton(telefon_text[1])]],
        resize_keyboard=True)
    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Отправить код еще раз", state=Personal.code)
async def resend_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data.get("phone")
    text = "Присылается смс-код. Пожалуйста, введите отправленный вам код."
    code = randint(100000, 999999)
    await state.update_data({
        "code": code,
    })
    sms_text = f"Ваш код активации: {code}."
    print(sms_text)
    sms = client.messages \
        .create(
        body=sms_text,
        from_='+1 408 872 8929',
        to=f"+{phone_number}"
    )
    telefon_text = ["Сменить номер телефона", "Отправить код еще раз"]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(telefon_text[0])], [types.KeyboardButton(telefon_text[1])]],
        resize_keyboard=True)
    await message.answer(text, reply_markup=keyboard)


# Telefon raqamni o'zgartirish uchun
@dp.message_handler(lambda message: message.text in ["Telefon raqamni o'zgartirish", "Сменить номер телефона"],
                    state=Personal.code)
async def resend_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = "uz" if data.get("language") == "🇺🇿O'zbekcha" else "eng"
    text = {
        "uz": {
            "guide": "Telefon raqamingiz qanday ? Telefon raqamingizni jo'natish uchun quyidagi \"Raqamni jo'natish\" tugmasini bosing."
        },
        "eng": {
            "guide": "Какой у тебя номер телефона? Для отправки номера телефона нажмите кнопку \"Отправить номер телефона \" ниже."
        },
    }
    keyboard = phone_uz if lang == "uz" else phone_eng
    await message.answer(text[lang]["guide"], reply_markup=keyboard)
    await Personal.phone.set()


@dp.message_handler(state=Personal.code)
async def code_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng"
    try:

        isauthenticated = data.get('code') == int(message.text)
    except:
        isauthenticated = False
    text = {
        "uz": "Ismingizni kiriting: ",
        "eng": "Введите ваше имя: ",
    }

    code_text = {
        "uz": "Notog'ri kod kiritildi.",
        "eng": "Неверный код."
    }
    if isauthenticated:
        await message.answer(text[lang])
        await Personal.next()
    else:
        await message.answer(code_text[lang])


@dp.message_handler(state=Personal.name)
async def name_input(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({
        "name": name,
    })
    data = await state.get_data()
    name = data.get("name")
    language = data.get("language")
    phone = data.get("phone")
    customer = Customer(username=name, customer_id=message.from_user.id, language=language, phone=phone)
    session.add(customer)
    session.commit()
    await state.reset_state()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    text = {
        "uz": "😃 Juda yaxshi birgalikda buyurtma beramizmi?",
        "eng": "😃 Привет, оформим вместе заказ?",
    }
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
    await message.answer(text[lang], reply_markup=keyboard)

    # await message.answer(f"Malumotlar -> \nname : {customer.name}\nphone : {custumer.phone},\nlanguage : {custumer.language}.")
