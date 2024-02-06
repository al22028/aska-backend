# Standard Library
from typing import List

# Third Party Library
import boto3
from aws_lambda_powertools import Logger
from botocore.config import Config
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.type_defs import (
    BucketTypeDef,
    CreateBucketOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    HeadObjectOutputTypeDef,
    ListBucketsOutputTypeDef,
    ListObjectsOutputTypeDef,
    ObjectTypeDef,
)

logger = Logger(service="aws_s3_client")


class S3(object):
    def __init__(self) -> None:
        self.client: S3Client = boto3.client(
            "s3",
            config=Config(signature_version="s3v4"),
            endpoint_url="https://s3.ap-northeast-1.amazonaws.com",
        )

    def list_buckets(self) -> List[BucketTypeDef]:
        """list buckets

        Returns:
            List[BucketTypeDef]: list of buckets
        """
        logger.info({"action": "list_buckets"})
        response: ListBucketsOutputTypeDef = self.client.list_buckets()
        logger.info({"response": response})
        buckets = response["Buckets"]
        return buckets

    def create_single_bucket(self, bucket_name: str) -> CreateBucketOutputTypeDef:
        """create bucket

        Args:
            bucket_name (str): bucket name

        Raises:
            BucketAlreadyExists: if bucket already exists

        Returns:
            CreateBucketOutputTypeDef: response
        """
        logger.info({"action": "create_bucket", "bucket_name": bucket_name})

        try:
            response: CreateBucketOutputTypeDef = self.client.create_bucket(Bucket=bucket_name)
            logger.info({"response": response})
        except self.client.exceptions.BucketAlreadyExists as e:
            logger.error({"error": e})
            raise e

        return response

    def delete_single_bucket(self, bucket_name: str) -> EmptyResponseMetadataTypeDef:
        """delete bucket

        Args:
            bucket_name (str): bucket name

        Raises:
            NoSuchBucket: if bucket does not exist

        Returns:
            EmptyResponseMetadataTypeDef: response
        """
        logger.info({"action": "delete_bucket", "bucket_name": bucket_name})
        try:
            response = self.client.delete_bucket(Bucket=bucket_name)
            logger.info({"response": response})
        except self.client.exceptions.NoSuchBucket as e:
            logger.error({"error": e})
            raise e
        return response

    def list_objects(self, bucket_name: str) -> List[ObjectTypeDef]:
        """list objects

        Args:
            bucket_name (str): bucket name

        Returns:
            List[ObjectTypeDef]: list of objects
        """
        logger.info({"action": "list_objects", "bucket_name": bucket_name})
        try:
            response: ListObjectsOutputTypeDef = self.client.list_objects(Bucket=bucket_name)
            logger.info({"response": response})
        except self.client.exceptions.NoSuchBucket as e:
            logger.error({"error": e})
            raise e
        objects = response["Contents"]
        return objects

    def create_presigned_url(
        self,
        bucket_name: str,
        client_method: str,
        object_key: str,
        expiration: int = 3600,
    ) -> str:
        """create presigned url

        Args:
            bucket_name (str): bucket name
            object_key (str): object name
            expiration (int, optional): expiration time. Defaults to 3600.

        Returns:
            str: presigned url
        """
        try:
            response = self.client.generate_presigned_url(
                ClientMethod=client_method,
                Params={
                    "Bucket": bucket_name,
                    "Key": object_key,
                },
                ExpiresIn=expiration,
            )
            logger.info({"response": response})
        except self.client.exceptions.NoSuchBucket as e:
            logger.error({"error": e})
            raise e
        return response

    def head_object(self, bucket_name: str, object_key: str) -> HeadObjectOutputTypeDef:
        """head object

        Args:
            bucket_name (str): bucket name
            object_key (str): object key

        Returns:
            dict: response
        """
        try:
            response = self.client.head_object(Bucket=bucket_name, Key=object_key)
            logger.info({"response": response})
        except self.client.exceptions.NoSuchBucket as e:
            logger.error({"error": e})
            raise e
        return response

    def delete_object(self, bucket_name: str, object_key: str) -> EmptyResponseMetadataTypeDef:
        """delete object

        Args:
            bucket_name (str): bucket name
            object_key (str): object key

        Returns:
            EmptyResponseMetadataTypeDef: response
        """
        try:
            response = self.client.delete_object(Bucket=bucket_name, Key=object_key)
            logger.info({"response": response})
        except self.client.exceptions.NoSuchBucket as e:
            logger.error({"error": e})
            raise e
        return response

    def fetch_object(self, bucket_name: str, object_key: str) -> bytes:
        """fetch object

        Args:
            bucket_name (str): bucket name
            object_key (str): object key

        Returns:
            bytes: object data
        """
        try:
            response = self.client.get_object(Bucket=bucket_name, Key=object_key)
            logger.info({"response": response})
        except self.client.exceptions.NoSuchBucket as e:
            logger.error({"error": e})
            raise e
        return response["Body"].read()

    def upload_object(
        self, bucket_name: str, object_key: str, data: bytes
    ) -> EmptyResponseMetadataTypeDef:
        """upload object

        Args:
            bucket_name (str): bucket name
            object_key (str): object key
            data (bytes): object data

        Returns:
            EmptyResponseMetadataTypeDef: response
        """
        try:
            response = self.client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
            logger.info({"response": response})
        except self.client.exceptions.NoSuchBucket as e:
            logger.error({"error": e})
            raise e
        return response
