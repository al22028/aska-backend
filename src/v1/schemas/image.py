# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema
from schemas.common import TimeStampSchema
from schemas.status import Status


class ImageCreateSchema(BaseSchema):
    """Image Create Schema"""

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
        example="44f97c86d4954afcbdc6f2443a159c28/1.png",
    )


class ImageCreateResponseSchema(BaseSchema):
    """Image Create Response Schema"""

    presigned_url: str = Field(
        ...,
        title="(PUT) Presigned URL",
        description="Presigned URL for PUT image file",
        example="https://example.com/presigned_url",
    )


class ImageUpdateSchema(BaseSchema):
    """Image Update Schema"""

    status: Status = Field(
        ...,
        title="Status",
        description="Status",
        example=Status.pending.value,
    )


class ImageSchema(ImageCreateSchema, TimeStampSchema):
    """Image Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Image ID",
        example="44f97c86d4954afcbdc6f2443a159c28",
    )
