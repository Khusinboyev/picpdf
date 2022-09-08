import types
from handlaers.startFor import *
from handlaers.admin_panel import *
from aiogram.utils import executor
from PIL import Image
import pathlib
import shutil
from os import listdir
from fpdf import FPDF
import os



############################## pic to pdf
@dp.message_handler(text="🌄Rasm »»» PDF📑")
async def convert(message: types.Message):
    await message.answer("Yaratiladigan PDF nomini kiriting")
    await From.pic_pdfNS.set()

@dp.message_handler(content_types=ContentType.TEXT, state=From.pic_pdfNS)
async def conN(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        sql.execute("""CREATE TABLE IF NOT EXISTS pdfs ("user_id"  INTEGER,"name"  INTEGER, "pic_id" INTEGER);""")
        db.commit()
        check = sql.execute(f"""SELECT user_id FROM pdfs WHERE user_id = {user_id}""").fetchone()

        if check == None:
            sql.execute(f"""INSERT INTO pdfs (user_id, name) VALUES ('{user_id}', '{message.text}')""")
            db.commit()
        await message.answer("Nom saqlandi. PDF ga aylantirish uchun biror rasm yuboring")
        await state.finish()
        await From.pic_pdfS.set()
    except:
        await message.answer("Iltimos PDF nomini to'g'ri kiriting")

@dp.message_handler(content_types=ContentType.PHOTO, state=From.pic_pdfS)
async def text(message: types.Message, state: FSMContext):
    id = message.from_user.id
    await message.photo[-1].download(destination_dir=f'files/{id}')
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add("✅TAYYOR✅", "➕ Rasm qo'shish 📤")
    await message.answer("Saqlandi", reply_markup=btn)

    name = sql.execute(f"""SELECT name FROM pdfs WHERE user_id = {message.from_user.id}""").fetchone()[0]
    sql.execute(f"""INSERT INTO pdfs (user_id, name, pic_id) VALUES ('{message.from_user.id}', '{name}', '{message.photo[0].file_id}')""")
    db.commit()

@dp.message_handler(text = "➕ Rasm qo'shish 📤", state=From.pic_pdfS)
async def text(message: types.Message):
    await message.answer('Menga yana yangi rasm yuborishingiz mumkin')

@dp.message_handler(text = "✅TAYYOR✅", state=From.pic_pdfS)
async def text(message: types.Message, state: FSMContext):
    user = message.from_user.id
    kk = await message.answer("Ma'lumotlar asosida PDF tayyorlanmoqda. \n\nIltimos biroz kuting...")
    try:
        name = sql.execute(f"""SELECT name FROM pdfs WHERE user_id = {message.from_user.id}""").fetchone()[0]
    except:
        name = message.from_user.id

    pics_dir = f'files/{user}/photos'

    path = f"files/{message.from_user.id}/photos/"

    image_1 = Image.open(fr'files/{message.from_user.id}/photos/{listdir(path)[0]}')
    im_1 = image_1.convert('RGB')
    image_list = []
    i = 0
    for file in pathlib.Path(pics_dir).iterdir():
        if i == 0:
            pass
        else:
            image_list.append(Image.open(fr'{file}').convert('RGB'))
        i += 1
    im_1.save(rf'files/{user}/{name}.pdf', save_all=True, append_images=image_list)
    await kk.delete()
    sent = await message.answer("Fayl yuborilmoqda...")
    await message.answer_document(document=open(f"files/{user}/{name}.pdf", 'rb'), caption="Powered by @pdfimage_bot", reply_markup=change_btn)
    await sent.delete()

    sql.execute("""DELETE FROM pdfs WHERE user_id = ?""", (message.from_user.id,))
    db.commit()
    shutil.rmtree(f"files/{message.from_user.id}", ignore_errors=True)
    await state.finish()

# ###########################################  text to pdf
#
#
#
@dp.message_handler(text="📝TEXT »»» PDF📑")
async def convert(message: types.Message):
    await message.answer("Tez kunda...")
#     sql.execute("""DELETE FROM pdfs WHERE user_id = ?""", (message.from_user.id,))
#     db.commit()
#     await From.text_pdfNS.set()
#
# @dp.message_handler(content_types=ContentType.TEXT, state=From.text_pdfNS)
# async def conN(message: types.Message, state: FSMContext):
#     try:
#         user_id = message.from_user.id
#         sql.execute("""CREATE TABLE IF NOT EXISTS pdfs ("user_id"  INTEGER,"name"  INTEGER, "pic_id" INTEGER);""")
#         db.commit()
#         check = sql.execute(f"""SELECT user_id FROM pdfs WHERE user_id = {user_id}""").fetchone()
#
#         if check == None:
#             sql.execute(f"""INSERT INTO pdfs (user_id, name) VALUES ('{user_id}', '{message.text}')""")
#             db.commit()
#         await message.answer("Nom saqlandi. PDF ga aylantirish uchun biror rasm yuboring")
#         await state.finish()
#         await From.text_pdfS.set()
#     except:
#         await message.answer("Iltimos PDF nomini to'g'ri kiriting")
#
# @dp.message_handler(text = "✅TAYYOR✅", state=From.text_pdfS)
# async def text(message: types.Message, state: FSMContext):
#     user = message.from_user.id
#     kk = await message.answer("Ma'lumotlar asosida PDF tayyorlanmoqda. \n\nIltimos biroz kuting...")
#     try:
#         name = sql.execute(f"""SELECT name FROM pdfs WHERE user_id = {message.from_user.id}""").fetchone()[0]
#     except:
#         name = message.from_user.id
#     texts = sql.execute(f"""SELECT pic_id FROM pdfs WHERE user_id = {message.from_user.id}""").fetchall()
#     tex = ''
#     for t in texts:
#         t = t[0]
#         if t == None:
#             pass
#         else:
#             tex += t + ' '
#     print(tex)
#
#
#     pdf = FPDF()
#     pdf.add_page()
#
#     pdf.add_font('gargi', '', 'gargi.ttf', uni=True)
#     pdf.set_font('gargi', '', 14)
#     pdf.write(8, tex)
#     pdf.ln(20)
#
#     print(user, name)
#     try:
#         pdf.output(f'files/{user}/{name}.pdf')
#     except:
#         pdf.output(f'files/{user}/{user}.pdf')
#
#     await kk.delete()
#     sent = await message.answer("Fayl yuborilmoqda...")
#     try:
#         await message.answer_document(document=open(f"files/{user}/{name}.pdf", 'wb'), caption="Powered by @pdfimage_bot", reply_markup=change_btn)
#     except:
#         await message.answer_document(document=open(f"files/{user}/{user}.pdf", 'wb'),
#                                       caption="Powered by @pdfimage_bot", reply_markup=change_btn)
#     await sent.delete()
#
#     sql.execute("""DELETE FROM pdfs WHERE user_id = ?""", (message.from_user.id,))
#     db.commit()
#     shutil.rmtree(f"files/{message.from_user.id}", ignore_errors=True)
#     await state.finish()
#
# @dp.message_handler(content_types=ContentType.TEXT, state=From.text_pdfS)
# async def text(message: types.Message):
#     id = message.from_user.id
#     btn = ReplyKeyboardMarkup(resize_keyboard=True)
#     btn.add("✅TAYYOR✅")
#     await message.answer("Saqlandi. Ya'na text yuboring yoki ✅TAYYOR✅ tugmasini bosing", reply_markup=btn)
#
#     name = sql.execute(f"""SELECT name FROM pdfs WHERE user_id = {id}""").fetchone()[0]
#     sql.execute(f"""INSERT INTO pdfs (user_id, name, pic_id) VALUES ('{id}', '{name}', '{message.text}')""")
#     db.commit()
#








if __name__ == "__main__":
    executor.start_polling(dp)
