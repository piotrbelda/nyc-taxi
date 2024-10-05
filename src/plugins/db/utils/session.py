import os
import re
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class SessionMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> Any:
        session_name = re.search(r'(\w+)[A-Z]', cls.__name__).group(1).lower()
        if cls._instances.get(session_name) is None:
            instance = super().__call__(*args, **kwargs)
            cls._instances[session_name] = instance
        return cls._instances[session_name]


class DBSession(metaclass=SessionMeta):
    def __init__(self, uri: str) -> None:
        engine = create_engine(uri)
        self.session: Session = sessionmaker(engine).__call__()


class AirflowSession(DBSession):
    def __init__(self) -> None:
        super().__init__(os.environ['AIRFLOW__DATABASE__SQL_ALCHEMY_CONN'])


class TaxiSession(DBSession):
    def __init__(self) -> None:
        super().__init__(os.environ['POSTGRES_URI'])
