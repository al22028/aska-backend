# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from aws.s3 import S3
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from config.settings import AWS_PDF_BUCKET
from database.base import Version
from database.session import with_session
from models.page import PageORM
from models.project import ProjectORM
from models.version import VersionORM
from schemas.common import DeletedSchema, DownloadURLSchema
from schemas.page import PageSchema
from schemas.version import (
    VersionCreateResponseSchema,
    VersionDetailSchema,
    VersionSchema,
    VersionUpdateSchema,
)
from sqlalchemy.orm.session import Session

s3 = S3()


class VersionController:

    versions = VersionORM()
    projects = ProjectORM()
    pages = PageORM()

    @with_session
    def fetch_all_versions(self, session: Session) -> list[VersionSchema]:
        versions: List[Version] = self.versions.find_all(db=session)
        return [VersionSchema(**version.serializer()) for version in versions]

    @with_session
    def fetch_project_pdfs(self, session: Session, project_id: str) -> list[VersionSchema]:
        if not self.projects.exists(db=session, project_id=project_id):
            raise NotFoundError("project not found")
        versions: List[Version] = self.versions.find_many_by_project_id(
            db=session, project_id=project_id
        )
        return [VersionSchema(**version.serializer()) for version in versions]

    @with_session
    def create_one(
        self, session: Session, project_id: str
    ) -> tuple[VersionCreateResponseSchema, int]:
        if not self.projects.exists(db=session, project_id=project_id):
            raise NotFoundError("Project not found")
        version = self.versions.create_one(db=session, project_id=project_id)
        presigned_url = s3.create_presigned_url(
            client_method="put_object",
            bucket_name=AWS_PDF_BUCKET,
            object_key=version.object_key,  # type: ignore
            expiration=3600,
        )
        return (
            VersionCreateResponseSchema(**version.serializer(), presigned_url=presigned_url),
            HTTPStatus.CREATED.value,
        )

    @with_session
    def find_one(self, session: Session, version_id: str) -> VersionDetailSchema:
        if not self.versions.exists(db=session, version_id=version_id):
            raise NotFoundError("version not found")
        version = self.versions.find_one(db=session, version_id=version_id)

        page_list = self.pages.find_many_by_version_id(db=session, version_id=version_id)
        serialized_page_list = [PageSchema(**page.serializer()) for page in page_list]
        return VersionDetailSchema(**version.serializer(), pages=serialized_page_list)

    @with_session
    def update_one(
        self, session: Session, version_id: str, version_data: VersionUpdateSchema
    ) -> VersionSchema:
        if not self.versions.exists(db=session, version_id=version_id):
            raise NotFoundError("version not found")
        updated_version = self.versions.update_one(
            db=session, version_id=version_id, version_data=version_data
        )
        return VersionSchema(**updated_version.serializer())

    @with_session
    def delete_one(self, session: Session, version_id: str) -> DeletedSchema:
        if not self.versions.exists(db=session, version_id=version_id):
            raise NotFoundError("version not found")
        self.versions.delete_one(db=session, version_id=version_id)
        return DeletedSchema(message="version deleted successfully")

    @with_session
    def generate_download_url(self, session: Session, version_id: str) -> DownloadURLSchema:
        if not self.versions.exists(db=session, version_id=version_id):
            raise NotFoundError("pdf not found")
        version = self.versions.find_one(db=session, version_id=version_id)
        return DownloadURLSchema(
            presigned_url=s3.create_presigned_url(
                client_method="get_object",
                bucket_name=AWS_PDF_BUCKET,
                object_key=version.object_key,  # type: ignore
                expiration=3600,
            )
        )
