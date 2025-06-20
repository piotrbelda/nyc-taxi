from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey, Index, Integer, Numeric, DateTime, Boolean

from ..config.env import TAXI_SCHEMA
from ..model import Base
from ..model.location import Location
from ..utils.consts import GeometryType


class Trip(Base):
    __tablename__ = 'trip'
    __table_args__ = (
        Index('idx_trip_tpep_pickup_datetime', 'tpep_pickup_datetime', postgresql_using='btree'),
        {'schema': TAXI_SCHEMA, 'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, unique=True)
    vendor_id = Column(Integer)
    tpep_pickup_datetime = Column(DateTime, nullable=False)
    tpep_dropoff_datetime = Column(DateTime, nullable=False)
    passenger_count = Column(Integer, nullable=False)
    trip_distance = Column(Numeric(10, 2))
    rate_code_id = Column(Integer)
    store_and_fwd_flag = Column(Boolean)
    pu_location_id = Column(Integer, ForeignKey(Location.id))
    do_location_id = Column(Integer, ForeignKey(Location.id))
    payment_type = Column(Integer)
    fare_amount = Column(Numeric(10, 2))
    extra = Column(Numeric(10, 2))
    mta_tax = Column(Numeric(10, 2))
    tip_amount = Column(Numeric(10, 2))
    tolls_amount = Column(Numeric(10, 2))
    improvement_surcharge = Column(Numeric(10, 2))
    total_amount = Column(Numeric(10, 2))
    congestion_surcharge = Column(Numeric(10, 2))
    airport_fee = Column(Numeric(10, 2))
    geom = Column(
        Geometry(
            geometry_type=GeometryType.LINESTRING.value,
            srid=4326,
            spatial_index=True,
            nullable=True,
        ),
        nullable=True,
    )
