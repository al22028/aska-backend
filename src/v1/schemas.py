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
        default="",
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


class DownloadURLSchema(BaseSchema):
    presigned_url: str = Field(
        ...,
        title="Download URL",
        description="Download URL",
        examples=[{"value": "https://example.com/download_url", "description": "Download URL"}],
    )


class ProjectDetailSchema(ProjectSchema):
    versions: list[VersionSchema]


class Status(Enum):
    """Status Enum"""

    pending = "PENDING"  # 待機状態
    preprocessing = "PREPROCESSING"  # 前処理中
    preprocessed = "PREPROCESSED"  # 前処理完了
    preprocessing_timedout = "PREPROCESSING_TIMEDOUT"  # 前処理タイムアウト
    preprocessing_failed = "PREPROCESSING_FAILED"  # 前処理失敗
    matching_calculation = "MATCHING_CALCULATION_IN_PROGRESS"  # マッチング計算中
    matching_calculation_timedout = "MATCHING_CALCULATION_TIMEDOUT"  # マッチング計算タイムアウト
    matching_calculation_failed = "MATCHING_CALCULATION_FAILED"  # マッチング計算失敗
    matching_calculation_success = "MATCHING_CALCULATION_SUCCESS"  # マッチング計算成功
    differential_calculation = "DIFFERENTIAL_CALCULATION_IN_PROGRESS"  # 差分計算中
    differential_calculation_timedout = "DIFFERENTIAL_CALCULATION_TIMEDOUT"  # 差分計算タイムアウト
    differential_calculation_no_differences_found = (
        "DIFFERENTIAL_CALCULATION_NO_DIFFERENCES_FOUND"  # 差分検出なし
    )
    differential_calculation_failed = "DIFFERENTIAL_CALCULATION_FAILED"  # 差分計算失敗
    differential_calculation_not_enough_matches = (
        "DIFFERENTIAL_CALCULATION_NOT_ENOUGH_MATCHES"  # マッチング数不足
    )
    completed = "COMPLETED"  # 正常終了
    failed = "FAILED"  # 異常終了
    canceled = "CANCELED"  # キャンセル
    retry = "RETRY"  # 再実行


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
    object_key: str = Field(
        ...,
        title="Object Key",
        description="Object Key",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28/1.png", "description": "Object Key"}],
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


class JsonCreateSchema(BaseSchema):
    """Json Create Schema"""

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
    object_key: str = Field(
        ...,
        title="Object Key",
        description="Object Key",
        examples=[
            {"value": "44f97c86d4954afcbdc6f2443a159c28/1.json", "description": "Object Key"}
        ],
    )


class JsonCreateResponseSchema(BaseSchema):
    """Json Create Response Schema"""

    presigned_url: str = Field(
        ...,
        title="(PUT) Presigned URL",
        description="Presigned URL for PUT json file",
        examples=[{"value": "https://example.com/presigned_url", "description": "Presigned URL"}],
    )


class JsonUpdateSchema(BaseSchema):
    """Json Update Schema"""

    status: Status = Field(
        title="Status",
        description="Status",
        examples=[{"value": "PREPROCESSING", "description": "Status"}],
    )


class JsonSchema(JsonCreateSchema, TimeStampSchema):
    """Json Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Json ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "ID"}],
    )


class LambdaInvokePayload(BaseModel):
    body: dict


class PageSchema(PageCreateSchema, TimeStampSchema):
    """Page Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Page ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "ID"}],
    )
    status: Status = Field(
        default=Status.pending.value,
        title="Status",
        description="Status",
        examples=[{"value": "PENDING", "description": "Status"}],
    )

    version: VersionSchema
    image: ImageSchema
    json: JsonSchema  # type: ignore


class VersionDetailSchema(VersionSchema):
    pages: list[PageSchema]


class MatchingCreateSchema(BaseSchema):
    """Matching Create Schema"""

    image1_id: str = Field(
        ...,
        title="Image1 ID",
        description="Image1 ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "Image1 ID"}],
    )
    image2_id: str = Field(
        ...,
        title="Image2 ID",
        description="Image2 ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "Image2 ID"}],
    )
    params: dict = Field(
        default={"threshold": 220, "eps": 20, "min_samples": 50, "acc": 0.1},
        title="Params",
        description="Params",
        examples=[
            {
                "value": {"threshold": 220, "eps": 20, "min_samples": 50, "acc": 0.1},
                "description": "Params",
            }
        ],
    )
    status: Status = Field(
        title="Status",
        description="Status",
        examples=[{"value": "MATCHING_CALCULATION_IN_PROGRESS", "description": "Status"}],
    )


class MatchingUpdateSchema(BaseSchema):
    """Matching Update Schema"""

    score: float = Field(
        title="Score",
        description="Score",
        examples=[{"value": 0.1, "description": "Score"}],
    )
    params: dict = Field(
        title="Params",
        description="Params",
        examples=[
            {
                "value": {"threshold": 220, "eps": 20, "min_samples": 50, "acc": 0.1},
                "description": "Params",
            }
        ],
    )
    status: Status = Field(
        title="Status",
        description="Status",
        examples=[{"value": "MATCHING_CALCULATION_IN_PROGRESS", "description": "Status"}],
    )
    bounding_boxes: dict = Field(
        title="bounding boxes",
        description="bounding boxes",
        examples=[
            {
                "value": {
                    "0": {"position": {"max_x": 100, "max_y": 100, "min_x": 0, "min_y": 0}},
                    "1": {"position": {"max_x": 10, "max_y": 10, "min_x": 0, "min_y": 0}},
                },
                "description": "bounding boxes",
            }
        ],
    )


class MatchingSchema(MatchingCreateSchema, MatchingUpdateSchema, TimeStampSchema):
    """Matching Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Matching ID",
        examples=[{"value": "44f97c86d4954afcbdc6f2443a159c28", "description": "ID"}],
    )
