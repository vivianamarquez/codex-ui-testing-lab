# Published workshop materials

`dist/` contains the workshop slides and the earlier hosted Flight Lab reference.
The live class now uses the local Flask app at http://127.0.0.1:5001 so Codex can
inspect source, make focused fixes, and verify the running UI.

Slides: https://ui-testing-codex-lab.vivianamarquez.chatgpt.site/slides

Edit the existing Sites project identified by `.openai/hosting.json`; preserve
its audience. Keep this mirror aligned with the Sites source checkout when
publishing. Do not deploy the deliberately broken local app as the reference.
