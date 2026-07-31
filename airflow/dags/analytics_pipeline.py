from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="analytics_pipeline",
    start_date=datetime(2026, 7, 20),
    schedule="*/15 * * * *",
    catchup=False,
) as dag:

    analytics = BashOperator(
        task_id="dbt_analytics",
        bash_command="""
        cd /opt/project/traffic_dbt &&
        dbt run --select traffic_weather_analysis weather_impact location_weather
        """
    )