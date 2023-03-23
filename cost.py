import aiogram
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
# Підставете свої токіни
# Параметри підключення до бази даних
con = sqlite3.connect("bd_article")
cur = con.cursor()

logging.basicConfig(level=logging.INFO)
TOKEN = ''

CHANNEL_ID = ''
bot = aiogram.Bot(token=TOKEN)

dp = aiogram.Dispatcher(bot, storage=MemoryStorage())
