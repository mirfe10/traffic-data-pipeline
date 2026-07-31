from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 7, 20),
    schedule="*/15 * * * *",
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract_weather",
        bash_command="""
        cd /opt/project/src &&
        python weather_extract.py
        """,
        retries=2,
        retry_delay=timedelta(minutes=2),
    )

    dbt = BashOperator(
        task_id="dbt_weather",
        bash_command="""
        cd /opt/project/traffic_dbt &&
        dbt run --select weather_clean
        """
    )

    extract >> dbt