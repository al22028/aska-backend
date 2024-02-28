# Standard Library
import uuid
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger
from database.base import Matching
from schemas import MatchingCreateSchema, MatchingUpdateSchema, Status
from sqlalchemy.orm.session import Session
from views.console import log_function_execution

logger = Logger("MatchingORM")


class MatchingORM(object):

    @log_function_execution(logger=logger)
    def find_all(self, db: Session) -> List[Matching]:
        return db.query(Matching).all()

    @log_function_execution(logger=logger)
    def find_one(self, db: Session, matching_id: str) -> Matching:
        return db.query(Matching).filter(Matching.id == matching_id).one()

    @log_function_execution(logger=logger)
    def find_one_or_404(self, db: Session, matching_id: str) -> Matching | None:
        return db.query(Matching).filter(Matching.id == matching_id).first()

    @log_function_execution(logger=logger)
    def exists(self, db: Session, matching_id: str) -> bool:
        matching = db.query(Matching).filter(Matching.id == matching_id).first()
        if matching:
            return True
        return False

    @log_function_execution(logger=logger)
    def create_one(self, db: Session, mathing_data: MatchingCreateSchema) -> Matching:
        id = str(uuid.uuid4()).replace("-", "")
        created_matching = Matching(
            **mathing_data.model_dump(),
            id=id,
        )
        db.add(created_matching)
        return created_matching

    @log_function_execution(logger=logger)
    def update_one(
        self, db: Session, matching_id: str, matching_data: MatchingUpdateSchema
    ) -> Matching:
        selected_matching = self.find_one(db, matching_id)
        selected_matching.status = matching_data.status
        db.add(selected_matching)
        return selected_matching

    @log_function_execution(logger=logger)
    def update_status(self, db: Session, matching_id: str, status: Status) -> Matching:
        selected_matching = self.find_one(db, matching_id)
        selected_matching.status = status.value
        db.add(selected_matching)
        return selected_matching

    @log_function_execution(logger=logger)
    def delete_one(self, db: Session, matching_id: str) -> bool:
        if not self.exists(db, matching_id):
            return False
        db.query(Matching).filter(Matching.id == matching_id).delete()
        return True
