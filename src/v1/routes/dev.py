# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.shared.types import Annotated
from controllers.dev import DevController
from schemas.diff import DiffSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

controller = DevController()


@router.post(
    "/diff",
    tags=["Dev"],
    summary="差分のjsonを計算",
    description="差分のJsonを計算します",
)
def create_image_diff(
    iimage1Id: Annotated[str, Query], image2Id: Annotated[str, Query]
) -> DiffSchema:
    return controller.create_image_diff(image1_id=iimage1Id, image2_id=image2Id)
