from sqlalchemy import Column, CheckConstraint, Integer, Text, UniqueConstraint

from ..model import Base
from ..config.env import TAXI_SCHEMA


class Location(Base):
    __tablename__ = 'location'
    __table_args__ = (
        UniqueConstraint('borough', 'zone', name='location_borough_zone_key'),
        CheckConstraint('id > 0'),
        {'schema': TAXI_SCHEMA, 'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, unique=True)
    zone = Column(Text, nullable=False)
    borough = Column(Text, nullable=False)
