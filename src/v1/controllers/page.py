# Third Party Library
from aws_lambda_powertools import Logger
from database.session import with_session
from models.image import ImageORM
from models.json import JsonORM
from models.page import PageORM
from models.version import VersionORM
from schemas.image import ImageCreateSchema
from schemas.json import JsonCreateSchema
from schemas.page import PageCreateSchema, PageSchema
from schemas.status import Status
from sqlalchemy.orm.session import Session

logger = Logger()


class PageController:
    pages = PageORM()
    images = ImageORM()
    jsons = JsonORM()
    versions = VersionORM()

    @with_session
    def find_all_pages(self, session: Session) -> list[PageSchema]:
        pages = self.pages.find_all(session)
        return [PageSchema(**page.serializer()) for page in pages]

    @with_session
    def bulk_insert_pages(self, pages: list[dict], session: Session) -> None:
        for index, page in enumerate(pages):
            if index == 0:
                self.versions.update_thumbnail(
                    db=session,
                    version_id=page["version_id"],
                    thumbnail=page["image"]["object_key"],
                )
                session.commit()
            created_page = self.pages.create_one(
                db=session,
                page_data=PageCreateSchema(
                    version_id=page["version_id"],
                    local_index=page["local_index"],
                    status=Status.preprocessed,
                ),
            )
            session.commit()
            self.jsons.create_one(
                db=session,
                json_data=JsonCreateSchema(
                    object_key=page["json"]["object_key"],
                    page_id=created_page.id,
                    status=Status(page["json"]["status"]),
                ),
            )
            session.commit()
            self.images.create_one(
                db=session,
                image_data=ImageCreateSchema(
                    object_key=page["image"]["object_key"],
                    page_id=created_page.id,
                    status=Status(page["image"]["status"]),
                ),
            )
            session.commit()

        post_version_id = pages[0]["version_id"]
        matching_results: list[tuple[int | None, int | None]] = []
        self.update_global_indices(session, pages, post_version_id, matching_results)

    @with_session
    def update_global_indices(
        self,
        session: Session,
        post_version_id: str,
        matching_results: list[tuple[int | None, int | None]],
    ) -> None:
        post_version = self.versions.find_one(db=session, version_id=post_version_id)
        prev_version = self.versions.find_previous_version(
            db=session, project_id=post_version.project_id
        )
        if prev_version is None:
            return
        prev_version_id = prev_version.id

        for prev_local_index, post_local_index in matching_results:
            if post_local_index is None:
                continue

            if prev_local_index is None:
                continue  # TODO: handle this case

            post_page_id = self.pages.find_page_by_index(
                db=session, version_id=post_version_id, index=post_local_index
            ).id
            post_global_index = self.pages.find_page_by_index(
                db=session, version_id=prev_version_id, index=prev_local_index
            ).global_index
            self.pages.update_global_index(
                db=session, page_id=post_page_id, global_index=post_global_index
            )
