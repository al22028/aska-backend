# Third Party Library
from aws_lambda_powertools import Logger
from database.session import with_session
from models.image import ImageORM
from models.json import JsonORM
from models.matching import MatchinORM
from models.page import PageORM
from models.version import VersionORM
from schemas.diff import DiffCreateSchema, DiffSchema
from sqlalchemy.orm.session import Session

logger = Logger("DiffController")


class DiffController:
    pages = PageORM()
    images = ImageORM()
    jsons = JsonORM()
    versions = VersionORM()
    matchings = MatchinORM()

    @with_session
    def find_all(self, session: Session) -> list[DiffSchema]:
        diffs = self.matchings.find_all(session)
        return [DiffSchema(**diff.serializer()) for diff in diffs]

    @with_session
    def find_by_ids(self, image1_id: str, image2_id: str, session: Session) -> DiffSchema:
        diff = self.matchings.find_by_ids(image1_id=image1_id, image2_id=image2_id, db=session)
        return DiffSchema(**diff.serializer())

    @with_session
    def create_one(self, diff_data: DiffCreateSchema, session: Session) -> DiffSchema:
        diff = self.matchings.create_one(diff_data=diff_data, db=session)
        return DiffSchema(**diff.serializer())
