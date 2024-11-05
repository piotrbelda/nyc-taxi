from datetime import datetime
from typing import Optional

import mlflow
from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression

router = APIRouter()


class Trip(BaseModel):
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    passenger_count: int
    trip_distance: float
    fare_amount: float
    pu_location_id: int
    do_location_id: int


def get_latest_taxi_model() -> LinearRegression:
    latest_models_metadata = mlflow.search_model_versions(
        max_results=5,
        filter_string="name = 'nyc-taxi'",
        order_by=["creation_timestamp ASC"],
    )
    latest_model_metadata = latest_models_metadata.pop()
    model = mlflow.sklearn.load_model(f"models:/{latest_model_metadata.name}/{latest_model_metadata.version}")
    return model


@router.post("")
def predict_trip_duration(trip: Trip):
    print(trip.__dict__)
    return {"trip": trip.pu_location_id}
