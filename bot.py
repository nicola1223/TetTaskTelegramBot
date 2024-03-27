import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.parser import get_bad_feedbacks
from dotenv import load_dotenv
import os
import json

bd_path = "files/bd.json"
parsed_feedbacks = []

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
    Checks the bot is working
    :param message:
    :return:
    """
    mess = "Это тестовое сообщение для проверки работоспособности"
    await bot.send_message(channel_id, mess)


async def send_message_to_channel():
    """
    Send message to channel
    :param message:
    :return:
    """
    for name, sku, productValuation, text, rating in get_bad_feedbacks(parsed_feedbacks):
        mess = (f"<b>Негативный отзыв</b>\n"
                f"Название товара: <b>{name}</b>\n"
                f"SKU товара: <b>{sku}</b>\n"
                f"Кол-во звезд: <b>{productValuation}</b>\n"
                f"Текущий рейтинг: <b>{rating}</b>\n"
                f"Текст отзыва:\n {text}")
        await bot.send_message(channel_id, mess, parse_mode=ParseMode.HTML)
        await asyncio.sleep(1)


async def get_data():
    global parsed_feedbacks
    with open(bd_path, "r") as file:
        parsed_feedbacks = json.load(file)["ids"]


async def save_data():
    with open(bd_path, "w") as file:
        json.dump({"ids": parsed_feedbacks}, file, indent=4, ensure_ascii=False)


async def main():
    scheduler.start()
    scheduler.add_job(send_message_to_channel, 'interval', seconds=1)
    dp.startup.register(get_data)
    dp.shutdown.register(save_data)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
