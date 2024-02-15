# Third Party Library
from database.session import with_session
from models.page import PageORM
from schemas import PageSchema
from sqlalchemy.orm.session import Session


class PageController:
    pages = PageORM()

    @with_session
    def find_all_pages(self, session: Session) -> list[PageSchema]:
        pages = self.pages.find_all(session)
        return [PageSchema(**page.serializer()) for page in pages]
