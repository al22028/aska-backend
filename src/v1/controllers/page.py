# Third Party Library
from aws_lambda_powertools import Logger
from database.session import with_session
from models.image import ImageORM
from models.json import JsonORM
from models.page import PageORM
from models.version import VersionORM
from schemas.image import ImageCreateSchema
from schemas.json import JsonCreateSchema
from schemas.page import PageCreateSchema, PageSchema, PageUpdateSchema
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
    def update_single_page(
        self, page_id: str, data: PageUpdateSchema, session: Session
    ) -> PageSchema:
        page = self.pages.find_one(session, page_id)
        page.local_index = data.local_index
        page.global_index = data.global_index
        page.status = data.status
        session.commit()
        return PageSchema(**page.serializer())

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
                    global_index=page["local_index"],
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
                    original_object_key=page["image"]["object_key"],  # FIXME: original_object_key
                    page_id=created_page.id,
                    status=Status(page["image"]["status"]),
                ),
            )
            session.commit()

        # after_version_id = pages[0]["version_id"]
        # matching_results: list[tuple[int | None, int | None]] = []  # todo
        # matching_results.sort(key=lambda pair: (pair[0] is None, pair[1]))
        # project_id = self.versions.find_one(db=session, version_id=after_version_id).project_id
        # self.update_global_indices(
        #     session=session,
        #     after_version_id=after_version_id,
        #     matching_results=matching_results,
        #     project_id=project_id,
        # )

    # @with_session
    # def update_global_indices(
    #     self,
    #     session: Session,
    #     after_version_id: str,
    #     matching_results: list[tuple[int | None, int | None]],
    #     project_id: str,
    # ) -> None:
    #     after_version = self.versions.find_one(db=session, version_id=after_version_id)
    #     before_version = self.versions.find_previous_version(
    #         db=session, project_id=after_version.project_id
    #     )
    #     if before_version is None:
    #         return
    #     before_version_id = before_version.id

    #     for before_local_index, after_local_index in matching_results:
    #         if after_local_index is None:
    #             continue

    #         # 対応するページがない場合は、global indexを1つ前のページのglobal indexから推定する
    #         if before_local_index is None:
    #             prev_after_local_index = after_local_index - 1
    #             if prev_after_local_index < 1:
    #                 after_global_index = 1
    #             prev_after_global_index = self.pages.find_page_by_index(
    #                 db=session, version_id=after_version_id, index=prev_after_local_index
    #             ).global_index
    #             after_global_index = prev_after_global_index + 1

    #             # 推定したglobal indexが他のglobal indexと重複していないか調べる
    #             for _, after_local_index_ in matching_results:
    #                 if after_local_index_ is None:
    #                     continue
    #                 after_global_index_ = self.pages.find_page_by_index(
    #                     db=session, version_id=after_version_id, index=after_local_index_
    #                 ).global_index
    #                 # 重複がある場合は、すべてのバージョンのglobal indexをずらす
    #                 if after_global_index_ == after_global_index:
    #                     self.insert_new_global_index(after_global_index, project_id)

    #         # 1つ前のバージョンに対応するページがある場合は、そのglobal indexを使う
    #         after_global_index = self.pages.find_page_by_index(
    #             db=session, version_id=before_version_id, index=before_local_index
    #         ).global_index
    #         after_page_id = self.pages.find_page_by_index(
    #             db=session, version_id=after_version_id, index=after_local_index
    #         ).id
    #         self.pages.update_global_index(
    #             db=session, page_id=after_page_id, global_index=after_global_index
    #         )

    # @with_session
    # def insert_new_global_index(
    #     self, session: Session, new_global_index: int, project_id: str
    # ) -> None:
    #     versions = self.versions.find_many_by_project_id(db=session, project_id=project_id)
    #     for version in versions:
    #         for page in version.pages:
    #             if page.global_index is None:
    #                 continue
    #             if page.global_index >= new_global_index:
    #                 self.pages.update_global_index(
    #                     db=session, page_id=page.id, global_index=page.global_index + 1
    #                 )
