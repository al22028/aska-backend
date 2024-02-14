# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.shared.types import Annotated
from controllers.image import ImageController
from schemas import (
    DeletedSchema,
    DownloadURLSchema,
    ImageCreateResponseSchema,
    ImageCreateSchema,
    ImageSchema,
    ImageUpdateSchema,
)

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

app = APIGatewayRestResolver()

controller = ImageController()


@router.get(
    "/",
    tags=["Image"],
    summary="ページに関するの画像を取得",
    description="ページに関するの画像を取得します。",
    response_description="画像",
    operation_id="fetchPageImage",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_page_image(pageId: Annotated[str, Query]) -> ImageSchema:
    return controller.fetch_page_image(page_id=pageId)


@router.get(
    "/all",
    tags=["Image"],
    summary="すべてのページの画像を取得",
    description="すべてのページの画像を取得します。",
    response_description="全画像",
    operation_id="fetchAllImages",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_all_images() -> List[ImageSchema]:
    return controller.fetch_all_images()


@router.post(
    "/",
    tags=["Image"],
    summary="画像を作成",
    description="画像を作成します。",
    response_description="作成した画像",
    operation_id="createSingleImage",
    responses={
        201: {"description": "成功"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
def create_one_image(image_data: ImageCreateSchema) -> ImageCreateResponseSchema:
    created_image, status_code = controller.create_one(image_data=image_data)
    return created_image, status_code  # type: ignore


@router.get(
    "/<imageId>",
    tags=["Image"],
    summary="画像を取得",
    description="画像を取得します。",
    response_description="Image",
    operation_id="fetchSingleImage",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_pdf(imageId: str) -> ImageSchema:
    return controller.find_one(image_id=imageId)


@router.get(
    "/<imageId>/download",
    tags=["Image"],
    summary="PDFのダウンロードURLを取得",
    description="PDFのダウンロードURLを取得します。",
    response_description="ダウンロードURL",
    operation_id="fetchSingleImageDownloadURL",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_image_download_url(imageId: str) -> DownloadURLSchema:
    return controller.generate_download_url(image_id=imageId)


@router.put(
    "/<imageId>",
    tags=["Image"],
    summary="画像を更新",
    description="画像を更新します。",
    response_description="更新した画像",
    operation_id="updateSingleImage",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def update_single_image(imageId: str, image_data: ImageUpdateSchema) -> ImageSchema:
    return controller.update_one(pdf_id=imageId, image_data=image_data)


@router.delete(
    "/<imageId>",
    tags=["Image"],
    summary="画像を削除",
    description="画像を削除します。",
    response_description="None",
    operation_id="deleteSingleImage",
    responses={
        204: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def delete_single_image(imageId: str) -> DeletedSchema:
    return controller.delete_one(image_id=imageId)
