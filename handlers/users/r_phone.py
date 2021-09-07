from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot
# from keyboards.default import phone_uz, phone_eng


@dp.message_handler(content_types=["photo"])
async def chosen_uz(message: types.Message):
    print(message.photo[-1])
    await message.answer("Qabul qilindi.")

    