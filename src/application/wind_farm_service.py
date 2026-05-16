# This service handles logic for the whole wind farm
class WindFarmService:
    def calculate_average_power(self, turbines):
        if not turbines:
            return 0

        total_power = sum(t.active_power for t in turbines)
        average_power = total_power / len(turbines)
        return average_power