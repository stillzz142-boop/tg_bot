import os
import random
from aiogram import Bot
from aiogram.types import Message, FSInputFile  # 👈 FSInputFile для локальных файлов

# 📂 Папка для сохранённых фоток пользователей
PHOTO_DIR = "media/photos"

# 📂 Папка для котиков (валпапка для котиков 🐱)
CATS_DIR = "media/cats"


async def get_start(message: Message, bot: Bot):
    await bot.send_message(
        message.from_user.id,
        f'<b>Привет, {message.from_user.first_name}, как тебя сюда занесло?)</b>'
    )
    await message.answer(f'<s>Привет, {message.from_user.first_name}, как тебя сюда занесло?)</s>')
    await message.reply(f'Привет, {message.from_user.first_name}, как тебя сюда занесло?)')


# 🔹 Красивый список команд
async def get_help(message: Message, bot: Bot):
    help_text = (
        "/start — начать работу\n"
        "/help — показать это сообщение\n"
        "/cancel — отменить все действия\n"
        "/cat — котик на сегодня 🐱"
    )
    await message.answer(help_text)


async def get_cancel(message: Message, bot: Bot):
    await message.answer("Отменили все нахой")


async def get_photo(message: Message, bot: Bot):
    await message.answer('Чё за шляпу ты отправил? Так и быть сохраню')

    # берём последнюю (самую большую) версию фото
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    # создаём папку media/photos, если её нет
    os.makedirs(PHOTO_DIR, exist_ok=True)

    # путь для сохранения фото
    file_path = os.path.join(PHOTO_DIR, f"{photo.file_unique_id}.jpg")

    # сохраняем файл в media/photos
    await bot.download_file(file.file_path, destination=file_path)


# 🐱 Команда /cat → присылает случайного котика (фото, гиф или webm)
async def get_cat(message: Message, bot: Bot):
    if not os.path.exists(CATS_DIR) or not os.listdir(CATS_DIR):
        await message.answer("Котиков пока нет 😿 (закинь фотки в media/cats)")
        return

    photo = random.choice(os.listdir(CATS_DIR))
    file_path = os.path.abspath(os.path.join(CATS_DIR, photo))  # абсолютный путь

    try:
        file = FSInputFile(file_path)  # правильный способ в aiogram 3

        # проверяем расширение файла
        ext = photo.lower().split(".")[-1]
        if ext in ["gif", "webm"]:  # 🎞 гифки и webm → отправляем как анимацию
            await bot.send_animation(message.chat.id, file, caption="Твой котик на сегодня 🐱")
        else:  # 📸 jpg, png и т.п. → отправляем как фото
            await bot.send_photo(message.chat.id, file, caption="Твой котик на сегодня 🐱")

    except Exception as e:
        await message.answer(f"Ошибка при отправке котика: {e}")
