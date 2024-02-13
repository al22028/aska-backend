# Standard Library
from datetime import datetime

# Third Party Library
from config.settings import AWS_IMAGE_HOST_DOMAIN, AWS_RDS_DATABASE_URL, SQLALCHEMY_ECHO_SQL
from sqlalchemy import Column, DateTime, ForeignKey, String, create_engine
from sqlalchemy.orm import Mapped, declarative_base, relationship

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
    status = Column(String, nullable=False)

    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        status: str,
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.status = status
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"<user id={self.id}, name={self.name}, email={self.email}, status={self.status}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "status": self.status,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(String(512), nullable=False)

    pdfs: Mapped[list["Pdf"]] = relationship(
        "Pdf", back_populates="project", cascade="all, delete", passive_deletes=True, uselist=True
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
            "pdfs": [pdf.serializer() for pdf in self.pdfs],
        }

    def detail_serializer(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
            "pdfs": [pdf.serializer() for pdf in self.pdfs],
        }


class Pdf(Base, TimestampMixin):
    __tablename__ = "pdfs"

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(String(512), nullable=True)
    thumbnail = Column(String, nullable=False, default="default.png")
    object_key = Column(String, nullable=True)

    project: Mapped["Project"] = relationship("Project", back_populates="pdfs")
    pages: Mapped["Page"] = relationship(
        "Page", back_populates="pdf", cascade="all, delete", passive_deletes=True, uselist=True
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
        return f"<pdf id={self.id}, title={self.title}, object_key={self.object_key}>"

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


class Page(Base, TimestampMixin):
    __tablename__ = "pages"

    id = Column(String, primary_key=True)
    pdf_id = Column(String, ForeignKey("pdfs.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    index = Column(String, nullable=False)

    pdf: Mapped["Pdf"] = relationship("Pdf", back_populates="pages")

    def __init__(self, id: str, pdf_id: str, index: str, status: str) -> None:
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
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }
