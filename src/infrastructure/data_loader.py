import pandas as pd
from database import get_db_engine

def load_csv_to_postgres(file_path, table_name):
    """Loads a CSV file into the PostgreSQL data warehouse."""
    engine = get_db_engine()
    if engine is not None:
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Success: Loaded data into {table_name}")

if __name__ == "__main__":
    source_file = "data/raw/T1.csv"
    load_csv_to_postgres(source_file, "wind_turbine_scada")
