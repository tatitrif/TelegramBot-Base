from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import DeclarativeBaseModel, UpdatedAtColumn, CreatedAtColumn, IdColumn


class User(DeclarativeBaseModel, IdColumn, UpdatedAtColumn, CreatedAtColumn):
    telegram_id: Mapped[int] = mapped_column(unique=True)
    is_bot: Mapped[bool] = mapped_column(Boolean)
    username: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    language_code: Mapped[str] = mapped_column(String(length=3), nullable=True)
