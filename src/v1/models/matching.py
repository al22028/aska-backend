# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger
from database.base import Matching
from sqlalchemy.orm.session import Session
from views.console import log_function_execution
from schemas.diff import DiffCreateSchema

logger = Logger("MatchinORM")


class MatchinORM(object):

    @log_function_execution(logger=logger)
    def find_all(self, db: Session) -> List[Matching]:
        return db.query(Matching).all()

    @log_function_execution(logger=logger)
    def find_by_ids(self, image1_id: str, image2_id: str, db: Session) -> Matching:
        matching = (
            db.query(Matching)
            .filter(Matching.image1_id == image1_id, Matching.image2_id == image2_id)
            .first()
        )
        if matching:
            return matching
        else:
            return (
                db.query(Matching)
                .filter(Matching.image2_id == image1_id, Matching.image1_id == image2_id)
                .one()
            )

    @log_function_execution(logger=logger)
    def create_one(self, diff_data: DiffCreateSchema, db: Session):
        matching = Matching(**diff_data.model_dump())
        db.add(matching)
        return matching
