# Wind Energy Analytics Platform

The main goal of this script is to read a large CSV file containing wind turbine metrics, clean the data based on business rules, calculate the average power, and save everything into a PostgreSQL database.

## Specification

* **Domain-Driven Design (DDD):** I structured my code into separate layers (Domain, Application, Infrastructure). This keeps the business logic completely separate from database frameworks.
* **Data Cleaning:** I used Python to clean raw SCADA data, like fixing negative values recorded by systems and ensuring data types are correct before saving.
* **Docker & Docker Compose:** Instead of installing database servers on my laptop, I containerized the app. The database and backend run in isolated virtual environments.
* **Apache Airflow:** I moved away from manual script execution. I wrote a custom DAG that tells Airflow to automatically run the Python pipeline.
* **Pathlib Module:** I learned how to use dynamic absolute paths instead of relative strings, so the script runs successfully both on my local machine and inside Docker containers.

---

## Project Structure

├── dags/
│   └── wind_farm_dag.py             # Airflow configuration file (DAG)
├── src/
│   ├── domain/
│   │   └── wind_turbine.py          # Domain model with business rules
│   ├── application/
│   │   └── wind_farm_service.py     # Application logic (averages calculation)
│   └── infrastructure/
│       ├── turbine_repository.py    # CSV file reader implementation
│       └── database.py              # PostgreSQL repository connection
├── data/
│   └── raw/
│       └── T1.csv                   # Raw source telemetry data
├── main.py                          # Main entry point to run the script
├── docker-compose.yaml              # Docker configuration for Postgres and Airflow
└── pyproject.toml                   # Project dependencies (managed by uv)


---

## How to Run the Project

### 1. Prerequisites
You only need **Docker** and **Git** installed on your system.

### 2. Startup Containers
Open your terminal in the project directory and run:
```bash
docker-compose up -d

This will automatically download and start PostgreSQL and Apache Airflow services in the background.
3. Run the Pipeline via Airflow

    Open your browser and go to http://localhost:8080 to access the Airflow panel.

    Find the pipeline named wind_energy_etl_pipeline.

    Turn the toggle switch to Active (blue).

    Click the Play button (Trigger DAG) on the right side to execute the pipeline.

4. Verify Success

You can click on the task, open the Logs, and scroll to the bottom. When the processing finishes, you will see my script output:
Plaintext

INFO - Average Power of the farm: 1307.68MW
INFO - Success: Data saved to PostgreSQL!

How to Stop

To close all services and free up your computer's RAM memory:
Bash

docker-compose down
