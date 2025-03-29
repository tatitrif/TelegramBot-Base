import asyncio
import logging

from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from fluentogram import TranslatorRunner

from bot.keyboards.builders import get_inline_keyboard, get_reply_keyboard

logger = logging.getLogger(__name__)

router = Router(name="common")


@router.message(CommandStart())
async def start_cmd(message: Message, i18n: TranslatorRunner):
    """Start command handler."""
    user_data = message.from_user
    await message.answer(text=i18n.start.hello(username=message.from_user.username))
    await message.answer(
        text=i18n.start.subscribe(),
        reply_markup=get_inline_keyboard(
            btm_data={
                i18n.start.subscribe.btm(): f"subscribe_{user_data.username}",
            }
        ),
    )


@router.callback_query(F.data.startswith("subscribe"))
async def subscribe_callback(callback: types.CallbackQuery, i18n: TranslatorRunner):
    await callback.message.edit_text(i18n.start.subscribe.answer())
    await asyncio.sleep(0.5)
    kbd = get_reply_keyboard(
        i18n.kbd.menu.btm1(),
    )
    await callback.message.answer(text=i18n.kbd.menu.title(), reply_markup=kbd)


@router.message(F.photo)
async def get_photo_handler(message: Message, i18n: TranslatorRunner):
    caption = message.caption
    file_id = message.photo[-1].file_id
    await message.answer(
        f"{i18n.msg.fdata()} {i18n.msg.fdata.photo()}: caption = {caption}, file_id = {file_id}"
    )
