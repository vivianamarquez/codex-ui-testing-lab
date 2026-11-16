const data = JSON.parse(document.getElementById('slide-data').textContent);
const slides = [...document.querySelectorAll('.slide')];
const stage = document.querySelector('.stage');
const frame = document.querySelector('.slide-frame');
const canvas = document.querySelector('.slide-canvas');
const selector = document.getElementById('slide-select');
const previous = document.getElementById('previous');
const next = document.getElementById('next');
const notes = document.getElementById('speaker-notes');
const notesToggle = document.getElementById('notes-toggle');
const copyButton = document.getElementById('copy-prompt');
const fullscreenButton = document.getElementById('fullscreen');
let current = 0;
function fit() {
  const style = getComputedStyle(stage);
  const width = stage.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
  const height = stage.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom);
  const scale = Math.max(.1, Math.min(width / 720, height / 405));
  frame.style.width = `${720 * scale}px`;
  frame.style.height = `${405 * scale}px`;
  canvas.style.transform = `scale(${scale})`;
}
function show(index, updateUrl = true) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, i) => { slide.hidden = i !== current; slide.inert = i !== current; });
  selector.value = String(current);
  previous.disabled = current === 0;
  next.disabled = current === slides.length - 1;
  document.getElementById('note-text').textContent = data[current].notes || 'No speaker notes for this slide.';
  document.getElementById('status').textContent = `Slide ${current + 1} of ${slides.length}: ${data[current].title}`;
  document.title = `${data[current].title} · UI testing with Codex`;
  copyButton.hidden = !data[current].prompt;
  copyButton.textContent = 'Copy prompt';
  if (updateUrl) history.replaceState(null, '', `#${current + 1}`);
  fit();
}
function fromHash() {
  const number = Number(location.hash.slice(1));
  show(Number.isInteger(number) && number > 0 ? number - 1 : 0, false);
}
previous.addEventListener('click', () => show(current - 1));
next.addEventListener('click', () => show(current + 1));
selector.addEventListener('change', () => show(Number(selector.value)));
notesToggle.addEventListener('click', () => {
  notes.hidden = !notes.hidden;
  notesToggle.setAttribute('aria-expanded', String(!notes.hidden));
  fit();
});
fullscreenButton.addEventListener('click', async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await stage.requestFullscreen();
  } catch {
    document.getElementById('status').textContent = 'Fullscreen is unavailable in this browser.';
  }
});
document.addEventListener('fullscreenchange', () => {
  const presenting = document.fullscreenElement === stage;
  fullscreenButton.textContent = presenting ? 'Exit fullscreen' : 'Fullscreen';
  if (presenting) {
    stage.tabIndex = -1;
    stage.focus({ preventScroll: true });
  } else {
    fullscreenButton.focus({ preventScroll: true });
  }
  fit();
});
copyButton.addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(data[current].prompt); copyButton.textContent = 'Copied'; }
  catch { copyButton.textContent = 'Select and copy the slide text'; }
});
document.addEventListener('keydown', event => {
  if (event.ctrlKey || event.metaKey || event.altKey || event.target.closest('a,button,select,input,textarea')) return;
  if (['ArrowRight','ArrowDown','PageDown',' '].includes(event.key)) { event.preventDefault(); show(current + 1); }
  if (['ArrowLeft','ArrowUp','PageUp'].includes(event.key)) { event.preventDefault(); show(current - 1); }
  if (event.key === 'Home') { event.preventDefault(); show(0); }
  if (event.key === 'End') { event.preventDefault(); show(slides.length - 1); }
});
window.addEventListener('hashchange', fromHash);
new ResizeObserver(fit).observe(stage);
fromHash();
