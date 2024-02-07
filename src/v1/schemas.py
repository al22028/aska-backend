# Third Party Library
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class TimeStampSchema(BaseSchema):
    created_at: str = Field(
        ...,
        description="isoformated created datetime",
        examples=[
            {"value": "2021-09-01T00:00:00.000Z", "description": "isoformated created datetime"}
        ],
    )
    updated_at: str = Field(
        ...,
        description="isoformated updated datetime",
        examples=[
            {"value": "2021-09-01T00:00:00.000Z", "description": "isoformated updated datetime"}
        ],
    )


class UserCreateSchema(BaseSchema):
    id: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="ID",
        description="Same as Cognito sub",
        examples=[{"value": "44f97c86-d495-4afc-bdc6-f2443a159c28", "description": "ID"}],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Name",
        description="Name",
        examples=[{"value": "Tsubasa Taro", "description": "Name"}],
    )
    email: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description="Email",
        examples=[{"value": "tsubasa@world-wing.com", "description": "Email Address"}],
    )
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseSchema):
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Name",
        description="Name",
        examples=[{"value": "Tsubasa Taro", "description": "Name"}],
    )


class UserSchema(UserCreateSchema, TimeStampSchema):
    pass


class ProjectCreateSchema(BaseSchema):
    title: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Title",
        description="Title",
        examples=[{"value": "Project A", "description": "Title"}],
    )
    description: str | None = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Description",
        description="Description",
        examples=[{"value": "description of the project", "description": "Description"}],
    )
    thumnail: str | None = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Thumnail",
        description="Thumnail",
        examples=[{"value": "https://example.com/thumnail.jpg", "description": "Thumnail"}],
    )


class ProjectUpdateSchema(BaseSchema):
    title: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Title",
        description="Title",
        examples=[{"value": "Project A", "description": "Title"}],
    )
    description: str | None = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Description",
        description="Description",
        examples=[{"value": "description of the project", "description": "Description"}],
    )
    thumnail: str | None = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Thumnail",
        description="Thumnail",
        examples=[{"value": "https://example.com/thumnail.jpg", "description": "Thumnail"}],
    )


class ProjectSchema(ProjectCreateSchema, TimeStampSchema):
    pass
