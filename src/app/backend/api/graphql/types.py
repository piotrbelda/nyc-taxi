import strawberry


@strawberry.type
class Location:
    id: int
    zone: str
    borough: str
    geom: str
