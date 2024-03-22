# Standard Library
import io
import json
import math
import os
from enum import Enum
from typing import TypeVar

# Third Party Library
import boto3
import cv2
import numpy as np
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import S3Event, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext
from pdf2image import convert_from_bytes
from PIL import Image
from pydantic import BaseModel

logger = Logger()


AWS_IMAGE_BUCKET = os.environ["AWS_IMAGE_BUCKET"]


lambda_client = boto3.client("lambda")

T = TypeVar("T")

IMAGE_HEIGHT = 1000


class Status(Enum):
    """Status Enum"""

    pending = "PENDING"  # 待機状態
    preprocessing = "PREPROCESSING"  # 前処理中
    preprocessed = "PREPROCESSED"  # 前処理完了
    preprocessing_timedout = "PREPROCESSING_TIMEDOUT"  # 前処理タイムアウト
    preprocessing_failed = "PREPROCESSING_FAILED"  # 前処理失敗


class JsonSchema(BaseModel):
    object_key: str
    status: str


class ImageSchema(BaseModel):
    object_key: str
    status: str
    original_object_key: str


class Payload(BaseModel):
    version_id: str
    local_index: int
    # FIXME: lint error
    json: JsonSchema  # type: ignore
    image: ImageSchema


class S3:
    client = boto3.client("s3")

    def __init__(self, bucket_name: str):
        self._bucket_name = bucket_name

    def get_object(self, object_key: str) -> dict:
        response = self.client.get_object(Bucket=self._bucket_name, Key=object_key)
        return json.loads(response["Body"].read())

    def put_object(self, object_key: str, body: bytes) -> None:
        self.client.put_object(Bucket=self._bucket_name, Key=object_key, Body=body)

    def upload_image_from_buffer(self, image_data: Image.Image, object_key: str) -> None:
        image_buffer = io.BytesIO()
        image_data.save(image_buffer, format="PNG")
        image_buffer.seek(0)
        self.client.upload_fileobj(
            Fileobj=image_buffer,
            Bucket=self._bucket_name,
            Key=object_key,
            ExtraArgs={"ContentType": "image/png"},
        )


s3 = S3(AWS_IMAGE_BUCKET)


# TODO: Refactor this function to use AWS Lambda Powertools
def extract_feature_points(img: np.ndarray) -> dict:
    """
    1枚の画像から特徴点を抽出する関数

    Args:
      img (ndarray): 画像のndarray形式データ

    Return:
      list:
        list[0] (cv2.Keypoint): 特徴点の座標等のデータのtuple
        list[1]               : 1つの特徴点に対する特徴量記述子のデータのリスト
    """
    detector = cv2.AKAZE_create()  # type: ignore

    kp, desc = detector.detectAndCompute(img, None)
    kpt = []
    # keypointをシリアライズ化してリストに格納
    kpt = [keypoint_serializer(k) for k in kp]
    res = {"keypoints": kpt, "descriptors": desc.tolist()}
    return res


def keypoint_serializer(kp: cv2.KeyPoint) -> dict:
    """
    JSONでデータを扱いたいため、cv2.Keypointをjsonにdumpsできる形にdecodeする
    1つのcv2.Keypointからパラメータ x,y,size,angle,response,octave,calss_idを取りだす
    取り出したパラメータを辞書型にして返す

    Args:
      kp (cv2.KeyPoint) : デコードするcv2.KeyPoint型のデータ

    Return:
      dict : cv2.KeyPointのパラメータを持った辞書
    """

    # TODO: パラメータを削った後のファイルサイズを確認してから検討
    return {
        "x": float(kp.pt[0]),
        "y": float(kp.pt[1]),
        "size": float(kp.size),
        "angle": float(kp.angle),
        "response": float(kp.response),
        "octave": int(kp.octave),
        "class_id": int(kp.class_id),
    }


def invoke_lambda(payloads: list[Payload]) -> None:
    logger.info(payloads)
    dict_payloads = [payload.model_dump() for payload in payloads]
    response = lambda_client.invoke(
        FunctionName="aska-api-dev-InvokedLambdaHandler",
        InvocationType="RequestResponse",
        Payload=json.dumps(dict_payloads).encode(),
    )
    logger.info(response["Payload"].read().decode("utf-8"))


def replace_red_with_white(img: Image) -> Image:
    pil_image = np.array(img)
    hsv = cv2.cvtColor(pil_image, cv2.COLOR_RGB2HSV)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    # TODO : Type check
    mask = mask1 + mask2  # type: ignore
    pil_image[mask != 0] = [255, 255, 255]
    pil_image = Image.fromarray(pil_image)
    return pil_image


def convert_to_images(version_id: str, pdf_file_data: bytes) -> None:
    images = convert_from_bytes(pdf_file_data)
    payloads: list[Payload] = []
    for i, image in enumerate(images):
        rw_image = replace_red_with_white(image)
        img = np.array(rw_image)
        serialized_keypoints = extract_feature_points(img)
        json_object_key = f"{version_id}/{i+1}.json"
        s3.put_object(json_object_key, json.dumps(serialized_keypoints).encode())

        original_image_object_key = f"{version_id}/original_{i+1}.png"
        resized_image_object_key = f"{version_id}/{i+1}.png"

        original_image = image.copy()
        # NOTE:  width, height
        size = (int(IMAGE_HEIGHT * math.sqrt(2)), IMAGE_HEIGHT)
        resized_image = image.resize(size)

        s3.upload_image_from_buffer(original_image, original_image_object_key)
        s3.upload_image_from_buffer(resized_image, resized_image_object_key)

        json_params = JsonSchema(object_key=json_object_key, status=Status.preprocessed.value)

        image_params = ImageSchema(
            object_key=resized_image_object_key,
            status=Status.preprocessed.value,
            original_object_key=original_image_object_key,
        )

        params = Payload(
            version_id=version_id, local_index=i + 1, json=json_params, image=image_params
        )
        payloads.append(params)
    invoke_lambda(payloads)


@event_source(data_class=S3Event)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: S3Event, context: LambdaContext) -> dict:
    logger.info(event)
    bucket_name = event.bucket_name
    object_key = event.object_key
    version_id, _ = object_key.split("/")
    response = boto3.client("s3").get_object(Bucket=bucket_name, Key=object_key)
    pdf_file_data = response["Body"].read()
    convert_to_images(version_id, pdf_file_data)
    return {"statusCode": 200, "body": json.dumps({"message": "Converted PDF to Images"})}
