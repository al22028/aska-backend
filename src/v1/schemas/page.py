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
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "Version ID"}],
    )
    status: Status = Field(
        default=Status.pending,
        title="Status",
        description="Status",
        examples=[{"value": "PENDING", "description": "Status"}],
    )
    local_index: int = Field(
        ...,
        title="local Index",
        description="local Index",
        examples=[{"value": 0, "description": "Local Index"}],
    )


class PageUpdateSchema(BaseSchema):
    """Page Update Schema"""

    status: Status = Field(
        ...,
        title="Status",
        description="Status",
        examples=[{"value": "PREPROCESSING", "description": "Status"}],
    )
    global_index: int = Field(
        title="Global Index",
        description="Global Index",
        examples=[{"value": 0, "description": "Global Index"}],
    )


class PageSchema(PageCreateSchema, TimeStampSchema):
    """Page Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Page ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "ID"}],
    )
    status: Status = Field(
        ...,
        title="Status",
        description="Status",
        examples=[{"value": "PENDING", "description": "Status"}],
    )
    version_id: str = Field(
        ...,
        title="Version ID",
        description="Version ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "Version ID"}],
    )
    image: ImageSchema
    json: JsonSchema  # type: ignore
