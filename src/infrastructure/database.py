import psycopg2
from src.domain.wind_turbine import WindTurbine

class PostgresTurbineRepository:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def save(self, turbines):
        with psycopg2.connect(host=self.host, database=self.database,
                              user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            for turbine in turbines:
                cur.execute(
                    "INSERT INTO wind_turbines (turbine_id, active_power, wind_speed) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (turbine.turbine_id, turbine.active_power, turbine.wind_speed)
                )
