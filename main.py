import asyncio
import re
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject, CommandStart
from datetime import datetime
from config_reader import config
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from database import Order, sel_ord_inf

# Enable logging so as not to miss important messages
logging.basicConfig(level=logging.INFO)

# Bot object
bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

# Dispatcher
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")


# Handler for the command /start + deep_link with id_doc '?start=iddoc_xxxxx'
pattern_iddoc = re.compile(r'iddoc_(\d+)')

@dp.message(CommandStart(
    deep_link=True,
    magic=F.args.regexp(pattern_iddoc)
))
async def cmd_start_dl(
   message: types.Message,
   command: CommandObject
):
    tmp = command.args.split("_")[1]
    id_doc = tmp if tmp.isdigit() else '0'
    ord = Order(id_doc)
    ord.select_from_db(sel_ord_inf)
    if ord.is_exist:
       answer = ', '.join(f'{attr}: {value}' for attr, value in vars(ord).items())
       await message.answer(f'Ответ: {answer}')
    else:
        await message.answer("По этому заказу нет информации")

# Handler for the command /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Жду ваших указаний мой господин!")


# Handler for the command /help
@dp.message(Command("help"))
@dp.message(CommandStart(
    deep_link=True, magic=F.args == "help"
))
async def cmd_start_help(message: Message):
    await message.answer("Этот бот для получения информации по вашим заказам.")

# Handler for any message
@dp.message()
async def answer_any_message(message: Message):
    if message.text.isdigit():
        id_doc = message.text
        ord = Order(id_doc)
        ord.select_from_db(sel_ord_inf)
        if ord.is_exist:
            answer = ', '.join(f'{attr}: {value}' for attr, value in vars(ord).items())
            await message.answer(f'Ответ: {answer}')
        else:
            await message.answer("По этому заказу нет информации")
    else:
        await message.answer("Я непонимать вас мой господин!")


# Starting the process of polling new updates
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
