# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from controllers.project import ProjectController
from schemas.common import DeletedSchema
from schemas.project import (
    ProjectCreateSchema,
    ProjectDetailSchema,
    ProjectSchema,
    ProjectUpdateSchema,
)

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()


controller = ProjectController()


@router.get(
    "/",
    tags=["Project"],
    summary="全てのプロジェクトを取得",
    description="全てのプロジェクトを取得します。",
    response_description="全プロジェクト",
    operation_id="fetchAllProjects",
)
def fetch_all_projects() -> List[ProjectSchema]:
    return controller.fetch_all_projects()


@router.get(
    "/<projectId>",
    tags=["Project"],
    summary="プロジェクト詳細の取得",
    description="特定のプロジェクトの詳細情報を取得します。",
    response_description="プロジェクト詳細",
    operation_id="fetchSingleProjectById",
    responses={200: {"description": "プロジェクト詳細"}, 404: {"description": "Not found"}},
)
def fetch_project(projectId: str) -> ProjectDetailSchema:
    return controller.find_one_or_404(project_id=projectId)


@router.post(
    "/",
    tags=["Project"],
    summary="新規プロジェクトの追加",
    description="新規にプロジェクトを追加します。",
    response_description="新規作成されたプロジェクト",
    operation_id="createSingleProject",
    responses={
        201: {"description": "新規作成されたプロジェクトの詳細"},
        422: {"description": "Validation Error"},
    },
)
def create_project(project: ProjectCreateSchema) -> ProjectDetailSchema:
    created_project, status_code = controller.create_one(project_data=project)
    return created_project, status_code  # type: ignore


@router.put(
    "/<projectId>",
    tags=["Project"],
    summary="プロジェクトの更新",
    description="特定のプロジェクトを更新します。更新できるのはtitle, description, thumbnailだけです。",
    response_description="更新されたプロジェクトの詳細",
    operation_id="updateSingleProjectById",
    responses={
        200: {"description": "更新されたプロジェクトの詳細"},
        400: {"description": "Bad Request"},
        404: {"description": "Project Not Found"},
    },
)
def update_project(projectId: str, project: ProjectUpdateSchema) -> ProjectDetailSchema:
    updated_project = controller.update_one(project_id=projectId, project_data=project)
    return updated_project


@router.delete(
    "/<projectId>",
    tags=["Project"],
    summary="プロジェクトの削除",
    description="特定のプロジェクトを削除します。",
    response_description="削除されたプロジェクト",
    operation_id="deleteSingleProjectById",
    responses={
        204: {"description": "削除されたプロジェクト"},
        404: {"description": "Project Not Found"},
    },
)
def delete_project(projectId: str) -> DeletedSchema:
    delete_project, status_code = controller.delete_one(project_id=projectId)
    return delete_project, status_code  # type: ignore
