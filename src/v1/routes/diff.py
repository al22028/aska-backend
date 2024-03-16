# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.diff import DiffController
from schemas.diff import DiffCreateSchema, DiffSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

app = APIGatewayRestResolver()

controller = DiffController()


@router.get(
    "/",
    tags=["Diff"],
    summary="全ての差分情報を取得",
    description="全ての差分情報を持つjsonを取得します。",
    response_description="バウンディングボックス情報",
    operation_id="fetchAllDiffs",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_all_diffs() -> list[DiffSchema]:
    return controller.find_all()


@router.get(
    "/<image1_id>/<image2_id>",
    tags=["Diff"],
    summary="画像対の差分情報を取得",
    description="画像対の差分情報を取得を持つjsonを取得します。",
    response_description="バウンディングボックス情報",
    operation_id="fetchDiffByImageIds",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def find_matched_image_diff(image1_id: str, image2_id: str) -> list[DiffSchema]:
    return controller.find_by_ids(image1_id=image1_id, image2_id=image2_id)


@router.post(
    "/",
    tags=["Diff"],
    summary="画像対の差分情報を作成",
    description="画像対の差分情報を作成します。",
    response_description="バウンディングボックス情報",
    operation_id="createDiff",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def create_diff(diff_data: DiffCreateSchema) -> DiffSchema:
    return controller.create_one(diff_data=diff_data)
