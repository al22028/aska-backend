# Standard Library
from datetime import datetime

# Third Party Library
from config.settings import AWS_RDS_DATABASE_URL, SQLALCHEMY_ECHO_SQL
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

    id = Column(String(36), primary_key=True)
    email = Column(String(256), nullable=False, unique=True)
    name = Column(String(256), nullable=False)
    status = Column(String(32), nullable=False)

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

    id = Column(String(256), primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(String(512), nullable=False)
    thumbnail = Column(String(256), nullable=True)

    pdfs: Mapped[list["Pdf"]] = relationship(
        "Pdf", back_populates="project", cascade="all, delete", passive_deletes=True
    )

    def __init__(self, id: str, title: str, description: str, thumbnail: str | None = None) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.thumbnail = thumbnail
        self.updated_at = datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"<project id={self.id}, title={self.title}, descripton={self.description}, thumbnail={self.thumbnail}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "thumbnail": self.thumbnail,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
            "pdfs": [pdf.serializer() for pdf in self.pdfs],
        }


class Pdf(Base, TimestampMixin):
    __tablename__ = "pdfs"

    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(256), nullable=True)
    thumbnail = Column(String(256), nullable=True)
    description = Column(String(512), nullable=True)
    object_key = Column(String(256), nullable=False)

    project: Mapped["Project"] = relationship("Project", back_populates="pdfs")
    # pages: Relationship = relationship(
    #     "Page", back_populates="pdf", cascade="all, delete", passive_deletes=True
    # )

    def __init__(
        self,
        id: str,
        project_id: str,
        object_key: str,
        title: str | None = None,
        thumbnail: str | None = None,
        description: str | None = None,
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
        return f"<pdf id={self.id}, peojct_id={self.project_id}, thumbnail={self.thumbnail}, description={self.description}, object_key={self.object_key}>"

    def __repr__(self) -> str:
        return self.__str__()

    def serializer(self) -> dict:
        return {
            "id": self.id,
            "projectId": self.project_id,
            "title": self.title,
            "thumbnail": self.thumbnail,
            "description": self.description,
            "objectKey": self.object_key,
            "updatedAt": self.updated_at.isoformat(),  # type: ignore
            "createdAt": self.created_at.isoformat(),  # type: ignore
        }


# class Page(Base, TimestampMixin):
#     __tablename__ = "pages"

#     id = Column(String(36), primary_key=True)
#     pdf_id = Column(String(36), ForeignKey("pdfs.id", ondelete="CASCADE"), nullable=False)
#     status = Column(String(32), nullable=False)

#     pdf: Relationship = relationship("Pdf", back_populates="pdf")  # type: ignore
#     child_image: Relationship = relationship(
#         "Image", back_populates="parent", cascade="all, delete", passive_deletes=True
#     )
#     child_paring: Relationship = relationship(
#         "Pairing", back_populates="parent", cascade="all, delete", passive_deletes=True
#     )

#     def __init__(self, pdf_id: str, status: str) -> None:
#         self.id = str(uuid.uuid4())
#         self.pdf_id = pdf_id
#         self.status = status

#     def __str__(self) -> str:
#         return f"<Page id={self.id}, pdf_id={self.pdf_id}, status={self.status}>"

#     def __repr__(self) -> str:
#         return self.__str__()

#     def serializer(self) -> dict:
#         return {
#             "id": self.id,
#             "pdfId": self.pdf_id,
#             "status": self.status,
#             "updatedAt": self.updated_at.isoformat(),  # type: ignore
#             "createdAt": self.created_at.isoformat(),  # type: ignore
#         }


# class Pairing(Base, TimestampMixin):
#     __tablename__ = "pairings"

#     id = Column(String(36), primary_key=True)
#     page_id = Column(String(36), ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
#     target_page_id = Column(String(36), ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
#     threshold = Column(Integer, nullable=False)
#     meta_data = Column(JSON, nullable=False)

#     parent: Relationship = relationship(
#         "Page", foreign_keys=[page_id, target_page_id], back_populates="child_paring"
#     )

#     def __init__(
#         self,
#         page_id: str,
#         target_page_id: str,
#         meta_data: dict,
#         threshold: int = 220,
#     ) -> None:
#         self.id = str(uuid.uuid4())
#         self.page_id = page_id
#         self.target_page_id = target_page_id
#         self.threshold = threshold
#         self.meta_data = meta_data

#     def __str__(self) -> str:
#         return f"<pairing id={self.id}, page_id={self.page_id}, target_page_id={self.target_page_id}, threshold={self.threshold}, meta_data={self.meta_data}>"

#     def __repr__(self) -> str:
#         return self.__str__()

#     def serializer(self) -> dict:
#         return {
#             "id": self.id,
#             "pageId": self.page_id,
#             "targetPageId": self.target_page_id,
#             "threshold": self.threshold,
#             "meta_data": self.meta_data,
#             "updatedAt": self.updated_at.isoformat(),  # type: ignore
#             "createdAt": self.created_at.isoformat(),  # type: ignore
#         }


# class Image(Base, TimestampMixin):
#     __tablename__ = "images"

#     id = Column(String(36), primary_key=True)
#     page_id = Column(String(36), ForeignKey("pages.id", ondelete="CASCADE"), nullable=True)
#     object_key = Column(String(256), nullable=False)

#     status = Column(String(32), nullable=False)
#     key_points = Column(JSON, nullable=False)

#     child: Relationship = relationship(
#         "Matching", back_populates="parent", cascade="all, delete", passive_deletes=True
#     )
#     parent: Relationship = relationship("Page", back_populates="child_image")

#     def __init__(self, page_id: str, object_key: str, key_points: dict, status: str) -> None:
#         self.id = str(uuid.uuid4())
#         self.page_id = page_id
#         self.object_key = object_key
#         self.key_points = key_points
#         self.status = status

#     def __str__(self) -> str:
#         return f"<image id={self.id}, page_id={self.page_id}, object_key={self.object_key}, key_points={self.key_points}, status={self.status}>"

#     def __repr__(self) -> str:
#         return self.__str__()

#     def serializer(self) -> dict:
#         return {
#             "id": self.id,
#             "pageId": self.page_id,
#             "objectKey": self.object_key,
#             "keyPoints": self.key_points,
#             "status": self.status,
#             "updatedAt": self.updated_at.isoformat(),  # type: ignore
#             "createdAt": self.created_at.isoformat(),  # type: ignore
#         }


# class Matching(Base, TimestampMixin):
#     __tablename__ = "matchings"

#     id = Column(String(36), primary_key=True)
#     image_id = Column(String(36), ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
#     target_image_id = Column(
#         String(36), ForeignKey("images.id", ondelete="CASCADE"), nullable=False
#     )
#     score = Column(Numeric(asdecimal=False), nullable=True)
#     status = Column(String(32), nullable=False)

#     parent: Relationship = relationship(
#         "Image", foreign_keys=[image_id, target_image_id], back_populates="child"
#     )

#     def __init__(self, image_id: str, target_image_id: str, score: float, status: str) -> None:
#         self.id = str(uuid.uuid4())
#         self.image_id = image_id
#         self.target_image_id = target_image_id
#         self.score = score  # type: ignore
#         self.status = status

#     def __str__(self) -> str:
#         return f"<matching id={self.id}, image_id={self.image_id}, target_image_id={self.target_image_id}, score={self.score}, status={self.status}>"

#     def __repr__(self) -> str:
#         return self.__str__()

#     def serializer(self) -> dict:
#         return {
#             "id": self.id,
#             "imageId": self.image_id,
#             "targetImageId": self.target_image_id,
#             "score": self.score,
#             "status": self.status,
#             "updatedAt": self.updated_at.isoformat(),  # type: ignore
#             "createdAt": self.created_at.isoformat(),  # type: ignore
#         }
