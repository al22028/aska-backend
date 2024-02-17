"""empty message

Revision ID: 1a3fcb3d7eae
Revises: 6e74ec5daeff
Create Date: 2024-02-18 03:06:48.344328

"""

# Standard Library
from typing import Sequence, Union

# Third Party Library
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1a3fcb3d7eae"
down_revision: Union[str, None] = "6e74ec5daeff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("unique_image_combination", "matchings", ["image1_id", "image2_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("unique_image_combination", "matchings", type_="unique")
    # ### end Alembic commands ###
