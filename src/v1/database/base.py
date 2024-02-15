# Standard Library
from datetime import datetime

# Third Party Library
from config.settings import AWS_IMAGE_HOST_DOMAIN, AWS_RDS_DATABASE_URL, SQLALCHEMY_ECHO_SQL
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import Mapped, declarative_base, relationship
from sqlalchemy.types import Integer

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
        return f"<user id={self.id}, name={self.name}, email={self.email}>"

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
    title = Column(String(256), nullable=False)
    description = Column(String(512), nullable=False)

    versions: Mapped[list["Version"]] = relationship(
        "Version",
        back_populates="project",
        cascade="all, delete",
        passive_deletes=True,
        uselist=True,
    )

    def __init__(
        self,
        id: str,
        title: str,
        description: str,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"<project id={self.id}, title={self.title}, descripton={self.description}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
            "versions": [version.serializer() for version in self.versions],
        }

    def detail_serializer(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
            "versions": [version.serializer() for version in self.versions],
        }


class Version(Base, TimestampMixin):
    __tablename__ = "versions"

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(String(512), nullable=True)
    thumbnail = Column(String, nullable=False, default="default.png")
    object_key = Column(String, nullable=True)

    project: Mapped["Project"] = relationship("Project", back_populates="versions")
    pages: Mapped[list["Page"]] = relationship(
        "Page", back_populates="version", cascade="all, delete", passive_deletes=True, uselist=True
    )

    def __init__(
        self,
        id: str,
        project_id: str,
        object_key: str,
        title: str,
        description: str,
        thumbnail: str = "default.png",
    ) -> None:
        self.id = id
        self.project_id = project_id
        self.title = title
        self.thumbnail = thumbnail
        self.description = description
        self.object_key = object_key
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"<version id={self.id}, title={self.title}, object_key={self.object_key}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "projectId": self.project_id,
            "title": self.title,
            "thumbnail": AWS_IMAGE_HOST_DOMAIN + "/" + self.thumbnail,
            "description": self.description,
            "objectKey": self.object_key,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }


class Image(Base, TimestampMixin):
    __tablename__ = "images"

    id = Column(String, primary_key=True)
    page_id = Column(String, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    object_key = Column(String, nullable=False)
    status = Column(String, nullable=False)

    page: Mapped["Page"] = relationship("Page", back_populates="image")

    def __init__(self, id: str, page_id: str, object_key: str, status: str) -> None:
        self.id = id
        self.page_id = page_id
        self.object_key = object_key
        self.status = status
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "pageId": self.page_id,
            "objectKey": self.object_key,
            "status": self.status,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }


class Json(Base, TimestampMixin):
    __tablename__ = "jsons"

    id = Column(String, primary_key=True)
    page_id = Column(String, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    object_key = Column(String, nullable=False)
    status = Column(String, nullable=False)

    page: Mapped["Page"] = relationship("Page", back_populates="json")

    def __init__(self, id: str, project_id: str, object_key: str, status: str) -> None:
        self.id = id
        self.project_id = project_id
        self.object_key = object_key
        self.status = status
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"<Json id={self.id}, project_id={self.project_id}, object_key={self.object_key}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "projectId": self.project_id,
            "objectKey": self.object_key,
            "status": self.status,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }


class Page(Base, TimestampMixin):
    __tablename__ = "pages"

    id = Column(String, primary_key=True)
    pdf_id = Column(String, ForeignKey("versions.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    index = Column(Integer, nullable=False)

    version: Mapped["Version"] = relationship("Version", back_populates="pages")
    image: Mapped["Image"] = relationship("Image", cascade="all, delete", passive_deletes=True)
    json: Mapped["Json"] = relationship("Json", cascade="all, delete", passive_deletes=True)

    def __init__(self, id: str, pdf_id: str, index: int, status: str) -> None:
        self.id = id
        self.pdf_id = pdf_id
        self.status = status
        self.index = index
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"<Page id={self.id}, pdf_id={self.pdf_id}, index={self.index}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "pdfId": self.pdf_id,
            "status": self.status,
            "index": self.index,
            "version": self.version.serializer(),
            "image": self.image.serializer(),
            "json": self.json.serializer(),
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }


class Matching(Base, TimestampMixin):
    __tablename__ = "matchings"

    id = Column(String, primary_key=True)
    image1_id = Column(String, ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    image2_id = Column(String, ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=True)
    status = Column(String, nullable=False)
    params = Column(JSON, nullable=False)
    bounding_boxes = Column(JSON, nullable=True)

    image1: Mapped["Image"] = relationship("Image", foreign_keys=[image1_id])
    image2: Mapped["Image"] = relationship("Image", foreign_keys=[image2_id])

    def __init__(
        self,
        id: str,
        image1_id: str,
        image2_id: str,
        score: float,
        status: str,
        params: dict,
        bounding_boxes: dict,
    ) -> None:
        self.id = id
        self.image1_id = image1_id
        self.image2_id = image2_id
        self.score = score  # type: ignore
        self.status = status
        self.params = params
        self.bounding_boxes = bounding_boxes
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"<Matching id={self.id}, image1_id={self.image1_id}, image2_id={self.image2_id}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "image1": self.image1.serializer(),
            "image2": self.image2.serializer(),
            "score": self.score,
            "status": self.status,
            "params": self.params,
            "boundingBoxes": self.bounding_boxes,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }
