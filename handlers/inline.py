from typing import Optional

from aiogram import Router, F, html
from aiogram.types import InlineQuery, \
    InputTextMessageContent, \
    InlineQueryResultCachedPhoto, InlineQueryResultArticle

from storage import get_images_by_id

router = Router()



@router.inline_query(F.query == "")
async def show_user_images(inline_query: InlineQuery):
    results = []
    for index, file_id in enumerate(get_images_by_id(inline_query.from_user.id)):
        # В итоговый массив запихиваем каждую запись
        results.append(InlineQueryResultCachedPhoto(
            id=str(index),  # ссылки у нас уникальные, потому проблем не будет
            photo_file_id=file_id
        ))
    # Важно указать is_personal=True!
    if (len(results) > 0):
        await inline_query.answer(
            results, is_personal=True,
            switch_pm_text="Добавить ещё »»",
            switch_pm_parameter="add"
        )
    else:
        await inline_query.answer(
            [InlineQueryResultArticle(
            id="0",
            title="Как-то пустовато...",
            description="Добавьте сюда что-нибудь",
            input_message_content=InputTextMessageContent(
                message_text="<a href='https://t.me/gtgebot?start=add'>Добавьте новую картинку!</a>",
                parse_mode="HTML"
            )
        )], is_personal=True,
        )