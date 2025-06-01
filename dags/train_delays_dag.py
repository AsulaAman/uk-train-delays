import sys
sys.path.insert(0, "/opt/airflow/scripts")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from extract_data import download_csv
from transform_data import clean_train_delays_data
from load_train_delays_to_db import load_train_delays_to_postgres
import os

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
    'train_delays_dag',
    description='ETL pipeline for UK Train Delays data',
    schedule_interval='@weekly',
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

# Define the tasks
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=clean_train_delays_data,
    )

    load_task = PythonOperator(
        task_id='load_to_db',
        python_callable=load_train_delays_to_postgres,
    )
    # Set the task dependencies
    extract_task >> transform_task >> load_task

print("Train Delays ETL DAG has been defined.")
