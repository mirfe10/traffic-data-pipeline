from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="traffic_pipeline",
    start_date=datetime(2026, 7, 20),
    schedule="*/5 * * * *",
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract_data",
        bash_command="""
        cd /opt/project/src &&
        python extract.py
        """
    )

    dbt = BashOperator(
        task_id="dbt_run",
        bash_command="""
        cd /opt/project/traffic_dbt &&
        dbt run
        """
    )

    extract >> dbt