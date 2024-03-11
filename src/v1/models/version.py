# Standard Library
import uuid
from typing import List

# Third Party Library
from database.base import Version
from schemas.version import VersionCreateSchema, VersionUpdateSchema
from sqlalchemy.orm.session import Session


class VersionORM(object):

    def find_all(self, db: Session) -> List[Version]:
        return db.query(Version).all()

    def find_one(self, db: Session, version_id: str) -> Version:
        return db.query(Version).filter(Version.id == version_id).one()

    def find_previous_version(self, db: Session, project_id: str) -> Version | None:
        project_version = (
            db.query(Version)
            .filter(Version.project_id == project_id)
            .order_by(Version.created_at)
            .all()
        )
        return project_version[-2] if len(project_version) > 1 else None

    def find_many_by_project_id(self, db: Session, project_id: str) -> List[Version]:
        return db.query(Version).filter(Version.project_id == project_id).all()

    def exists(self, db: Session, version_id: str) -> bool:
        user = db.query(Version).filter(Version.id == version_id).first()
        if user:
            return True
        return False

    def create_one(self, db: Session, version_data: VersionCreateSchema) -> Version:
        id = str(uuid.uuid4()).replace("-", "")
        created_pdf = Version(
            **version_data.model_dump(),
            id=id,
            object_key=f'{id}/{version_data.title.replace(" ", "_")}.pdf',
        )
        db.add(created_pdf)
        return created_pdf

    def update_one(self, db: Session, version_id: str, pdf_data: VersionUpdateSchema) -> Version:
        updated_pdf = self.find_one(db, version_id)
        updated_pdf.title = pdf_data.title
        updated_pdf.description = pdf_data.description
        db.add(updated_pdf)
        return updated_pdf

    def update_thumbnail(self, db: Session, version_id: str, thumbnail: str) -> Version:
        updated_pdf = self.find_one(db, version_id)
        updated_pdf.thumbnail = thumbnail
        db.add(updated_pdf)
        return updated_pdf

    def delete_one(self, db: Session, version_id: str) -> None:
        deleted_pdf = self.find_one(db=db, version_id=version_id)
        db.delete(deleted_pdf)
        return None
