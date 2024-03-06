# Third Party Library
from aws_lambda_powertools import Logger
from database.session import with_session
from models.image import ImageORM
from models.json import JsonORM
from models.page import PageORM
from schemas import ImageCreateSchema, JsonCreateSchema, PageCreateSchema, PageSchema, Status
from sqlalchemy.orm.session import Session

logger = Logger()


class PageController:
    pages = PageORM()
    images = ImageORM()
    jsons = JsonORM()

    @with_session
    def find_all_pages(self, session: Session) -> list[PageSchema]:
        pages = self.pages.find_all(session)
        return [PageSchema(**page.serializer()) for page in pages]

    @with_session
    def bulk_insert_pages(self, pages: list[dict], session: Session) -> None:
        for page in pages:
            created_page = self.pages.create_one(
                db=session,
                page=PageCreateSchema(
                    version_id=page["version_id"],
                    local_index=page["local_index"],
                    status=Status.preprocessed,
                ),
            )
            created_json = self.jsons.create_one(
                db=session,
                json=JsonCreateSchema(
                    object_key=page["json"]["object_key"],
                    page_id=created_page.id,
                    status=Status(page["json"]["status"]),
                ),
            )
            created_image = self.images.create_one(
                db=session,
                image=ImageCreateSchema(
                    object_key=page["image"]["object_key"],
                    page_id=created_page.id,
                    status=Status(page["image"]["status"]),
                ),
            )
            logger.info(created_page, created_json, created_image)
