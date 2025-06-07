from datetime import datetime

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
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    passenger_count: int
    trip_distance: float
    fare_amount: float
    pu_location_id: int
    do_location_id: int
