import re
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple

import httpx
from airflow.models.dag import DAG
from airflow.models.connection import Connection
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.session import provide_session
from scrapy import Selector

from test import VAR

TAXI_DATA_PAGE_URL = 'https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page'


def sort_by_year_month(s: str) -> Tuple[int, int]:
    search = re.search(r"(\d{4})-(\d{2})", s)
    return int(search.group(1)), int(search.group(2))


def get_latest_taxi_file_hyperlink() -> list[str]:
    response = httpx.get(TAXI_DATA_PAGE_URL, timeout=10)
    selector = Selector(text = response.content)
    hyperlinks = selector.xpath('//div[@class="faq-answers"]//li//a/@href').getall()
    hyperlinks = sorted(hyperlinks, key=sort_by_year_month)
    return hyperlinks[-1]


tmp_dir = tempfile.gettempdir()

@provide_session
def create_connection(session=None):
    conn = Connection(
        conn_id='file_path',
        conn_type='fs',
        host=tmp_dir,
    )

    if not session.query(Connection).filter(Connection.conn_id == conn.conn_id).first():
        session.add(conn)
        session.commit()

with DAG(
    dag_id='test',
    default_args={
        'depends_on_past': False,
        'email': ['piotrek.belda@wp.pl'],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description='A simple tutorial DAG',
    schedule=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["example"],
):
    latest_file_url = get_latest_taxi_file_hyperlink()
    file_path = Path(tmp_dir) / Path(latest_file_url).name

    download_data = BashOperator(
        task_id='download_data',
        bash_command=f'curl {latest_file_url} -o {str(file_path)}',
    )

    create_connection()

    file_sensor = FileSensor(
        task_id='file_sensor',
        filepath=str(file_path.parent),
        fs_conn_id='file_path',
    )

    sleep = BashOperator(
        task_id='sleep_1',
        bash_command=f'sleep 1',
    )

    download_data >> file_sensor >> sleep
 