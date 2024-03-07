# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema


class DeletedSchema(BaseSchema):
    message: str = Field(
        default="Object deleted successfully",
        title="Message",
        description="Message",
        examples=[{"value": "Object deleted successfully", "description": "Message"}],
    )


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


class DownloadURLSchema(BaseSchema):
    presigned_url: str = Field(
        ...,
        title="Download URL",
        description="Download URL",
        examples=[{"value": "https://example.com/download_url", "description": "Download URL"}],
    )
