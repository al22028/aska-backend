# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema
from schemas.common import TimeStampSchema
from schemas.version import VersionSchema


class ProjectCreateSchema(BaseSchema):
    title: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Title",
        description="Title",
        example="Project A",  # type: ignore
    )
    description: str = Field(
        ...,
        min_length=0,
        max_length=512,
        title="Description",
        description="Description",
        example="Project A Description",  # type: ignore
    )


class ProjectUpdateSchema(ProjectCreateSchema):
    pass


class ProjectSchema(ProjectUpdateSchema, TimeStampSchema):
    id: str = Field(
        ...,
        title="ID",
        description="Project ID",
        example="44f97c86d4954afcbdc6f2443a159c28",  # type: ignore
    )


class ProjectDetailSchema(ProjectSchema):
    versions: list[VersionSchema]
