from models.chat import Chat
from repositories.base import SQLAlchemyRepository


class ChatRepository(SQLAlchemyRepository):
    model = Chat
