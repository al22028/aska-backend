# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema


class DeletedSchema(BaseSchema):
    message: str = Field(
        default="Object deleted successfully",
        title="Message",
        description="Message",
        example="Object deleted successfully",
    )


class TimeStampSchema(BaseSchema):
    created_at: str = Field(
        ..., description="isoformated created datetime", example="2021-09-01T00:00:00.000Z"
    )
    updated_at: str = Field(
        ..., description="isoformated updated datetime", example="2021-09-01T00:00:00.000Z"
    )


class DownloadURLSchema(BaseSchema):
    presigned_url: str = Field(
        ...,
        title="Download URL",
        description="Download URL",
        example="https://example.com/download_url",
    )
