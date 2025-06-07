import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .api.locations import locations
from .api.predict import predict
from .api.trips import trips
from .api.graphql.query import Query

app = FastAPI(title="NYC Taxi")
app.include_router(locations.router, prefix="/locations")
app.include_router(trips.router, prefix="/trips")
app.include_router(predict.router, prefix="/predict")


@app.get("/")
def ping():
    return {"ping": "pong"}


schema = strawberry.Schema(Query)
graphQLRouter = GraphQLRouter(schema)

app.include_router(graphQLRouter, prefix="/graphql")
