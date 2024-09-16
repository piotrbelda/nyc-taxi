from typing import Any

from session import Session as PostgresSession
from sqlalchemy.orm import Session


class SessionMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs) -> Any:
        if cls._instance is None:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance


class DBSession(metaclass=SessionMeta):
    def __init__(self) -> None:
        self.session: Session = PostgresSession()
