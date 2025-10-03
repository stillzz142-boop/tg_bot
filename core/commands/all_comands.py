import asyncio
from aiogram import Bot
from aiogram.types import BotCommand
from core.settings import settings
from aiogram.client.default import DefaultBotProperties


async def set_commands():
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    commands = [
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="help", description="Памагите"),
        BotCommand(command="language", description="Язык"),
        BotCommand(command="cat", description="Котик на сегодня")  # 🐱 добавили котика
    ]
    await bot.set_my_commands(commands)
    await bot.session.close()
    print("Команды установлены ✅")


if __name__ == "__main__":
    asyncio.run(set_commands())
