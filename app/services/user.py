import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from schemas.user import UserSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, user_data):
        user_info = await UserRepository(self.session).find_one_or_none(id=user_data.id)
        if not user_info:
            try:
                user_schema = UserSchema(
                    id=user_data.id,
                    is_bot=user_data.is_bot,
                    username=user_data.username,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                    language_code=user_data.language_code,
                )

                user_dict = user_schema.model_dump()
                entity = await UserRepository(self.session).add_one(user_dict)
                await self.session.commit()
                await self.session.refresh(entity)
                logger.info(f"Add: {str(entity)}")

            except SQLAlchemyError as err:
                logger.error(f"SQLAlchemyError: {str(err)}")
                raise

    async def find_one(self, data):
        pass
