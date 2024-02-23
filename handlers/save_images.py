from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PhotoSize, \
    InlineKeyboardMarkup, InlineKeyboardButton

from states import SaveCommon
from storage import add_photo

router = Router()


@router.message(F.photo[-1].as_("photo"))
async def save_image(message: Message, photo: PhotoSize):
    if (add_photo(message.from_user.id, photo.file_id, photo.file_unique_id)):
        #await state.clear()
        kb = [[InlineKeyboardButton(
            text="Попробовать ↪️",
            switch_inline_query=""
        )]]
        await message.reply(
            text="🌠 | Изображение сохранено!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
        )
    else:
        await message.reply(
            text="⚠️ Погодите! Это фото уже добавлено в вашу галлерею."
        )