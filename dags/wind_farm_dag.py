from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 5, 17),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG context
with DAG(
    'wind_energy_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for wind turbine data analytics',
    schedule_interval='@daily',
    catchup=False,

) as dag:
# Task to run the ETL pipeline script
    run_etl_task = BashOperator(
        task_id='run_wind_energy_etl',
        bash_command='python /opt/airflow/main.py',
    )