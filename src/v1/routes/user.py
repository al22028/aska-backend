# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.user import UserController
from schemas import UserCreateSchema, UserSchema, UserUpdateSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()


controller = UserController()


@router.get(
    "/",
    tags=["User"],
    summary="Fetch All Users",
    response_description="List of Users",
    operation_id="fetchAllUsers",
)
def fetch_all_users() -> List[UserSchema]:
    return controller.fetch_all_users()


@router.get(
    "/<userId>",
    tags=["User"],
    summary="Fetch User",
    response_description="User",
    operation_id="fetchSingleUserById",
)
def fetch_user(userId: str) -> UserSchema:
    return UserSchema(
        id=userId,
        name="John Doe",
        email="sadc@mail.com",
        created_at="2021-10-10",
        updated_at="2021-10-10",
    )


@router.post(
    "/",
    tags=["User"],
    summary="Create User",
    response_description="User",
    operation_id="createSingleUser",
    responses={201: {"description": "User Created"}},
)
def create_user(user: UserCreateSchema) -> UserSchema:
    created_user, status_code = controller.create_one(user_data=user)
    return created_user, status_code  # type: ignore


@router.put(
    "/<userId>",
    tags=["User"],
    summary="Update User",
    response_description="User",
    operation_id="updateSingleUserById",
)
def update_user(userId: str, user: UserUpdateSchema) -> UserSchema:
    updated_user = controller.update_one(user_id=userId, user_data=user)
    return updated_user
