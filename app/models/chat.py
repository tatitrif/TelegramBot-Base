from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import User
from .base import DeclarativeBaseModel, UpdatedAtColumn, CreatedAtColumn, IdColumn


class Chat(DeclarativeBaseModel, IdColumn, UpdatedAtColumn, CreatedAtColumn):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    msg_text: Mapped[str] = mapped_column(nullable=True)
