from typing import List

import pandas as pd
from fastapi import APIRouter

from taxi_db.model import Trip as TripModel
from taxi_model.model import get_latest_taxi_model
from taxi_model.pipeline import pipeline

from ...model.trip import Trip

router = APIRouter()


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
