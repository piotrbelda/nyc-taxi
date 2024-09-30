"""trip table added

Revision ID: cbda9585ac48
Revises: 
Create Date: 2024-09-30 18:42:20.629243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbda9585ac48'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        schema='data'
    )


def downgrade() -> None:
    op.drop_table('trip', schema='data')
