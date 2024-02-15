# Standard Library
import uuid
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger
from database.base import Image, Page
from schemas import ImageCreateSchema, ImageUpdateSchema
from sqlalchemy.orm.session import Session
from views.console import log_function_execution

logger = Logger("ImageORM")


class ImageORM(object):

    @log_function_execution(logger=logger)
    def find_all(self, db: Session) -> List[Image]:
        return db.query((Image)).all()

    @log_function_execution(logger=logger)
    def find_one(self, db: Session, image_id: str) -> Image:
        return db.query((Image)).filter(Image.id == image_id).one()

    @log_function_execution(logger=logger)
    def find_one_or_404(self, db: Session, image_id: str) -> Image | None:
        return db.query((Image)).filter(Image.id == image_id).first()

    @log_function_execution(logger=logger)
    def find_by_page_id(self, db: Session, page_id: str) -> Image:
        return db.query((Image)).filter(Image.page_id == page_id).one()

    @log_function_execution(logger=logger)
    def exists(self, db: Session, image_id: str) -> bool:
        image = db.query((Image)).filter(Image.id == image_id).first()
        if image:
            return True
        return False

    @log_function_execution(logger=logger)
    def create_one(self, db: Session, image_data: ImageCreateSchema) -> Image:
        id = str(uuid.uuid4()).replace("-", "")
        page = db.query(Page).filter(Page.id == image_data.page_id).one()
        pdf_id = page.pdf_id
        page_index = page.index
        object_key = f"{pdf_id}/{page_index}.png"
        created_image = Image(
            **image_data.model_dump(),
            id=id,
            object_key=object_key,
        )
        db.add(created_image)
        return created_image

    @log_function_execution(logger=logger)
    def update_one(self, db: Session, image_id: str, image_data: ImageUpdateSchema) -> Image:
        selected_image = self.find_one(db, image_id)
        selected_image.status = image_data.status.value
        db.add(selected_image)
        return selected_image

    @log_function_execution(logger=logger)
    def delete_one(self, db: Session, image_id: str) -> bool:
        if not self.exists(db, image_id):
            return False
        db.query((Image)).filter(Image.id == image_id).delete()
        return True
