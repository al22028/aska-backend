# Standard Library
from typing import List

# Third Party Library
from database.base import Project
from schemas import ProjectCreateSchema, ProjectUpdateSchema
from sqlalchemy.orm.session import Session


class ProjectORM(object):

    def find_all(self, db: Session) -> List[Project]:
        return db.query(Project).all()

    def find_one(self, db: Session, project_id: str) -> Project:
        return db.query(Project).filter(Project.id == project_id).one()

    def exists(self, db: Session, project_id: str) -> bool:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            return True
        return False

    def create_one(self, db: Session, project_data: ProjectCreateSchema) -> Project:
        create_project = Project(**project_data.model_dump())
        db.add(create_project)
        return create_project

    def update_one(
        self, db: Session, project_id: str, project_data: ProjectUpdateSchema
    ) -> Project:
        project = self.find_one(db, project_id)
        project.title = project_data.title
        project.description = project_data.description
        project.thumbnail = project_data.thumnail
        db.add(project)
        return project

    def delete_one(self, db: Session, project_id: str) -> None:
        project = self.find_one(db, project_id)
        db.delete(project)
        return None
