# Standard Library
from http import HTTPStatus
from typing import List

# Third Party Library
from database.base import User
from database.session import with_session
from models.user import UserORM
from aws_lambda_powertools.event_handler.exceptions import NotFoundError, BadRequestError
from schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from sqlalchemy.orm.session import Session


class UserController:

    users = UserORM()

    @with_session
    def fetch_all_users(self, session: Session) -> list[UserSchema]:
        users: List[User] = self.users.find_all(db=session)
        return [UserSchema(**user.serializer()) for user in users]

    @with_session
    def create_one(self, session: Session, user_data: UserCreateSchema) -> tuple[UserSchema, int]:
        if self.users.exists(db=session, user_id=user_data.id):
            raise BadRequestError("userId already in use")
        if self.users.find_by_email(db=session, email=user_data.email):
            raise BadRequestError("email already in use")
        user = self.users.create_one(db=session, user_data=user_data)
        return UserSchema(**user.serializer()), HTTPStatus.CREATED.value

    @with_session
    def find_one(self, session: Session, user_id: str) -> UserSchema:
        user = self.users.find_one(db=session, user_id=user_id)
        return UserSchema(**user.serializer())

    @with_session
    def find_one_or_404(self, session: Session, user_id: str) -> UserSchema:
        if not self.users.exists(db=session, user_id=user_id):
            raise NotFoundError
        user = self.users.find_one(db=session, user_id=user_id)
        return UserSchema(**user.serializer())

    @with_session
    def update_one(self, session: Session, user_id: str, user_data: UserUpdateSchema) -> UserSchema:
        if not self.users.exists(db=session, user_id=user_id):
            raise NotFoundError
        user = self.users.update_one(db=session, user_id=user_id, user_data=user_data)
        return UserSchema(**user.serializer())

    @with_session
    def delete_one(self, session: Session, user_id: str) -> None:
        if not self.users.exists(db=session, user_id=user_id):
            raise NotFoundError
        self.users.delete_one(db=session, user_id=user_id)
        return None
