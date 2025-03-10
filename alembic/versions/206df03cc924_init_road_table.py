"""init road table

Revision ID: 206df03cc924
Revises: ba7b595e452d
Create Date: 2025-02-24 16:54:10.286691

"""
from typing import Sequence, Union

from alembic import op
from geoalchemy2.types import Geometry
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '206df03cc924'
down_revision: Union[str, None] = 'ba7b595e452d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'road',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('type', sa.VARCHAR(length=1), nullable=True),
        sa.Column('geom', Geometry(geometry_type='LINESTRING', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', spatial_index=False), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        schema='data',
    )
    op.create_index('idx_road_geom', 'road', ['geom'], unique=False, schema='data', postgresql_using='gist')


def downgrade() -> None:
    op.drop_table('road', schema='data')
