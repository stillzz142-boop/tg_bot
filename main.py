from aiogram import Bot, Dispatcher
from aiogram.types import Message
from core.handlers.basic import get_start, get_photo, get_help, get_cancel, get_cat  # добавили get_cat
import asyncio
import logging
from core.settings import settings
from aiogram import F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот врум врум')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот заглох')

async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s -"
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode="HTML"))

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # фото → уходит в get_photo (basic.py)
    dp.message.register(get_photo, F.photo)

    # команды
    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.message.register(get_help, Command(commands=['help']))
    dp.message.register(get_cancel, Command(commands=['cancel']))
    dp.message.register(get_cat, Command(commands=['cat']))  # 🐱 команда для котиков

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print("Бот остановлен вручную")
