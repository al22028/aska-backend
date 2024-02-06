# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.utilities.validation import validator
from schemas import UserCreateSchema, UserSchema, UserUpdateSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()


@router.get(
    "/",
    tags=["User"],
    summary="Fetch All Users",
    response_description="List of Users",
    operation_id="fetchAllUsers",
)
def fetch_all_users() -> List[UserSchema]:
    users = [
        UserSchema(
            id="1",
            name="John Doe",
            email="sadc@mail.com",
            created_at="2021-10-10",
            updated_at="2021-10-10",
        ),
    ]
    return users


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
)
@validator(request_body=UserCreateSchema)
def create_user(user: UserCreateSchema) -> UserSchema:
    return UserSchema(
        **user.model_dump(),
        created_at="2021-10-10",
        updated_at="2021-10-10",
    )


@router.put(
    "/<userId>",
    tags=["User"],
    summary="Update User",
    response_description="User",
    operation_id="updateSingleUserById",
)
@validator(request_body=UserUpdateSchema)
def update_user(userId: str, user: UserUpdateSchema) -> UserSchema:
    return UserSchema(
        id=userId,
        **user.model_dump(),
        created_at="2021-10-10",
        updated_at="2021-10-10",
    )
