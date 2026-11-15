from datetime import timedelta

import pytest

from airline_demo.fixtures import SCHEDULE_DAYS, flight_options
from airline_demo.search import AIRPORTS, validate_search


@pytest.mark.parametrize("origin,destination", [
    (origin, destination) for origin in AIRPORTS for destination in AIRPORTS if origin != destination
])
def test_schedule_consistency_on_all_routes(valid_parameters, demo_today, origin, destination):
    params = valid_parameters | {"origin": origin, "destination": destination,
                                "return_date": valid_parameters["departure"]}
    trip, errors = validate_search(params, demo_today)
    assert not errors
    options = flight_options(trip, demo_today)
    assert options == flight_options(trip, demo_today)
    assert len(options) == (0 if {origin, destination} == {"JFK", "SFO"} else 2)
    for option in options:
        assert (option.outbound.origin, option.outbound.destination) == (origin, destination)
        assert (option.inbound.origin, option.inbound.destination) == (destination, origin)
        assert option.outbound.departure.date() == trip.departure
        assert option.inbound.departure.date() == trip.return_date
        assert option.outbound.departure < option.outbound.arrival < option.inbound.departure < option.inbound.arrival


@pytest.mark.parametrize("days,expected", [(0, 2), (SCHEDULE_DAYS, 2), (SCHEDULE_DAYS + 1, 0)])
def test_schedule_window_is_inclusive(valid_parameters, demo_today, days, expected):
    travel_date = (demo_today + timedelta(days=days)).isoformat()
    trip, errors = validate_search(valid_parameters | {"departure": travel_date, "return_date": travel_date}, demo_today)
    assert not errors  # Outside the schedule is valid input, with no inventory.
    assert len(flight_options(trip, demo_today)) == expected
