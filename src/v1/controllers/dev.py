# Standard Library
import json
import time

# Third Party Library
import boto3
from aws.lambda_client import LambdaClient
from aws_lambda_powertools import Logger
from config.settings import AWS_IMAGE_BUCKET, AWS_TMP_BUCKET
from database.base import Page
from database.session import with_session
from models.image import ImageORM
from models.json import JsonORM
from models.matching import MatchinORM
from models.page import PageORM
from models.user import UserORM
from models.version import VersionORM
from schemas.common import DeletedSchema
from schemas.diff import DiffCreateSchema, DiffSchema
from schemas.status import Status
from sqlalchemy.orm.session import Session

logger = Logger("DevController")

# TODO: PARAMSをschemaに変更する
PARAMS = {
    "match_threshold": 0.85,
    "threshold": 220,
    "eps": 20,
    "min_samples": 50,
}


class DevController:
    pages = PageORM()
    users = UserORM()
    images = ImageORM()
    jsons = JsonORM()
    versions = VersionORM()
    matchings = MatchinORM()
    lambda_client = LambdaClient()
    s3 = boto3.client("s3")
    lambda_client = boto3.client("lambda")

    def get_object_body(self, bucket: str, key: str) -> str:
        response = self.s3.get_object(Bucket=bucket, Key=key)
        return response["Body"].read().decode("utf-8")

    def calculate_macthing_score(self, page1: Page, page2: Page) -> float:
        payload = {
            "body": {
                "bucket_name": AWS_IMAGE_BUCKET,
                "before": {
                    "json_object_key": page1.json.object_key,
                },
                "after": {
                    "json_object_key": page2.json.object_key,
                },
            }
        }
        response = self.lambda_client.invoke(
            FunctionName="aska-api-dev-MatchingCalculateHandler",
            InvocationType="RequestResponse",
            LogType="Tail",
            Payload=bytes(json.dumps(payload).encode()),
        )
        logger.info(response)
        body = json.loads(response["Payload"].read().decode("utf-8"))
        logger.info(body)
        return body["score"]

    def calculate_bouding_boxes(self, page1: Page, page2: Page, params: dict = PARAMS) -> dict:
        # TODO: payloadをschemaに変更する
        payload = {
            "body": {
                "bucket_name": AWS_IMAGE_BUCKET,
                "before": {
                    "json_object_key": page1.json.object_key,
                    "image_object_key": page1.image.object_key,
                },
                "after": {
                    "json_object_key": page2.json.object_key,
                    "image_object_key": page2.image.object_key,
                },
                "params": params,
                "is_dev": True,
            }
        }
        response = self.lambda_client.invoke(
            FunctionName="aska-api-dev-ImageDiffHandler",
            InvocationType="RequestResponse",
            LogType="Tail",
            Payload=bytes(json.dumps(payload).encode()),
        )
        logger.info(response)
        response = response["Payload"].read().decode("utf-8")
        object_key = json.loads(json.loads(response)["body"])["objectKey"]
        file_body = self.get_object_body(bucket=AWS_TMP_BUCKET, key=object_key)
        body = json.loads(file_body)
        time.sleep(1)
        logger.info(body)
        return body

    @with_session
    def create_image_diff(self, session: Session, image1_id: str, image2_id: str) -> dict:
        image1 = self.images.find_one(db=session, image_id=image1_id)
        image2 = self.images.find_one(db=session, image_id=image2_id)
        page1 = self.pages.find_one(db=session, page_id=image1.page_id)
        page2 = self.pages.find_one(db=session, page_id=image2.page_id)
        score = self.calculate_macthing_score(page1, page2)
        logger.info(f"Matching score: {score}")
        bounding_boxes = self.calculate_bouding_boxes(page1, page2)
        logger.info(f"Bounding boxes: {bounding_boxes}")
        diff = self.matchings.create_one(
            diff_data=DiffCreateSchema(
                image1_id=image1.id,
                image2_id=image2.id,
                score=score,
                status=Status.preprocessed,
                params=PARAMS,
                bounding_boxes=bounding_boxes,
            ),
            db=session,
        )
        return DiffSchema(**diff.serializer())

    @with_session
    def delete_single_user(self, session: Session, user_id: str) -> DeletedSchema:
        user = self.users.find_one(db=session, user_id=user_id)
        self.users.delete_one(db=session, user_id=user.id)
        return DeletedSchema(message="User deleted")
