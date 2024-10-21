"""add geom column to location

Revision ID: 488a287c84a9
Revises: fc0ede421b05
Create Date: 2024-10-21 17:03:08.980957

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2.types import Geometry


# revision identifiers, used by Alembic.
revision: str = '488a287c84a9'
down_revision: Union[str, None] = 'fc0ede421b05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'location',
        sa.Column(
            'geom',
            Geometry(
                geometry_type='MULTIPOLYGON',
                srid=4326,
                from_text='ST_GeomFromEWKT',
                name='geometry',
                spatial_index=False,
            ),
            nullable=True,
        ),
        schema='data'
    )
    op.create_index('idx_location_geom', 'location', ['geom'], unique=False, schema='data', postgresql_using='gist')


def downgrade() -> None:
    op.drop_index('idx_location_geom', table_name='location', schema='data', postgresql_using='gist')
    op.drop_column('location', 'geom', schema='data')
