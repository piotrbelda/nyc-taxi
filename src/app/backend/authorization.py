from http import HTTPStatus

from fastapi import HTTPException, Request


def verify_api_key(request: Request) -> None:
    if request.headers.get("x-api-key") != "1234":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="Invalid API key")
