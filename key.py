from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()


TOKEN = "1957402156:AAHFkqRkgjI0JpO08ynrz1_2mBaNnWYOzKM"

bot = Bot(token=TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot, storage=storage)
