"""Product rules, independent of Flask and browser validation."""

from dataclasses import dataclass
from datetime import date
from typing import Mapping

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
