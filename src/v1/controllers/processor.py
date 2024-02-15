# Standard Library
import json

# Third Party Library
from aws.lambda_client import LambdaClient
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import S3Event
from models.image import ImageORM
from models.json import JsonORM
from models.page import PageORM
from models.version import VersionORM
from schemas import LambdaInvokePayload

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
        # self._version_id, self._page_index = self.parse_object_key()
        # self._version = self.find_version()
        # self._page = self.find_page()

    # @with_session
    # def find_version(self, session: Session) -> Version:
    #     self._version = self.versions.find_one(db=session, version_id=self._version_id)
    #     return self._version

    # @with_session
    # def find_page(self, session: Session) -> Page:
    #     self._page = self.pages.find_page_by_index(
    #         db=session, version_id=self._version_id, page_index=self._page_index
    #     )
    #     return self._page

    def parse_object_key(self) -> tuple[str, int]:
        """Parse object key to get version id and page index

        Returns:
            tuple[str, int]: version id and page index
        """
        version_id, file_name = self._object_key.split("/")
        page_index = int(file_name.split(".")[0])
        return version_id, page_index

    # @with_session
    # def create_json(self, session: Session) -> Json:
    #     json_data = JsonCreateSchema(page_id=self._page.id, status=Status.pending)  # type: ignore
    #     self._json = self.jsons.create_one(db=session, json_data=json_data)
    #     return self._json

    def find_matching(self) -> None:
        # マッチングを取得 or 作成処理
        pass


class JsonProcessor(Processor):
    def __init__(self, event: S3Event) -> None:
        super().__init__(event)

    def calculate_matching_score(self, target_json_object_key: str) -> None:
        """Calculate matching score

        Args:
            target_json_object_key (str): target json object key

        Returns:
            _type_: _description_
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

    # @with_session
    # def create_json(self, session: Session) -> Json:
    #     json_data = JsonCreateSchema(page_id=self._page.id, status=Status.pending)  # type: ignore
    #     self._json = self.jsons.create_one(db=session, json_data=json_data)
    #     return self._json


class ImageProcessor(Processor):

    def __init__(self, event: S3Event) -> None:
        super().__init__(event)

    # @with_session
    # def create_image(self, session: Session) -> Image:
    #     image_data = ImageCreateSchema(page_id=self._page.id, status=Status.pending)  # type: ignore
    #     self._image = self.images.create_one(db=session, image_data=image_data)
    #     return self._image


def calculate_matching_score(event: S3Event) -> None:
    json_processor = JsonProcessor(event)
    json_processor.calculate_matching_score(target_json_object_key="id231321/1.json")
