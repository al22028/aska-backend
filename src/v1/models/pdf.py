# Standard Library
import uuid
from typing import List

# Third Party Library
from database.base import Pdf
from schemas import PdfCreateSchema, PdfUpdateSchema
from sqlalchemy.orm.session import Session


class PdfORM(object):

    def find_all(self, db: Session) -> List[Pdf]:
        return db.query(Pdf).all()

    def find_one(self, db: Session, pdf_id: str) -> Pdf:
        return db.query(Pdf).filter(Pdf.id == pdf_id).one()

    def find_many_by_project_id(self, db: Session, project_id: str) -> List[Pdf]:
        return db.query(Pdf).filter(Pdf.project_id == project_id).all()

    def exists(self, db: Session, pdf_id: str) -> bool:
        user = db.query(Pdf).filter(Pdf.id == pdf_id).first()
        if user:
            return True
        return False

    def create_one(self, db: Session, pdf_data: PdfCreateSchema) -> Pdf:
        id = str(uuid.uuid4()).replace("-", "")
        created_pdf = Pdf(
            **pdf_data.model_dump(),
            id=id,
            object_key=f'{id}/{pdf_data.title.replace(" ", "_")}.pdf',
        )
        db.add(created_pdf)
        return created_pdf

    def update_one(self, db: Session, pdf_id: str, pdf_data: PdfUpdateSchema) -> Pdf:
        updated_pdf = self.find_one(db, pdf_id)
        updated_pdf.title = pdf_data.title
        updated_pdf.description = pdf_data.description
        db.add(updated_pdf)
        return updated_pdf

    def delete_one(self, db: Session, pdf_id: str) -> None:
        deleted_pdf = self.find_one(db, pdf_id)
        db.delete(deleted_pdf)
        return None
