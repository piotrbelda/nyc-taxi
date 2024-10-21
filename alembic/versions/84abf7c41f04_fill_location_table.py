"""fill location table

Revision ID: 84abf7c41f04
Revises: edaf40dec2cb
Create Date: 2024-10-06 09:28:12.335323

"""
from typing import Sequence, Union

import pandas as pd
from alembic import op
from geoalchemy2.functions import ST_GeomFromText

from taxi_db.model import Location
from taxi_db.utils.session import TaxiSession

# revision identifiers, used by Alembic.
revision: str = '84abf7c41f04'
down_revision: Union[str, None] = '488a287c84a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

session  = TaxiSession().session


def upgrade() -> None:
    df = pd.read_csv("alembic/data/taxi_zones.csv")
    df = df.drop_duplicates(subset=['zone', 'borough'])
    for _, row in df.iterrows():
        object_id, _, geom_text, _, zone, _, borough = row
        geom = ST_GeomFromText(geom_text, 4326)
        location = Location(id=object_id, zone=zone, borough=borough, geom=geom)
        session.add(location)
    session.commit()


def downgrade() -> None:
    op.execute(
        """
            DELETE FROM data.trip;
            DELETE FROM data.location;
        """
    )
