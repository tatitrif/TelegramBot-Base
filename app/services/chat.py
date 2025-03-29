import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.chat import ChatRepository
from schemas.chat import ChatSchema

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, user_id, msg_text):
        try:
            user_schema = ChatSchema(
                user_id=user_id,
                msg_text=msg_text,
            )
            user_dict = user_schema.model_dump()

            entity = await ChatRepository(self.session).add_one(user_dict)
            await self.session.commit()
            await self.session.refresh(entity)
            logger.info(f"Add: {str(entity)}")

        except SQLAlchemyError as err:
            logger.error(f"SQLAlchemyError: {str(err)}")
            raise
