import datetime as datetime
import re

from sqlalchemy import func, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    declared_attr,
    DeclarativeBase,
)


class UpdatedAtColumn:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        doc="Time of creation",
    )


class CreatedAtColumn:
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        doc="Time of modification",
    )


class IdColumn:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class DeclarativeBaseModel(AsyncAttrs, DeclarativeBase):
    """Base class for all models."""

    @declared_attr
    def __tablename__(self) -> str:
        """Table name based on class name."""
        # e.g. SomeModelName -> some_model_name
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__name__).lower()

    __abstract__ = True

    repr_cols_num = 3  # print first columns
    repr_cols = ()  # extra printed columns

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}, ...>"
