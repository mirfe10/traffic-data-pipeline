FROM apache/airflow:2.11.0

USER root
RUN apt-get update && apt-get install -y gcc build-essential

USER airflow

COPY airflow-requirements.txt /airflow-requirements.txt

RUN pip install --no-cache-dir -r /airflow-requirements.txt