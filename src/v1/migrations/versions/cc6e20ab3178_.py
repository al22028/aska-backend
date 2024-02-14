"""empty message

Revision ID: cc6e20ab3178
Revises: bba3448b4f0b
Create Date: 2024-02-14 18:23:20.353428

"""

# Standard Library
from typing import Sequence, Union

# Third Party Library
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cc6e20ab3178"
down_revision: Union[str, None] = "bba3448b4f0b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "status")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("status", sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
