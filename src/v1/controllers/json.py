# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from aws.s3 import S3
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from config.settings import AWS_IMAGE_BUCKET
from database.base import Json
from database.session import with_session
from models.json import JsonORM
from models.page import PageORM
from schemas import (
    DeletedSchema,
    DownloadURLSchema,
    JsonCreateResponseSchema,
    JsonCreateSchema,
    JsonSchema,
    JsonUpdateSchema,
)
from sqlalchemy.orm.session import Session

s3 = S3()


class JsonController:

    jsons = JsonORM()
    pages = PageORM()

    @with_session
    def fetch_all_jsons(self, session: Session) -> list[JsonSchema]:
        jsons: List[Json] = self.jsons.find_all(db=session)
        return [JsonSchema(**json.serializer()) for json in jsons]

    @with_session
    def fetch_page_json(self, session: Session, page_id: str) -> JsonSchema:
        page = self.jsons.exists(db=session, page_id=page_id)
        if not page:
            raise NotFoundError("page not found")
        json: Json = self.jsons.find_by_page_id(db=session, page_id=page_id)
        return JsonSchema(**json.serializer())

    @with_session
    def create_one(
        self, session: Session, json_data: JsonCreateSchema
    ) -> tuple[JsonCreateResponseSchema, int]:
        json = self.jsons.create_one(db=session, json_data=json_data)
        presigned_url = s3.create_presigned_url(
            client_method="put_object",
            bucket_name=AWS_IMAGE_BUCKET,
            object_key=json.object_key,  # type: ignore
            expiration=3600,
        )
        return (
            JsonCreateResponseSchema(**json.serializer(), presigned_url=presigned_url),
            HTTPStatus.CREATED.value,
        )

    @with_session
    def find_one(self, session: Session, json_id: str) -> JsonSchema:
        if not self.jsons.exists(db=session, json_id=json_id):
            raise NotFoundError("json not found")
        json = self.jsons.find_one(db=session, json_id=json_id)
        return JsonSchema(**json.serializer())

    @with_session
    def update_one(self, session: Session, json_id: str, json_data: JsonUpdateSchema) -> JsonSchema:
        if not self.jsons.exists(db=session, json_id=json_id):
            raise NotFoundError("json not found")
        json = self.jsons.update_one(db=session, json_id=json_id, json_data=json_data)
        return JsonSchema(**json.serializer())

    @with_session
    def delete_one(self, session: Session, json_id: str) -> DeletedSchema:
        if not self.jsons.exists(db=session, json_id=json_id):
            raise NotFoundError("json not found")
        self.jsons.delete_one(db=session, json_id=json_id)
        return DeletedSchema(message="json deleted successfully")

    @with_session
    def generate_download_url(self, session: Session, json_id: str) -> DownloadURLSchema:
        if not self.jsons.exists(db=session, json_id=json_id):
            raise NotFoundError("json not found")
        json = self.jsons.find_one(db=session, json_id=json_id)
        return DownloadURLSchema(
            presigned_url=s3.create_presigned_url(
                client_method="get_object",
                bucket_name=AWS_IMAGE_BUCKET,
                object_key=json.object_key,  # type: ignore
                expiration=3600,
            )
        )
