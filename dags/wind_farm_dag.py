import sys
from pathlib import Path

# 1. CRITICAL: Setup python path BEFORE importing project modules
# Airflow execution environments need to know where the root directory is.
sys.path.append('/opt/airflow')

# 2. Standard and Airflow imports
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import csv

# 3. Project domain and infrastructure imports (now Python will find them perfectly!)
from src.infrastructure.database import PostgresTurbineRepository
from src.application.wind_farm_service import WindFarmService
from src.domain.wind_turbine import WindTurbine

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 5, 17),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define database connection and file paths for Airflow environment
base_dir = Path("/opt/airflow")
csv_file = base_dir / "data" / "raw" / "T1.csv"


def get_postgres_repo():
    """Helper function to create database repository instance"""
    return PostgresTurbineRepository(
        host="wind_postgres_dw",
        database="wind_energy_dw",
        user="admin",
        password="admin_password"
    )


# ==========================================
# Task functions for Medallion Architecture
# ==========================================

def run_bronze_layer():
    """Step 1: Read raw CSV and save to bronze table"""
    postgres = get_postgres_repo()
    postgres.truncate("wind_data_bronze")
    raw_rows = []

    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            raw_rows.append((row[0], "T1", row[1], row[2]))

    postgres.save_bronze(raw_rows)


def run_silver_layer():
    """Step 2: Clean data from bronze and save to silver table"""
    postgres = get_postgres_repo()
    postgres.truncate("wind_data_silver")
    raw_rows = postgres.read_bronze()

    clean_turbines = []
    for date_time, turbine_id, active_power, wind_speed in raw_rows:
        try:
            turbine = WindTurbine(
                date_time=date_time,
                turbine_id=turbine_id,
                active_power=float(active_power),
                wind_speed=float(wind_speed),
            )
            clean_turbines.append(turbine)
        except (TypeError, ValueError):
            continue

    postgres.save_silver(clean_turbines)


def run_gold_layer():
    """Step 3: Calculate average power from silver and save to gold table"""
    postgres = get_postgres_repo()
    postgres.truncate("wind_data_gold")
    silver_rows = postgres.read_silver()

    turbines = []
    for created_at, turbine_id, active_power, wind_speed in silver_rows:
        turbines.append(
            WindTurbine(
                date_time=str(created_at),
                turbine_id=turbine_id,
                active_power=float(active_power),
                wind_speed=float(wind_speed),
            )
        )

    service = WindFarmService()
    avg_power = service.calculate_average_power(turbines)
    postgres.save_gold(datetime.now(), avg_power)


# ==========================================
# DAG Context Definition
# ==========================================
with DAG(
        'wind_energy_medallion_pipeline',
        default_args=default_args,
        description='Medallion architecture ETL pipeline for wind turbine data',
        schedule_interval='@daily',
        catchup=False,
        max_active_runs=1,
) as dag:
    # Define Airflow Tasks using PythonOperator
    bronze_task = PythonOperator(
        task_id='load_to_bronze',
        python_callable=run_bronze_layer,
    )

    silver_task = PythonOperator(
        task_id='clean_to_silver',
        python_callable=run_silver_layer,
    )

    gold_task = PythonOperator(
        task_id='report_to_gold',
        python_callable=run_gold_layer,
    )

    # Set the pipeline workflow order (Dependencies)
    bronze_task >> silver_task >> gold_task
