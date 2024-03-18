# Standard Library
import random
import string
from http import HTTPStatus
from typing import List

# Third Party Library
from aws.cognito import Cognito
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError
from database.base import User
from database.session import with_session
from models.user import UserORM
from schemas.user import UserCreateResponsSchema, UserCreateSchema, UserSchema, UserUpdateSchema
from sqlalchemy.orm.session import Session


def generate_password() -> str:
    """Generate random password

    Returns:
        str: random password
    """
    length = random.randint(8, 12)
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    # 最低1つの数字を確実に含むようにする
    password = "".join(random.choice(characters) for i in range(length - 1)) + random.choice(
        string.digits
    )

    password_list = list(password)
    random.shuffle(password_list)
    password = "".join(password_list)

    return password


class UserController:
    cognito = Cognito()

    users = UserORM()

    @with_session
    def fetch_all_users(self, session: Session) -> list[UserSchema]:
        users: List[User] = self.users.find_all(db=session)
        return [UserSchema(**user.serializer()) for user in users]

    @with_session
    def create_one(
        self, session: Session, user_data: UserCreateSchema
    ) -> tuple[UserCreateResponsSchema, int]:
        if self.users.find_by_email(db=session, email=user_data.email):
            raise BadRequestError("email already in use")
        # create user in cognito
        password = generate_password()
        user_id = self.cognito.create_user(user_data.email, password)

        self.cognito.confirm_user(user_data.email, password)
        self.cognito.verify_email(user_data.email)
        # create user in database
        user = self.users.create_one(db=session, id=user_id, user_data=user_data)
        serialized_user = user.serializer()
        serialized_user["password"] = password
        return UserCreateResponsSchema(**serialized_user), HTTPStatus.CREATED.value

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
        self.cognito.delete_user(user_id)
        return None
