"""Flight Lab: a local flight-search app."""

import os
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Mapping

from flask import Flask, render_template, request, url_for

AIRPORTS = {
    "ATL": "Atlanta",
    "JFK": "New York",
    "LAX": "Los Angeles",
    "SFO": "San Francisco",
}
FIELDS = ("origin", "destination", "departure", "return_date", "passengers")


@dataclass(frozen=True)
class Search:
    origin: str
    destination: str
    departure: date
    return_date: date
    passengers: int

    def parameters(self):
        return {
            "origin": self.origin,
            "destination": self.destination,
            "departure": self.departure.isoformat(),
            "return_date": self.return_date.isoformat(),
            "passengers": str(self.passengers),
        }


def validate_search(values: Mapping[str, str], today: date):
    """Return (Search, {}) or (None, field errors); never trust HTML controls."""
    errors = {}
    for field in ("origin", "destination"):
        if values.get(field) not in AIRPORTS:
            errors[field] = f"Choose a supported {field} airport."
    if not errors and values["origin"] == values["destination"]:
        errors["destination"] = "Choose a destination different from your origin."

    dates = {}
    for field, label in (("departure", "departure"), ("return_date", "return")):
        raw = values.get(field, "")
        try:
            parsed = date.fromisoformat(raw)
            if parsed.isoformat() != raw:
                raise ValueError
            dates[field] = parsed
        except (ValueError, TypeError):
            errors[field] = f"Enter a valid {label} date in YYYY-MM-DD format."
    if "departure" in dates and dates["departure"] < today:
        errors["departure"] = f"Departure must be on or after {today.isoformat()}."
    if len(dates) == 2 and dates["return_date"] < dates["departure"]:
        errors["return_date"] = "Return must be on or after departure. Same-day returns are welcome."

    passenger_value = values.get("passengers", "")
    if passenger_value not in tuple(str(n) for n in range(1, 10)):
        errors["passengers"] = "Choose between 1 and 9 passengers."
    if errors:
        return None, errors
    return Search(
        origin=values["origin"], destination=values["destination"],
        departure=dates["departure"], return_date=dates["return_date"],
        passengers=int(passenger_value),
    ), {}


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


def effective_today(app):
    """Use the configured demo date or the UTC calendar date."""
    return app.config["DEMO_TODAY"] or datetime.now(timezone.utc).date()


def page_context(today):
    return {"airports": AIRPORTS, "today": today,
            "schedule_end": today + timedelta(days=SCHEDULE_DAYS)}


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(DEMO_TODAY=os.environ.get("DEMO_TODAY"))
    if test_config:
        app.config.update(test_config)
    fixed_today = app.config["DEMO_TODAY"]
    if fixed_today is not None:
        try:
            parsed = date.fromisoformat(fixed_today)
            if parsed.isoformat() != fixed_today:
                raise ValueError
        except (TypeError, ValueError) as exc:
            raise ValueError("DEMO_TODAY must be a date in YYYY-MM-DD format.") from exc
        app.config["DEMO_TODAY"] = parsed

    @app.get("/")
    def search():
        today = effective_today(app)
        defaults = {
            "origin": "ATL", "destination": "JFK",
            "departure": (today + timedelta(days=7)).isoformat(),
            "return_date": (today + timedelta(days=10)).isoformat(),
            "passengers": "1",
        }
        values = {field: request.args.get(field, defaults[field]) for field in FIELDS}
        return render_template("search.html", values=values, errors={}, **page_context(today))

    @app.get("/results")
    def results():
        today = effective_today(app)
        values = {field: request.args.get(field, "") for field in FIELDS}
        trip, errors = validate_search(values, today)
        if errors:
            return render_template("search.html", values=values, errors=errors,
                                   **page_context(today)), 422
        return render_template(
            "results.html", trip=trip, options=flight_options(trip, today),
            edit_url=url_for("search", **{key: value for key, value in trip.parameters().items()
                                         if key != "passengers"}), **page_context(today),
        )

    return app
