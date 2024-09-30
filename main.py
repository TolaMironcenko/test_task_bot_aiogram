import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import requests

TOKEN: str = getenv("BOT_TOKEN")
CURRENCY_TOKEN: str = getenv("CURRENCY_TOKEN")

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Добрый день. Как вас зовут?")
    
@dp.message()
async def answer_handler(message: Message) -> None:
    try:
        req: str = "https://api.freecurrencyapi.com/v1/latest?apikey=" + CURRENCY_TOKEN + "&currencies=RUB"
        res: str = requests.get(req)
        await message.answer(f'Рад знакомству, {message.text}! Курс доллара сегодня {res.json()["data"]["RUB"]:0.2f}р')
    except TypeError:
        await message.answer("Nice try!")
        
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
