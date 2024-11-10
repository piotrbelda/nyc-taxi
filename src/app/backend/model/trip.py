from datetime import datetime

from pydantic import BaseModel


class Trip(BaseModel):
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    passenger_count: int
    trip_distance: float
    fare_amount: float
    pu_location_id: int
    do_location_id: int
