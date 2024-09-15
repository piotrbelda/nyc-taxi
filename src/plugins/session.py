from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

airflow_url = URL.create(
    drivername="postgresql+psycopg2",
    username="airflow",
    password="airflow",
    host="db.taxi",
    port=5432,
    database="taxi",
    query={
        "options": "-csearch_path=airflow",
    }
)

engine = create_engine(airflow_url)
Session = sessionmaker(engine)
