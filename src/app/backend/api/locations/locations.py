from fastapi import APIRouter
from sqlalchemy.orm import Session

from taxi_db.model import Location
from taxi_db.utils.session import TaxiSession

router = APIRouter()


@router.get("/{location_id}")
def get_location(location_id: int):
    session: Session = TaxiSession().session
    location: Location = session.get(Location, location_id)
    return {"id": location.borough if location else "not found"}
