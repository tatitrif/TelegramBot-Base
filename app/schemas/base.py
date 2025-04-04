import typing

import orjson
from pydantic import ConfigDict, BaseModel


def orjson_dumps(
    v: typing.Any,
    *,
    default: typing.Callable[[typing.Any], typing.Any] | None,
) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
