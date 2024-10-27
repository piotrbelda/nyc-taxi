"""location ids nullable

Revision ID: ba7b595e452d
Revises: e0c147d064cd
Create Date: 2024-10-27 08:56:44.227366

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'ba7b595e452d'
down_revision: Union[str, None] = 'e0c147d064cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "trip",
        "pu_location_id",
        existing_type=sa.INTEGER(),
        nullable=True,
        schema="data",
    )
    op.alter_column(
        "trip",
        "do_location_id",
        existing_type=sa.INTEGER(),
        nullable=True,
        schema="data",
    )


def downgrade() -> None:
    op.alter_column(
        "trip",
        "do_location_id",
        existing_type=sa.INTEGER(),
        nullable=False,
        schema="data",
    )
    op.alter_column(
        "trip",
        "pu_location_id",
        existing_type=sa.INTEGER(),
        nullable=False,
        schema="data",
    )
