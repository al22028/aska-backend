# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from database.base import Project
from database.session import with_session
from models.project import ProjectORM
from schemas import ProjectCreateSchema, ProjectSchema, ProjectUpdateSchema
from sqlalchemy.orm.session import Session


class ProjectController:

    projects = ProjectORM()

    @with_session
    def fetch_all_projects(self, session: Session) -> list[ProjectSchema]:
        projects: List[Project] = self.projects.find_all(db=session)
        return [ProjectSchema(**project.serializer()) for project in projects]

    @with_session
    def create_one(
        self, session: Session, project_data: ProjectCreateSchema
    ) -> tuple[ProjectSchema, int]:
        project = self.projects.create_one(db=session, project_data=project_data)
        return ProjectSchema(**project.serializer()), HTTPStatus.CREATED.value

    @with_session
    def find_one(self, session: Session, project_id: str) -> ProjectSchema:
        project = self.projects.find_one(db=session, project_id=project_id)
        return ProjectSchema(**project.serializer())

    @with_session
    def find_one_or_404(self, session: Session, project_id: str) -> ProjectSchema:
        if not self.projects.exists(db=session, project_id=project_id):
            raise NotFoundError
        project = self.projects.find_one(db=session, project_id=project_id)
        return ProjectSchema(**project.serializer())

    @with_session
    def update_one(
        self, session: Session, project_id: str, project_data: ProjectUpdateSchema
    ) -> ProjectSchema:
        if not self.projects.exists(db=session, project_id=project_id):
            raise NotFoundError
        project = self.projects.update_one(
            db=session, project_id=project_id, project_data=project_data
        )
        return ProjectSchema(**project.serializer())

    @with_session
    def delete_one(self, session: Session, project_id: str) -> None:
        if not self.projects.exists(db=session, project_id=project_id):
            raise NotFoundError
        self.projects.delete_one(db=session, project_id=project_id)
        return None
