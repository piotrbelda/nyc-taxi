import os
import re
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class SessionMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> Any:
        session_name = re.search('(\w+)([A-Z]\w+)', cls.__class__.__name__).group(1).lower()
        if cls._instances.get(session_name) is None:
            instance = super().__call__(*args, **kwargs)
            cls._instances[session_name] = instance
        return cls._instances[session_name]


class DBSession(ABC, metaclass=SessionMeta):
    def __init__(self) -> None:
        engine = create_engine(self.get_uri())
        self.session: Session = sessionmaker(engine).__call__()

    @abstractmethod
    def get_uri(self) -> str:
        pass


class AirflowSession(DBSession):
    def get_uri(self) -> str:
        return os.environ['AIRFLOW__DATABASE__SQL_ALCHEMY_CONN']
