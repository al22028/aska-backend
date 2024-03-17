# Third Party Library
from pydantic import Field
from schemas.base import BaseSchema
from schemas.common import TimeStampSchema
from schemas.status import Status


class ParamsSchema(BaseSchema):
    """Params Schema"""

    match_threshold: float = Field(
        ...,
        title="Match Threshold",
        description="Match Threshold",
        example=0.85,  # type: ignore
    )
    threshold: int = Field(
        ...,
        title="Threshold",
        description="Threshold",
        example=220,  # type: ignore
    )
    eps: int = Field(
        ...,
        title="Eps",
        description="Eps",
        example=20,  # type: ignore
    )
    min_samples: int = Field(
        ...,
        title="Min Samples",
        description="Min Samples",
        example=50,  # type: ignore
    )


class BoundingBoxSchema(BaseSchema):
    """Bounding Box Schema"""

    max_x: int = Field(
        ...,
        title="Max X",
        description="Max X",
        example=0,  # type: ignore
    )
    max_y: int = Field(
        ...,
        title="Max Y",
        description="Max Y",
        example=0,  # type: ignore
    )
    min_x: int = Field(
        ...,
        title="Min X",
        description="Min X",
        example=100,  # type: ignore
    )
    min_y: int = Field(
        ...,
        title="Min Y",
        description="Min Y",
        example=100,  # type: ignore
    )


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
    params: ParamsSchema = Field(
        ...,
        title="Params",
        params="Params",
        example={
            "matchThreshold": 0.85,
            "threshold": 220,
            "eps": 20,
            "minSamples": 50,
        },  # type: ignore
    )
    bounding_boxes: list[BoundingBoxSchema] = Field(
        ...,
        title="Bounding Boxes",
        description="Bounding Boxes",
        example=[{"maxX": 0, "maxY": 0, "minX": 100, "minY": 100}, {"maxX": 0, "maxY": 0, "minX": 100, "minY": 100}],  # type: ignore
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
