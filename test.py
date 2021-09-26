"""
This bot is created for the demonstration of a usage of inline keyboards.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '1926333455:AAFF9fhatJWs1ELyKY6m-jqsoK7DxMNYQ0o'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    hour_plus = (
        ('+', 'h++'),
        ('+', 's++'),
    
    )
    clock_values = (

        ('12', '12'),
        ('00', '00'),
    
        )
    hour_minus = (
        ('-', 'h--'),
        ('-', 's--'),
    
        )
    text_keyboard = {
            "uz" : "✅ Tasdiqlash",
            "eng" : "✅ Подтвердить"
        }
    lang = "uz"    
    row_btns1 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in hour_plus)
    row_btns2 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in clock_values)
    row_btns3 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in hour_minus)
    row_btns4 = (types.InlineKeyboardButton(text_keyboard[lang], callback_data="✅"), )


    keyboard_markup.row(*(row_btns1))
    keyboard_markup.row(*(row_btns2))
    keyboard_markup.row(*(row_btns3))
    keyboard_markup.row(*(row_btns4))



    await message.reply("Buyrtmani qabul qilishda o'zingiz uchun qulay vaqtni yoki izohni yozing:", reply_markup=keyboard_markup)


# Use multiple registrators. Handler will execute when one of the filters is OK
@dp.callback_query_handler()  # if cb.data == 'no'
# @dp.callback_query_handler(text='+')  # if cb.data == 'yes'
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    keyboards = query.message.reply_markup.inline_keyboard
    k_hour_plus = keyboards[0][0]
    k_sec_plus = keyboards[0][1]
    k_hour = keyboards[1][0]
    k_sec = keyboards[1][1]
    k_hour_minus = keyboards[2][0]
    k_sec_minus = keyboards[2][0]
    # print(k_hour_plus, k_sec_plus, k_hour, k_sec, k_hour_minus, k_sec_minus)
    print(k_hour)
    print(k_sec)
    h = k_hour["text"]
    s = k_sec["text"]
    if query.data == "h++" and h == "23":
        h = "00"
    elif query.data == "h--" and h == "00":
        h = "23"
    elif  query.data == "h++":
        h = str(int(k_hour["text"]) + 1).zfill(2)
    elif query.data == "h--":
        h = str(int(k_hour["text"]) - 1).zfill(2)       
    elif query.data == "s++" and s == "50" and h == "23":
        h = "00"
        s = "00"    
    elif query.data == "s++" and s == "50":
        h = str(int(k_hour["text"]) + 1).zfill(2)
        s = "00"
    elif query.data == "s--" and s == "00" and h == "00":
        h = "23"
        s = "50"
    elif query.data == "s--" and s == "00":
        h = str(int(k_hour["text"]) - 1).zfill(2)       
        s = "50"
    elif query.data == "s++":
        s = str(int(k_sec["text"]) + 10).zfill(2)
    elif query.data == "s--":
        s = str(int(k_sec["text"]) - 10).zfill(2)
        
    elif query.data == "✅":
        print("✅ Tasdiqlandi")
        query.message.text = "✅ Tasdiqlandi"    
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    # default row_width is 3, so here we can omit it actually
    # kept for clearness
    # h = str(int(query.data) + 1).zfill(2)
    # s = str(int(query.data) + 1).zfill(2)

    hour_plus = (
        ('+', 'h++'),
        ('+', 's++'),
    
    )
    clock_values = (

        (h, h),
        (s, s),
    
        )
    hour_minus = (
        ('-', 'h--'),
        ('-', 's--'),
    
        )
    lang = "uz"
    text_keyboard = {
        "uz" : "✅ Tasdiqlash",
        "eng" : "✅ Подтвердить"
    }

    # in real life for the callback_data the callback data factory should be used
    # here the raw string is used for the simplicity
    row_btns1 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in hour_plus)
    row_btns2 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in clock_values)
    row_btns3 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in hour_minus)
    row_btns4 = (types.InlineKeyboardButton(text_keyboard[lang], callback_data="✅"), )


    keyboard_markup.row(*(row_btns1))
    keyboard_markup.row(*(row_btns2))
    keyboard_markup.row(*(row_btns3))
    keyboard_markup.row(*(row_btns4))


    answer_data = query.data

    print(query.message.message_id)
    # always answer callback queries, even if you have nothing to say
    # await query.answer(f'You answered with {answer_data!r}')
    await bot.delete_message(
                            query.from_user.id,
                            query.message.message_id,
)
    # if answer_data == 'h++':
    #     text = int(query.date) + 1
    # elif answer_data == 's++':
    #     text = int(query.date) + 1

    # else:
    #     text = f'Unexpected callback data {answer_data!r}!'

    # await bot.send_message(query.from_user.id, text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)    