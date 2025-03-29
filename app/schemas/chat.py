from schemas.base import BaseSchema


class ChatSchema(BaseSchema):
    user_id: int
    msg_text: str | None = None
