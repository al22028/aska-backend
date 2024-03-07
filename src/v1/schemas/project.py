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
        examples=[{"value": "Project A", "description": "Title"}],
    )
    description: str = Field(
        default="",
        min_length=0,
        max_length=512,
        title="Description",
        description="Description",
        examples=[{"value": "description of the project", "description": "Description"}],
    )


class ProjectUpdateSchema(ProjectCreateSchema):
    pass


class ProjectSchema(ProjectUpdateSchema, TimeStampSchema):
    id: str = Field(
        ...,
        title="ID",
        description="Project ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "ID"}],
    )


class ProjectDetailSchema(ProjectSchema):
    versions: list[VersionSchema]
