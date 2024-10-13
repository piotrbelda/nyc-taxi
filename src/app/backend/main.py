from fastapi import FastAPI

from .api.locations import locations
from .api.trips import trips

app = FastAPI(title="NYC Taxi")
app.include_router(locations.router, prefix="/locations")
app.include_router(trips.router, prefix="/trips")


@app.get("/")
def ping():
    return {"ping": "pong"}
