"""Shared user-facing actions and assertions, not application logic."""

import re
from urllib.parse import urlencode

from playwright.sync_api import expect

LABELS = {
    "origin": "Origin airport",
    "destination": "Destination airport",
    "departure": "Departure date",
    "return_date": "Return date",
    "passengers": "Passengers",
}
AIRPORTS = {
    "ATL": "Atlanta (ATL)", "JFK": "New York (JFK)",
    "LAX": "Los Angeles (LAX)", "SFO": "San Francisco (SFO)",
}


def trip(**changes):
    return {
        "origin": "ATL", "destination": "JFK", "departure": "2030-01-22",
        "return_date": "2030-01-25", "passengers": "2", **changes,
    }


def field(page, name):
    return page.get_by_label(LABELS[name], exact=True)


def fill_search(page, values):
    for name, value in values.items():
        if name in ("origin", "destination", "passengers"):
            field(page, name).select_option(value)
        else:
            field(page, name).fill(value)


def search(page, values):
    fill_search(page, values)
    page.get_by_role("button", name="Search flights", exact=True).click()
    expect(page.get_by_role("heading", name="Your flight results", exact=True)).to_be_visible()


def submitted_search(page, values):
    """Exercise invalid submissions that native date/select controls cannot express."""
    return page.goto("/results?" + urlencode(values))


def assert_fields(page, values):
    for name, value in values.items():
        expect(field(page, name)).to_have_value(value)


def assert_summary(page, values):
    summary = page.get_by_role("region", name="Search summary", exact=True)
    expect(summary).to_be_visible()
    for name, value in values.items():
        # A term and its definition share a semantic definition-list item.
        term = summary.get_by_role("term").filter(has_text=re.compile(rf"^{LABELS[name]}$"))
        definition = term.locator("..").get_by_role("definition")
        expect(definition).to_have_text(AIRPORTS[value] if name in ("origin", "destination") else value)


def assert_options(page, values):
    expect(page.get_by_role("heading", name="2 round-trip options", exact=True)).to_be_visible()
    expect(page.get_by_role("article")).to_have_count(2)
    for number in (1, 2):
        option = page.get_by_role("article", name=f"Option {number}", exact=True)
        for label, origin, destination, day in (
            ("Outbound", values["origin"], values["destination"], values["departure"]),
            ("Return", values["destination"], values["origin"], values["return_date"]),
        ):
            leg = option.get_by_text(label, exact=True).locator("../..")
            expect(leg.get_by_text(day, exact=True)).to_have_count(2)
            endpoints = leg.locator("strong").filter(has=page.locator("time"))
            expect(endpoints).to_have_count(2)
            expect(endpoints.nth(0)).to_contain_text(origin)
            expect(endpoints.nth(1)).to_contain_text(destination)
            expect(leg.locator("time")).to_have_count(2)
            for index in range(2):
                expect(leg.locator("time").nth(index)).to_have_attribute("datetime", re.compile(rf"^{day}T.*\+00:00$"))


def assert_no_horizontal_overflow(page):
    # Retrying geometry assertion; no sleeps and no dependence on browser chrome zoom.
    page.wait_for_function("document.documentElement.scrollWidth <= innerWidth")


def assert_readable_controls(page):
    """Conservative en-US native-date budget; see README's visual-review caveat."""
    for name in LABELS:
        control = field(page, name)
        expect(control).to_be_visible()
        handle = control.element_handle()
        page.wait_for_function(
            """el => {
                const s = getComputedStyle(el), r = el.getBoundingClientRect();
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                ctx.font = `${s.fontWeight} ${s.fontSize} ${s.fontFamily}`;
                const text = el.tagName === 'SELECT'
                    ? el.selectedOptions[0].textContent : '01/22/2030';
                const content = r.width - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight)
                    - parseFloat(s.borderLeftWidth) - parseFloat(s.borderRightWidth);
                const icon = el.type === 'date' ? 24 : 0;
                return r.left >= 0 && r.right <= innerWidth + 1
                    && content >= ctx.measureText(text).width + icon;
            }""",
            arg=handle,
        )
