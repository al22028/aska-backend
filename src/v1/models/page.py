# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger
from database.base import Page
from schemas import PageCreateSchema
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
    def find_many_by_pdf_id(self, db: Session, pdf_id: str) -> List[Page]:
        return db.query(Page).filter(Page.pdf_id == pdf_id).all()

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
