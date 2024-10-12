import asyncio
import re
import logging
from aiogram import Bot, Dispatcher, F, types 
from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.enums.dice_emoji import DiceEmoji
from datetime import datetime
from config_reader import config
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile


# Enable logging so as not to miss important messages
logging.basicConfig(level=logging.INFO)
# Bot object
bot = Bot(
   token=config.bot_token.get_secret_value(),
   default=DefaultBotProperties(
    parse_mode=ParseMode.HTML
    #..............   
   )       
)
# Dispatcher
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

@dp.message(Command("help"))
@dp.message(CommandStart(
    deep_link=True, magic=F.args == "help"
))
async def cmd_start_help(message: types.Message):
    await message.answer("Это сообщение со справкой")

pattern_iddoc = re.compile(r'iddoc_(\d+)')
# Handler for the command /start + deep_link
@dp.message(CommandStart(
    deep_link=True,                
    magic=F.args.regexp(pattern_iddoc)                
))
async def cmd_start_dl(
   message: types.Message,
   command: CommandObject
):
   id_doc = command.args.split("_")[1]
   await message.answer(f'ID_DOC {id_doc}')

# Handler for the command /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  await message.answer("Hello!")

@dp.message(F.animation)
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id)

# Хэндлер на команду /test1
@dp.message(F.text,Command("Hello"))
async def cmd_test1(message: types.Message):
    await message.reply(f"Hello <u>{message.from_user.full_name}</u>!")

# Хэндлер на команду /test2
# Где-то в другом месте, например, в функции main():

async def cmd_test2(message: types.Message):
    await message.answer_dice(DiceEmoji.DART)
dp.message.register(cmd_test2, Command("2"))

@dp.message(Command("test"))
async def cmd_test1(message: types.Message, test1, test2):
    await message.answer(f'Выводим test1: {test1} test2: {test2}')


@dp.message(Command("settimer"))
async def cmd_settimer(
        message: types.Message,
        command: CommandObject
):
    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    # Пробуем разделить аргументы на две части по первому встречному пробелу
    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/settimer time message"
        )
        return
    await message.answer(
        "Таймер добавлен!\n"
        f"Время: {delay_time}\n"
        f"Текст: {text_to_send}"
    )

@dp.message(Command("info"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer(f"Бот запущен {started_at}")

@dp.message(Command('images'))
async def upload_photo(message: Message):
    # Сюда будем помещать file_id отправленных файлов, чтобы потом ими воспользоваться
    file_ids = []

    # Чтобы продемонстрировать BufferedInputFile, воспользуемся "классическим"
    # открытием файла через `open()`. Но, вообще говоря, этот способ
    # лучше всего подходит для отправки байтов из оперативной памяти
    # после проведения каких-либо манипуляций, например, редактированием через Pillow
    with open("buffer_emulation.png", "rb") as image_from_buffer:
        result = await message.answer_photo(
            BufferedInputFile(
                image_from_buffer.read(),
                filename="image from buffer.jpg"
            ),
            caption="Изображение из буфера"
        )
        file_ids.append(result.photo[-1].file_id)

    # Отправка файла из файловой системы
    image_from_pc = FSInputFile("sun.jpg")
    result = await message.answer_photo(
        image_from_pc,
        caption="Изображение из файла на компьютере"
    )
    file_ids.append(result.photo[-1].file_id)

    # Отправка файла по ссылке
    image_from_url = URLInputFile("https://clipart-library.com/new_gallery/289-2896071_python-logo-png-165709.png")
    result = await message.answer_photo(
        image_from_url,
        caption="Изображение по ссылке"
    )
    file_ids.append(result.photo[-1].file_id)
    await message.answer("Отправленные файлы:\n"+"\n".join(file_ids))

@dp.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"tmp/{message.photo[-1].file_id}.jpg"
    )

@dp.message(F.text)
async def echo_with_time(message: types.Message):
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
    added_text = f"<u>Создано в {time_now}</u>"
    # Отправляем новое сообщение с добавленным текстом
    await message.answer(f"{message.text}\n\n{added_text}")

# Starting the process of polling new updates
async def main():
  await dp.start_polling(bot, test1 = [1, 2, 3], test2 = [4, 5, 6])

if __name__ == "__main__":
  asyncio.run(main())


 