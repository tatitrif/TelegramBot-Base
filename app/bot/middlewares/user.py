import logging
from collections.abc import Callable, Awaitable
from typing import Any, cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from cachetools import TTLCache
from sqlalchemy.ext.asyncio import AsyncSession

from services.chat import ChatService
from services.user import UserService

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.cache = TTLCache(
            maxsize=1000,
            ttl=60 * 60 * 6,  # 6 часов
        )

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event = cast(Message, event)
        from_user = getattr(event, "from_user", None)
        msg_text = getattr(event, "text", None)
        session: AsyncSession = data["session"]

        if from_user.id not in self.cache:
            await UserService(session).add_one(from_user)
            self.cache[from_user.id] = None

        if msg_text:
            await ChatService(session).add_one(from_user.id, msg_text)

        return await handler(event, data)
