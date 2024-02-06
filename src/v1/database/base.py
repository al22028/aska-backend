# Standard Library
from datetime import datetime

# Third Party Library
from config.settings import AWS_RDS_DATABASE_URL, SQLALCHEMY_ECHO_SQL
from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.orm import declarative_base

Engine = create_engine(AWS_RDS_DATABASE_URL, echo=SQLALCHEMY_ECHO_SQL)
Base = declarative_base()


class TimestampMixin(object):
    """Timestamp Mixin"""

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String(256), nullable=False, unique=True)
    name = Column(String(256), nullable=False)

    def __init__(
        self,
        id: str,
        name: str,
        email: str,
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"<User id={self.id}, name={self.name}, email={self.email}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String(256), nullable=False)
    team_id = Column(String, nullable=False)

    def __init__(
        self,
        id: str,
        name: str,
        team_id: str,
    ) -> None:
        self.id = id
        self.name = name
        self.team_id = team_id
        self.is_deleted = False
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"<Project id={self.id}, name={self.name}, team_id={self.team_id}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "teamId": self.team_id,
            "isDeleted": self.is_deleted,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }
