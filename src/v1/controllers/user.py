# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from database.base import User
from database.session import with_session
from models.user import UserORM
from schemas import UserCreateSchema, UserSchema
from sqlalchemy.orm.session import Session


class UserController:

    users = UserORM()

    @with_session
    def fetch_all_users(self, session: Session) -> list[UserSchema]:
        users: List[User] = self.users.find_all(db=session)
        return [UserSchema(**user.serializer()) for user in users]

    @with_session
    def create_one(self, session: Session, user_data: UserCreateSchema) -> tuple[UserSchema, int]:
        user = self.users.create_one(db=session, user_data=user_data)
        return UserSchema(**user.serializer()), HTTPStatus.CREATED.value

    @with_session
    def find_one(self, session: Session, user_id: str) -> UserSchema:
        user = self.users.find_one(db=session, user_id=user_id)
        return UserSchema(**user.serializer())

    @with_session
    def update_one(self, session: Session, user_id: str, user_data: UserCreateSchema) -> UserSchema:
        user = self.users.update_one(db=session, user_id=user_id, user_data=user_data)
        return UserSchema(**user.serializer())

    @with_session
    def delete_one(self, session: Session, user_id: str) -> None:
        self.users.delete_one(db=session, user_id=user_id)
        return None
