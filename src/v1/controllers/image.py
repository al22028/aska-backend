# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from aws.s3 import S3
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from config.settings import AWS_IMAGE_BUCKET
from database.base import Image
from database.session import with_session
from models.image import ImageORM
from models.page import PageORM
from schemas import (
    DeletedSchema,
    DownloadURLSchema,
    ImageCreateResponseSchema,
    ImageCreateSchema,
    ImageSchema,
    ImageUpdateSchema,
)
from sqlalchemy.orm.session import Session

s3 = S3()


class ImageController:

    images = ImageORM()
    pages = PageORM()

    @with_session
    def fetch_all_images(self, session: Session) -> list[ImageSchema]:
        images: List[Image] = self.images.find_all(db=session)
        return [ImageSchema(**image.serializer()) for image in images]

    @with_session
    def fetch_page_image(self, session: Session, page_id: str) -> ImageSchema:
        page = self.pages.exists(db=session, page_id=page_id)
        if not page:
            raise NotFoundError("page not found")
        image: Image = self.images.find_by_page_id(db=session, page_id=page_id)
        return ImageSchema(**image.serializer())

    @with_session
    def create_one(
        self, session: Session, image_data: ImageCreateSchema
    ) -> tuple[ImageCreateResponseSchema, int]:
        image = self.images.create_one(db=session, image_data=image_data)
        presigned_url = s3.create_presigned_url(
            client_method="put_object",
            bucket_name=AWS_IMAGE_BUCKET,
            object_key=image.object_key,  # type: ignore
            expiration=3600,
        )
        return (
            ImageCreateResponseSchema(**image.serializer(), presigned_url=presigned_url),
            HTTPStatus.CREATED.value,
        )

    @with_session
    def find_one(self, session: Session, image_id: str) -> ImageSchema:
        if not self.images.exists(db=session, image_id=image_id):
            raise NotFoundError("iamge not found")
        image = self.images.find_one(db=session, image_id=image_id)
        return ImageSchema(**image.serializer())

    @with_session
    def update_one(
        self, session: Session, image_id: str, image_data: ImageUpdateSchema
    ) -> ImageSchema:
        if not self.images.exists(db=session, image_id=image_id):
            raise NotFoundError("image not found")
        image = self.images.update_one(db=session, image_id=image_id, image_data=image_data)
        return ImageSchema(**image.serializer())

    @with_session
    def delete_one(self, session: Session, image_id: str) -> DeletedSchema:
        if not self.images.exists(db=session, image_id=image_id):
            raise NotFoundError("image not found")
        self.images.delete_one(db=session, image_id=image_id)
        return DeletedSchema(message="image deleted successfully")

    @with_session
    def generate_download_url(self, session: Session, image_id: str) -> DownloadURLSchema:
        if not self.images.exists(db=session, image_id=image_id):
            raise NotFoundError("image not found")
        image = self.images.find_one(db=session, image_id=image_id)
        return DownloadURLSchema(
            presigned_url=s3.create_presigned_url(
                client_method="get_object",
                bucket_name=AWS_IMAGE_BUCKET,
                object_key=image.object_key,  # type: ignore
                expiration=3600,
            )
        )
