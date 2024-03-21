# Standard Library
import uuid
from typing import List

# Third Party Library
from database.base import Version
from models.project import ProjectORM
from schemas.version import VersionUpdateSchema
from sqlalchemy.orm.session import Session


class VersionORM(object):

    projects = ProjectORM()

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

    def create_one(self, db: Session, project_id: str) -> Version:
        id = str(uuid.uuid4()).replace("-", "")
        versions = self.find_many_by_project_id(db, project_id)
        version_number = len(versions) + 1
        title = f"V{version_number}"
        created_version = Version(
            id=id,
            title=title,
            description="",
            project_id=project_id,
            object_key=f"{id}/{title}.pdf",
        )
        db.add(created_version)
        return created_version

    def update_one(
        self, db: Session, version_id: str, version_data: VersionUpdateSchema
    ) -> Version:
        updated_version = self.find_one(db, version_id)
        updated_version.title = version_data.title
        updated_version.description = version_data.description
        db.add(updated_version)
        return updated_version

    def update_thumbnail(self, db: Session, version_id: str, thumbnail: str) -> Version:
        updated_pdf = self.find_one(db, version_id)
        updated_pdf.thumbnail = thumbnail
        db.add(updated_pdf)
        return updated_pdf

    def delete_one(self, db: Session, version_id: str) -> None:
        deleted_pdf = self.find_one(db=db, version_id=version_id)
        db.delete(deleted_pdf)
        return None
