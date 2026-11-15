from datetime import timedelta

from flask import Blueprint, current_app, render_template, request, url_for

from . import effective_today
from .fixtures import SCHEDULE_DAYS, flight_options
from .search import AIRPORTS, FIELDS, validate_search

bp = Blueprint("flights", __name__)


def page_context(today):
    return {"airports": AIRPORTS, "today": today,
            "schedule_end": today + timedelta(days=SCHEDULE_DAYS)}


@bp.get("/")
def search():
    today = effective_today(current_app)
    defaults = {
        "origin": "ATL", "destination": "JFK",
        "departure": (today + timedelta(days=7)).isoformat(),
        "return_date": (today + timedelta(days=10)).isoformat(),
        "passengers": "1",
    }
    values = {field: request.args.get(field, defaults[field]) for field in FIELDS}
    return render_template("search.html", values=values, errors={}, **page_context(today))


@bp.get("/results")
def results():
    today = effective_today(current_app)
    values = {field: request.args.get(field, "") for field in FIELDS}
    trip, errors = validate_search(values, today)
    if errors:
        return render_template("search.html", values=values, errors=errors,
                               **page_context(today)), 422
    return render_template(
        "results.html", trip=trip, options=flight_options(trip, today),
        edit_url=url_for("flights.search", **trip.parameters()), **page_context(today),
    )
