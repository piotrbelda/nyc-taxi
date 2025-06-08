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
            vendor_id=trip.vendor_id,
            tpep_pickup_datetime=trip.tpep_pickup_datetime,
            tpep_dropoff_datetime=trip.tpep_dropoff_datetime,
            passenger_count=trip.passenger_count,
            trip_distance=trip.trip_distance,
            rate_code_id=trip.rate_code_id,
            store_and_fwd_flag=trip.store_and_fwd_flag,
            pu_location_id=trip.pu_location_id,
            do_location_id=trip.do_location_id,
            payment_type=trip.payment_type,
            fare_amount=trip.fare_amount,
            extra=trip.extra,
            mta_tax=trip.mta_tax,
            tip_amount=trip.tip_amount,
            tolls_amount=trip.tolls_amount,
            improvement_surcharge=trip.improvement_surcharge,
            total_amount=trip.total_amount,
            congestion_surcharge=trip.congestion_surcharge,
            airport_fee=trip.airport_fee,
            geom=trip.geom,
        )
