# Third Party Library
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class TimeStampSchema(BaseSchema):
    created_at: str = Field(
        ..., description="isoformated created datetime", example="2021-09-01T00:00:00.000Z"
    )
    updated_at: str = Field(
        ..., description="isoformated updated datetime", example="2021-09-01T00:00:00.000Z"
    )


class UserCreateSchema(BaseSchema):
    id: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="ID",
        description="Same as Cognito sub",
        example="44f97c86-d495-4afc-bdc6-f2443a159c28",
    )
    name: str = Field(
        ..., min_length=1, max_length=256, title="Name", description="Name", example="Tsubasa Taro"
    )
    email: EmailStr = Field(
        ...,
        min_length=1,
        max_length=256,
        description="Email",
        examples=[{"value": "tsubasa@world-wing.com", "description": "Email Address"}],
    )
    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserCreateSchema, TimeStampSchema):
    pass
