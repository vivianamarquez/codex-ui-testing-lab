# UI testing exercise prompt

Copy this into a new practice session when you are ready to verify the UI and
write the regression test:

---

Help me practice UI testing with Codex. Use this flight-search app as the example,
then turn the verified interactions into a reusable Python regression test.

1. Read `AGENTS.md`, `docs/acceptance-criteria.md`, and the README. Inspect the
   existing test fixtures. Use the acceptance criteria as expected behavior.
2. Start or locate the local app. Use `DEMO_TODAY=2030-01-15` and confirm the
   displayed effective date. Report the URL and who started the server.
   Use `uv sync --locked` and `uv run playwright install chromium` for setup.
3. Use the built-in browser to configure Atlanta (ATL) → New York (JFK), departure
   `2030-01-22`, return `2030-01-25`, and **2 passengers**. Include keyboard
   interaction. Submit, inspect the results, select Edit search, and inspect
   all five preserved values.
4. Report observations against **AC-01, AC-02, and AC-08**, following
   `docs/results-template.md`. Separate passed, failed, and blocked checks.
   Include the exact observed values, evidence, and limitations. List other
   criteria as unattempted.
5. Create `tests/e2e/test_flight_search.py` using Python Playwright and the provided
   pytest fixtures. Mark it `browser`. Use accessible labels and roles, assert
   the exact summary and edited form values, and use Playwright's waiting
   assertions. Keep it independent of test order and the machine's real date.
6. Run `uv run pytest tests/e2e/test_flight_search.py`, then `uv run pytest`.
   Report the actual outcomes and retain useful failure evidence. If a command
   cannot run, explain the blocker and provide the command for me to run.
7. Keep application code unchanged. Keep assertions aligned with the acceptance
   criteria. Report issues or ambiguous requirements with reproduction steps
   and evidence. Label any test drafted without browser access as unverified.
8. Summarize the changed files, evidence, and assertions I should review. Have me
   manually repeat Edit search and compare all values. Keep work local and stop
   servers you started when the exercise is finished.
