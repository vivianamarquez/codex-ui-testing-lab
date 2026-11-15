"""Flask application setup and demo date."""

import os
from datetime import date, datetime, timezone

from flask import Flask


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

    from .routes import bp

    app.register_blueprint(bp)
    return app


def effective_today(app):
    """Use the configured demo date or the UTC calendar date."""
    return app.config["DEMO_TODAY"] or datetime.now(timezone.utc).date()
