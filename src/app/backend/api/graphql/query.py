import strawberry
from sqlalchemy.orm import Session

from taxi_db.utils.session import TaxiSession
from .types import Location as LocationType
from taxi_db.model import Location


@strawberry.type
class Query:
    @strawberry.field
    def getLocation(self, id: int) -> LocationType:
        session: Session = TaxiSession().session
        location: Location = session.get(Location, id)
        return LocationType(
            id=location.id,
            zone=location.zone,
            borough=location.borough,
            geom=location.geom,
        )
