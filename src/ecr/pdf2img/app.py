# Standard Library
import io
import json
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
from pydantic import BaseModel

logger = Logger()


AWS_IMAGE_BUCKET = os.environ["AWS_IMAGE_BUCKET"]


client = boto3.client("s3")
lambda_client = boto3.client("lambda")

T = TypeVar("T")


class Status(Enum):
    """Status Enum"""

    pending = "PENDING"  # 待機状態
    preprocessing = "PREPROCESSING"  # 前処理中
    preprocessed = "PREPROCESSED"  # 前処理完了
    preprocessing_timedout = "PREPROCESSING_TIMEDOUT"  # 前処理タイムアウト
    preprocessing_failed = "PREPROCESSING_FAILED"  # 前処理失敗


class JsonPayload(BaseModel):
    object_key: str
    status: Status


class ImagePayload(JsonPayload):
    pass


class LmabdaInvokePayload(BaseModel):
    version_id: str
    local_index: int
    json: JsonPayload
    image: ImagePayload


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


def invoke_lambda(payload: LmabdaInvokePayload) -> None:
    logger.info(payload)
    response = lambda_client.invoke(
        FunctionName="aska-api-dev-InvokedLambdaHandler",
        InvocationType="Event",
        Payload=payload.model_dump_json().encode(),
    )
    logger.info(response["Payload"].read().decode("utf-8"))


def convert_to_images(id: str, pdf_file_data: bytes) -> None:
    logger.info("Convert PDF to Images")
    images = convert_from_bytes(pdf_file_data)
    for i, image in enumerate(images):
        img = np.array(image)
        serialized_keypoints = extract_feature_points(img)
        json_object_key = f"{id}/{i+1}.json"
        client.put_object(
            Bucket=AWS_IMAGE_BUCKET,
            Key=json_object_key,
            Body=json.dumps(serialized_keypoints).encode(),
        )
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        image_object_key = f"{id}/{i+1}.png"
        client.upload_fileobj(
            Fileobj=buffer,
            Bucket=AWS_IMAGE_BUCKET,
            Key=image_object_key,
            ExtraArgs={"ContentType": "image/png"},
        )
        invoke_lambda(
            LmabdaInvokePayload(
                version_id=id,
                local_index=i,
                json=JsonPayload(object_key=json_object_key, status=Status.preprocessed),
                image=ImagePayload(object_key=image_object_key, status=Status.preprocessed),
            )
        )


@event_source(data_class=S3Event)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: S3Event, context: LambdaContext) -> dict:
    logger.info(event)
    bucket_name = event.bucket_name
    object_key = event.object_key
    pdf_id, _ = object_key.split("/")
    response = client.get_object(Bucket=bucket_name, Key=object_key)
    pdf_file_data = response["Body"].read()
    convert_to_images(pdf_id, pdf_file_data)
    return {"statusCode": 200, "body": json.dumps({"message": "Converted PDF to Images"})}
