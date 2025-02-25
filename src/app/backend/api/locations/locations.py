import binascii

import pandas as pd
from fastapi import APIRouter
from geoalchemy2.functions import ST_AsEWKB
from sqlalchemy.orm import Session

from taxi_db.model import Location
from taxi_db.utils.session import TaxiSession

router = APIRouter()


@router.get("/")
def get_locations():
    session: Session = TaxiSession().session
    locations_df = pd.read_sql(
        session.query(
            Location.borough,
            Location.zone,
            ST_AsEWKB(Location.geom).label(Location.geom.name),
        ).statement,
        con=session.get_bind(),
    )
    locations_df[Location.geom.name] = locations_df[Location.geom.name].apply(lambda geom: binascii.hexlify(geom).decode("utf-8"))
    return locations_df.to_dict(orient="records")


@router.get("/{location_id}")
def get_location(location_id: int):
    session: Session = TaxiSession().session
    location: Location = session.get(Location, location_id)
    return {"borough": location.borough, "zone": location.zone} if location else {}
