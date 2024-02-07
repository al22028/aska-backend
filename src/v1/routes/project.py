# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.project import ProjectController
from schemas import ProjectCreateSchema, ProjectSchema, ProjectUpdateSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()


controller = ProjectController()


@router.get(
    "/",
    tags=["Project"],
    summary="Fetch All Projects",
    response_description="List of Projects",
    operation_id="fetchAllProjects",
)
def fetch_all_projects() -> List[ProjectSchema]:
    return controller.fetch_all_projects()


@router.get(
    "/<projectId>",
    tags=["Project"],
    summary="Fetch Project",
    response_description="Project",
    operation_id="fetchSingleProjectById",
)
def fetch_project(projectId: str) -> ProjectSchema:
    return controller.find_one_or_404(project_id=projectId)


@router.post(
    "/",
    tags=["Project"],
    summary="Create Project",
    response_description="Project",
    operation_id="createSingleProject",
    responses={201: {"description": "Project Created"}, 422: {"description": "Validation Error"}},
)
def create_project(project: ProjectCreateSchema) -> ProjectSchema:
    created_project, status_code = controller.create_one(project_data=project)
    return created_project, status_code  # type: ignore


@router.put(
    "/<projectId>",
    tags=["Project"],
    summary="Update Project",
    response_description="Project",
    operation_id="updateSingleProjectById",
    responses={
        200: {"description": "Project Updated"},
        400: {"description": "Bad Request"},
        404: {"description": "Project Not Found"},
    },
)
def update_project(projectId: str, project: ProjectUpdateSchema) -> ProjectSchema:
    updated_project = controller.update_one(project_id=projectId, project_data=project)
    return updated_project
