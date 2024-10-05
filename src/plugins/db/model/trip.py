from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, DateTime, Boolean

from config.env import TAXI_SCHEMA

Base = declarative_base()


class Trip(Base):
    __tablename__ = 'trip'
    __table_args__ = {'schema': TAXI_SCHEMA}

    id = Column(Integer, primary_key=True, unique=True)
    vendor_id = Column(Integer)
    tpep_pickup_datetime = Column(DateTime, nullable=False)
    tpep_dropoff_datetime = Column(DateTime, nullable=False)
    passenger_count = Column(Integer, nullable=False)
    trip_distance = Column(Numeric(10, 2))
    rate_code_id = Column(Integer)
    store_and_fwd_flag = Column(Boolean)
    pu_location_id = Column(Integer, nullable=False)
    do_location_id = Column(Integer, nullable=False)
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
