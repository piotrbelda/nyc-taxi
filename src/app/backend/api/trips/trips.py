from fastapi import APIRouter
from sqlalchemy.orm import Session

from taxi_db.model import Trip
from taxi_db.utils.session import TaxiSession

router = APIRouter()


@router.get("/{trip_id}")
def get_trip(trip_id: int):
    session: Session = TaxiSession().session
    trip: Trip = session.get(Trip, trip_id)
    return {"id": trip.trip_distance if trip else "not found"}
