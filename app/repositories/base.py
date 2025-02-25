from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import insert, select, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import DeclarativeBaseModel

ModelType = TypeVar("ModelType", bound=DeclarativeBaseModel)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> RowMapping:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filter_by) -> RowMapping:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """
    Этот класс реализует базовый интерфейс для работы с базой данных.

    Упрощает работу с аннотациями типов. Поддерживает все классические операции CRUD, а
    также пользовательские запросы.
    """

    model: type[ModelType] = None

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория с помощью сеанса базы данных.

        Args:
            session (AsyncSession): Сеанс базы данных.
        """
        self.session = session
        if self.model is None:
            raise ValueError("Модель должна быть указана в дочернем классе")

    async def add_one(self, data) -> type[ModelType]:
        """
        Создание объекта.

        Args:
            data: Схема вводимых данных.

        Returns:
            Type[ModelType]: экземпляр модель БД.
        """
        stmt = insert(self.model).values(data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_one(self, **filter_dict) -> type[ModelType] | None:
        """
        Находит один объект.

        Args:
           **filter_dict: Критерии фильтрации в виде именованных параметров.

        Returns:
            Type[ModelType]: экземпляр модель БД.
        """
        stmt = select(self.model).filter_by(**filter_dict)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_one_or_none(self, **filter_dict) -> type[ModelType] | None:
        """
        Находит только один объект или ничего.

        Args:
           **filter_dict: Критерии фильтрации в виде именованных параметров.

        Returns:
            Type[ModelType]: экземпляр модель БД.
        """
        stmt = select(self.model).filter_by(**filter_dict)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
