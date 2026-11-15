"""Infrastructure check only. The learner will add test_flight_search.py."""

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.browser


def test_search_page_is_ready(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.get_by_role("heading", name="Where will you go next?")).to_be_visible()
    expect(page.get_by_label("Origin airport")).to_be_visible()
    expect(page.get_by_role("button", name="Search flights")).to_be_enabled()
