# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.dev import DevController
from schemas.diff import DiffSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

controller = DevController()


@router.post(
    "/diff/<image1_id>/<image2_id>",
    tags=["Dev"],
    summary="差分のjsonを計算",
    description="差分のJsonを計算します",
)
def create_image_diff(image1_id: str, image2_id: str) -> DiffSchema:
    return controller.create_image_diff(image1_id=image1_id, image2_id=image2_id)
