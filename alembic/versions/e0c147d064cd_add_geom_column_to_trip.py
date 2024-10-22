"""add geom column to trip

Revision ID: e0c147d064cd
Revises: 84abf7c41f04
Create Date: 2024-10-22 16:06:05.774388

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2.types import Geometry


# revision identifiers, used by Alembic.
revision: str = 'e0c147d064cd'
down_revision: Union[str, None] = '84abf7c41f04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'trip',
        sa.Column(
            'geom',
            Geometry(
                geometry_type='LINESTRING',
                srid=4326,
                from_text='ST_GeomFromEWKT',
                name='geometry',
                spatial_index=False,
            ),
            nullable=True,
        ),
        schema='data',
    )
    op.create_index('idx_trip_geom', 'trip', ['geom'], unique=False, schema='data', postgresql_using='gist')


def downgrade() -> None:
    op.drop_index('idx_trip_geom', table_name='trip', schema='data', postgresql_using='gist')
    op.drop_column('trip', 'geom', schema='data')
