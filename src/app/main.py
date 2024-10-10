from fastapi import FastAPI

app = FastAPI(title='NYC Taxi')


@app.get('/')
def ping():
    return {'ping': 'pong'}


@app.get('/trips/{trip_id}')
def get_trip(trip_id: int):
    return {'trip_id': trip_id}
