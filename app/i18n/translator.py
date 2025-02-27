from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

from core.config import settings

translator_hub = TranslatorHub(
    {
        "ru": (
            "ru",
            "en",
        ),
        "en": ("en",),
    },
    [
        FluentTranslator(
            locale="ru",
            translator=FluentBundle.from_files(
                "ru", Path("./i18n/locales/ru").glob("*.ftl")
            ),
        ),
        FluentTranslator(
            locale="en",
            translator=FluentBundle.from_files(
                "en", Path("./i18n/locales/en").glob("*.ftl")
            ),
        ),
    ],
    root_locale=settings.telegram.lang_default,
)
