class WindTurbine:
    def __init__(self, turbine_id: str, active_power: float, wind_speed: float):
        # Validate turbine_id
        if not isinstance(turbine_id, str):
            raise TypeError("Turbine ID must be a string")
        self.turbine_id = turbine_id

        # Validate active_power
        if not isinstance(active_power, (float, int)):
            raise TypeError("Active power must be a float or int")
        if active_power < 0:
            raise ValueError("Active power cannot be negative")
        self.active_power = active_power

        # Validate wind_speed
        if not isinstance(wind_speed, (float, int)):
            raise TypeError("Wind speed must be a float or int")
        if wind_speed < 0:
            raise ValueError("Wind speed cannot be negative")
        self.wind_speed = wind_speed

    def is_operating(self) -> bool:
        # Returns True if the turbine is generating power
        return self.active_power > 0

    def get_report(self) -> str:
        # Returns a formatted status report for the turbine
        return f"Turbine: {self.turbine_id} about power: {self.active_power} got now {self.wind_speed}"

    def calculate_efficiency(self) -> str:
        # Calculates and returns the efficiency based on power and wind speed
        if self.wind_speed == 0:
            return "Efficiency is: 0"

        result = self.active_power / self.wind_speed
        return f"Efficiency is: {result}"
    
    def get_active_power(self):
        return self.active_power