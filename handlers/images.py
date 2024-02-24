from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PhotoSize, \
    InlineKeyboardMarkup, InlineKeyboardButton

from states import DeleteCommon
from storage import add_photo, delete_image
from filters import viabot

router = Router()

@router.message(
    DeleteCommon.waiting_for_delete_start,
    F.photo[-1].file_unique_id.as_("file_unique_id"),
    viabot.ViaBotFilter()
)
async def image_deletion_handler(
        message: Message,
        state: FSMContext,
        file_unique_id: str
):
    delete_image(message.from_user.id, file_unique_id)
    await state.clear()
    await message.answer(
        text="♻️ <i>Изображение удалено!</i> "
             "<i>Изображение изчезает не сразу, обычно это происходит в течении 5 минут, тк Telegram кеширует inline запросы</i>")

@router.message(F.photo[-1].as_("photo"))
async def save_image(message: Message, photo: PhotoSize):
    if (add_photo(message.from_user.id, photo.file_id, photo.file_unique_id)):
        #await state.clear()
        kb = [[InlineKeyboardButton(
            text="Попробовать ↪️",
            switch_inline_query=""
        )]]
        await message.reply(
            text="🌠 | Изображение сохранено!\nВы всегда сможете его удалить командой /delete\n<i>Изображения появляются не сразу, обычно это происходит в течении 5 минут, тк Telegram кеширует inline запросы</i>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
        )
    else:
        await message.reply(
            text="⚠️ Погодите! Это фото уже добавлено в вашу галерею."
        )
