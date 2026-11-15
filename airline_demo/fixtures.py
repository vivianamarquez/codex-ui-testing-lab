"""Repeatable synthetic flight schedules."""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

from .search import Search

SCHEDULE_DAYS = 180
# Synthetic route durations in hours.
ROUTE_HOURS = {
    frozenset(("ATL", "JFK")): 2,
    frozenset(("ATL", "LAX")): 5,
    frozenset(("ATL", "SFO")): 5,
    frozenset(("JFK", "LAX")): 6,
    frozenset(("LAX", "SFO")): 1,
}


@dataclass(frozen=True)
class Leg:
    identifier: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime


@dataclass(frozen=True)
class FlightOption:
    outbound: Leg
    inbound: Leg


def flight_options(search: Search, today: date):
    """Two round trips for scheduled routes inside today's inclusive window.

    JFK–SFO has an empty schedule in both directions.
    All times use UTC. Even a same-day return departs after outbound arrival.
    """
    duration = ROUTE_HOURS.get(frozenset((search.origin, search.destination)))
    end = today + timedelta(days=SCHEDULE_DAYS)
    if duration is None or not today <= search.departure <= search.return_date <= end:
        return []
    options = []
    for index in range(2):
        outbound = datetime.combine(search.departure, time(8 + index), timezone.utc)
        inbound = datetime.combine(search.return_date, time(16 + index), timezone.utc)
        options.append(FlightOption(
            Leg(f"DEMO-{101 + index * 2}", search.origin, search.destination,
                outbound, outbound + timedelta(hours=duration)),
            Leg(f"DEMO-{102 + index * 2}", search.destination, search.origin,
                inbound, inbound + timedelta(hours=duration)),
        ))
    return options
