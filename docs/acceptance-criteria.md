# Acceptance criteria

Flight Lab supports round-trip searches between **ATL, JFK, LAX, and SFO**.
The five search fields are origin, destination, departure date, return date, and passengers.

## Search

| ID | Expected behavior |
| --- | --- |
| **AC-01** | A valid search opens the results page. |
| **AC-02** | The summary matches all five submitted values. Flight options match the requested route and dates. |

## Validate

All five fields are required.

| ID | Expected behavior |
| --- | --- |
| **AC-03** | Origin and destination must be different airports. |
| **AC-04** | Return must be on or after departure. Same-day returns are allowed. |
| **AC-05** | Departure must be today or later. |
| **AC-06** | Accept whole-number passenger counts from **1 to 9**. Reject malformed values such as `1.0`. |
| **AC-07** | Explain invalid inputs and preserve valid values so users can correct the search. |

## Edit

| ID | Expected behavior |
| --- | --- |
| **AC-08** | **Edit search** restores all five submitted values. |

## Empty results

| ID | Expected behavior |
| --- | --- |
| **AC-09** | Show **“No flights found”**, the correct summary, and **Edit search** when a valid search has no options. |

## Layout

| ID | Expected behavior |
| --- | --- |
| **UI-01** | On desktop, all fields and **Search flights** are visible and independently usable, with no overlap. |
| **UI-02** | At **390 × 844**, the form, errors, results, and editing work without horizontal scrolling, overlap, or clipped controls. Vertical scrolling is allowed. |

<details>
<summary>Demo data and input details</summary>

- With the README setup, “today” is **January 15, 2030**. Defaults, validation, date minimums, and schedules all use this date.
- **ATL → JFK, January 22–25, 2030, 2 passengers** returns two round-trip options.
- Every distinct route has two options from today through **today +180 days**, inclusive, except **JFK ↔ SFO**, which has none. Dates beyond that window are valid searches with no results.
- Passenger count does not change flight availability.
- Flight times are UTC. For same-day trips, the return departs after the outbound arrival.
- Submitted dates and result summaries use `YYYY-MM-DD`. Browser date fields may display a local format.
- Both date fields have today as their minimum. Browser controls may prevent missing or past dates before submission. Invalid submitted values produce field errors; malformed dates may appear blank, while other valid values are preserved.

</details>
