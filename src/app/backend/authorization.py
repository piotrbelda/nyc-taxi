from http import HTTPStatus

from fastapi import HTTPException, Request

from .config.env import X_API_KEY


def verify_api_key(request: Request) -> None:
    if request.headers.get("x-api-key") != X_API_KEY:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="Invalid API key")
