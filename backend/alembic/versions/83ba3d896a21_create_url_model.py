"""Create URL model

Revision ID: 83ba3d896a21
Revises:
Create Date: 2025-02-17 21:19:59.798065

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "83ba3d896a21"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "url",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("short_url_key", sa.String(length=25), nullable=False),
        sa.Column("target_url", sa.String(length=2048), nullable=False),
        sa.Column("secret_key", sa.String(length=50), nullable=False),
        sa.Column("admin_url", sa.String(length=100), nullable=False),
        sa.Column("clicks", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_url_secret_key"), "url", ["secret_key"], unique=True)
    op.create_index(op.f("ix_url_short_url_key"), "url", ["short_url_key"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_url_short_url_key"), table_name="url")
    op.drop_index(op.f("ix_url_secret_key"), table_name="url")
    op.drop_table("url")
    # ### end Alembic commands ###
