# Standard Library

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.image import ImageController
from schemas import ImageSchema

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
