import strawberry
from fastapi import Depends, FastAPI
from strawberry.fastapi import GraphQLRouter

from .api.locations import locations
from .api.predict import predict
from .api.trips import trips
from .api.graphql.query import Query
from .authorization import verify_api_key

app = FastAPI(title="NYC Taxi", dependencies=[Depends(verify_api_key)])
app.include_router(locations.router, prefix="/locations")
app.include_router(trips.router, prefix="/trips")
app.include_router(predict.router, prefix="/predict")


@app.get("/ping")
def ping():
    return {"ping": "pong"}


schema = strawberry.Schema(Query)
graphQLRouter = GraphQLRouter(schema)

app.include_router(graphQLRouter, prefix="/graphql")
