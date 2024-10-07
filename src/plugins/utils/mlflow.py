import mlflow

from functools import wraps
from typing import Callable


def mlflow_task(run_name: str):
    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            mlflow.set_experiment('test')
            with mlflow.start_run(nested=True, run_name=run_name):
                result = function(*args, **kwargs)
                return result

        return wrapper

    return decorator


def mlflow_dag(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        mlflow.set_experiment('test')
        with mlflow.start_run():
            result = function(*args, **kwargs)
            return result

    return wrapper
