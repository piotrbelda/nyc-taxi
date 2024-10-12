from fastapi import FastAPI
from sqlalchemy.orm import Session

# from plugins.db.model.trip import Trip
# from db.utils.session import TaxiSession

app = FastAPI(title='NYC Taxi')


@app.get('/')
def ping():
    return {'ping': 'pong'}


@app.get('/trips/{trip_id}')
def get_trip(trip_id: int):
    # session: Session = TaxiSession().session
    # trip = session.get(Trip, trip_id)
    return {'id': 11}
