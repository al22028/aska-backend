# Third Party Library
from pydantic import ConfigDict, Field
from schemas.base import BaseSchema
from schemas.common import TimeStampSchema


class UserCreateSchema(BaseSchema):
    id: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="ID",
        description="Same as Cognito sub",
        example="44f97c86-d495-4afc-bdc6-f2443a159c28",  # type: ignore
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Name",
        description="Name",
        example="Tsubasa Taro",  # type: ignore
    )
    email: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description="Email",
        example="tsubasa@world-wing.com",  # type: ignore
    )
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseSchema):
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Name",
        description="Name",
        example="Tsubasa Taro",  # type: ignore
    )


class UserSchema(UserCreateSchema, TimeStampSchema):
    pass
