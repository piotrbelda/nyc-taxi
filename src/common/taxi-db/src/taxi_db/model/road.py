from sqlalchemy import Column, Integer, Text, VARCHAR
from geoalchemy2 import Geometry

from ..model import Base
from ..config.env import TAXI_SCHEMA


class Road(Base):
    __tablename__ = "road"
    __table_args__ = (
        {
            "schema": TAXI_SCHEMA,
            "extend_existing": True,
        },
    )

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Text, nullable=False)
    type = Column(VARCHAR(length=1), nullable=True)
    geom = Column(
        Geometry(
            geometry_type="LINESTRING",
            srid=4326,
            spatial_index=True,
            nullable=True,
        ),
        nullable=True,
    )
