# 🌬️ Wind Energy Analytics Platform

A Data Engineering pipeline that ingests wind turbine SCADA telemetry, validates the readings, and calculates the average power output of the turbine.

Built with **Python**, **Apache Airflow**, **PostgreSQL** and **Docker**, using **Domain-Driven Design (DDD)** and the **Medallion Architecture**.

---

## 🎯 Main Goal
*(Business Analyst perspective)*

The goal is to calculate the average power output (kW) of a wind turbine from raw SCADA readings, ensuring invalid measurements never reach the final number.

### ⚠️ The Problem

SCADA systems produce large volumes of readings, and not all of them are usable:

* **Invalid readings:** sensors sometimes report negative power or wind speed, which are physically impossible. This dataset contains 57 such rows.
* **Repeated readings:** network retries can send the same measurement twice. A unique constraint on (timestamp, turbine) makes sure a reading is stored only once.

If these rows reach the calculation, the reported average is wrong. This pipeline validates every reading before it counts toward the result.

---

## 🏢 Business Context
*(Business Analyst perspective)*

Average power output is the basis for financial calculations in wind energy. Revenue depends on how much energy a turbine actually produced (kWh), which is derived from its power output over time.

Before any of that can be calculated, the underlying readings have to be trustworthy. A single negative value in the input shifts the average — and every number built on top of it.

This pipeline focuses on that first step: producing a validated average power figure that downstream calculations can rely on.

---

## 🧠 Proposed Solution & Architecture
*(Architect perspective)*

The data flows through three layers (**Medallion Architecture**), each reading from the previous one:

| Layer | Stage | What happens here |
| :--- | :--- | :--- |
| 🥉 **Bronze** | Raw ingestion | Stores CSV rows in PostgreSQL as text, exactly as they arrive — including invalid ones. |
| 🥈 **Silver** | Validation | Reads from Bronze and applies domain rules. Rejects negative power and wind speed; a unique constraint prevents the same reading being stored twice. |
| 🥇 **Gold** | Analytics | Reads from Silver and calculates the average power output. |

### Domain-Driven Design (DDD)

Business rules are kept separate from technical database code:

* `src/domain/` — validation rules for a single reading (`wind_turbine.py`). This part does not know a database exists.
* `src/application/` — the average power calculation (`wind_farm_service.py`).
* `src/infrastructure/` — PostgreSQL reads and writes (`database.py`).

This separation is what makes the unit tests in `tests/` run in milliseconds, without a database or Docker.

---

## 🔍 Decisions & Rationale
*(Architect + Data Analyst perspective)*

| Decision | Why we chose it |
| :--- | :--- |
| **Domain model validation** | Business rules live in plain Python classes, so they can be tested without a database or Docker. |
| **3 data layers (Medallion)** | Raw history stays intact in Bronze while Gold serves clean metrics. Each layer reads from the previous one, not from the source file. |
| **Bronze stores text, not numbers** | The raw layer must accept whatever the sensor sends. Rejecting bad values is Silver's job, not the database schema's. |
| **Schema created on first start (`init.sql`)** | The project runs straight after cloning, with no manual table creation. |
| **Tables truncated before each write** | Re-running the pipeline produces the same result instead of duplicating data. |
| **Unique constraint on (timestamp, turbine)** | Protects against the same reading being stored twice if the source repeats it. |
| **`max_active_runs=1`** | Prevents two runs from overwriting each other's data mid-pipeline. |
| **Apache Airflow** | In a real setup nobody re-runs a script by hand — Airflow schedules it and reports failures. |
| **Docker Compose** | The whole environment (Postgres + Airflow) starts with a single command. |

---

## 🛠️ Tech Stack

* **Language:** Python 3.10
* **Architecture:** Domain-Driven Design (DDD) & Medallion Architecture
* **Orchestration:** Apache Airflow
* **Database:** PostgreSQL 15
* **Testing:** pytest
* **Containers:** Docker & Docker Compose

---

## 📈 Result
*(Problem Solver / Product Owner perspective)*

Running the pipeline on the sample dataset:

| Layer | Rows |
| :--- | ---: |
| Bronze | 50,530 |
| Silver | 50,473 |
| Gold | 1 |

**57 readings were rejected** by the Silver layer — real invalid values present in the source data, not synthetic ones. The final result is an average power output of **1,309 kW**.

Re-running the pipeline produces the same numbers: the layers truncate before writing, so repeated runs do not duplicate data.

---

## ▶️ How to Run

Start the environment:

    docker compose up -d

This starts:

* **PostgreSQL** on port `5434` — the bronze, silver and gold tables are created automatically on first start
* **Airflow** at `http://localhost:8080`

Get the Airflow login password (generated on first start):

    docker exec wind_airflow cat /opt/airflow/standalone_admin_password.txt

If that file doesn't exist yet, Airflow is still starting — wait a minute. You can also set your own password:

    docker exec wind_airflow airflow users reset-password --username admin --password admin

Then open Airflow, find the `wind_energy_medallion_pipeline` DAG, enable it and trigger a run.

---

## 🧪 Tests

The domain rules run without a database or Docker:

    pip install pytest
    python -m pytest tests/ -v

The tests cover the validation rules (negative power, negative wind speed, wrong types) and the division-by-zero guard in the efficiency calculation.

---

## 📚 Sources

* **Architecture:** [Databricks Medallion Architecture Guide](https://www.databricks.com/glossary/medallion-architecture)
* **Methodology:** Domain-Driven Design (DDD)
* **Dataset:** Wind turbine SCADA data (Kaggle)

---

## 🛠️ Project Structure

```text
wind-energy-analytics-platform/
├── dags/
│   └── wind_farm_dag.py           # Airflow: what runs, in what order
├── data/
│   └── raw/
│       └── T1.csv                 # SCADA readings from turbine T1
├── src/
│   ├── domain/
│   │   └── wind_turbine.py        # Validation rules for a single reading
│   ├── application/
│   │   └── wind_farm_service.py   # Average power calculation
│   └── infrastructure/
│       └── database.py            # PostgreSQL reads and writes
├── tests/
│   └── test_wind_turbine.py       # Unit tests for the domain rules
├── docker-compose.yml             # Postgres + Airflow
├── init.sql                       # Creates bronze/silver/gold tables
├── pyproject.toml
└── README.md
```
