# Flight Lab

A local flight-search app built with Flask.

## Run

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

Start the app:

```sh
uv sync --locked
DEMO_TODAY=2030-01-15 uv run flask --app app run --debug --port 5001
```

Open **http://127.0.0.1:5001**. `DEMO_TODAY` fixes the date for reproducible
searches. Without it, the app uses the current UTC date. Stop the server with Ctrl-C.

The server returns HTTP 200 for valid searches and HTTP 422 for invalid ones.
These responses do not verify the rendered UI.

## Branches

- `main`: the app and acceptance criteria, without tests or agent instructions.
- `with-tests`: the same app with Python tests, Playwright, and `AGENTS.md`.

Switch with `git switch main` or `git switch with-tests`, then run `uv sync --locked`.

[Acceptance criteria](docs/acceptance-criteria.md) · [Codex Site](https://ui-testing-codex-lab.vivianamarquez.chatgpt.site/)
