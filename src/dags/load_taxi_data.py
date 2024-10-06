import re
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Tuple

import httpx
import pandas as pd
from pyarrow.parquet import ParquetFile
from airflow.models.dag import DAG
from airflow.models.connection import Connection
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from scrapy import Selector
from sqlalchemy.orm import Session

from db.utils.session import AirflowSession, TaxiSession
from db.model.location import Location
from db.model.trip import Trip

TAXI_DATA_PAGE_URL = 'https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page'
TAXI_COLUMNS = [
    Trip.vendor_id.name,
    Trip.tpep_pickup_datetime.name,
    Trip.tpep_dropoff_datetime.name,
    Trip.passenger_count.name,
    Trip.trip_distance.name,
    Trip.rate_code_id.name,
    Trip.store_and_fwd_flag.name,
    Trip.pu_location_id.name,
    Trip.do_location_id.name,
    Trip.payment_type.name,
    Trip.fare_amount.name,
    Trip.extra.name,
    Trip.mta_tax.name,
    Trip.tip_amount.name,
    Trip.tolls_amount.name,
    Trip.improvement_surcharge.name,
    Trip.total_amount.name,
    Trip.congestion_surcharge.name,
    Trip.airport_fee.name,
]

tmp_dir = tempfile.gettempdir()
airflow_session = AirflowSession().session
taxi_session = TaxiSession().session


def sort_by_year_month(s: str) -> Tuple[int, int]:
    search = re.search(r"(\d{4})-(\d{2})", s)
    return int(search.group(1)), int(search.group(2))


def get_latest_taxi_file_hyperlink() -> str:
    response = httpx.get(TAXI_DATA_PAGE_URL, timeout=10)
    selector = Selector(text = response.content)
    hyperlinks = selector.xpath('//div[@class="faq-answers"]//li//a[@title="Yellow Taxi Trip Records"]/@href').getall()
    hyperlinks = sorted(hyperlinks, key=sort_by_year_month)
    return hyperlinks[-1]


def create_connection(session: Session, **kwargs: Any) -> Connection:
    connection = Connection(**kwargs)

    if not session.query(Connection).filter(Connection.conn_id == connection.conn_id).first():
        session.add(connection)
        session.commit()

    return connection


def get_locations_df(session: Session) -> pd.DataFrame:
    return pd.read_sql(
        session.query(Location).statement,
        con=session.get_bind(),
    )


def upload_file(file_path: Path, session: Session) -> dict:
    parquet = ParquetFile(file_path)
    for batch_num, batch in enumerate(parquet.iter_batches(batch_size=10000), start=1):
        trip_df: pd.DataFrame = batch.to_pandas()
        trip_df.columns = TAXI_COLUMNS
        location_df = get_locations_df(session)
        df = pd.merge(trip_df, location_df, how='inner', left_on=Trip.pu_location_id.name, right_on=Location.id.name)
        df = pd.merge(df, location_df, how='inner', left_on=Trip.do_location_id.name, right_on=Location.id.name)
        df = df[TAXI_COLUMNS]
        df.to_sql(name=Trip.__tablename__, con=session.get_bind(), if_exists='append', index=False)
        if batch_num == 100:
            break
    return {}


with DAG(
    dag_id='load_taxi_data',
    default_args={
        'depends_on_past': False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 0,
        "retry_delay": timedelta(minutes=1),
    },
    description='Load latest NYC taxi data',
    schedule=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["load"],
):
    latest_file_url = get_latest_taxi_file_hyperlink()
    file_path = Path(tmp_dir) / Path(latest_file_url).name

    download_data = BashOperator(
        task_id='download_data',
        bash_command=f'curl {latest_file_url} -o {str(file_path)}',
    )

    file_connection = create_connection(
        airflow_session,
        conn_id='file_path',
        conn_type='fs',
        host=tmp_dir,
    )

    check_file_exists = FileSensor(
        task_id='file_sensor',
        filepath=str(file_path.parent),
        fs_conn_id=file_connection.conn_id,
    )

    upload_data = PythonOperator(
        task_id='upload_file',
        python_callable=upload_file,
        op_args=[file_path, taxi_session],
    )

    download_data >> check_file_exists >> upload_data
