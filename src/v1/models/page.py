# Standard Library
import uuid
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger
from database.base import Page
from schemas import PageCreateSchema, PageUpdateSchema, Status
from sqlalchemy.orm.session import Session
from views.console import log_function_execution

logger = Logger("PageORM")


class PageORM(object):

    @log_function_execution(logger=logger)
    def find_all(self, db: Session) -> List[Page]:
        return db.query(Page).all()

    @log_function_execution(logger=logger)
    def find_one(self, db: Session, page_id: str) -> Page:
        return db.query(Page).filter(Page.id == page_id).one()

    @log_function_execution(logger=logger)
    def find_one_or_404(self, db: Session, page_id: str) -> Page | None:
        return db.query(Page).filter(Page.id == page_id).first()

    @log_function_execution(logger=logger)
    def find_many_by_version_id(self, db: Session, version_id: str) -> List[Page]:
        return db.query(Page).filter(Page.version_id == version_id).all()

    @log_function_execution(logger=logger)
    def pdf_page_not_found(self, db: Session, version_id: str, page_index: str) -> bool:
        """Check if the page exists in the database.

        Args:
            db (Session): Session
            version_id (str): version id
            page_index (str): index of the page

        Returns:
            bool: if the page does not exist in the database return True else False
        """
        page = (
            db.query(Page).filter(Page.version_id == version_id, Page.index == page_index).first()
        )
        if not page:
            return True
        return False

    @log_function_execution(logger=logger)
    def update_status(self, db: Session, page_id: str, status: str) -> Page:
        page = self.find_one(db, page_id)
        page.status = status
        db.add(page)
        return page

    @log_function_execution(logger=logger)
    def exists(self, db: Session, page_id: str) -> bool:
        page = db.query(Page).filter(Page.id == page_id).first()
        if page:
            return True
        return False

    @log_function_execution(logger=logger)
    def create_one(self, db: Session, page_data: PageCreateSchema) -> Page:
        created_page = Page(**page_data.model_dump())
        db.add(created_page)
        return created_page

    @log_function_execution(logger=logger)
    def update_one(self, db: Session, page_id: str, page_data: PageUpdateSchema) -> Page:
        selected_page = self.find_one(db, page_id)
        selected_page.status = page_data.status
        db.add(selected_page)
        return selected_page

    @log_function_execution(logger=logger)
    def delete_one(self, db: Session, page_id: str) -> bool:
        if not self.exists(db, page_id):
            return False
        db.query(Page).filter(Page.id == page_id).delete()
        return True

    @log_function_execution(logger=logger)
    def find_page_by_index(self, db: Session, version_id: str, index: int) -> Page:
        selected_page = (
            db.query(Page).filter(Page.version_id == version_id, Page.index == index).first()
        )
        if selected_page:
            return selected_page
        else:
            created_page = Page(
                id=str(uuid.uuid4()).replace("-", ""),
                version_id=version_id,
                index=index,
                status=Status.preprocessing.value,
            )
            db.add(created_page)
            return created_page
