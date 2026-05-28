# Import tools we need for this project
from src.infrastructure.database import PostgresTurbineRepository
from src.infrastructure.turbine_repository import TurbineRepository
from src.application.wind_farm_service import WindFarmService
from datetime import datetime
from pathlib import Path
import csv

# Find the path to our T1.csv file
base_dir = Path(__file__).resolve().parent
csv_file = base_dir / "data" / "raw" / "T1.csv"

# Create an empty list to hold raw data from CSV
raw_rows = []

# Connect to our PostgreSQL database with login data
postgres = PostgresTurbineRepository(
    host="wind_postgres_dw",
    database="wind_energy_dw",
    user="admin",
    password="admin_password"
)

# ==========================================
# 1. BRONZE LAYER (Save raw data)
# ==========================================
# Open the CSV file to read it
with open(csv_file, mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the first row with column names
    # Go through every row in the file
    for row in reader:
        # Save turbine ID, power, and wind speed into our list
        raw_rows.append(("T1", row[1], row[2]))

# Send all raw data to the bronze table in database
postgres.save_bronze(raw_rows)

# ==========================================
# 2. SILVER LAYER (Save clean data as objects)
# ==========================================
# Create a repository object and give it the file path string
repo = TurbineRepository(str(csv_file))

# Use the repository to clean data and give us a list of turbine objects
clean_turbines = repo.load_turbines()

# Send all clean turbine objects to the silver table in database
postgres.save_silver(clean_turbines)

# ==========================================
# 3. GOLD LAYER (Save final business result)
# ==========================================
# Create a service object to do the math
service = WindFarmService()

# Calculate the average power using our clean turbine list
avg_power = service.calculate_average_power(clean_turbines)

# Get the exact time right now
current_time = datetime.now()

# Send the current time and the average power to the gold table
postgres.save_gold(current_time, avg_power)

# Print success message on the screen
print(f"Success: Gold layer updated! Avg Power: {avg_power:.2f} MW")