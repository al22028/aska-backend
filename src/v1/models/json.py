# Standard Library
import uuid
from typing import List

# Third Party Library
from aws_lambda_powertools import Logger
from database.base import Json
from schemas import JsonCreateSchema, JsonUpdateSchema, Status
from sqlalchemy.orm.session import Session
from views.console import log_function_execution

logger = Logger("JsonORM")


class JsonORM(object):

    @log_function_execution(logger=logger)
    def find_all(self, db: Session) -> List[Json]:
        return db.query(Json).all()

    @log_function_execution(logger=logger)
    def find_one(self, db: Session, json_id: str) -> Json:
        return db.query(Json).filter(Json.id == json_id).one()

    @log_function_execution(logger=logger)
    def find_one_or_404(self, db: Session, json_id: str) -> Json | None:
        return db.query(Json).filter(Json.id == json_id).first()

    @log_function_execution(logger=logger)
    def exists(self, db: Session, json_id: str) -> bool:
        json = db.query(Json).filter(Json.id == json_id).first()
        if json:
            return True
        return False

    @log_function_execution(logger=logger)
    def create_one(self, db: Session, json_data: JsonCreateSchema) -> Json:
        id = str(uuid.uuid4()).replace("-", "")
        created_json = Json(
            **json_data.model_dump(),
            id=id,
        )
        db.add(created_json)
        return created_json

    @log_function_execution(logger=logger)
    def update_one(self, db: Session, json_id: str, json_data: JsonUpdateSchema) -> Json:
        selected_json = self.find_one(db, json_id)
        selected_json.status = json_data.status
        db.add(selected_json)
        return selected_json

    @log_function_execution(logger=logger)
    def delete_one(self, db: Session, json_id: str) -> bool:
        if not self.exists(db, json_id):
            return False
        db.query((Json)).filter(Json.id == json_id).delete()
        return True

    @log_function_execution(logger=logger)
    def find_by_page_id(self, db: Session, page_id: str) -> Json:
        return db.query(Json).filter(Json.page_id == page_id).one()

    @log_function_execution(logger=logger)
    def update_status(self, db: Session, json_id: str, status: Status) -> Json:
        json = self.find_one(db, json_id)
        json.status = status
        db.add(json)
        db.commit()
        return json
