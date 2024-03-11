# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.json import JsonController
from schemas.common import DownloadURLSchema
from schemas.json import JsonSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

app = APIGatewayRestResolver()

controller = JsonController()


@router.get(
    "/",
    tags=["Json"],
    summary="全てのJsonを取得",
    description="全てのJsonを取得します。",
    response_description="全Json",
    operation_id="fetchAllJsonss",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_all_jsons() -> list[JsonSchema]:
    return controller.fetch_all_jsons()


@router.get(
    "/<jsonId>/download",
    tags=["Json"],
    summary="JsonのダウンロードURLを取得",
    description="JsonのダウンロードURLを取得します。",
    response_description="ダウンロードURL",
    operation_id="fetchSingleJsonDownloadURL",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_json_download_url(jsonId: str) -> DownloadURLSchema:
    return controller.generate_download_url(json_id=jsonId)
