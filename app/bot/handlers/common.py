from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="common")


@router.message(Command("start"))
async def start_cmd(message: Message):
    """Start command handler."""
    await message.answer(
        "👋 /start",
    )
