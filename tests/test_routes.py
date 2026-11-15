"""HTTP/template correctness checks; these do not execute a browser journey."""

from html.parser import HTMLParser
from urllib.parse import parse_qs, urlsplit

import pytest


class FormHTML(HTMLParser):
    """Only the standard form values/links needed for server-rendering checks."""

    def __init__(self, response):
        super().__init__()
        self.values = {}
        self.links = []
        self.inputs = {}
        self.select = None
        self.feed(response.get_data(as_text=True))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "select":
            self.select = attrs.get("name")
        if tag == "option" and "selected" in attrs:
            self.values[self.select] = attrs.get("value")
        if tag == "input":
            name = attrs.get("name")
            self.values[name] = attrs.get("value")
            self.inputs[name] = attrs
        if tag == "a":
            self.links.append(attrs.get("href"))


def test_search_page_and_date_minimums(client, demo_today):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Find your next flight" in response.data
    form = FormHTML(response)
    assert form.values == {"origin": "ATL", "destination": "JFK", "departure": "2030-01-22",
                           "return_date": "2030-01-25", "passengers": "1"}
    for field in ("departure", "return_date"):
        assert form.inputs[field]["min"] == demo_today.isoformat()
        assert "required" in form.inputs[field]
    assert client.get("/static/styles.css").status_code == 200


def test_results_summary_and_edit_parameters(client, valid_parameters):
    # A non-default route makes accidental use of the defaults detectable.
    params = valid_parameters | {"origin": "SFO", "destination": "LAX", "passengers": "7"}
    response = client.get("/results", query_string=params)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    for value in ("San Francisco (SFO)", "Los Angeles (LAX)", "2030-01-22", "2030-01-25"):
        assert value in html
    assert "<dt>Passengers</dt><dd>7</dd>" in html
    assert "2 round-trip options" in html
    edit = next(link for link in FormHTML(response).links if link.startswith("/?"))
    assert parse_qs(urlsplit(edit).query) == {key: [value] for key, value in params.items()}
    assert FormHTML(client.get(edit)).values == params


@pytest.mark.parametrize("overrides,message", [
    ({"destination": "ATL"}, "different from your origin"),
    ({"origin": "XXX"}, "supported origin"),
    ({"departure": "2030-01-14"}, "on or after 2030-01-15"),
    ({"return_date": "2030-01-21"}, "on or after departure"),
    ({"return_date": "2030-02-30"}, "valid return date"),
    ({"passengers": "0"}, "between 1 and 9"),
    ({"passengers": "10"}, "between 1 and 9"),
])
def test_server_rejects_invalid_requests_and_preserves_fields(client, valid_parameters, overrides, message):
    params = valid_parameters | overrides
    response = client.get("/results", query_string=params)
    assert response.status_code == 422
    assert message in response.get_data(as_text=True)
    assert b'role="alert"' in response.data
    assert b'aria-invalid="true"' in response.data
    assert FormHTML(response).values == params


def test_missing_query_is_recoverable(client):
    response = client.get("/results")
    assert response.status_code == 422
    assert b"Check your search details" in response.data


def test_empty_results_keep_summary_and_edit(client, valid_parameters):
    params = valid_parameters | {"origin": "JFK", "destination": "SFO"}
    response = client.get("/results", query_string=params)
    assert response.status_code == 200
    for text in (b"No flights found", b"Search summary", b"New York (JFK)",
                 b"San Francisco (SFO)", b"2030-01-22", b"2030-01-25", b"Edit search"):
        assert text in response.data
    assert b"DEMO-101" not in response.data


def test_untrusted_values_are_escaped(client, valid_parameters):
    response = client.get("/results", query_string=valid_parameters | {"origin": '<script>alert("x")</script>'})
    assert response.status_code == 422
    assert b"<script>" not in response.data
    assert b"&lt;script&gt;" in response.data
