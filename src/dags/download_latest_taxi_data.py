import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple

import httpx
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from scrapy import Selector

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
    file_name = Path(latest_file_url).name
    download_data = BashOperator(
        task_id='download_data',
        bash_command=f'wget {latest_file_url} -O $(pwd)/{file_name}',
    )

    download_data
 