"""An isolated deterministic server; each test gets a fresh browser context."""

from threading import Thread

import pytest
from playwright.sync_api import expect
from werkzeug.serving import make_server

from app import create_app


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    external = pytestconfig.getoption("--base-url") or pytestconfig.getini("base_url")
    if external:
        yield external.rstrip("/")
        return

    server = make_server(
        "127.0.0.1", 0, create_app({"DEMO_TODAY": "2030-01-15"}), threaded=True
    )
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        worker.join(timeout=5)
        server.server_close()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 900},
        "locale": "en-US",
        "timezone_id": "UTC",
        "device_scale_factor": 1,
    }


@pytest.fixture(autouse=True)
def open_search(page):
    page.goto("/")
    expect(page.get_by_role("heading", name="Find flights", exact=True)).to_be_visible()
    expect(page.get_by_text("Effective today:")).to_contain_text("2030-01-15")
