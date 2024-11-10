from datetime import datetime
from typing import List

import mlflow
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression

from taxi_db.model import Trip as TripModel
from taxi_model.pipeline import pipeline

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
def predict_trip_duration(trips: List[Trip]):
    df = pd.DataFrame(
        [
            {
                TripModel.tpep_pickup_datetime.name: trip.tpep_pickup_datetime,
                TripModel.tpep_dropoff_datetime.name: trip.tpep_dropoff_datetime,
                TripModel.pu_location_id.name: trip.pu_location_id,
                TripModel.do_location_id.name: trip.do_location_id,
                TripModel.trip_distance.name: trip.trip_distance,
            }
            for trip in trips
        ]
    )
    X = pipeline.fit_transform(df)
    model = get_latest_taxi_model()
    predictions = model.predict(X)
    return {"predictions": predictions.tolist()}
