# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema


class DeletedSchema(BaseSchema):
    message: str = Field(
        default="Object deleted successfully",
        title="メッセージ",
        description="削除成功",
        example="Object deleted successfully",  # type: ignore
    )


class TimeStampSchema(BaseSchema):
    created_at: str = Field(
        ...,
        title="作成時刻",
        description="isoformated created datetime",
        example="2021-09-01T00:00:00.000Z",  # type: ignore
    )
    updated_at: str = Field(
        ...,
        title="更新時刻",
        description="isoformated updated datetime",
        example="2021-09-01T00:00:00.000Z",  # type: ignore
    )


class DownloadURLSchema(BaseSchema):
    presigned_url: str = Field(
        ...,
        title="ダウンロードURL",
        description="presigned URL for download file",
        example="https://example.com/download_url",  # type: ignore
    )
