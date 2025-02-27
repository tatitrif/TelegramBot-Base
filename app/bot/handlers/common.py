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
    await message.answer(i18n.start.hello(username=message.from_user.username))
    await message.answer(
        text="Subscribe text",
        reply_markup=get_inline_keyboard(
            btm_data={
                "Subscribe": f"subscribe_{user_data.username}",
            }
        ),
    )


@router.callback_query(F.data.startswith("subscribe"))
async def subscribe_callback(callback: types.CallbackQuery):
    kbd = get_reply_keyboard(
        "Получить информацию по товару",
        placeholder="Выберите действие",
        sizes=(2,),
    )
    await callback.message.answer("Subscribed", reply_markup=kbd)
    await callback.message.delete()
