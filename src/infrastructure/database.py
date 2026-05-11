import psycopg2
from sqlalchemy import create_engine

# Connection string for our PostgreSQL Docker container
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL = "postgresql://admin:admin_password@localhost:5432/wind_energy_dw"

def get_db_engine():
    """
    Creates and returns a SQLAlchemy engine for database connection.
    This is part of our Infrastructure layer.
    """
    try:
        engine = create_engine(DATABASE_URL)
        print("Success: Connected to the PostgreSQL data warehouse.")
        return engine
    except Exception as error:
        print(f"Error: Could not create database engine. Details: {error}")
        return None

if __name__ == "__main__":
    # Test the connection when the script is run directly
    get_db_engine()
