# Import our classes from different folders
from src.infrastructure.turbine_repository import TurbineRepository
from src.application.wind_farm_service import WindFarmService

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

# Calculate the sum of power from all working turbines
total = service.calculate_total_power(turbines)

# Print the final result on the screen
print(f"Total Power of the farm: {total} MW")