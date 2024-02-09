# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.shared.types import Annotated
from controllers.pdf import PdfController
from schemas import (
    DeletedSchema,
    DownloadURLSchema,
    PdfCreateResponseSchema,
    PdfCreateSchema,
    PdfSchema,
    PdfUpdateSchema,
)

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

app = APIGatewayRestResolver()

controller = PdfController()


@router.get(
    "/",
    tags=["Pdf"],
    summary="プロジェクトに関する全てのPDFを取得",
    description="プロジェクトに関する全てのPDFを取得します。",
    response_description="全PDF",
    operation_id="fetchProjectPdfs",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_project_pdfs(projectId: Annotated[str, Query]) -> List[PdfSchema]:
    return controller.fetch_project_pdfs(project_id=projectId)


@router.get(
    "/all",
    tags=["Pdf"],
    summary="すべてのプロジェクトのPDFを取得",
    description="すべてのプロジェクトのPDFを取得します。",
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
    operation_id="createSinglePdf",
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
    operation_id="fetchSinglePdf",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_pdf(pdfId: str) -> PdfSchema:
    return controller.find_one(pdf_id=pdfId)


@router.get(
    "/<pdfId>/download",
    tags=["Pdf"],
    summary="PDFのダウンロードURLを取得",
    description="PDFのダウンロードURLを取得します。",
    response_description="ダウンロードURL",
    operation_id="fetchSinglePdfDownloadURL",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_pdf_download_url(pdfId: str) -> DownloadURLSchema:
    return controller.generate_download_url(pdf_id=pdfId)


@router.put(
    "/<pdfId>",
    tags=["Pdf"],
    summary="PDFを更新",
    description="PDFを更新します。",
    response_description="更新したPDF",
    operation_id="updateSinglePdf",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def update_single_pdf(pdfId: str, pdf_data: PdfUpdateSchema) -> PdfSchema:
    return controller.update_one(pdf_id=pdfId, pdf_data=pdf_data)


@router.delete(
    "/<pdfId>",
    tags=["Pdf"],
    summary="PDFを削除",
    description="PDFを削除します。",
    response_description="None",
    operation_id="deleteSinglePdf",
    responses={
        204: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def delete_single_pdf(pdfId: str) -> DeletedSchema:
    return controller.delete_one(pdf_id=pdfId)
