import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import aioschedule
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
    await bot.send_message(channel_id)


async def scheduler():
    """
    Создает расписание для отправки сообщения в канал
    :return:
    """
    aioschedule.every().minutes(5).do(send_message_to_channel)
    while True:
        aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup():
    asyncio.create_task(scheduler())


async def main():
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == '__main__':
    asyncio.run(main())
