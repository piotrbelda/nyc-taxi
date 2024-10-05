from datetime import datetime, timedelta

import mlflow
from airflow.models.dag import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor

def test():
    mlflow.set_experiment('test')
    with mlflow.start_run():
        db = load_diabetes()
        X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

        # Create and train models.
        rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
        rf.fit(X_train, y_train)

        # Use the model to make predictions on the test dataset.
        predictions = rf.predict(X_test)
        mlflow.log_artifact("/opt/airflow/dags/mlflow_test.py")
        mlflow.log_param('test_param', 13)


with DAG(
    dag_id='mlflow_test',
    default_args={
        'depends_on_past': False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    description='Mlflow test',
    schedule=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["test"],
):
    # mlflow.create_experiment("test")
    python_test = PythonOperator(
        task_id='python_test',
        python_callable=test,
    )

    bash_test = BashOperator(
        task_id='bash_test',
        bash_command='sleep 3',
    )

    python_test >> bash_test
