# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Path
from aws_lambda_powertools.shared.types import Annotated
from controllers.image import ImageController
from schemas.common import DownloadURLSchema
from schemas.image import ImageSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

app = APIGatewayRestResolver()

controller = ImageController()


@router.get(
    "/",
    tags=["Image"],
    summary="全ての画像を取得",
    description="全ての画像を取得します。",
    response_description="全画像",
    operation_id="fetchAllIimages",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_all_images() -> list[ImageSchema]:
    return controller.fetch_all_images()


@router.get(
    "/<imageId>/download",
    tags=["Image"],
    summary="画像のダウンロードURLを取得",
    description="画像のダウンロードURLを取得します。",
    response_description="ダウンロードURL",
    operation_id="fetchSingleImageDownloadURL",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_image_download_url(
    imageId: Annotated[
        str,
        Path(
            title="画像ID",
            description="ダウンロードしたい画像のIDを指定してください。",
            example="44f97c86d4954afcbdc6f2443a159c28",
        ),
    ]
) -> DownloadURLSchema:
    return controller.generate_download_url(image_id=imageId)
