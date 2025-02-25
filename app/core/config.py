from functools import lru_cache

from pydantic import SecretStr, BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings


class EnvSettings(BaseSettings):
    """
    Application settings.

    These parameters can be configured with environment variables.
    """

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class TelegramConfig(EnvSettings, env_prefix="TELEGRAM_"):
    bot_token: SecretStr


class AppConfig(BaseModel):
    telegram: TelegramConfig


# noinspection PyArgumentList
@lru_cache
def create_app_config() -> AppConfig:
    return AppConfig(
        telegram=TelegramConfig(),
    )


settings = create_app_config()
