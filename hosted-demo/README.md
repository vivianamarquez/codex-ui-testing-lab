# Hosted Flight Lab

Public demo: https://flight-lab-ui-workshop.vivianamarquez.chatgpt.site

Student guide: https://flight-lab-ui-workshop.vivianamarquez.chatgpt.site/workshop.html

Workshop slides: https://flight-lab-ui-workshop.vivianamarquez.chatgpt.site/slides

The 16-slide presentation preserves the Google Slides deck’s text, images, links
and speaker notes. Edit `dist/slides.html`, `dist/slides.css` and `dist/slides.js`
for future Sites updates; changes do not sync back to Google Slides.

`dist/` is the complete static site: HTML, CSS and JavaScript. It keeps the original
Flight Lab UI and uses January 15, 2030 as its fixed calendar date. Each browser’s
query string holds its search; learners do not share mutable application state.

To preview changes from the repository root:

```sh
python3 -m http.server 5173 --directory hosted-demo/dist
```

Open http://127.0.0.1:5173. Stop with Ctrl-C when finished. This is maintainer setup;
students use the published URL.

Publish updates with the Sites plugin, reusing the project ID in
`.openai/hosting.json`. Use a separate deployment checkout so only this site’s
source is pushed. The app runs in the browser; the original Flask implementation
and its server-specific tests remain in the repository for local practice.
