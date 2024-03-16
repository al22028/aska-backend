# Third Party Library
from aws_lambda_powertools import Logger
from models.image import ImageORM
from models.json import JsonORM
from models.matching import MatchinORM
from models.page import PageORM
from models.version import VersionORM
from schemas.diff import DiffCreateSchema, DiffSchema
from schemas.payload import LambdaInvokePayload
from database.base import Image
from database.session import with_session
from sqlalchemy.orm.session import Session
from aws.lambda_client import LambdaClient
from config.settings import AWS_IMAGE_BUCKET

logger = Logger("DevController")


class DevController:
    pages = PageORM()
    images = ImageORM()
    jsons = JsonORM()
    versions = VersionORM()
    matchings = MatchinORM()
    lambda_client = LambdaClient()

    def calculate_macthing_score(self, image1: Image, image2: Image) -> None:
        response = self.lambda_client.invoke(
            function_name="aska-api-dev-MatchingCalculateHandler",
            payload=LambdaInvokePayload(
                body={
                    "bucket_name": AWS_IMAGE_BUCKET,
                    "before": image1.object_key,
                    "after": image2.object_key,
                }
            ),
        )

    @with_session
    def create_image_diff(self, session: Session, image1_id: str, image2_id: str) -> dict:
        image1 = self.images.find_one(db=session, id=image1_id)
        image2 = self.images.find_one(db=session, id=image2_id)

        diff = self.matchings.create_one(
            diff_data=DiffCreateSchema(
                image1_id=image1.id,
                image2_id=image2.id,
                score=0.0,
            ),
            db=session,
        )
        return DiffSchema(**diff.serializer())
