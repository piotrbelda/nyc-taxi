from datetime import datetime
from typing import Optional

import strawberry


@strawberry.type
class Location:
    id: int
    zone: str
    borough: str
    geom: str


@strawberry.type
class Trip:
    id: int
    vendor_id: Optional[int] = None
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    passenger_count: int
    trip_distance: Optional[float] = None
    rate_code_id: Optional[int] = None
    store_and_fwd_flag: Optional[bool] = None
    pu_location_id: Optional[int] = None
    do_location_id: Optional[int] = None
    payment_type: Optional[int] = None
    fare_amount: Optional[float] = None
    extra: Optional[float] = None
    mta_tax: Optional[float] = None
    tip_amount: Optional[float] = None
    tolls_amount: Optional[float] = None
    improvement_surcharge: Optional[float] = None
    total_amount: Optional[float] = None
    congestion_surcharge: Optional[float] = None
    airport_fee: Optional[float] = None
    geom: Optional[str] = None
