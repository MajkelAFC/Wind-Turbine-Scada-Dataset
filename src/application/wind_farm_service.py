# This service handles logic for the whole wind farm
class WindFarmService:
    def calculate_total_power(self, turbines):
        # Start with zero power
        total_power = 0

        # Look at each turbine in the list one by one
        for t in turbines:
            # Check if the turbine is working (generating power)
            if t.is_operating():
                # Add its power to our total sum
                # Note: we need () because get_active_power is a method/function
                total_power += t.get_active_power()

        # Give back the final sum
        return total_power