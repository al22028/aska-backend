# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Path
from aws_lambda_powertools.shared.types import Annotated
from controllers.page import PageController
from schemas.page import PageSchema, PageUpdateSchema

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


@router.get(
    "/<pageId>",
    tags=["Page"],
    summary="単一ページを取得",
    description="単一ページを取得します。",
    response_description="単一ページ",
    operation_id="fetchSinglePage",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_single_page(
    pageId: Annotated[
        str,
        Path(
            ...,
            title="ページID",
            description="取得するページのID",
            example="44f97c86d4954afcbdc6f2443a159c28",
        ),
    ]
) -> PageSchema:
    return controller.find_single_page(page_id=pageId)


@router.put(
    "/<pageId>",
    tags=["Page"],
    summary="単一ページを更新",
    description="単一ページを更新します。",
    response_description="単一ページ",
    operation_id="updateSinglePage",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def update_single_page(
    pageId: Annotated[
        str,
        Path(
            ...,
            title="ページID",
            description="更新するページのID",
            example="44f97c86d4954afcbdc6f2443a159c28",
        ),
    ],
    data: PageUpdateSchema,
) -> PageSchema:
    return controller.update_single_page(page_id=pageId, data=data)
