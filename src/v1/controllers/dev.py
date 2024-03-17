# Standard Library
import json
import time

# Third Party Library
import boto3
from aws.lambda_client import LambdaClient
from aws_lambda_powertools import Logger
from config.settings import AWS_IMAGE_BUCKET
from database.base import Image, Page
from database.session import with_session
from models.image import ImageORM
from models.json import JsonORM
from models.matching import MatchinORM
from models.page import PageORM
from models.version import VersionORM
from schemas.diff import DiffCreateSchema, DiffSchema
from schemas.payload import LambdaInvokePayload
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
    images = ImageORM()
    jsons = JsonORM()
    versions = VersionORM()
    matchings = MatchinORM()
    lambda_client = LambdaClient()
    s3 = boto3.client("s3")

    def get_object_body(self, bucket: str, key: str) -> str:
        response = self.s3.get_object(Bucket=bucket, Key=key)
        return response["Body"].read().decode("utf-8")

    def calculate_macthing_score(self, image1: Image, image2: Image) -> float:
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
        logger.info(response)
        body = json.loads(response["Payload"].read().decode("utf-8"))["body"]
        time.sleep(1)
        logger.info(body)
        return body["score"]

    def calculate_bouding_boxes(self, page1: Page, page2: Page, params: dict = PARAMS) -> dict:
        # TODO: payloadをschemaに変更する
        response = self.lambda_client.invoke(
            function_name="aska-api-dev-ImageDiffHandler",
            payload={
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
            },
        )
        logger.info(response)
        body = json.loads(response)["body"]
        time.sleep(1)
        logger.info(body)
        file_body = self.get_object_body(bucket=AWS_IMAGE_BUCKET, key=body["objectKey"])
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
        score = self.calculate_macthing_score(image1, image2)
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
