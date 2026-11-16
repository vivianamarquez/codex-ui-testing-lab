"""The verified search-and-edit journey: AC-01, AC-02, and AC-08."""

import re

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.browser


def test_round_trip_search_preserves_trip_details(page: Page, base_url: str):
    # Both the hosted demo and the local server use 2030-01-15 as today.
    page.goto(base_url)
    page.get_by_label("Origin airport", exact=True).select_option("ATL")
    page.get_by_label("Destination airport", exact=True).select_option("JFK")
    page.get_by_label("Departure date", exact=True).fill("2030-01-22")
    page.get_by_label("Return date", exact=True).fill("2030-01-25")
    page.get_by_label("Passengers", exact=True).select_option("2")
    page.get_by_role("button", name="Search flights", exact=True).press("Enter")

    # AC-01: submitting the valid search opens the results page.
    expect(page).to_have_url(re.compile(r"(?:/results\?|[?&]view=results(?:&|$))"))
    expect(page.get_by_role("heading", name="Your flight results", exact=True)).to_be_visible()

    # AC-02: check each value beside its label in the visible search summary.
    summary = page.get_by_role("region", name="Search summary", exact=True)
    expect(summary).to_be_visible()
    expected_summary = {
        "Origin airport": "Atlanta (ATL)",
        "Destination airport": "New York (JFK)",
        "Departure date": "2030-01-22",
        "Return date": "2030-01-25",
        "Passengers": "2",
    }
    for label, expected_value in expected_summary.items():
        term = page.get_by_role("term").filter(has_text=re.compile(f"^{re.escape(label)}$"))
        # Each definition-list entry groups a label and value in one div.
        entry = summary.locator("div").filter(has=term)
        value = entry.get_by_role("definition")
        expect(value).to_be_visible()
        expect(value).to_have_text(expected_value)

    # AC-08: editing restores the exact values in all five form controls.
    summary.get_by_role("link", name="Edit search", exact=True).click()
    expect(page.get_by_role("heading", name="Where will you go next?", exact=True)).to_be_visible()
    expected_form = {
        "Origin airport": "ATL",
        "Destination airport": "JFK",
        "Departure date": "2030-01-22",
        "Return date": "2030-01-25",
        "Passengers": "2",
    }
    for label, expected_value in expected_form.items():
        control = page.get_by_label(label, exact=True)
        expect(control).to_be_visible()
        expect(control).to_have_value(expected_value)
