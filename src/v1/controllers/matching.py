# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from database.base import Matching
from database.session import with_session
from models.matching import MatchingORM
from schemas import MatchingCreateSchema, MatchingSchema, MatchingUpdateSchema
from sqlalchemy.orm.session import Session


class MatchingController:

    matchings = MatchingORM()

    @with_session
    def fetch_all_matchings(self, session: Session) -> list[MatchingSchema]:
        matchings: List[Matching] = self.matchings.find_all(db=session)
        return [MatchingSchema(**matching.serializer()) for matching in matchings]

    @with_session
    def create_one(
        self, session: Session, matching_data: MatchingCreateSchema
    ) -> tuple[MatchingSchema, int]:
        matching = self.matchings.create_one(db=session, matching_data=matching_data)
        return MatchingSchema(**matching.serializer()), HTTPStatus.CREATED.value

    @with_session
    def find_one(self, session: Session, matching_id: str) -> MatchingSchema:
        matching = self.matchings.find_one(db=session, matching_id=matching_id)
        return MatchingSchema(**matching.serializer())

    @with_session
    def find_one_or_404(self, session: Session, matching_id: str) -> MatchingSchema:
        if not self.matchings.exists(db=session, matching_id=matching_id):
            raise NotFoundError
        matching = self.matchings.find_one(db=session, matching_id=matching_id)
        return MatchingSchema(**matching.serializer())

    @with_session
    def update_one(
        self, session: Session, matching_id: str, matching_data: MatchingUpdateSchema
    ) -> MatchingSchema:
        if not self.matchings.exists(db=session, matching_id=matching_id):
            raise NotFoundError
        matching = self.matchings.update_one(
            db=session, matching_id=matching_id, matching_data=matching_data
        )
        return MatchingSchema(**matching.serializer())

    @with_session
    def delete_one(self, session: Session, matching_id: str) -> None:
        if not self.matchings.exists(db=session, matching_id=matching_id):
            raise NotFoundError
        self.matchings.delete_one(db=session, matching_id=matching_id)
        return None
