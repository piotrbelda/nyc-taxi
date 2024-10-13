from fastapi import FastAPI
from sqlalchemy.orm import Session

from taxi_db.model import Location, Trip
from taxi_db.utils.session import TaxiSession

app = FastAPI(title='NYC Taxi')


@app.get('/')
def ping():
    return {'ping': 'pong'}


@app.get('/trips/{trip_id}')
def get_trip(trip_id: int):
    session: Session = TaxiSession().session
    trip: Trip = session.get(Trip, trip_id)
    return {'id': trip.trip_distance if trip else 'not found'}


@app.get('/locations/{location_id}')
def get_location(location_id: int):
    session: Session = TaxiSession().session
    location: Location = session.get(Location, location_id)
    return {'id': location.borough if location else 'not found'}
