# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from database.base import Pdf
from database.session import with_session
from models.pdf import PdfORM
from schemas import PdfCreateSchema, PdfSchema
from sqlalchemy.orm.session import Session


class ProjectController:

    pdfs = PdfORM()

    @with_session
    def fetch_all_pdfs(self, session: Session) -> list[PdfSchema]:
        pdfs: List[Pdf] = self.pdfs.find_all(db=session)
        return [PdfSchema(**pdf.serializer()) for pdf in pdfs]

    @with_session
    def create_one(self, session: Session, pdf_data: PdfCreateSchema) -> tuple[PdfSchema, int]:
        pdf = self.pdfs.create_one(db=session, pdf_data=pdf_data)
        return PdfSchema(**pdf.serializer()), HTTPStatus.CREATED.value
