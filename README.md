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
searches. Stop the server with Ctrl-C.

## Tests

```sh
uv run playwright install chromium
uv run pytest
```

The browser test starts its own app server. Add `--headed` to watch it run.

[Acceptance criteria](docs/acceptance-criteria.md) · [Codex Site](https://ui-testing-codex-lab.vivianamarquez.chatgpt.site/)
