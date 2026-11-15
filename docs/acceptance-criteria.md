# Acceptance criteria

Practice these three checks with **ATL → JFK, January 22–25, 2030, 2 passengers**.
Start the app with `DEMO_TODAY=2030-01-15`.

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
- The server validates submissions: valid searches return HTTP 200; invalid ones
  return HTTP 422 with a populated form and field errors. Malformed date values
  may appear blank in a native date control; other valid values remain available.
- Native controls can prevent missing values and dates before today. Both date
  fields have today's minimum; the server checks return-versus-departure ordering
  and rejects identical airports. Test server rejection separately from a control
  preventing a selection.
- The effective date is `DEMO_TODAY`, or the UTC date when unset. Validation, form
  defaults, minimum dates, and schedules all use that date.
- Synthetic flights cover today through today +180 days, inclusive. Dates outside
  that window are valid searches with empty results. Passenger count preserves
  the requested party size and does not change synthetic availability.
- All distinct supported routes have two options within the schedule window,
  except JFK–SFO in both directions, which has an empty schedule.
- Each option's outbound and return legs match the requested route and dates.
  Times are UTC; a same-day return departs after the outbound arrival.

For empty-results practice, use **JFK → SFO** with the same dates and 2 passengers.
