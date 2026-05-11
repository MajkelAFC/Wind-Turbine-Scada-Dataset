import csv
# Import the turbine domain model to ensure data follows business rules
from src.domain.wind_turbine import WindTurbine


class TurbineRepository:
    """
    Repository class responsible for loading wind turbine data from external CSV files.
    This acts as an Infrastructure layer in DDD, translating raw data into Domain objects.
    """

    def __init__(self, file_path):
        # Initialize the repository with the path to the data source
        self.file_path = file_path

    def load_turbines(self):
        """
        Reads the CSV file, cleans the data, and returns a list of WindTurbine objects.
        """
        turbines = []

        # Open the CSV file for reading
        with open(self.file_path, "r") as file:
            # DictReader uses the first line of the CSV as keys for each row dictionary
            reader = csv.DictReader(file)

            # Iterate through each record in the data set
            for row in reader:
                # Extract the active power and convert to float
                raw_power = float(row["LV ActivePower (kW)"])

                # Data Cleaning: SCADA systems sometimes record small negative values.
                # We enforce a floor of 0 to satisfy domain validation rules.
                clean_power = max(0, raw_power)

                # Map CSV columns to the WindTurbine Domain Model.
                # Note: 'turbine_id' is set to 'T1' as it's missing in the raw T1.csv file.
                t = WindTurbine(
                    turbine_id="T1",
                    active_power=clean_power,
                    wind_speed=float(row["Wind Speed (m/s)"])
                )

                # Collect the valid domain object into our list
                turbines.append(t)

        # Return the collection of domain objects to the application layer
        return turbines