# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema
from schemas.common import TimeStampSchema
from schemas.status import Status


class JsonCreateSchema(BaseSchema):
    """Json Create Schema"""

    page_id: str = Field(
        ...,
        title="Page ID",
        description="Page ID",
        example="44f97c86d4954afcbdc6f2443a159c28",
    )
    status: Status = Field(
        ...,
        title="Status",
        description="Status",
        example=Status.pending.value,
    )
    object_key: str = Field(
        ...,
        title="Object Key",
        description="Object Key",
        example="44f97c86d4954afcbdc6f2443a159c28/1.json",
    )


class JsonCreateResponseSchema(BaseSchema):
    """Json Create Response Schema"""

    presigned_url: str = Field(
        ...,
        title="(PUT) Presigned URL",
        description="Presigned URL for PUT json file",
        example="https://example.com/presigned_url",
    )


class JsonUpdateSchema(BaseSchema):
    """Json Update Schema"""

    status: Status = Field(
        ...,
        title="Status",
        description="Status",
        example=Status.pending.value,
    )


class JsonSchema(JsonCreateSchema, TimeStampSchema):
    """Json Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Json ID",
        example="44f97c86d4954afcbdc6f2443a159c28",
    )
