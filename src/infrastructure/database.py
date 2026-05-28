import psycopg2


class PostgresTurbineRepository:
    def __init__(self, database, host, user, password):
        self.database = database
        self.host = host
        self.user = user
        self.password = password

    def save_bronze(self, raw_data_list):
        # Open connection to Postgres database
        with psycopg2.connect(database=self.database, host=self.host, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            # Loop and insert all raw rows into the bronze table
            for raw_data in raw_data_list:
                cur.execute("INSERT INTO wind_data_bronze (turbine_id, active_power, wind_speed) VALUES (%s, %s, %s)",
                            raw_data)

    def save_silver(self, clean_turbines):
        # Open connection to Postgres database
        with psycopg2.connect(database=self.database, host=self.host, user=self.user, password=self.password) as conn:
            cur = conn.cursor()

            # Tell Postgres to use Day-Month-Year format for dates
            cur.execute("SET datestyle = 'iso, dmy';")

            # Loop and insert clean data, ignore duplicates using ON CONFLICT
            for turbine in clean_turbines:
                cur.execute(
                    "INSERT INTO wind_data_silver (created_at, turbine_id, active_power, wind_speed) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (turbine.date_time, turbine.turbine_id, turbine.active_power, turbine.wind_speed)
                )

    def save_gold(self, timestamp, average_power):
        # Open connection to Postgres database
        with psycopg2.connect(database=self.database, host=self.host, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            # Insert the final calculated average power report
            cur.execute(
                "INSERT INTO wind_data_gold (calculated_at, average_power_mw) VALUES (%s, %s)",
                (timestamp, average_power)
            )