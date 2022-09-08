import pytz
import datetime
from function.functions import *
from databas import *
from key import *
from buttons.mButtons import *
from Statess.statess import From
from aiogram.dispatcher import FSMContext

sent_number = types.ReplyKeyboardMarkup(resize_keyboard=True)
sent_number.add(types.KeyboardButton(text="Raqamni yuborish📱", request_contact=True))

@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    user_id = message.chat.id
    sql.execute("""CREATE TABLE IF NOT EXISTS users ("user_id"  INTEGER,"date"  INTEGER, "lang" INTEGER, "tel_Num" INTEGER);""")
    db.commit()
    check = sql.execute(f"""SELECT user_id FROM users WHERE user_id = {user_id}""").fetchone()

    if check == None:
        sana = datetime.datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%d-%m-%Y %H:%M')
        sql.execute(f"""INSERT INTO users (user_id, date, lang) VALUES ('{user_id}', '{sana}', '{message.from_user.language_code}')""")
        db.commit()

    sql.execute("SELECT id FROM channels")
    rows = sql.fetchall()
    join_inline = types.InlineKeyboardMarkup(row_width=1)
    title = 1
    for row in rows:
        all_details = await dp.bot.get_chat(chat_id=row[0])
        url = all_details['invite_link']
        join_inline.insert(InlineKeyboardButton(f"{title} - kanal", url=url))
        title += 1
    join_inline.add(InlineKeyboardButton("✅Obuna bo'ldim", callback_data="check"))
    if await functions.check_on_start(message.from_user.id):
        await message.answer(f"""Assalomu alaykum! """, reply_markup=change_btn)
    else:
        await message.answer("Botimizdan foydalanish uchun kanalimizga azo bo'ling", reply_markup=join_inline)

@dp.callback_query_handler( text="check")
async def check(call: CallbackQuery):
    user_id = call.from_user.id
    if await functions.check_on_start(user_id):
        await call.answer()
        await call.message.delete()
        await call.message.answer("Xush keldiz", reply_markup=change_btn)
    else:
        await call.answer(show_alert=True, text="Botimizdan foydalanish uchun kanalimizga azo bo'ling")
