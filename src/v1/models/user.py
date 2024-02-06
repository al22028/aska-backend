# Standard Library
from typing import List

# Third Party Library
from database.base import User
from schemas import UserCreateSchema, UserUpdateSchema
from sqlalchemy.orm.session import Session


class UserORM(object):

    def find_all(self, db: Session) -> List[User]:
        return db.query(User).all()

    def find_one(self, db: Session, user_id: str) -> User:
        return db.query(User).filter(User.id == user_id).one()

    def exists(self, db: Session, user_id: str) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return True
        return False

    def find_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create_one(self, db: Session, user_data: UserCreateSchema) -> User:
        created_user = User(**user_data.model_dump())
        db.add(created_user)
        return created_user

    def update_one(self, db: Session, user_id: str, user_data: UserUpdateSchema) -> User:
        user = self.find_one(db, user_id)
        user.name = user_data.name
        db.add(user)
        return user

    def delete_one(self, db: Session, user_id: str) -> None:
        user = self.find_one(db, user_id)
        db.delete(user)
        return None
