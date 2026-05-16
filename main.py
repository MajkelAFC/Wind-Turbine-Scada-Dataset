# Import our classes from different folders
from src.infrastructure.turbine_repository import TurbineRepository
from src.application.wind_farm_service import WindFarmService
from src.infrastructure.database import PostgresTurbineRepository

# Set the path to the data file
path = "data/raw/T1.csv"

# Create a repository object to handle files
repo = TurbineRepository(path)

# Load all turbines from CSV and save them in a list
turbines = repo.load_turbines()

# Loop through the list and print a report for each turbine
for t in turbines:
    print(t.get_report())

# Create a service object to do calculations
service = WindFarmService()

# Calculate the avg of power from all working turbines
avg_power = service.calculate_average_power(turbines)

# Print the final result on the screen
print(f"Average Power of the farm: {avg_power:.2f}MW")

# Create an instance of object
postgres = PostgresTurbineRepository(host="localhost", database="wind_energy_dw",
                                     user="admin",password="admin_password")

try:
    postgres.save(turbines)
    print("Success: Data saved to PostgreSQL!")
except Exception as e:
    print(f"Error: {e}")