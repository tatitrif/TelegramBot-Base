from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import DeclarativeBaseModel, UpdatedAtColumn, CreatedAtColumn, IdColumn


class User(DeclarativeBaseModel, IdColumn, UpdatedAtColumn, CreatedAtColumn):
    telegram_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    language_code: Mapped[str] = mapped_column(String(length=2), nullable=True)
