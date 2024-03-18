# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Path
from aws_lambda_powertools.shared.types import Annotated
from controllers.user import UserController
from schemas.common import DeletedSchema
from schemas.user import UserCreateResponsSchema, UserCreateSchema, UserSchema, UserUpdateSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()


controller = UserController()


@router.get(
    "/",
    tags=["User"],
    summary="全てのユーザーを取得",
    description="全てのユーザーを取得します。",
    response_description="AllUsers",
    operation_id="fetchAllUsers",
)
def fetch_all_users() -> List[UserSchema]:
    return controller.fetch_all_users()


@router.get(
    "/<userId>",
    tags=["User"],
    summary="特定のユーザーを取得",
    description="特定のユーザーを取得します。",
    response_description="User",
    operation_id="fetchSingleUserById",
    responses={
        200: {"description": "User"},
        404: {"description": "User Not Found"},
    },
)
def fetch_user(
    userId: Annotated[
        str,
        Path(
            title="ユーザーID",
            description="CognitoのSubに相当するユーザーIDを指定してください。",
            example="e7b45a98-1031-7095-d7ee-6748af941d2a",
        ),
    ],
) -> UserSchema:
    return controller.find_one_or_404(user_id=userId)


@router.post(
    "/",
    tags=["User"],
    summary="ユーザーの新規登録",
    description="ユーザーの新規登録",
    response_description="User",
    operation_id="createSingleUser",
    responses={201: {"description": "User Created"}},
)
def create_user(user: UserCreateSchema) -> UserCreateResponsSchema:
    created_user, status_code = controller.create_one(user_data=user)
    return created_user, status_code  # type: ignore


@router.put(
    "/<userId>",
    tags=["User"],
    summary="特定ユーザーの更新",
    description="特定ユーザーを更新します。",
    response_description="User",
    operation_id="updateSingleUserById",
    responses={
        200: {"description": "User Updated"},
        400: {"description": "Bad Request"},
        404: {"description": "User Not Found"},
    },
)
def update_user(
    userId: Annotated[
        str,
        Path(
            title="ユーザーID",
            description="CognitoのSubに相当するユーザーIDを指定してください。",
            example="e7b45a98-1031-7095-d7ee-6748af941d2a",
        ),
    ],
    user: UserUpdateSchema,
) -> UserSchema:
    updated_user = controller.update_one(user_id=userId, user_data=user)
    return updated_user


@router.delete(
    "/<userId>",
    tags=["User"],
    summary="特定ユーザーの削除",
    description="特定ユーザーを削除します。",
    response_description="User",
    operation_id="deleteSingleUserById",
    responses={
        200: {"description": "User Deleted"},
        404: {"description": "User Not Found"},
    },
)
def delete_single_user(
    userId: Annotated[
        str,
        Path(
            title="ユーザーID",
            description="CognitoのSubに相当するユーザーIDを指定してください。",
            example="e7b45a98-1031-7095-d7ee-6748af941d2a",
        ),
    ],
) -> DeletedSchema:
    controller.delete_one(user_id=userId)
    return DeletedSchema(message="User deleted successfully"), HTTPStatus.OK  # type: ignore
