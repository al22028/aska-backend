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
