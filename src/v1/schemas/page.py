# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema
from schemas.common import TimeStampSchema
from schemas.image import ImageSchema
from schemas.json import JsonSchema
from schemas.status import Status


class PageCreateSchema(BaseSchema):
    """Page Create Schema"""

    version_id: str = Field(
        ...,
        title="Version ID",
        description="Version ID",
        example="44f97c86d4954afcbdc6f2443a159c28",  # type: ignore
    )
    status: Status = Field(
        default=Status.pending,
        title="Status",
        description="Status",
        example=Status.pending.value,  # type: ignore
    )
    local_index: int = Field(
        ...,
        title="Local Index",
        description="Local Index",
        example=1,  # type: ignore
    )
    global_index: int = Field(
        ...,
        title="Global Index",
        description="Global Index",
        example=1,  # type: ignore
    )


class PageUpdateSchema(BaseSchema):
    """Page Update Schema"""

    status: Status = Field(
        ...,
        title="Status",
        description="Status",
        example=Status.pending.value,  # type: ignore
    )
    local_index: int = Field(
        ...,
        title="Local Index",
        description="Local Index",
        example=1,  # type: ignore
    )
    global_index: int = Field(
        title="Global Index",
        description="Global Index",
        example=1,  # type: ignore
    )


class PageSchema(PageCreateSchema, TimeStampSchema):
    """Page Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Page ID",
        example="44f97c86d4954afcbdc6f2443a159c28",  # type: ignore
    )
    status: Status = Field(
        ...,
        title="Status",
        description="Status",
        example=Status.pending.value,  # type: ignore
    )
    version_id: str = Field(
        ...,
        title="Version ID",
        description="Version ID",
        example="44f97c86d4954afcbdc6f2443a159c28",  # type: ignore
    )
    version: int = Field(
        title="Version Number",
        description="Version Number",
        example=1,  # type: ignore
    )
    image: ImageSchema
    json: JsonSchema  # type: ignore
