"""empty message

Revision ID: 6e74ec5daeff
Revises: 25cd4e5ff0b2
Create Date: 2024-02-15 10:23:51.285660

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6e74ec5daeff"
down_revision: Union[str, None] = "25cd4e5ff0b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("pages", sa.Column("version_id", sa.String(), nullable=False))
    op.drop_constraint("pages_pdf_id_fkey", "pages", type_="foreignkey")
    op.create_foreign_key(None, "pages", "versions", ["version_id"], ["id"], ondelete="CASCADE")
    op.drop_column("pages", "pdf_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("pages", sa.Column("pdf_id", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, "pages", type_="foreignkey")  # type: ignore
    op.create_foreign_key(
        "pages_pdf_id_fkey", "pages", "versions", ["pdf_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("pages", "version_id")
    # ### end Alembic commands ###
