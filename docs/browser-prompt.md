# Browser investigation prompt

Copy this after reviewing the annotation fix. The same prompt is on slide 7.

```text
Use the built-in browser to challenge Flight Lab at http://127.0.0.1:5001. Try meaningful edge cases and report what breaks, with evidence I can reproduce. Leave application code unchanged during this investigation.

Read docs/acceptance-criteria.md for expected behavior. Do not read the instructor walkthrough, rehearsal artifacts, or application source to predict failures; first observe the UI. Effective today is 2030-01-15.

Run these six scenarios. Explicitly set all five fields at the start of each scenario. All dates are in 2030; use 2 passengers unless specified.
S1 Search and edit: ATL to JFK, Jan 22–25. Submit using Enter on Search flights. Compare all five results-summary values, then Edit search and compare all five controls. AC-01/02/08.
S2 Invalid date and recovery: ATL to JFK, Jan 22–21. Verify the date error and retained inputs; change only return to Jan 25 and submit. Verify that the error clears and the results summary is correct. AC-04/07/01/02.
S3 Boundaries: ATL to JFK, Jan 22–22, 9 passengers. Same-day return and 9 passengers are valid. Compare results and edited values. AC-04/06/02/08.
S4 Same airport: ATL to ATL, Jan 22–25. Reject the route and preserve inputs. Change only destination to JFK and verify recovery. AC-03/07/01/02.
S5 Empty results: JFK to SFO, Jan 22–25. Expect No flights found, an accurate summary, and Edit search retaining all five values. AC-09/02/08.
S6 Mobile: at an actual 390 × 844 CSS viewport, repeat S1 and S2. Check UI-02: no horizontal scrolling, overlap, clipped labels or inaccessible controls. Vertical scrolling is allowed. Record the measured viewport and restore it afterward. If viewport control is unavailable, mark this scenario blocked.

For each scenario report criterion, expected, actual values, viewport, passed/failed/blocked/unattempted, and supporting screenshot. Separate browser-native prevention from application validation. Reproduce each suspected defect once; group duplicate symptoms by likely cause. Give reproduction steps, impact, severity with rationale, and what needs fixing. Don't infer a pass from an HTTP response or an agent completion message.
Stop after the six scenarios and a reviewable report. Do not fix code, create tests, publish changes, or claim complete release coverage.
```
