# Acceptance criteria

Practice these three checks with **ATL → JFK, January 22–25, 2030, 2 passengers**.
Open the [hosted demo](https://flight-lab-ui-workshop.vivianamarquez.chatgpt.site).
Its effective date is fixed at January 15, 2030. The
[student prompt](browser-prompt.md) includes these criteria, ready to paste into Codex.

| ID | Expected behavior |
| --- | --- |
| **AC-01** | A valid round-trip search opens the results page. |
| **AC-02** | The summary shows the exact origin, destination, departure date, return date, and passenger count submitted. |
| **AC-08** | Edit search returns a form containing those same five values. |

For each check, report **passed, failed, or blocked**, what you observed, and the
evidence. A successful sample shows two round-trip options. Check the values on
the page, then compare the edited controls with your original input.

## Follow-up checks

| ID | Expected behavior |
| --- | --- |
| AC-03 | Identical origin and destination airports are rejected. |
| AC-04 | A return before departure is rejected; a same-day return is allowed. |
| AC-05 | Departure before the effective date is rejected; departure today is allowed. |
| AC-06 | Only passenger counts 1–9 are accepted. |
| AC-07 | Errors explain the problem and preserve valid inputs for correction. |
| AC-09 | A valid search with an empty schedule shows “No flights found,” the accurate summary, and Edit search. |

## Input and data rules

- All five fields are required. Airports: ATL, JFK, LAX, SFO.
- Submitted dates use `YYYY-MM-DD`; results display that same format. Native
  date controls may display dates in the browser's local format.
- Passenger values are `1` through `9`; malformed values such as `1.0` are rejected.
- Invalid searches show a populated form and field errors. Malformed date values
  may appear blank in a native date control; other valid values remain available.
- Native controls can prevent missing values and dates before today. Both date
  fields have today's minimum; the app also checks return-versus-departure ordering
  and rejects identical airports. Distinguish a field preventing a selection from
  an error shown after submission.
- Validation, form defaults, minimum dates, and schedules use the effective date.
- Synthetic flights cover today through today +180 days, inclusive. Dates outside
  that window are valid searches with empty results. Passenger count preserves
  the requested party size and does not change synthetic availability.
- All distinct supported routes have two options within the schedule window,
  except JFK–SFO in both directions, which has an empty schedule.
- Each option's outbound and return legs match the requested route and dates.
  Times are UTC; a same-day return departs after the outbound arrival.

For empty-results practice, use **JFK → SFO** with the same dates and 2 passengers.

## Local Flask implementation

The original local app uses `DEMO_TODAY`, or the UTC date when unset. Start it with
`DEMO_TODAY=2030-01-15` for these inputs. It validates on the server: valid searches
return HTTP 200 and invalid searches return HTTP 422. The hosted exercise performs
validation in the browser; HTTP status checks apply to the local implementation.
