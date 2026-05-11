import csv
# Import the turbine model to create objects
from wind_turbine import WindTurbine


class TurbineRepository:
    def __init__(self, file_path):
        # Save the path to our CSV file
        self.file_path = file_path

    def load_turbines(self):
        # Create an empty list to store our turbine objects
        turbines = []

        # Open the file in 'read' mode
        with open(self.file_path, "r") as file:
            # Use DictReader to see column names from the first line
            reader = csv.DictReader(file)

            # Go through every line in the file
            for row in reader:
                # Create a new WindTurbine object using data from the row
                # We convert text from CSV to float numbers here
                t = WindTurbine(
                    row["turbine_id"],
                    float(row["active_power"]),
                    float(row["wind_speed"])
                )
                # Add the new turbine to our list
                turbines.append(t)

                # Return the full list of objects to the program
        return turbines