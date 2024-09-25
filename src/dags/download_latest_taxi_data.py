import re
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Tuple

import httpx
import pandas as pd
from airflow.models.dag import DAG
from airflow.models.connection import Connection
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from scrapy import Selector
from sqlalchemy.orm import Session

from session import AirflowSession, TaxiSession

TAXI_DATA_PAGE_URL = 'https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page'

tmp_dir = tempfile.gettempdir()
airflow_session = AirflowSession().session
taxi_session = TaxiSession().session


def sort_by_year_month(s: str) -> Tuple[int, int]:
    search = re.search(r"(\d{4})-(\d{2})", s)
    return int(search.group(1)), int(search.group(2))


def get_latest_taxi_file_hyperlink() -> list[str]:
    response = httpx.get(TAXI_DATA_PAGE_URL, timeout=10)
    selector = Selector(text = response.content)
    hyperlinks = selector.xpath('//div[@class="faq-answers"]//li//a/@href').getall()
    hyperlinks = sorted(hyperlinks, key=sort_by_year_month)
    return hyperlinks[-1]


def create_connection(session: Session, **kwargs: Any) -> Connection:
    connection = Connection(**kwargs)

    if not session.query(Connection).filter(Connection.conn_id == connection.conn_id).first():
        session.add(connection)
        session.commit()

    return connection


def upload_file(file_path: Path, session: Session) -> dict:
    df = pd.read_parquet(str(file_path)).iloc[:20000]
    df.to_sql(
        name='trip',
        con=session.get_bind(),
        if_exists='append',
        chunksize=1000,
    )
    return {}


with DAG(
    dag_id='load_taxi_data',
    default_args={
        'depends_on_past': False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
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

    file_sensor = FileSensor(
        task_id='file_sensor',
        filepath=str(file_path.parent),
        fs_conn_id=file_connection.conn_id,
    )

    sleep = BashOperator(
        task_id='sleep_1',
        bash_command='sleep 3',
    )

    uploader = PythonOperator(
        task_id='upload_file',
        python_callable=upload_file,
        op_args=[file_path, taxi_session],
    )

    download_data >> file_sensor >> sleep >> uploader
 