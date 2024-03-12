# Third Party Library
from pydantic import ConfigDict, Field
from schemas.base import BaseSchema
from schemas.common import TimeStampSchema


class UserCreateSchema(BaseSchema):
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="名前",
        description="名前",
        example="Tsubasa Taro",  # type: ignore
    )
    email: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="メールアドレス",
        description="メールアドレス",
        example="tsubasa@world-wing.com",  # type: ignore
    )
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseSchema):
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="名前",
        description="名前",
        example="Tsubasa Taro",  # type: ignore
    )


class UserSchema(UserCreateSchema, TimeStampSchema):
    id: str = Field(
        ...,
        title="ユーザーID",
        description="CognitoのユーザーID(sub)",
        example="e7b45a98-1031-7095-d7ee-6748af941d2a",  # type: ignore
    )


class UserCreateResponsSchema(UserSchema):
    password: str = Field(
        ..., title="パスワード", description="初期パスワード", example="p@ssw0rd"  # type: ignore
    )
