"""fill location table

Revision ID: 84abf7c41f04
Revises: edaf40dec2cb
Create Date: 2024-10-06 09:28:12.335323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84abf7c41f04'
down_revision: Union[str, None] = 'edaf40dec2cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open('/app/src/plugins/db/sql/taxi_locations.sql', 'r') as file:
        sql_script = file.read()

    op.execute(sql_script)


def downgrade() -> None:
    op.execute(
        """
            SET search_path to 'data';
            DELETE FROM location;
        """
    )
