# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.shared.types import Annotated
from controllers.version import VersionController
from schemas import (
    DeletedSchema,
    DownloadURLSchema,
    VersionCreateResponseSchema,
    VersionCreateSchema,
    VersionDetailSchema,
    VersionSchema,
    VersionUpdateSchema,
)

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

app = APIGatewayRestResolver()

controller = VersionController()


@router.get(
    "/",
    tags=["Version"],
    summary="プロジェクトに関する全てのPDF(バージョン)を取得",
    description="プロジェクトに関する全てのPDF(バージョン)を取得します。",
    response_description="全PDF(バージョン)",
    operation_id="fetchProjectVersions",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_project_versions(projectId: Annotated[str, Query]) -> List[VersionSchema]:
    return controller.fetch_project_pdfs(project_id=projectId)


@router.get(
    "/all",
    tags=["Version"],
    summary="すべてのプロジェクトのPDF(バージョン)を取得",
    description="すべてのプロジェクトのPDF(バージョン)を取得します。",
    response_description="全PDF",
    operation_id="fetchAllVersions",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_all_versions() -> List[VersionSchema]:
    return controller.fetch_all_versions()


@router.post(
    "/",
    tags=["Version"],
    summary="PDF(バージョン)を作成",
    description="PDF(バージョン)を作成します。",
    response_description="作成したPDF(バージョン)",
    operation_id="createSingleVersion",
    responses={
        201: {"description": "成功"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
def create_single_version(version_data: VersionCreateSchema) -> VersionCreateResponseSchema:
    created_pdf, status_code = controller.create_one(version_data=version_data)
    return created_pdf, status_code  # type: ignore


@router.get(
    "/<versionId>",
    tags=["Version"],
    summary="PDF(バージョン)を取得",
    description="PDF(バージョン)を取得します。",
    response_description="PDF(バージョン)",
    operation_id="fetchSingleVersion",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_version_by_id(versionId: str) -> VersionDetailSchema:
    return controller.find_one(version_id=versionId)


@router.get(
    "/<versionId>/download",
    tags=["Version"],
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
def fetch_single_version_download_url(versionId: str) -> DownloadURLSchema:
    return controller.generate_download_url(version_id=versionId)


@router.put(
    "/<versionId>",
    tags=["Version"],
    summary="PDF(バージョン)を更新",
    description="PDF(バージョン)を更新します。",
    response_description="更新したPDF(バージョン)",
    operation_id="updateSingleVersion",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def update_single_version(versionId: str, version_data: VersionUpdateSchema) -> VersionSchema:
    return controller.update_one(pdf_id=versionId, version_data=version_data)


@router.delete(
    "/<versionId>",
    tags=["Version"],
    summary="PDF(バージョン)を削除",
    description="PDF(バージョン)を削除します。",
    response_description="None",
    operation_id="deleteSingleVersionById",
    responses={
        204: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def delete_single_version(versionId: str) -> DeletedSchema:
    return controller.delete_one(version_id=versionId)
