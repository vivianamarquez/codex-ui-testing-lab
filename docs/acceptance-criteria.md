# Flight-search acceptance criteria

These are the agreed product requirements. The initial journey is round-trip
search only, ending at results. The primary live demonstration is **AC-01,
AC-02, and AC-08**; the remaining criteria are bounded follow-up practice.

| ID | Requirement | Expected behavior |
| --- | --- | --- |
| AC-01 | Valid round-trip search | Given supported, different airports, valid dates, and 1–9 passengers, submitting opens the results page. A valid search can have zero options. |
| AC-02 | Search details remain accurate | The results summary shows exactly the submitted origin, destination, departure date, return date, and passenger count. Both cities and airport codes are shown. |
| AC-03 | Different airports are required | A search with the same origin and destination is rejected with a destination error. |
| AC-04 | Date ordering is enforced | A return before departure is rejected. A same-day return is allowed. |
| AC-05 | Departure date is not in the past | A departure before the application's effective today is rejected. Departure today is allowed. |
| AC-06 | Passenger limits are enforced | Only integer passenger choices 1–9 are accepted. Missing, out-of-range, and non-integer values are rejected. |
| AC-07 | Invalid input is recoverable | Feedback explains each invalid field. Valid values already entered are retained, so the traveler can correct and resubmit. |
| AC-08 | Editing a search preserves values | “Edit search” returns a form containing the submitted airports, both dates, and passenger count. |
| AC-09 | Empty results are understandable | A valid search with no scheduled options shows “No flights found,” the search summary, and “Edit search.” It is not a validation error. |

## Exact input and feedback contract

- Supported airports: Atlanta (ATL), New York (JFK), Los Angeles (LAX),
  San Francisco (SFO). No free-text airport lookup or unsupported trip type.
- All five fields are required. Dates sent to the server use `YYYY-MM-DD`;
  impossible dates are rejected. The browser's native date display can vary by
  locale; the results summary always displays ISO dates unambiguously.
- Passenger values are the canonical strings `1` through `9` on submission.
  Values such as `1.0`, `01`, `+1`, and whitespace are invalid requests.
- Valid `GET /results?...` requests return HTTP 200. Server-side invalid requests
  return HTTP **422** and render the populated search form, an error summary with
  field links, and associated inline messages. No session or database is used.
- Native `required` and date `min` constraints can stop submission before the
  server is reached. Selects offer only supported airports and 1–9 passengers
  on the initial form. They do **not** disable choosing identical airports.
- Both date inputs have `min=effective today`. There is no JavaScript to change
  the return minimum when departure changes. A return before departure but
  after today can be submitted; the **server** rejects it with an explanation.
- On server errors, all valid inputs are preserved. Invalid airport/passenger
  query values are displayed as marked invalid options. An impossible or malformed
  date may appear blank in the native date control; other valid values remain.
- Edit uses the submitted values in query parameters. A manually forged edit URL
  is not accepted as a valid search until submission passes server validation.

**Evidence distinction:** an inability to select 10 passengers demonstrates a UI
constraint, not server enforcement. To verify rejection of forged values, use a
direct HTTP request or the baseline HTTP tests. Native validation messages belong
to the browser and may vary by locale; do not assert their exact wording.

## Effective date and schedule contract

`DEMO_TODAY=2030-01-15` freezes the application date for rehearsals. With no setting,
use the UTC calendar date, independent of the machine's timezone. The date is
computed once per request and shared by validation, rendered minimums/defaults,
and synthetic schedule generation. Fixed tests use the same date explicitly.

Flights are available through today +180 days **inclusive**, with no booking
horizon imposed by validation. Both travel dates must be in that schedule window
to produce options. Outside the window, the search remains valid and returns none.
JFK–SFO in either direction always returns none. Every other distinct supported
pair produces two deterministic options, independent of passenger count 1–9.

Each option contains outbound origin → destination and return destination → origin
legs on the requested dates. All times are UTC, and even a same-day inbound leg
departs after the outbound arrival. Flight identifiers are synthetic, with a
`DEMO-` prefix. No live inventory, prices, randomness, or timezone conversion.

## Rehearsal inputs

With `DEMO_TODAY=2030-01-15`:

- Main: ATL → JFK; departure `2030-01-22`; return `2030-01-25`; **2 passengers**.
  Expect two round-trip options and all five values preserved on edit.
- Empty: JFK → SFO, with the same dates and passengers. Expect no flights and
  the accurate summary/edit action.
- Same-day boundary: ATL → JFK; both dates `2030-01-15`; 1 or 9 passengers.
  Expect acceptance and two options.
- Recoverable validation: ATL → ATL, otherwise main inputs. Expect a destination
  error; correct to JFK without re-entering the valid dates or passengers.

In live-date mode, derive travel dates from the displayed effective today rather
than reusing the fixed examples without the fixed-date setting.
