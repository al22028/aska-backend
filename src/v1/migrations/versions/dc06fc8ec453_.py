"""empty message

Revision ID: dc06fc8ec453
Revises: 87476f24d9f7
Create Date: 2024-02-13 12:53:11.717001

"""

# Standard Library
from typing import Sequence, Union

# Third Party Library
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc06fc8ec453"
down_revision: Union[str, None] = "87476f24d9f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "matchings",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("image1_id", sa.String(), nullable=False),
        sa.Column("image2_id", sa.String(), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("params", sa.JSON(), nullable=False),
        sa.Column("bounding_boxes", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["image1_id"], ["images.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["image2_id"], ["images.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("matchings")
    # ### end Alembic commands ###
