import asyncio
import re
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.enums.dice_emoji import DiceEmoji
from datetime import datetime
from config_reader import config
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


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


# Handler for the command /start + deep_link
@dp.message(CommandStart(
    deep_link=True,                
    magic=F.args.regexp(re.compile(r'iddoc_(\d+)'))                
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




@dp.message(Command("info"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer(f"Бот запущен {started_at}")

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

 