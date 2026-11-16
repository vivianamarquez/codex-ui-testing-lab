"""AC-01–09: normal searches, boundaries, rejection, recovery, and editing."""

from datetime import datetime
import re

import pytest
from playwright.sync_api import expect

from tests.helpers import (
    LABELS, assert_fields, assert_options, assert_summary, field,
    search, submitted_search, trip,
)


def test_defaults_and_required_fields(page):
    assert_fields(page, trip(passengers="1"))
    for name in LABELS:
        expect(field(page, name)).to_have_attribute("required", "")
    for name in ("departure", "return_date"):
        expect(field(page, name)).to_have_attribute("min", "2030-01-15")


@pytest.mark.parametrize("passengers", ["1", "2", "9"])
def test_valid_search_and_edit_preserve_every_value(page, passengers):
    values = trip(passengers=passengers)
    search(page, values)
    assert_summary(page, values)
    assert_options(page, values)
    page.get_by_role("link", name="Edit search", exact=True).click()
    assert_fields(page, values)  # Regression: edit URL previously dropped passengers.


@pytest.mark.parametrize("day", ["2030-01-15", "2030-07-14"])
def test_same_day_at_both_schedule_boundaries(page, day):
    values = trip(origin="JFK", destination="LAX", departure=day, return_date=day, passengers="9")
    search(page, values)
    assert_summary(page, values)
    assert_options(page, values)
    for number in (1, 2):
        option = page.get_by_role("article", name=f"Option {number}", exact=True)
        times = option.locator("time")
        expect(times).to_have_count(4)
        outbound_arrival = datetime.fromisoformat(times.nth(1).get_attribute("datetime"))
        return_departure = datetime.fromisoformat(times.nth(2).get_attribute("datetime"))
        assert return_departure > outbound_arrival


@pytest.mark.parametrize("changes", [
    {"origin": "JFK", "destination": "SFO"},
    {"origin": "SFO", "destination": "JFK"},
    {"departure": "2030-07-14", "return_date": "2030-07-15"},
    {"departure": "2030-07-15", "return_date": "2030-07-15"},
])
@pytest.mark.parametrize("edit_link", ["Edit search", "Change search details"])
def test_empty_results_and_recovery_links(page, changes, edit_link):
    values = trip(passengers="9", **changes)
    search(page, values)
    assert_summary(page, values)
    expect(page.get_by_role("heading", name="No flights found", exact=True)).to_be_visible()
    expect(page.get_by_role("article")).to_have_count(0)
    page.get_by_role("link", name=edit_link, exact=True).click()
    assert_fields(page, values)


@pytest.mark.parametrize("changes,name,message", [
    ({"destination": "ATL"}, "destination", "different from your origin"),
    ({"return_date": "2030-01-21"}, "return_date", "on or after departure"),
    ({"departure": "2030-01-14"}, "departure", "on or after 2030-01-15"),
    ({"origin": "BOS"}, "origin", "supported origin"),
    ({"departure": "2030-02-30"}, "departure", "valid departure date"),
    ({"return_date": "not-a-date"}, "return_date", "valid return date"),
    *[({"passengers": value}, "passengers", "between 1 and 9") for value in ("0", "10", "1.0", "1.5", "abc")],
])
def test_invalid_submission_explains_error_and_preserves_valid_fields(page, changes, name, message):
    values = trip(**changes)
    submitted_search(page, values)
    alert = page.get_by_role("alert")
    expect(alert).to_contain_text(message)
    expect(field(page, name)).to_have_attribute("aria-invalid", "true")
    assert_fields(page, {key: value for key, value in values.items() if key != name})
    expect(page.get_by_role("article")).to_have_count(0)


@pytest.mark.parametrize("name", list(LABELS))
@pytest.mark.parametrize("omitted", [False, True], ids=["empty", "omitted"])
def test_each_field_is_required_on_submission(page, name, omitted):
    values = trip()
    if omitted:
        del values[name]
    else:
        values[name] = ""
    submitted_search(page, values)
    expect(page.get_by_role("alert")).to_be_visible()
    expect(field(page, name)).to_have_attribute("aria-invalid", "true")
    assert_fields(page, {key: value for key, value in values.items() if key != name})


def test_multiple_errors_can_be_corrected(page):
    submitted_search(page, trip(origin="BOS", departure="2030-02-30", passengers="1.0"))
    expect(page.get_by_role("alert").get_by_role("link")).to_have_count(3)
    assert_fields(page, {"destination": "JFK", "return_date": "2030-01-25"})
    page.get_by_role("alert").get_by_role("link", name=re.compile("supported origin")).click()
    expect(field(page, "origin")).to_be_focused()
    search(page, trip())
    assert_summary(page, trip())
    assert_options(page, trip())
    expect(page.get_by_role("alert")).to_have_count(0)


@pytest.mark.parametrize("name", ["departure", "return_date"])
@pytest.mark.parametrize("value,validity", [("", "valueMissing"), ("2030-01-14", "rangeUnderflow")])
def test_native_date_constraints_block_submission(page, name, value, validity):
    field(page, name).fill(value)
    page.get_by_role("button", name="Search flights", exact=True).click()
    expect(page.get_by_role("heading", name="Find flights", exact=True)).to_be_visible()
    expect(field(page, name)).to_be_focused()
    page.wait_for_function("([el, flag]) => el.validity[flag]", arg=[field(page, name).element_handle(), validity])


def test_keyboard_search_edit_and_back(page):
    page.keyboard.press("Tab")
    expect(page.get_by_role("link", name="Skip to content", exact=True)).to_be_focused()
    page.keyboard.press("Enter")
    page.keyboard.press("Tab")
    expect(field(page, "origin")).to_be_focused()
    page.keyboard.press("l")
    page.keyboard.press("Tab")
    expect(field(page, "destination")).to_be_focused()
    page.keyboard.press("s")
    # Native date segment tab stops vary by platform; semantic focus still uses keyboard input.
    field(page, "passengers").press("9")
    page.keyboard.press("Tab")
    submit = page.get_by_role("button", name="Search flights", exact=True)
    expect(submit).to_be_focused()
    page.keyboard.press("Shift+Tab")
    expect(field(page, "passengers")).to_be_focused()
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    values = trip(origin="LAX", destination="SFO", passengers="9")
    assert_summary(page, values)
    page.get_by_role("link", name="Edit search", exact=True).press("Enter")
    assert_fields(page, values)
    page.go_back()
    assert_summary(page, values)
