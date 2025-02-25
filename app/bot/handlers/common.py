import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from services.user import UserService

logger = logging.getLogger(__name__)

router = Router(name="common")


@router.message(CommandStart())
async def start_cmd(message: Message, session: AsyncSession):
    """Start command handler."""
    user_data = message.from_user
    await UserService(session).add_one(user_data)
