import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from taxi_db.model import Trip

__all__ = ["pipeline"]

categorical_feats = [Trip.pu_location_id.name, Trip.do_location_id.name]
numerical_feats = [Trip.trip_distance.name]


class TaxiTransformer(TransformerMixin):
    def __init__(self, pickup_col: str, dropoff_col: str) -> None:
        self.pickup_col = pickup_col
        self.dropoff_col = dropoff_col

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        X[self.pickup_col] = pd.to_datetime(X[self.pickup_col])
        X[self.dropoff_col] = pd.to_datetime(X[self.dropoff_col])
        return X


class TaxiDictTransformer(TransformerMixin):
    def __init__(self, categorical_feats, numerical_feats) -> None:
        self.categorical_feats = categorical_feats
        self.numerical_feats = numerical_feats

    def fit(self, X, y=None):
        return self
    
    def transform(self, X: pd.DataFrame) -> list[dict]:
        return X[[*categorical_feats, *numerical_feats]].copy().to_dict(orient="records")


preprocessor = ColumnTransformer(
    transformers=[
        ("cat", "passthrough", categorical_feats),
        ("num", "passthrough", numerical_feats),
    ]
)

pipeline = Pipeline(
    steps=[
        (
            "taxi_transformer",
            TaxiTransformer(
                Trip.tpep_pickup_datetime.name,
                Trip.tpep_dropoff_datetime.name,
            ),
        ),
        # ("select_columns", preprocessor),
        ("taxi_dict_transformer", TaxiDictTransformer(categorical_feats, numerical_feats)),
        ("dict_vectorizer", DictVectorizer(sparse=False)),
        # ("regressor", LinearRegression()),
    ]
)
