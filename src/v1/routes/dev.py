# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.openapi.params import Path, Query
from aws_lambda_powertools.shared.types import Annotated
from controllers.dev import DevController
from schemas.common import DeletedSchema
from schemas.diff import DiffSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

controller = DevController()


@router.post(
    "/diff",
    tags=["Dev"],
    summary="差分のjsonを計算",
    description="差分のJsonを計算します",
)
def create_image_diff(
    image1Id: Annotated[
        str, Query(description="画像1のID", example="44f97c86d4954afcbdc6f2443a159c28")
    ],
    image2Id: Annotated[
        str, Query(description="画像2のID", example="44f97c86d4954afcbdc6f2443a159c29")
    ],
) -> DiffSchema:
    return controller.create_image_diff(image1_id=image1Id, image2_id=image2Id)


@router.delete(
    "/users/<userId>",
    tags=["Dev"],
    summary="ユーザーを削除",
    description="APIのみのユーザーを削除します",
)
def delete_single_user_dev(
    userId: Annotated[
        str,
        Path(
            title="ユーザーID",
            description="API側のユーザーのみ削除します。Cognitoのユーザーに関しては削除しません。",
            example="e7b45a98-1031-7095-d7ee-6748af941d2a",
        ),
    ]
) -> DeletedSchema:
    return controller.delete_single_user(user_id=userId)
