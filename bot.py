import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))


bot = Bot(token=os.environ.get("TOKEN"))

dp = Dispatcher()

scheduler = AsyncIOScheduler()

channel_id = os.environ.get("CHANNEL_ID")


@dp.message(Command("start"))
async def start(message: types.Message):
    """
    Обработчик команды /start для проверки работоспособности бота
    :param message:
    :return:
    """

    mess = "Это тестовое сообщение для проверки работоспособности"
    await bot.send_message(channel_id, mess)


async def send_message_to_channel():
    """
    Отправляет сообщение в канал
    :param message:
    :return:
    """
    mess = "Сообщение"  # TODO: Добавить текст сообщения для товара
    await bot.send_message(channel_id, mess)


async def main():
    scheduler.start()
    scheduler.add_job(send_message_to_channel, 'interval', hours=1)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
