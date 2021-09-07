from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp, bot
from database.database import Organization, session, Customer
# from keyboards.default import phone_uz, phone_eng


@dp.message_handler(Text(equals="☎️Biz bilan aloqa", ignore_case=True))
async def chosen_uz(message: types.Message):
    text = "Agar sizda savollar bo'lsa biz bilan bog'lanishingiz mumkin:\nTelefon raqamlarimiz:\n+998 (95)177-38-98\n+998 (97) 700-92-21\n+998 (90) 941-52-00"     
    await message.answer(text)



@dp.message_handler(Text(equals="☎️Связаться с нами", ignore_case=True))
async def chosen_uz(message: types.Message):
    # organization = session.query(Organization).all().first()
    text = "Вы можете связаться с нами, если у вас возникнут вопросы:\nНаши телефоны:\n+998 (95)177-38-98\n+998 (97) 700-92-21\n+998 (90) 941-52-00"     
    await message.answer(text)    