import logging
from datetime import datetime

import pandas as pd
from airflow.decorators import dag, task
import mlflow
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from db.model.trip import Trip
from db.utils.session import TaxiSession

session = TaxiSession().session

logger = logging.getLogger(__name__)

categorical_feats = [Trip.pu_location_id.name, Trip.do_location_id.name]
numerical_feats = [Trip.trip_distance.name]


@dag(
    dag_id='train_taxi_model',
    description='Train NYC Taxi trip duration model',
)
def train_taxi_model():
    @task
    def load_latest_data(session: Session) -> dict:
        latest_trip_date: datetime = session.query(func.max(Trip.tpep_pickup_datetime)).scalar()
        logger.info(f'Latest trip date: {str(latest_trip_date)}')
        df = pd.read_sql(
            session.query(Trip).where(
                extract('year', Trip.tpep_pickup_datetime) == latest_trip_date.year,
                extract('month', Trip.tpep_pickup_datetime) == latest_trip_date.month,
            ).limit(100000).statement,
            con=session.get_bind(),
        )
        df[Trip.tpep_pickup_datetime.name] = df[Trip.tpep_pickup_datetime.name].astype(str)
        df[Trip.tpep_dropoff_datetime.name] = df[Trip.tpep_dropoff_datetime.name].astype(str)
        logger.info(f'Loaded DataFrame shape: {df.shape}, dtypes: {df.dtypes}')
        return df.to_dict(orient='list')

    @task
    def transform_data(df_dict: dict) -> dict:
        df = pd.DataFrame(df_dict)
        df[Trip.tpep_pickup_datetime.name] = pd.to_datetime(df[Trip.tpep_pickup_datetime.name])
        df[Trip.tpep_dropoff_datetime.name] = pd.to_datetime(df[Trip.tpep_dropoff_datetime.name])
        df['duration'] = df.apply(
            lambda x: (x[Trip.tpep_dropoff_datetime.name] - x[Trip.tpep_pickup_datetime.name]).total_seconds() / 60,
            axis=1,
        )
        df[categorical_feats] = df[categorical_feats].astype('object')
        df = df[[*categorical_feats, *numerical_feats, 'duration']]
        return df.to_dict(orient='list')

    @task
    def train_model(df_dict: dict) -> None:
        df = pd.DataFrame(df_dict)
        dv = DictVectorizer()
        train_dicts = df[categorical_feats + numerical_feats].to_dict(orient="records")
        X_train = dv.fit_transform(train_dicts)
        y_train = df['duration'].values

        with mlflow.start_run(run_name='train_taxi_model'):
            lr = LinearRegression()
            lr.fit(X_train, y_train)
            y_pred = lr.predict(X_train)
            rmse = root_mean_squared_error(y_train, y_pred)
            mlflow.log_metric('rmse', rmse)

    df_dict = load_latest_data(session)
    df_dict_transformed = transform_data(df_dict)
    train_model(df_dict_transformed)


train_taxi_model()
