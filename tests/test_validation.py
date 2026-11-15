from datetime import date

import pytest

from airline_demo import create_app, effective_today
from airline_demo.search import validate_search


@pytest.mark.parametrize("overrides,field", [
    ({"destination": "ATL"}, "destination"),
    ({"origin": "XYZ"}, "origin"),
    ({"destination": ""}, "destination"),
    ({"departure": "2030-01-14"}, "departure"),
    ({"return_date": "2030-01-21"}, "return_date"),
    ({"departure": "2030-02-30"}, "departure"),
    ({"return_date": "not-a-date"}, "return_date"),
    ({"departure": "20300122"}, "departure"),
    ({"passengers": "0"}, "passengers"),
    ({"passengers": "10"}, "passengers"),
    ({"passengers": "-1"}, "passengers"),
    ({"passengers": "1.5"}, "passengers"),
    ({"passengers": "two"}, "passengers"),
    ({"passengers": ""}, "passengers"),
])
def test_invalid_values(valid_parameters, demo_today, overrides, field):
    trip, errors = validate_search(valid_parameters | overrides, demo_today)
    assert trip is None
    assert field in errors
    assert errors[field]


@pytest.mark.parametrize("passengers", ["1", "9"])
def test_today_same_day_and_passenger_boundaries(valid_parameters, demo_today, passengers):
    params = valid_parameters | {"departure": demo_today.isoformat(),
                                "return_date": demo_today.isoformat(), "passengers": passengers}
    trip, errors = validate_search(params, demo_today)
    assert errors == {}
    assert trip.parameters() == params


def test_missing_fields_are_all_reported(demo_today):
    trip, errors = validate_search({}, demo_today)
    assert trip is None
    assert set(errors) == {"origin", "destination", "departure", "return_date", "passengers"}


@pytest.mark.parametrize("bad_date", ["", "tomorrow", "2030-02-30", "20300115"])
def test_bad_demo_date_fails_at_startup(bad_date):
    with pytest.raises(ValueError, match="DEMO_TODAY"):
        create_app({"DEMO_TODAY": bad_date})


def test_environment_date_is_used(monkeypatch):
    monkeypatch.setenv("DEMO_TODAY", "2040-02-29")
    assert effective_today(create_app()) == date(2040, 2, 29)


def test_default_clock_is_explicitly_utc(monkeypatch):
    from datetime import datetime, timezone

    class Clock:
        @staticmethod
        def now(tz):
            assert tz is timezone.utc
            return datetime(2040, 2, 29, tzinfo=tz)

    monkeypatch.delenv("DEMO_TODAY", raising=False)
    monkeypatch.setattr("airline_demo.datetime", Clock)
    assert effective_today(create_app()) == date(2040, 2, 29)
