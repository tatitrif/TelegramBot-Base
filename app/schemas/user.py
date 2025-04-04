from schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id: int

    is_bot: bool
    username: str
    first_name: str | None = None
    last_name: str | None = None
    language_code: str
