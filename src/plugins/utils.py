from typing import Any

from session import Session


class SessionMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs) -> Any:
        cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


class DBSession(metaclass=SessionMeta):
    session = Session()
