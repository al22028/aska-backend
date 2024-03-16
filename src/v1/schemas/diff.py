# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema
from schemas.common import TimeStampSchema
from schemas.status import Status


class DiffUpdateSchema(BaseSchema):
    """Diff Update Schema"""

    score: float = Field(
        ...,
        title="Score",
        description="Score",
        example=90.0,  # type: ignore
    )
    status: Status = Field(
        ...,
        title="Status",
        description="Status",
        example=Status.matching_calculation_success.value,  # type: ignore
    )
    params: dict = Field(
        ...,
        title="Params",
        params="Params",
        example={"threshold": 0.5},  # type: ignore
    )
    bounding_boxes: dict = Field(
        ...,
        title="Bounding Boxes",
        description="Bounding Boxes",
        example={"image1": {"x": 0, "y": 0, "w": 100, "h": 100}, "image2": {"x": 0, "y": 0, "w": 100, "h": 100}},  # type: ignore
    )


class DiffCreateSchema(DiffUpdateSchema):
    """Diff Create Schema"""

    image1_id: str = Field(
        ...,
        title="Image1 ID",
        description="Image1 ID",
        example="44f97c86d4954afcbdc6f2443a159c28",  # type: ignore
    )
    image2_id: str = Field(
        ...,
        title="Image2 ID",
        description="Page ID",
        example="44f97c86d4954afcbdc6f2443a159c28",  # type: ignore
    )


class DiffSchema(DiffCreateSchema, TimeStampSchema):
    """Diff Schema"""

    id: str = Field(
        ...,
        title="ID",
        description="Diff ID",
        example="44f97c86d4954afcbdc6f2443a159c28",  # type: ignore
    )
