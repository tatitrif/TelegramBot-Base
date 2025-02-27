from collections.abc import Callable, Awaitable
from typing import Any, cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from cachetools import TTLCache
from sqlalchemy.ext.asyncio import AsyncSession

from services.user import UserService


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
        user = event.from_user

        if user.id not in self.cache:
            session: AsyncSession = data["session"]
            await UserService(session).add_one(user)
            self.cache[user.id] = None
        return await handler(event, data)
