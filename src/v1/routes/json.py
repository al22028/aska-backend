# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.shared.types import Annotated
from controllers.json import JsonController
from schemas import (
    DeletedSchema,
    DownloadURLSchema,
    JsonCreateResponseSchema,
    JsonCreateSchema,
    JsonSchema,
    JsonUpdateSchema,
)

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

app = APIGatewayRestResolver()

controller = JsonController()


@router.get(
    "/",
    tags=["JSON"],
    summary="指定されたページの特徴点データを取得",
    description="指定されたページの特徴点データを取得します。",
    response_description="特徴点データ",
    operation_id="fetchPageJson",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_page_json(pageId: Annotated[str, Query]) -> JsonSchema:
    return controller.fetch_page_json(page_id=pageId)


@router.get(
    "/all",
    tags=["JSON"],
    summary="すべてのページの特徴点データを取得",
    description="すべてのページの特徴点データを取得します。",
    response_description="全特徴点データ",
    operation_id="fetchAllJsons",
    responses={200: {"description": "成功"}, 500: {"description": "Internal Server Error"}},
)
def fetch_all_jsons() -> List[JsonSchema]:
    return controller.fetch_all_jsons()


@router.post(
    "/",
    tags=["JSON"],
    summary="特徴点データのJSONを作成",
    description="特徴点データを表すJSONを作成します。",
    response_description="作成したJSON",
    operation_id="createSingleJson",
    responses={
        201: {"description": "成功"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
def create_one_json(json_data: JsonCreateSchema) -> JsonCreateResponseSchema:
    created_json, status_code = controller.create_one(json_data=json_data)
    return created_json, status_code  # type: ignore


@router.get(
    "/<jsonId>",
    tags=["JSON"],
    summary="特徴点データを取得",
    description="特徴点データを取得します。",
    response_description="特徴点データ",
    operation_id="fetchSingleJson",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_json(jsonId: str) -> JsonSchema:
    return controller.find_one(json_id=jsonId)


@router.get(
    "/<jsonId>/download",
    tags=["JSON"],
    summary="JSONのダウンロードURLを取得",
    description="JSONのダウンロードURLを取得します。",
    response_description="ダウンロードURL",
    operation_id="fetchSingleJsonDownloadURL",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def fetch_single_json_download_url(jsonId: str) -> DownloadURLSchema:
    return controller.generate_download_url(image_id=jsonId)


@router.put(
    "/<jsonId>",
    tags=["JSON"],
    summary="特徴点データを更新",
    description="特徴点データを更新します。",
    response_description="更新した特徴点データ",
    operation_id="updateSingleJson",
    responses={
        200: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def update_single_json(jsonId: str, json_data: JsonUpdateSchema) -> JsonSchema:
    return controller.update_one(json_id=jsonId, json_data=json_data)


@router.delete(
    "/<jsonId>",
    tags=["JSON"],
    summary="特徴点データを削除",
    description="特徴点データを削除します。",
    response_description="None",
    operation_id="deleteSingleJson",
    responses={
        204: {"description": "成功"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def delete_single_json(jsonId: str) -> DeletedSchema:
    return controller.delete_one(json_id=jsonId)
