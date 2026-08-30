CREATE TABLE IF NOT EXISTS wind_data_bronze (
    id SERIAL PRIMARY KEY,
    date_time VARCHAR(50),
    turbine_id VARCHAR(50),
    active_power VARCHAR(50),
    wind_speed VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS wind_data_silver (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    turbine_id VARCHAR(50),
    active_power NUMERIC,
    wind_speed NUMERIC
);

CREATE TABLE IF NOT EXISTS wind_data_gold (
    id SERIAL PRIMARY KEY,
    calculated_at TIMESTAMP,
    average_power_mw NUMERIC
);
