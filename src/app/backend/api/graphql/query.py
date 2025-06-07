import strawberry
from sqlalchemy.orm import Session

from taxi_db.utils.session import TaxiSession
from .types import Location as LocationType, Trip as TripType
from taxi_db.model import Location, Trip


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

    @strawberry.field
    def getTrip(self, id: int) -> TripType:
        session: Session = TaxiSession().session
        trip: Trip = session.get(Trip, id)
        return TripType(
            id=trip.id,
            tpep_pickup_datetime=trip.tpep_pickup_datetime,
            tpep_dropoff_datetime=trip.tpep_dropoff_datetime,
            passenger_count=trip.passenger_count,
            trip_distance=trip.trip_distance,
            fare_amount=trip.fare_amount,
            pu_location_id=trip.pu_location_id,
            do_location_id=trip.do_location_id,
        )
