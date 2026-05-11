# Pandas is a powerful library for data tables (called DataFrames)
import pandas as pd
# Import our own function to connect to the database
from database import get_db_engine


def verify_turbine_data():
    """verifying turbines data"""
    # 1. Start the connection 'engine' to the database
    engine = get_db_engine()

    # 2. Write a SQL command to ask for the first 5 rows
    query = "SELECT * FROM wind_turbine_scada LIMIT 5;"

    # 3. Use Pandas to run the query and put results into a table (df)
    df = pd.read_sql(query, engine)

    # 4. Show the table on the screen
    print(df)


# This part makes sure the function runs only if we start this file directly
if __name__ == "__main__":
    verify_turbine_data()