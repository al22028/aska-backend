# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.diff import DiffController
from schemas.diff import DiffSchema

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
