"""Shared fixed date and automatic local server for Python browser tests."""

from datetime import date
from threading import Thread

import pytest
from werkzeug.serving import make_server

from airline_demo import create_app


@pytest.fixture(scope="session")
def demo_today():
    return date(2030, 1, 15)


@pytest.fixture(scope="session")
def app(demo_today):
    return create_app({"TESTING": True, "DEMO_TODAY": demo_today.isoformat()})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def valid_parameters():
    return {
        "origin": "ATL", "destination": "JFK", "departure": "2030-01-22",
        "return_date": "2030-01-25", "passengers": "2",
    }


@pytest.fixture(scope="session")
def base_url(request, app):
    """Respect --base-url; otherwise bind an ephemeral port, with no sleeps.

    The socket is listening before the thread starts, so requests wait for
    the server normally. Only browser tests that use base_url start it.
    """
    configured = request.config.getoption("--base-url")
    if configured:
        yield configured.rstrip("/")
        return
    server = make_server("127.0.0.1", 0, app, threaded=True)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
