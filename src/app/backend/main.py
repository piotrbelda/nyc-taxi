from typing import Any, Callable

import strawberry
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from .api.locations import locations
from .api.predict import predict
from .api.trips import trips
from .api.graphql.query import Query
from .authorization import verify_api_key

app = FastAPI(
    title="NYC Taxi",
    dependencies=[Depends(verify_api_key)],
)
app.include_router(locations.router, prefix="/locations")
app.include_router(trips.router, prefix="/trips")
app.include_router(predict.router, prefix="/predict")

X_ORIGINS = [
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=X_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return {"ping": "pong"}


@app.middleware("http")
def log_requests(request: Request, call_next: Callable[[Request], Any]):
    print(f"request has been made!, method: {request.method}, path: {request.url.path}")
    return call_next(request)


schema = strawberry.Schema(Query)
graphQLRouter = GraphQLRouter(schema)

app.include_router(graphQLRouter, prefix="/graphql")
