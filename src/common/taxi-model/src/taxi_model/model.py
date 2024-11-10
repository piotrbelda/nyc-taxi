import mlflow
from sklearn.linear_model import LinearRegression


def get_latest_taxi_model() -> LinearRegression:
    latest_models_metadata = mlflow.search_model_versions(
        max_results=5,
        filter_string="name = 'nyc-taxi'",
        order_by=["creation_timestamp ASC"],
    )
    latest_model_metadata = latest_models_metadata.pop()
    model = mlflow.sklearn.load_model(f"models:/{latest_model_metadata.name}/{latest_model_metadata.version}")
    return model
