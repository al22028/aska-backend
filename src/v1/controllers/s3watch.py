# Third Party Library
from aws.s3 import S3
from aws_lambda_powertools.utilities.data_classes import S3Event
from database.session import with_session
from models.page import PageORM
from schemas import PageCreateSchema, Status
from sqlalchemy.orm.session import Session


class WatchController:
    client = S3()
    pages = PageORM()

    def __init__(self, event: S3Event) -> None:
        self.event = event
        self._bucket_name = self.event.bucket_name
        self._object_key = self.event.object_key
        self.version_id, self.page_index = self.parse_object_key()
        if self.pages.pdf_page_not_found(version_id=self.version_id, page_index=self.page_index):
            self.create_page()

    def parse_object_key(self) -> tuple[str, int]:
        """Parse the object key to get the version_id and page_index

        Returns:
            tuple[str, str]: version_id, page_index
        """
        version_id, file_name = self._object_key.split("/")
        page_index = int(file_name.split(".")[0])
        return version_id, page_index

    @with_session
    def create_page(self, session: Session) -> None:
        """Create a page in the database"""
        page_data = PageCreateSchema(
            version_id=self.version_id,
            index=self.page_index,
            status=Status.pending,
        )
        self.pages.create_one(db=session, page_data=page_data)
