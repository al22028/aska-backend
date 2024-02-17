# Standard Library
import json

# Third Party Library
from aws.lambda_client import LambdaClient
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import S3Event
from database.base import Image, Json, Page, Version
from database.session import with_session
from models.image import ImageORM
from models.json import JsonORM
from models.page import PageORM
from models.version import VersionORM
from schemas import ImageCreateSchema, JsonCreateSchema, LambdaInvokePayload, Status
from sqlalchemy.orm.session import Session
from views.console import log_function_execution

logger = Logger()


class Processor:
    lambda_client = LambdaClient()
    versions = VersionORM()
    pages = PageORM()
    images = ImageORM()
    jsons = JsonORM()

    @log_function_execution(logger=logger)
    def __init__(self, event: S3Event) -> None:
        self._event = event
        self._bucket_name = event.bucket_name
        self._object_key = event.object_key
        self._version_id, self._page_index = self.parse_object_key()

    @log_function_execution(logger=logger)
    def parse_object_key(self) -> tuple[str, int]:
        """Parse object key to get version id and page index

        Returns:
            tuple[str, int]: version id and page index
        """
        version_id, file_name = self._object_key.split("/")
        page_index = int(file_name.split(".")[0])
        return version_id, page_index

    @with_session
    @log_function_execution(logger=logger)
    def find_version(self, session: Session) -> Version:
        version = self.versions.find_one(db=session, version_id=self._version_id)
        return version

    @with_session
    @log_function_execution(logger=logger)
    def find_previous_version(self, session: Session) -> Version | None:
        version = self.find_version()
        return self.versions.find_previous_version(
            db=session, project_id=version.project_id  # type: ignore
        )

    @with_session
    @log_function_execution(logger=logger)
    def find_target_pages(self, session: Session) -> list[Page]:
        previous_version = self.find_previous_version()
        if previous_version is None:
            return []
        else:
            target_pages = self.pages.find_many_by_version_id(
                db=session, version_id=previous_version.id  # type: ignore
            )
            return target_pages

    @with_session
    @log_function_execution(logger=logger)
    def find_page(self, session: Session) -> Page:
        selected_page = self.pages.find_page_by_index(
            db=session, version_id=self._version_id, index=self._page_index
        )
        return selected_page

    @log_function_execution(logger=logger)
    def find_matching(self) -> None:
        pass


class JsonProcessor(Processor):
    @log_function_execution(logger=logger)
    def __init__(self, event: S3Event) -> None:
        super().__init__(event)

    @log_function_execution(logger=logger)
    def calculate_matching_score(self, target_json_object_key: str) -> None:
        """Calculate matching score

        Args:
            target_json_object_key (str): target json object key
        """
        response, status_code = self.lambda_client.invoke(
            function_name="aska-api-dev-MatchingCalculateHandler",
            payload=LambdaInvokePayload(
                body={
                    "bucket_name": self._bucket_name,
                    "before": self._object_key,
                    "after": target_json_object_key,
                }
            ),
        )
        json_response = json.loads(response)
        logger.info(f'score: {json_response["score"]}, status_code: {status_code}')

    @with_session
    @log_function_execution(logger=logger)
    def create_json(self, session: Session) -> Json:
        selected_page = self.find_page()
        json_data = JsonCreateSchema(page_id=selected_page.id, status=Status.preprocessed.value, object_key=self._object_key)  # type: ignore
        created_json = self.jsons.create_one(db=session, json_data=json_data)
        return created_json


class ImageProcessor(Processor):

    def __init__(self, event: S3Event) -> None:
        super().__init__(event)

    @with_session
    @log_function_execution(logger=logger)
    def create_image(self, session: Session) -> Image:
        selected_page = self.find_page()
        image_data = ImageCreateSchema(
            page_id=selected_page.id, status=Status.preprocessed.value, object_key=self._object_key  # type: ignore
        )
        created_image = self.images.create_one(db=session, image_data=image_data)
        return created_image


def calculate_matching_score(event: S3Event) -> None:
    json_processor = JsonProcessor(event)
    json_processor.create_json()
    target_pages = json_processor.find_target_pages()
    for target_page in target_pages:
        target_json_object_key = target_page.json.object_key
        json_processor.calculate_matching_score(target_json_object_key)
