class WindTurbine:
    def __init__(self, date_time: str, turbine_id: str, active_power: float, wind_speed: float):
        # Check if date is a string text
        if not isinstance(date_time, str):
            raise TypeError("Date time must be a string")
        self.date_time = date_time

        # Check if ID is a string text
        if not isinstance(turbine_id, str):
            raise TypeError("Turbine ID must be a string")
        self.turbine_id = turbine_id

        # Check if power is a number and is not negative
        if not isinstance(active_power, (float, int)):
            raise TypeError("Active power must be a float or int")
        if active_power < 0:
            raise ValueError("Active power cannot be negative")
        self.active_power = active_power

        # Check if wind speed is a number and is not negative
        if not isinstance(wind_speed, (float, int)):
            raise TypeError("Wind speed must be a float or int")
        if wind_speed < 0:
            raise ValueError("Wind speed cannot be negative")
        self.wind_speed = wind_speed

    def is_operating(self) -> bool:
        # Returns True if the turbine makes any power
        return self.active_power > 0

    def get_report(self) -> str:
        # Returns a simple text report about the turbine status
        return f"[{self.date_time}] Turbine: {self.turbine_id} about power: {self.active_power} got now {self.wind_speed}"

    def calculate_efficiency(self) -> str:
        # Calculate efficiency, but check if wind speed is 0 to avoid crash
        if self.wind_speed == 0:
            return "Efficiency is: 0"

        result = self.active_power / self.wind_speed
        return f"Efficiency is: {result}"

    def get_active_power(self) -> float:
        # Just return the current active power value
        return self.active_power