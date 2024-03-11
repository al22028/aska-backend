# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema
from schemas.common import TimeStampSchema
from schemas.page import PageSchema


class VersionUpdateSchema(BaseSchema):
    title: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="タイトル",
        description="バージョンタイトル",
        example="K12345_V1",
    )
    description: str = Field(
        ...,
        min_length=0,
        max_length=512,
        title="詳細情報",
        description="バージョンの詳細情報",
        example="5月末時点のバージョン",
    )


class VersionCreateSchema(VersionUpdateSchema):
    project_id: str = Field(
        ...,
        title="Project ID",
        description="Project ID",
        example="44f97c86d4954afcbdc6f2443a159c28",
    )


class VersionSchema(VersionCreateSchema, VersionUpdateSchema, TimeStampSchema):
    id: str = Field(
        ..., title="ID", description="Version ID", example="44f97c86d4954afcbdc6f2443a159c28"
    )
    thumbnail: str = Field(
        ..., title="Thumbnail", description="Thumbnail", example="https://example.com/thumbnail.jpg"
    )


class VersionCreateResponseSchema(VersionSchema):
    presigned_url: str = Field(
        ...,
        title="(PUT) Presigned URL",
        description="Presigned URL for PUT pdf file",
        example="https://example.com/presigned_url",
    )


class VersionDetailSchema(VersionSchema):
    pages: list[PageSchema]
