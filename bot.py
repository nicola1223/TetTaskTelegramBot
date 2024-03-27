import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))


bot = Bot(token=os.environ.get("TOKEN"))

dp = Dispatcher()

channel_id = os.environ.get("CHANNEL_ID")


@dp.message(Command("start"))
async def start(message: types.Message):
    await bot.send_message(channel_id, message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
