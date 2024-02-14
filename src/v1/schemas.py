# Standard Library
from enum import Enum

# Third Party Library
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


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


class UserCreateSchema(BaseSchema):
    id: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="ID",
        description="Same as Cognito sub",
        examples=[{"value": "44f97c86-d495-4afc-bdc6-f2443a159c28", "description": "ID"}],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Name",
        description="Name",
        examples=[{"value": "Tsubasa Taro", "description": "Name"}],
    )
    email: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description="Email",
        examples=[{"value": "tsubasa@world-wing.com", "description": "Email Address"}],
    )
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseSchema):
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Name",
        description="Name",
        examples=[{"value": "Tsubasa Taro", "description": "Name"}],
    )


class UserSchema(UserCreateSchema, TimeStampSchema):
    pass


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


class PdfUpdateSchema(BaseSchema):
    title: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Title",
        description="Title",
        examples=[{"value": "PDF A", "description": "Title"}],
    )
    description: str = Field(
        default="",
        min_length=0,
        max_length=512,
        title="Description",
        description="Description",
        examples=[{"value": "description of the pdf", "description": "Description"}],
    )


class PdfCreateSchema(PdfUpdateSchema):
    project_id: str = Field(
        ...,
        title="Project ID",
        description="Project ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "Project ID"}],
    )


class PdfSchema(PdfCreateSchema, PdfUpdateSchema, TimeStampSchema):
    id: str = Field(
        ...,
        title="ID",
        description="PDF ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "ID"}],
    )
    thumbnail: str = Field(
        ...,
        title="Thumbnail",
        description="Thumbnail",
        examples=[{"value": "https://example.com/thumbnail.jpg", "description": "Thumbnail"}],
    )


class PdfCreateResponseSchema(PdfSchema):
    presigned_url: str = Field(
        ...,
        title="(PUT) Presigned URL",
        description="Presigned URL for PUT pdf file",
        examples=[{"value": "https://example.com/presigned_url", "description": "Presigned URL"}],
    )


class DownloadURLSchema(BaseSchema):
    presigned_url: str = Field(
        ...,
        title="Download URL",
        description="Download URL",
        examples=[{"value": "https://example.com/download_url", "description": "Download URL"}],
    )


class ProjectDetailSchema(ProjectSchema):
    pdfs: list[PdfSchema]


class Status(Enum):
    """Status Enum"""

    pending = "PENDING"
    preprocessing = "PREPROCESSING"
    processing = "PROCESSING"
    completed = "COMPLETED"
    failed = "FAILED"


class PageCreateSchema(BaseSchema):
    """Page Create Schema"""

    pdf_id: str = Field(
        ...,
        title="PDF ID",
        description="PDF ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "PDF ID"}],
    )
    status: Status = Field(
        default=Status.pending,
        title="Status",
        description="Status",
        examples=[{"value": "PENDING", "description": "Status"}],
    )
    index: int = Field(
        ...,
        title="Index",
        description="Index",
        examples=[{"value": 0, "description": "Index"}],
    )


class PageUpdateSchema(BaseSchema):
    """Page Update Schema"""

    status: Status = Field(
        title="Status",
        description="Status",
        examples=[{"value": "PREPROCESSING", "description": "Status"}],
    )


class PageSchema(PageCreateSchema, TimeStampSchema):
    """Page Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Page ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "ID"}],
    )


class ImageCreateSchema(BaseSchema):
    """Image Create Schema"""

    page_id: str = Field(
        ...,
        title="Page ID",
        description="Page ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "Page ID"}],
    )
    status: Status = Field(
        default=Status.pending,
        title="Status",
        description="Status",
        examples=[{"value": "PENDING", "description": "Status"}],
    )


class ImageCreateResponseSchema(BaseSchema):
    """Image Create Response Schema"""

    presigned_url: str = Field(
        ...,
        title="(PUT) Presigned URL",
        description="Presigned URL for PUT image file",
        examples=[{"value": "https://example.com/presigned_url", "description": "Presigned URL"}],
    )


class ImageUpdateSchema(BaseSchema):
    """Image Update Schema"""

    status: Status = Field(
        title="Status",
        description="Status",
        examples=[{"value": "PREPROCESSING", "description": "Status"}],
    )


class ImageSchema(ImageCreateSchema, TimeStampSchema):
    """Image Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Image ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "ID"}],
    )
