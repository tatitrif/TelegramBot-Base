from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from storage.db import db_manager


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with db_manager.session() as session:
            data["session"] = session
            try:
                result = await handler(event, data)  # Обрабатываем событие
                return result
            except Exception as e:
                await session.rollback()  # Откат изменений в случае ошибки
                raise e
            finally:
                await session.close()  # Закрываем сессию
