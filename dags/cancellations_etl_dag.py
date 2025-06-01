import sys
sys.path.insert(0, "/opt/airflow/scripts")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from extract_data import download_csv
from transform_data import clean_cancellation_data
from load_to_db import load_cancellations_to_postgres
import os

# Define the URLS for the data sources
DATA_URLS = {
    "train_delays": "https://dataportal.orr.gov.uk/statistics/table-3184.csv",
    "cancellations": "https://dataportal.orr.gov.uk/media/3024/table-3124.csv",
    "punctuality": "https://dataportal.orr.gov.uk/media/3025/table-3138.csv",
}

RAW_DATA_DIR = "data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Define the function to download CSV files
def extract_data():
    for name, url in DATA_URLS.items():
        download_csv(name, url)

# Define the DAG
with DAG(
    'cancellations_etl_dag',
    description='ETL pipeline for UK Train Cancellations data',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    # Define the tasks
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        dag=dag
    )
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=clean_cancellation_data,
        dag=dag
    )

    load_task = PythonOperator(
        task_id='load_to_postgresql',
        python_callable=load_cancellations_to_postgres,
        dag=dag
    )

    # Set the task dependencies
    transform_task >> load_task

print("Cancellations ETL DAG has been defined.")
