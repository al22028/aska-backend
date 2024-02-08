# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.pdf import PdfController
from schemas import PdfCreateResponseSchema, PdfCreateSchema, PdfSchema

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
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_all_pdfs() -> List[PdfSchema]:
    return controller.fetch_all_pdfs()


@router.post(
    "/",
    tags=["Pdf"],
    summary="PDFを作成",
    description="PDFを作成します。",
    response_description="作成したPDF",
    operation_id="createOnePdf",
    responses={
        201: {"description": "成功"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
def create_one_pdf(pdf_data: PdfCreateSchema) -> PdfCreateResponseSchema:
    created_pdf, status_code = controller.create_one(pdf_data=pdf_data)
    return created_pdf, status_code  # type: ignore


@router.get(
    "/<pdfId>",
    tags=["Pdf"],
    summary="PDFを取得",
    description="PDFを取得します。",
    response_description="PDF",
    operation_id="fetchOnePdf",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_pdf(pdfId: str) -> PdfSchema:
    return controller.find_one(pdf_id=pdfId)
