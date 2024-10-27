import pandas as pd
from fastapi import APIRouter
from sqlalchemy.orm import Session

from taxi_db.model import Location
from taxi_db.utils.session import TaxiSession

router = APIRouter()


@router.get("/")
def get_locations():
    session: Session = TaxiSession().session
    return pd.read_sql(session.query(Location.borough, Location.zone).statement, con=session.get_bind()).to_dict(orient="records")


@router.get("/{location_id}")
def get_location(location_id: int):
    session: Session = TaxiSession().session
    location: Location = session.get(Location, location_id)
    return {"borough": location.borough, "zone": location.zone} if location else {}
