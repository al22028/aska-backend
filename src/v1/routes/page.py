# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.page import PageController
from schemas.page import PageSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

app = APIGatewayRestResolver()

controller = PageController()


@router.get(
    "/",
    tags=["Page"],
    summary="全てのページを取得",
    description="全てのページを取得します。",
    response_description="全ページ",
    operation_id="fetchAllPages",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_all_pages() -> list[PageSchema]:
    return controller.find_all_pages()
