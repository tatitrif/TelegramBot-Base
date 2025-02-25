from models.user import User
from repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
