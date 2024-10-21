"""index created for trip.tpep_pickup_datetime

Revision ID: fc0ede421b05
Revises: 84abf7c41f04
Create Date: 2024-10-09 05:22:13.391255

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fc0ede421b05'
down_revision: Union[str, None] = 'edaf40dec2cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('idx_trip_tpep_pickup_datetime', 'trip', ['tpep_pickup_datetime'], unique=False, schema='data', postgresql_using='btree')


def downgrade() -> None:
    op.drop_index('idx_trip_tpep_pickup_datetime', table_name='trip', schema='data', postgresql_using='btree')
