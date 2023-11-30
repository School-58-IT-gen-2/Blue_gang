import aiogram
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.filters.command import Command
from aiogram import types
from dotenv import load_dotenv

import os


load_dotenv()

TOKEN = os.getenv('token')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
