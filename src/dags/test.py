from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

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
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        bash_command="sleep 5",
    )

    t3 = BashOperator(
        task_id="another_sleeping",
        bash_command="sleep 2",
    )

    t1 >> t2 >> t3
