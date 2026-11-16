// The hosted exercise runs entirely in the browser, with a fixed demo calendar.
const airports = { ATL: 'Atlanta', JFK: 'New York', LAX: 'Los Angeles', SFO: 'San Francisco' };
const fields = ['origin', 'destination', 'departure', 'return_date', 'passengers'];
const today = '2030-01-15';
const scheduleEnd = '2030-07-14';
const params = new URLSearchParams(location.search);
const form = document.querySelector('form');
const values = Object.fromEntries(fields.map(name => [name, params.get(name) ?? form.elements[name].value]));
const escape = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));

// Keep query values in their original fields when following Edit search.
for (const name of fields) {
  const control = form.elements[name];
  if (control.tagName === 'SELECT' && ![...control.options].some(option => option.value === values[name])) {
    control.add(new Option(values[name] || 'Choose a value', values[name]));
  }
  control.value = values[name];
}

function validate(v) {
  const errors = {};
  for (const name of ['origin', 'destination']) {
    if (!Object.hasOwn(airports, v[name])) errors[name] = `Choose a supported ${name} airport.`;
  }
  if (!errors.origin && !errors.destination && v.origin === v.destination) {
    errors.destination = 'Choose a destination different from your origin.';
  }
  for (const [name, label] of [['departure', 'departure'], ['return_date', 'return']]) {
    const date = new Date(`${v[name]}T00:00:00Z`);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(v[name]) || Number.isNaN(date.valueOf()) || date.toISOString().slice(0, 10) !== v[name]) {
      errors[name] = `Enter a valid ${label} date in YYYY-MM-DD format.`;
    }
  }
  if (!errors.departure && v.departure < today) errors.departure = `Departure must be on or after ${today}.`;
  if (!errors.departure && !errors.return_date && v.return_date < v.departure) {
    errors.return_date = 'Return must be on or after departure. Same-day returns are welcome.';
  }
  if (!/^[1-9]$/.test(v.passengers)) errors.passengers = 'Choose between 1 and 9 passengers.';
  return errors;
}

function showErrors(errors) {
  document.title = 'Check your search · Flight Lab';
  const summary = document.createElement('div');
  summary.className = 'error-summary';
  summary.setAttribute('role', 'alert');
  summary.innerHTML = '<h3>Check your search details</h3><ul>' + Object.entries(errors)
    .map(([name, message]) => `<li><a href="#${name}">${escape(message)}</a></li>`).join('') + '</ul>';
  form.before(summary);
  for (const [name, message] of Object.entries(errors)) {
    const control = form.elements[name];
    control.setAttribute('aria-invalid', 'true');
    control.setAttribute('aria-describedby', `${name}-error`);
    const error = document.createElement('p');
    error.id = `${name}-error`;
    error.className = 'field-error';
    error.textContent = message;
    control.after(error);
  }
}

function showResults(v) {
  document.title = 'Your flight results · Flight Lab';
  const editUrl = '/?' + new URLSearchParams(v);
  const summary = [
    ['Origin airport', `${airports[v.origin]} (${v.origin})`],
    ['Destination airport', `${airports[v.destination]} (${v.destination})`],
    ['Departure date', v.departure], ['Return date', v.return_date], ['Passengers', v.passengers],
  ].map(([label, value]) => `<div><dt>${label}</dt><dd>${escape(value)}</dd></div>`).join('');
  const durations = { 'ATL-JFK': 2, 'ATL-LAX': 5, 'ATL-SFO': 5, 'JFK-LAX': 6, 'LAX-SFO': 1 };
  const duration = durations[[v.origin, v.destination].sort().join('-')];
  const hasFlights = duration && v.return_date <= scheduleEnd;
  function leg(label, identifier, origin, destination, date, hour) {
    const time = h => `${String(h).padStart(2, '0')}:00`;
    return `<div class="flight-leg">
      <div class="leg-label"><strong>${label}</strong><span>${identifier}</span></div>
      <div class="leg-end"><strong>${origin} <time>${time(hour)}</time></strong><span>${date}</span></div>
      <div class="flight-line" aria-hidden="true"><span>Nonstop</span><div>────────→</div></div>
      <div class="leg-end"><strong>${destination} <time>${time(hour + duration)}</time></strong><span>${date}</span></div>
    </div>`;
  }
  const options = hasFlights
    ? `<div class="options-heading"><h2 id="options-heading">2 round-trip options</h2><span>All times UTC · Synthetic schedule</span></div>` + [0, 1].map(i =>
      `<article class="flight-card" aria-labelledby="option-${i + 1}"><h3 id="option-${i + 1}">Option ${i + 1}</h3>` +
      leg('Outbound', `DEMO-${101 + i * 2}`, v.origin, v.destination, v.departure, 8 + i) +
      leg('Return', `DEMO-${102 + i * 2}`, v.destination, v.origin, v.return_date, 16 + i) + '</article>').join('')
    : `<div class="panel empty-state"><span class="empty-icon" aria-hidden="true">↗</span>
      <h2 id="options-heading">No flights found</h2>
      <p>There are no synthetic flight options for this route and these dates.</p>
      <p>Try another route or dates between ${today} and ${scheduleEnd}. New York ↔ San Francisco has no scheduled options.</p>
      <a class="button" href="${escape(editUrl)}">Change search details</a></div>`;
  document.querySelector('main').innerHTML = `
    <section class="intro results-intro"><p class="eyebrow">Your next change of scene</p>
      <h1>Your flight results</h1><p class="lead">${airports[v.origin]} ↔ ${airports[v.destination]}. A round trip, made simple.</p></section>
    <section class="panel summary" aria-labelledby="summary-heading">
      <div class="panel-heading"><h2 id="summary-heading">Search summary</h2><a class="edit-link" href="${escape(editUrl)}">Edit search <span aria-hidden="true">↗</span></a></div>
      <dl class="summary-grid">${summary}</dl>
    </section><section class="options" aria-labelledby="options-heading">${options}</section>`;
}

if (params.get('view') === 'results') {
  // Missing submitted fields must fail, rather than silently use the defaults.
  const submitted = Object.fromEntries(fields.map(name => [name, params.get(name) ?? '']));
  const errors = validate(submitted);
  if (Object.keys(errors).length) showErrors(errors);
  else showResults(submitted);
}
