# Instructor demo: create a reusable test

The student exercise is complete before this demonstration. Use the same hosted
[Flight Lab](https://flight-lab-ui-workshop.vivianamarquez.chatgpt.site) and the browser evidence from the class.

## Before class

Open this `instructor-demo` folder as a Codex project. With Python 3.12 installed,
run these commands in its terminal:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

This folder starts with no test file. `pytest.ini` points tests at the hosted demo.
The test runtime is local; Flight Lab stays hosted. Keep this terminal open.

## At the end of class

1. Review the class’s AC-01, AC-02 and AC-08 browser evidence.
2. Paste the prompt below into Codex. If this is a new chat, include the observed
   values and screenshots from the browser check so it has that context.
3. Inspect the created file. Show how each assertion maps to a criterion.
4. Run it in the terminal and discuss the actual result:

   ```sh
   python -m pytest test_flight_search.py --headed
   ```

### Prompt

```text
Create test_flight_search.py in this folder using Python, pytest and Playwright.
Target https://flight-lab-ui-workshop.vivianamarquez.chatgpt.site through the base_url fixture configured in pytest.ini.
Use the verified browser journey and these acceptance criteria:
AC-01: A valid search opens results.
AC-02: The summary matches all five submitted values.
AC-08: Edit search returns a form containing those same five values.

Explicitly set ATL, JFK, departure 2030-01-22, return 2030-01-25 and 2 passengers.
Assert the results heading, each exact value beside its summary label, and all
five control values after Edit search. Use accessible labels and roles,
Playwright's waiting assertions, and no fixed sleeps. Keep the test readable.
Use the existing .venv, run the test, and report the actual outcome.
Do not change the hosted application or create an app server fixture.
```

The generated test is the live output of the demonstration. Rehearse in a copy
of this folder, keeping this one ready for class. A fallback reference lives at
`../tests/e2e/test_flight_search.py`; identify it as prepared if you use it.

## Explain the next step

A saved test runs its assertions without an agent deciding each action. Teams can
run tests after UI changes and in CI, adding stable journeys one at a time.
Python is one choice for the test; the application's implementation language can
be different. People still review requirements, failures and test maintenance.
