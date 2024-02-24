import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, InputFile
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv
# from translations import translations
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from storage import is_user_already_exists, create_user
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import FSInputFile
from aiogram.filters.command import Command, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from states import DeleteCommon


# from config_reader import config
from handlers import images, inline


load_dotenv()
TOKEN = getenv('TOKEN')

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject) -> None:
    args = command.args
    kb = [[InlineKeyboardButton(text="Открыть сохраненки ➡️",switch_inline_query="")]]
    rmk = InlineKeyboardMarkup(inline_keyboard=kb)
    welcome_text = "<i>Добро пожаловать, {}!</i>\n<i>Я бот для хранения всех твоих мемов прямо в <b>Telegram!</b></i>\n\n<i>Чтобы добавить файл в ваши сохраненные мемы просто перешлите его мне, а чтобы отправить его пропишите</i> <code>@gtgebot</code> <i>в нужном чате.</i>".format(hbold(message.from_user.full_name))
    if (args == "add"):
        await message.reply("<i>Просто перешлите картинку мне.</i>")
    elif (args):
        if (args.startswith("ref_")):
            if (is_user_already_exists(message.from_user.id)):
                await message.reply(text=welcome_text, reply_markup=rmk)
            else:
                create_user(message.from_user.id, args.replace("ref_", ""))
                await message.reply(text=welcome_text, reply_markup=rmk)
    else:
        if (is_user_already_exists(message.from_user.id)):
            await message.reply(text=welcome_text, reply_markup=rmk)
        else:
            create_user(message.from_user.id)
            await message.reply(text=welcome_text, reply_markup=rmk) #<i>Отказ от ответственности: пожайлуста не изпользуйте бота для спама или рассылок запрещенных правилами Telegram файлов. Пользуясь этим ботом, вы принимаете <a href='https://gotoge.nyako.tk/tos'>условия пользования ботом</a>.</i>

@dp.message(Command("delete"), StateFilter(None), F.chat.type == "private")
async def cmd_delete(message: Message, state: FSMContext):
    kb = []
    kb.append([
        InlineKeyboardButton(
            text="Выбрать изображение",
            switch_inline_query_current_chat=""
        )
    ])
    await state.set_state(DeleteCommon.waiting_for_delete_start)
    await message.answer(
        text="Выберите, что хотите удалить:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
    )


async def database_dump():
    await bot.send_document("-1001629983946", FSInputFile("database.db"), caption=f"<i>Gotoge Database Dump</i>\n<b>Forming date:</b> <pre>{datetime.now()}</pre>")

scheduler = AsyncIOScheduler()
scheduler.add_job(database_dump, trigger='cron', hour='*/12')




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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp.include_routers(
        images.router, inline.router
    )
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
