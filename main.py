import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv
# from translations import translations
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# from config_reader import config
from handlers import save_images, inline


load_dotenv()
TOKEN = getenv('TOKEN')


dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject) -> None:
    args = command.args
    if (args == "add"):
        await message.reply("<i>Просто перешлите картинку мне.</i>")
    else:
        await message.answer("<i>Добро пожаловать, {}!</i>\n<i>Я бот для хранения и быстрого всех твоих мемов прямо в <b>Telegram!</b></i>\n\n<i>Чтобы добавить файл в ваши сохраненные мемы просто перешлите его мне, а чтобы отправить его пропишите</i> <code>@gtgebot</code> <i>в нужном чате.</i>".format(hbold(message.from_user.full_name))) #<i>Отказ от ответственности: пожайлуста не изпользуйте бота для спама или рассылок запрещенных правилами Telegram файлов. Пользуясь этим ботом, вы принимаете <a href='https://gotoge.nyako.tk/tos'>условия пользования ботом</a>.</i>


"""

@dp.message()
async def echo_handler(message: types.Message) -> None:
    
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)

    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
"""

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp.include_routers(
        save_images.router, inline.router
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
