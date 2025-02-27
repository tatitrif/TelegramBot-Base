import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluentogram import TranslatorHub

from core.config import settings

logger = logging.getLogger(__name__)


class TranslatorRunnerMiddleware(BaseMiddleware):
    def __init__(
        self,
        translator_hub_alias: str = "_translator_hub",
        translator_runner_alias: str = "i18n",
    ):
        self.translator_hub_alias = translator_hub_alias
        self.translator_runner_alias = translator_runner_alias

    async def __call__(
        self,
        event_handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        ctx_data: dict[str, Any],
    ) -> None:
        from_user = getattr(event, "from_user", None)
        translator_hub: TranslatorHub | None = ctx_data.get(self.translator_hub_alias)

        if from_user is None or translator_hub is None:
            return await event_handler(event, ctx_data)

        lang = from_user.language_code
        langs = translator_hub.locales_map.keys()
        if lang not in langs:
            lang = settings.telegram.lang_default

        ctx_data[self.translator_runner_alias] = (
            translator_hub.get_translator_by_locale(lang)
        )
        await event_handler(event, ctx_data)
