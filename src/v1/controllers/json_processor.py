# type: ignore

# Third Party Library
from aws.lambda_client import LambdaClient
from aws_lambda_powertools.utilities.data_classes import S3Event
from database.base import Image, Json, Page, Version
from database.session import with_session
from models.image import ImageORM
from models.json import JsonORM
from models.page import PageORM
from models.version import VersionORM
from schemas import JsonCreateSchema, LambdaInvokePayload, Status
from sqlalchemy.orm.session import Session


class JsonProcessor:

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
        # self._image = None
        # if not self._page.image:
        #     self._image = self.create_image()

    @with_session
    def find_version(self, session: Session) -> Version:
        self._version = self.versions.find_one(db=session, version_id=self._version_id)
        return self._version

    @with_session
    def find_page(self, session: Session) -> Page:
        self._page = self.pages.find_page_by_index(
            db=session, version_id=self._version_id, page_index=self._page_index
        )
        return self._page

    def parse_object_key(self) -> tuple[str, int]:
        """Parse object key to get version id and page index

        Returns:
            tuple[str, int]: version id and page index
        """
        version_id, file_name = self._object_key.split("/")
        page_index = int(file_name.split(".")[0])
        return version_id, page_index

    @with_session
    def create_json(self, session: Session) -> Json:
        json_data = JsonCreateSchema(page_id=self._page.id, status=Status.pending)  # type: ignore
        self._json = self.jsons.create_one(db=session, json_data=json_data)
        return self._json

    def find_matching(self) -> None:
        # マッチングを取得 or 作成処理
        pass

    def calculate_macthing_score(self, target_image: str) -> None:
        response = self.lambda_client.invoke(
            function_name="aska-api-dev-MatchingCalculateHandler",
            payload=LambdaInvokePayload(
                body={
                    "bucket_name": self._bucket_name,
                    "before": self._object_key,
                    "after": target_image,
                }
            ),
        )
        print(response)

    def calculate_differential(self, target_image: Image) -> None:
        # 差分計算
        pass


def calculate_matching_score(event: S3Event) -> None:
    processor = JsonProcessor(event)
    processor.calculate_macthing_score("id231321/1.json")
