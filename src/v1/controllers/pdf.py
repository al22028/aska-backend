# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from aws.s3 import S3
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from config.settings import AWS_PDF_BUCKET
from database.base import Pdf
from database.session import with_session
from models.pdf import PdfORM
from schemas import PdfCreateResponseSchema, PdfCreateSchema, PdfSchema, PdfUpdateSchema
from sqlalchemy.orm.session import Session

s3 = S3()


class PdfController:

    pdfs = PdfORM()

    @with_session
    def fetch_all_pdfs(self, session: Session) -> list[PdfSchema]:
        pdfs: List[Pdf] = self.pdfs.find_all(db=session)
        return [PdfSchema(**pdf.serializer()) for pdf in pdfs]

    @with_session
    def create_one(
        self, session: Session, pdf_data: PdfCreateSchema
    ) -> tuple[PdfCreateResponseSchema, int]:
        pdf = self.pdfs.create_one(db=session, pdf_data=pdf_data)
        presigned_url = s3.create_presigned_url(
            client_method="put_object",
            bucket_name=AWS_PDF_BUCKET,
            object_key=pdf.title,  # type: ignore
            expiration=3600,
        )
        return (
            PdfCreateResponseSchema(**pdf.serializer(), presigned_url=presigned_url),
            HTTPStatus.CREATED.value,
        )

    @with_session
    def find_one(self, session: Session, pdf_id: str) -> PdfSchema:
        if not self.pdfs.exists(db=session, pdf_id=pdf_id):
            raise NotFoundError("pdf not found")
        pdf = self.pdfs.find_one(db=session, pdf_id=pdf_id)
        return PdfSchema(**pdf.serializer())

    @with_session
    def update_one(self, session: Session, pdf_id: str, pdf_data: PdfUpdateSchema) -> PdfSchema:
        if not self.pdfs.exists(db=session, pdf_id=pdf_id):
            raise NotFoundError("pdf not found")
        pdf = self.pdfs.update_one(db=session, pdf_id=pdf_id, pdf_data=pdf_data)
        return PdfSchema(**pdf.serializer())
