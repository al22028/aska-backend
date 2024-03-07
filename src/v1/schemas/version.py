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
        examples=[{"value": "K12345_V1", "description": "Title"}],
    )
    description: str = Field(
        ...,
        min_length=0,
        max_length=512,
        title="詳細情報",
        description="バージョンの詳細情報",
        examples=[{"value": "5月末時点のバージョン", "description": "Description"}],
    )


class VersionCreateSchema(VersionUpdateSchema):
    project_id: str = Field(
        ...,
        title="Project ID",
        description="Project ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "Project ID"}],
    )


class VersionSchema(VersionCreateSchema, VersionUpdateSchema, TimeStampSchema):
    id: str = Field(
        ...,
        title="ID",
        description="Version ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "ID"}],
    )
    thumbnail: str = Field(
        ...,
        title="Thumbnail",
        description="Thumbnail",
        examples=[{"value": "https://example.com/thumbnail.jpg", "description": "Thumbnail"}],
    )


class VersionCreateResponseSchema(VersionSchema):
    presigned_url: str = Field(
        ...,
        title="(PUT) Presigned URL",
        description="Presigned URL for PUT pdf file",
        examples=[{"value": "https://example.com/presigned_url", "description": "Presigned URL"}],
    )


class VersionDetailSchema(VersionSchema):
    pages: list[PageSchema]
