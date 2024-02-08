# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.pdf import PdfController
from schemas import PdfSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

app = APIGatewayRestResolver()

controller = PdfController()


@router.get(
    "/",
    tags=["Pdf"],
    summary="全てのPDFを取得",
    description="全てのPDFを取得します。",
    response_description="全PDF",
    operation_id="fetchAllPdfs",
)
def fetch_all_pdfs() -> List[PdfSchema]:
    return controller.fetch_all_pdfs()
