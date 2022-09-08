from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton



main_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_btn.add("📊Statistika", "🔧Kanallar", "📤Reklama", "♻️ Tozalash")

channel_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
channel_btn.add("➕Kanal qo'shish", "❌Kanalni olib tashlash")
channel_btn.add("📋 Kanallar ro'yxati", "🔙Orqaga qaytish")

reklama_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
reklama_btn.add("📨Forward xabar yuborish", "📬Oddiy xabar yuborish", "🔙Orqaga qaytish")



change_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
change_btn.add("🌄Rasm »»» PDF📑", "📝TEXT »»» PDF📑")