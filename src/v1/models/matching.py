# Standard Library
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger
from database.base import Matching
from sqlalchemy.orm.session import Session
from views.console import log_function_execution

logger = Logger("MatchinORM")


class MatchinORM(object):

    @log_function_execution(logger=logger)
    def find_all(self, db: Session) -> List[Matching]:
        return db.query(Matching).all()
