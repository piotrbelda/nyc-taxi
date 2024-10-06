"""init revision

Revision ID: edaf40dec2cb
Revises: 
Create Date: 2024-10-06 09:01:59.638257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edaf40dec2cb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'location',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('zone', sa.Text(), nullable=False),
        sa.Column('borough', sa.Text(), nullable=False),
        sa.CheckConstraint('id > 0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('borough', 'zone', name='location_borough_zone_key'),
        sa.UniqueConstraint('id'),
        schema='data',
    )
    op.create_table(
        'trip',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vendor_id', sa.Integer(), nullable=True),
        sa.Column('tpep_pickup_datetime', sa.DateTime(), nullable=False),
        sa.Column('tpep_dropoff_datetime', sa.DateTime(), nullable=False),
        sa.Column('passenger_count', sa.Integer(), nullable=False),
        sa.Column('trip_distance', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('rate_code_id', sa.Integer(), nullable=True),
        sa.Column('store_and_fwd_flag', sa.Boolean(), nullable=True),
        sa.Column('pu_location_id', sa.Integer(), nullable=False),
        sa.Column('do_location_id', sa.Integer(), nullable=False),
        sa.Column('payment_type', sa.Integer(), nullable=True),
        sa.Column('fare_amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('extra', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('mta_tax', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('tip_amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('tolls_amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('improvement_surcharge', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('congestion_surcharge', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('airport_fee', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['do_location_id'], ['data.location.id'], ),
        sa.ForeignKeyConstraint(['pu_location_id'], ['data.location.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        schema='data',
    )


def downgrade() -> None:
    op.drop_table('trip', schema='data')
    op.drop_table('location', schema='data')
