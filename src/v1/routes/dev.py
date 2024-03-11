# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.user import UserController
from schemas.user import UserSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()


controller = UserController()


@router.get(
    "/",
    tags=["Dev"],
    summary="開発用",
    description="全てのユーザーを取得します。",
    response_description="AllUsers",
    operation_id="fetchAllUsers",
)
def fetch_all_users() -> List[UserSchema]:
    return controller.fetch_all_users()
