"""Geometry regressions from the reviewed UI, at actual CSS viewport sizes."""

import re

import pytest
from playwright.sync_api import expect

from tests.helpers import (
    LABELS, assert_fields, assert_no_horizontal_overflow, assert_options,
    assert_readable_controls, assert_summary, field, search, submitted_search, trip,
)


@pytest.mark.parametrize("width,height", [
    (390, 844), (480, 844), (481, 844),
    (600, 844), (601, 844), (768, 1024), (896, 778), (1280, 900),
])
def test_form_results_errors_and_edit_fit_viewport(page, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.wait_for_function(
        "([w, h]) => innerWidth === w && innerHeight === h && visualViewport.scale === 1",
        arg=[width, height],
    )
    # Font metrics must reflect the loaded UI, not a transient fallback font.
    page.evaluate("document.fonts.ready")
    values = trip(passengers="9")
    field(page, "passengers").select_option("9")
    assert_no_horizontal_overflow(page)
    assert_readable_controls(page)  # Regression: 481px dates/passenger text clipped.
    submit = page.get_by_role("button", name="Search flights", exact=True)
    # Regression: a translated button previously overlapped the passenger control.
    page.wait_for_function(
        """([button, ...fields]) => button.getBoundingClientRect().top >=
            Math.max(...fields.map(el => el.getBoundingClientRect().bottom))""",
        arg=[submit.element_handle(), *[field(page, name).element_handle() for name in LABELS]],
    )
    if width >= 768:
        for name in LABELS:
            expect(field(page, name)).to_be_in_viewport()
        expect(submit).to_be_in_viewport()
    search(page, values)
    assert_summary(page, values)
    assert_options(page, values)
    assert_no_horizontal_overflow(page)
    page.get_by_role("link", name="Edit search", exact=True).click()
    assert_fields(page, values)
    assert_readable_controls(page)
    submitted_search(page, trip(departure="2030-02-30", return_date="2030-03-02"))
    expect(page.get_by_role("alert")).to_contain_text("valid departure date")
    assert_fields(page, {"origin": "ATL", "destination": "JFK", "return_date": "2030-03-02", "passengers": "2"})
    assert_no_horizontal_overflow(page)
    assert_readable_controls(page)
    search(page, trip(departure="2030-03-01", return_date="2030-03-02"))
    assert_summary(page, trip(departure="2030-03-01", return_date="2030-03-02"))
    assert_no_horizontal_overflow(page)


def test_desktop_button_aligns_with_helper_and_select_arrows_are_inset(page):
    page.set_viewport_size({"width": 896, "height": 778})
    button = page.get_by_role("button", name="Search flights", exact=True)
    helper = page.get_by_text("Same-day returns are welcome.", exact=False)
    expect(button).to_be_visible()
    expect(helper).to_be_visible()
    page.wait_for_function(
        """([button, helper]) => {
            const b = button.getBoundingClientRect(), h = helper.getBoundingClientRect();
            return Math.abs((b.top + b.height / 2) - (h.top + h.height / 2)) <= 1;
        }""",
        arg=[button.element_handle(), helper.element_handle()],
    )
    # Native arrow pixels aren't in the DOM. Preserve the reviewed custom-arrow inset.
    for name in ("origin", "destination", "passengers"):
        expect(field(page, name)).to_have_css("background-image", re.compile(r"^url\("))
        expect(field(page, name)).to_have_css("background-position-x", "calc(100% - 14px)")


@pytest.mark.parametrize("viewport", [(390, 844), (768, 1024)])
def test_empty_state_fits_and_preserves_values_on_edit(page, viewport):
    page.set_viewport_size({"width": viewport[0], "height": viewport[1]})
    values = trip(origin="JFK", destination="SFO", passengers="9")
    search(page, values)
    expect(page.get_by_role("heading", name="No flights found", exact=True)).to_be_visible()
    assert_summary(page, values)
    assert_no_horizontal_overflow(page)
    page.get_by_role("link", name="Change search details", exact=True).click()
    assert_fields(page, values)
    assert_no_horizontal_overflow(page)
    assert_readable_controls(page)
