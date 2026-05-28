# Wind Energy Analytics Platform

A simple Data Engineering pipeline built with Python, Apache Airflow, and PostgreSQL. The project processes wind turbine telemetry data using the **Medallion Architecture** (Bronze -> Silver -> Gold) and follows **Domain-Driven Design (DDD)** principles.

---

## Architecture Overview

The pipeline processes data through three distinct layers:
1. **Bronze Layer**: Raw CSV data is loaded into the database as an append-only log.
2. **Silver Layer**: Data is cleaned and validated using a Python domain model (`WindTurbine`). Only valid records with accurate timestamps are stored. Duplicates are handled using `ON CONFLICT DO NOTHING`.
3. **Gold Layer**: Business metrics (such as average power output) are calculated and saved for reporting.

---

## Tech Stack

* **Language:** Python 3.10
* **Orchestration:** Apache Airflow
* **Database:** PostgreSQL 15
* **Containerization:** Docker & Docker Compose

---

## How to Run the Project

### 1. Start the Environment
Run Docker Compose to start PostgreSQL and Apache Airflow:
```bash
docker compose up -d

2. Access Apache Airflow

    Open your browser and go to: http://localhost:8080

    Username: admin

    Password: To get the auto-generated password, run this command in your terminal:
    
docker compose exec airflow cat /opt/airflow/standalone_admin_password.txt

3. Run the Pipeline

    Find the wind_energy_medallion_pipeline DAG in the Airflow UI.

    Turn the switch to Active and click the Trigger button to execute the pipeline.
