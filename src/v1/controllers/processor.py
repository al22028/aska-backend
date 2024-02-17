# Standard Library
import json

# Third Party Library
from aws.lambda_client import LambdaClient
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import S3Event
from database.base import Image, Json, Page, Version
from database.session import session_maker, with_session
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

    def __init__(self, event: S3Event) -> None:
        self._event = event
        self._bucket_name = event.bucket_name
        self._object_key = event.object_key
        self._version_id, self._page_index = self.parse_object_key()
        self._session: Session = session_maker()

    def __del__(self) -> None:
        self._session.close()

    def parse_object_key(self) -> tuple[str, int]:
        """Parse object key to get version id and page index

        Returns:
            tuple[str, int]: version id and page index
        """
        version_id, file_name = self._object_key.split("/")
        page_index = int(file_name.split(".")[0])
        return version_id, page_index

    @log_function_execution(logger=logger)
    def find_version(self) -> Version:
        version = self.versions.find_one(db=self._session, version_id=self._version_id)
        self._session.commit()
        return version

    @log_function_execution(logger=logger)
    def find_previous_version(self) -> Version | None:
        version = self.find_version()
        previous_verson = self.versions.find_previous_version(
            db=self._session, project_id=version.project_id  # type: ignore
        )
        self._session.commit()
        return previous_verson

    @log_function_execution(logger=logger)
    def find_target_pages(self) -> list[Page]:
        previous_version = self.find_previous_version()
        if previous_version is None:
            return []
        else:
            target_pages = self.pages.find_many_by_version_id(
                db=self._session, version_id=previous_version.id  # type: ignore
            )
            self._session.commit()
            return target_pages

    @log_function_execution(logger=logger)
    def find_page(self) -> Page:
        selected_page = self.pages.find_page_by_index(
            db=self._session, version_id=self._version_id, index=self._page_index
        )
        self._session.commit()
        return selected_page

    @log_function_execution(logger=logger)
    def find_matching(self) -> None:
        pass


class JsonProcessor(Processor):
    @log_function_execution(logger=logger)
    def __init__(self, event: S3Event) -> None:
        super().__init__(event)

    @log_function_execution(logger=logger)
    def _calculate_matching_score(self, target_page: Page) -> None:
        """Calculate matching score

        Args:
            target_json_object_key (str): target json object key
        """
        self.jsons.update_status(db=self._session, json_id=target_page.json.id, status=Status.matching_calculation.value)  # type: ignore
        response, status_code = self.lambda_client.invoke(
            function_name="aska-api-dev-MatchingCalculateHandler",
            payload=LambdaInvokePayload(
                body={
                    "bucket_name": self._bucket_name,
                    "before": self._object_key,
                    "after": target_page.json.object_key,
                }
            ),
        )
        json_response = json.loads(response)
        logger.info(f'score: {json_response["score"]}, status_code: {status_code}')
        self.jsons.update_status(db=self._session, json_id=target_page.json.id, status=Status.matching_calculation_success.value)  # type: ignore

    @log_function_execution(logger=logger)
    def create_json(self) -> Json:
        selected_page = self.find_page()
        json_data = JsonCreateSchema(page_id=selected_page.id, status=Status.preprocessed.value, object_key=self._object_key)  # type: ignore
        created_json = self.jsons.create_one(db=self._session, json_data=json_data)
        self._session.commit()
        return created_json

    def calculate_matching_score_for_each_page(self) -> None:
        self.create_json()
        target_pages = self.find_target_pages()
        for target_page in target_pages:
            self._calculate_matching_score(target_page=target_page)


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
