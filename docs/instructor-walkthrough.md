# Instructor walkthrough (contains spoilers)

## Prepare before recording

Open this repo in Codex and start the app using the two commands in README.md.
Keep the source checkout and built-in browser together. Use the local URL, not
the hosted reference app. Prepare dependencies before the recording.

The recording is a complete customer session: open with the problem and outcome,
show live browser actions and human review, then close with adoption. The slides
contain all copyable prompts. Click **View prompt** or **Copy prompt** below a slide.

## A 9½-minute recording route

| Time | Slides | What to show |
| --- | --- | --- |
| 0:00–1:15 | 1–4 | Problem, outcome, brief Codex orientation and browser access. |
| 1:15–2:30 | 5–6 | Open the local app live. Annotate the overlapping button, send the focused fix, inspect its diff and reload. |
| 2:30–4:45 | 7–8 | Send the six-scenario investigation. Show actual clicks, the two-passenger search, Edit search resetting to one, and a mobile failure. Reproduce a finding yourself. |
| 4:45–6:45 | 9–10 | Ask for focused fixes. Inspect the diff, rerun the failing paths, show all five restored values and actual test output. |
| 6:45–7:15 | 11 | Explain `/goal` as a bounded follow-up; do not wait for ten extra cases in the recording. |
| 7:15–9:15 | 12–13 | Assign the pilot, ownership, office hour, two-week review, and proposed measures. |
| 9:15–9:30 | Close | Ask each engineer to try one real UI journey and bring evidence plus one friction point. |

Slide 14 is an optional test-creation follow-up. For a ten-minute submission,
prioritize the complete live fix-and-verify cycle. If you include test creation,
shorten elsewhere and time the complete recording. These timings are a target,
not a measured recording duration. Trim agent waiting time if needed; announce
cuts and distinguish prepared evidence from actions executed during recording.

## Deliberate issues in the starting checkout

| Issue | Reproduce | Expected fix |
| --- | --- | --- |
| Desktop overlap (UI-01) | On the search page, Search flights overlaps Passengers. Select the button with Annotate. | Remove the negative vertical transform on `.form-bottom button`; retain the normal form-bottom layout. |
| Edit loses passenger count (AC-08) | Submit ATL/JFK, Jan 22–25, 2030, 2 passengers. Results show 2; Edit search restores 1. Also reproduces with 9 and in empty results. | Include `passengers` in the edit URL in `app.py`. Preserve the other four values. |
| Mobile overflow (UI-02) | Use a measured 390 × 844 viewport. The panel has a 640px minimum and extends outside the screen. | Remove the fixed mobile panel minimum; keep responsive fields and usable controls. Do not conceal overflow. |

The annotations are created **in the live browser toolbar**, not on the slide.
Click Annotate → select the button → write and save the comment → send the chat
request. The slide’s screenshot is a prepared reference. If annotation UI is
unavailable, explain the limitation; a text-only substitute is not an annotation
demonstration. See the official [browser guide](https://learn.chatgpt.com/docs/browser?surface=app#browser-use).

## Investigation and verification

Use slide 7’s prompt (also in browser-prompt.md). Let Codex observe the browser
before reading source. Six scenarios cover search/edit, date recovery, same-day
with 9 passengers, invalid route recovery, empty results, and mobile search/error
paths. An invalid-input error is expected behavior, not automatically a bug.

Expected seeded results after the annotation fix:

- S1, S3, and S5 expose the same passenger-retention defect. Count it once.
- S2 and S4 should reject invalid input, retain values, and recover after correction.
- S6 exposes mobile overflow and repeats the state-retention failure.

Review one finding yourself before asking for fixes. Verify the exact submitted
values and screenshots, not only Codex’s completion statement. After fixes, rerun
the same scenarios and the existing tests. The seeded suite should have two
failures: one server/template check and the saved browser check for edit values.
The corrected copy should pass all 51 existing tests. The suite does not cover
all visual behavior, so also inspect both desktop and narrow layouts.

## Rehearsal and reset

The working repo is the intentionally broken class starting point. Our preparation
rehearses fixes in `artifacts/local-workshop/rehearsal/`, keeping the starting app
unchanged. Evidence and test output are under `artifacts/local-workshop/`.
Do not treat prepared screenshots as a live run. Make a separate copy of app.py,
templates/, static/, tests/, pyproject.toml and uv.lock before practicing fixes.
After a real class, review and reverse only the intended demo fix hunks to reset;
do not reset the entire repo or discard unrelated slide edits.

## Adoption commitment

Propose a two-week pilot. Engineer: one real UI task and a reviewed fix. Reviewer:
verify evidence and scope. Champion: collect prompts, friction and the scorecard.
Facilitator: first-week office hours and a two-week review. Admin: access blockers.
Team lead: decide whether to expand based on the evidence.

Measure second reviewer-accepted use among eligible engineers; time to an accepted
check including review/rework against a manual baseline; and confirmed/rejected
findings plus missed defects. These are proposed indicators. Seeded defects and
rehearsal test counts demonstrate this example only, not productivity gains.
