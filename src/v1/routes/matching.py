# Standard Library
from http import HTTPStatus
from typing import List, Tuple

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.matching import MatchingController
from schemas import DeletedSchema, MatchingCreateSchema, MatchingSchema, MatchingUpdateSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()


controller = MatchingController()


@router.get(
    "/",
    tags=["Matching"],
    summary="全てのマッチングを取得",
    description="全てのマッチングを取得します。",
    response_description="AllMatchings",
    operation_id="fetchAllMatchings",
)
def fetch_all_matchings() -> List[MatchingSchema]:
    return controller.fetch_all_matchings()


@router.get(
    "/<matchingId>",
    tags=["Matching"],
    summary="特定のマッチングを取得",
    description="特定のマッチングを取得します。",
    response_description="Matching",
    operation_id="fetchSingleMatchingById",
    responses={
        200: {"description": "Matching"},
        404: {"description": "Matching Not Found"},
    },
)
def fetch_matching(matchingId: str) -> MatchingSchema:
    return controller.find_one_or_404(matching_id=matchingId)


@router.post(
    "/",
    tags=["Matching"],
    summary="マッチングの新規登録",
    description="マッチングの新規登録",
    response_description="Matching",
    operation_id="createSingleMatching",
    responses={201: {"description": "Matching Created"}},
)
def create_matching(matching: MatchingCreateSchema) -> Tuple[MatchingSchema, int]:
    created_matching, status_code = controller.create_one(matching_data=matching)
    return created_matching, status_code


@router.put(
    "/<matchingId>",
    tags=["Matching"],
    summary="特定マッチングの更新",
    description="特定マッチングを更新します。",
    response_description="Matching",
    operation_id="updateSingleMatchingById",
    responses={
        200: {"description": "Matching Updated"},
        400: {"description": "Bad Request"},
        404: {"description": "Matching Not Found"},
    },
)
def update_matching(matchingId: str, matching: MatchingUpdateSchema) -> MatchingSchema:
    updated_matching = controller.update_one(matching_id=matchingId, matching_data=matching)
    return updated_matching


@router.delete(
    "/<matchingId>",
    tags=["Matching"],
    summary="特定マッチングの削除",
    description="特定マッチングを削除します。",
    response_description="Matching",
    operation_id="deleteSingleMatchingById",
    responses={
        200: {"description": "Matching Deleted"},
        404: {"description": "Matching Not Found"},
    },
)
def delete_single_matching(matchingId: str) -> Tuple[DeletedSchema, HTTPStatus]:
    controller.delete_one(matching_id=matchingId)
    return DeletedSchema(message="Matching deleted successfully"), HTTPStatus.OK
