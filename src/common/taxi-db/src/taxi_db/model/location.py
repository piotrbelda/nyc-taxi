from sqlalchemy import Column, CheckConstraint, Integer, Text, UniqueConstraint
from geoalchemy2 import Geometry

from ..config.env import TAXI_SCHEMA
from ..model import Base
from ..utils.consts import GeometryType


class Location(Base):
    __tablename__ = "location"
    __table_args__ = (
        UniqueConstraint("borough", "zone", name="location_borough_zone_key"),
        CheckConstraint("id > 0"),
        {"schema": TAXI_SCHEMA, "extend_existing": True}
    )

    id = Column(Integer, primary_key=True, unique=True)
    zone = Column(Text, nullable=False)
    borough = Column(Text, nullable=False)
    geom = Column(
        Geometry(
            geometry_type=GeometryType.MULTIPOLYGON.value,
            srid=4326,
            spatial_index=True,
            nullable=True,
        ),
        nullable=True,
    )
