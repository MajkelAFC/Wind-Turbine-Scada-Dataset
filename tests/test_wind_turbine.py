import pytest

from src.domain.wind_turbine import WindTurbine


def make_turbine(active_power=100.0, wind_speed=10.0):
    """Helper: build a valid turbine, overriding only what a test cares about."""
    return WindTurbine(
        date_time="2018-01-01 00:00",
        turbine_id="T1",
        active_power=active_power,
        wind_speed=wind_speed,
    )


def test_valid_reading_is_accepted():
    turbine = make_turbine()
    assert turbine.active_power == 100.0


def test_negative_power_is_rejected():
    with pytest.raises(ValueError):
        make_turbine(active_power=-5.0)


def test_negative_wind_speed_is_rejected():
    with pytest.raises(ValueError):
        make_turbine(wind_speed=-2.0)


def test_turbine_id_must_be_text():
    with pytest.raises(TypeError):
        WindTurbine(
            date_time="2018-01-01 00:00",
            turbine_id=1,
            active_power=100.0,
            wind_speed=10.0,
        )


def test_efficiency_handles_zero_wind_speed():
    """Dividing by zero would crash — the class must guard against it."""
    turbine = make_turbine(wind_speed=0.0)
    assert turbine.calculate_efficiency() == "Efficiency is: 0"


def test_turbine_is_not_operating_at_zero_power():
    turbine = make_turbine(active_power=0.0)
    assert turbine.is_operating() is False
