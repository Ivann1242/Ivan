import { coefficientGap, compactHeight, drawResearchFigure, drawTitoTracer, figureHeight, figureWidth } from './research-drawing.js';

function addPlayback(figure, kind, cycle, render) {
  const button = figure.querySelector('button');
  const label = button.querySelector('.action-label');
  const result = figure.querySelector('.figure-result');
  const status = figure.querySelector('.figure-status');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const isProjection = kind === 'cambrian';
  const replayLabel = isProjection ? 'Replay projection' : 'Replay cycle';
  const duration = isProjection ? 2200 : 3600;
  const stops = [0];
  const path = [];
  if (!isProjection) {
    path.push(cycle[0].source);
    const period = cycle.reduce((sum, edge) => sum + edge.weight, 0);
    for (const edge of cycle) {
      path.push(path[path.length - 1] + edge.weight);
      stops.push((path[path.length - 1] - path[0]) / period);
    }
  } else {
    stops.push(1);
  }

  let elapsed = duration;
  let startedAt = null;
  let frame = 0;
  let step = stops.length - 1;
  function display(progress) {
    render(progress);
    if (isProjection) {
      result.textContent = progress < 1 ? '6 chambers' : '6 chambers → 5';
    } else {
      const reached = stops.filter(stop => stop <= progress).length;
      result.textContent = path.slice(0, reached).join(' → ');
    }
  }
  function setAction(state, text) {
    button.dataset.state = state;
    label.textContent = text;
  }
  function steppedAction() {
    if (isProjection) {
      setAction('step', step === 0 ? 'Apply projection' : 'Show weak order');
    } else {
      setAction('step', step === stops.length - 1 ? 'Start at '+path[0] : 'Next residue');
    }
  }
  function tick(now) {
    elapsed = Math.min(duration, now - startedAt);
    const fraction = elapsed / duration;
    const smooth = fraction * fraction * (3 - 2 * fraction);
    display(smooth);
    if (elapsed < duration) {
      frame = requestAnimationFrame(tick);
    } else {
      startedAt = null;
      step = stops.length - 1;
      setAction('replay', replayLabel);
      status.textContent = isProjection ? '312 projects to 132. Five chambers remain.' :
        'The cycle ends at '+path[path.length-1]+', back in residue '+path[0]+'.';
    }
  }
  function pause() {
    if (startedAt === null) return;
    elapsed = Math.min(duration, performance.now() - startedAt);
    cancelAnimationFrame(frame);
    startedAt = null;
    setAction('paused', 'Resume');
    status.textContent = 'Paused.';
  }
  function applyPreference() {
    if (reducedMotion.matches) {
      if (startedAt !== null) pause();
      elapsed = duration;
      step = stops.length - 1;
      display(1);
      steppedAction();
    } else {
      elapsed = duration;
      setAction('ready', isProjection ? 'Project 312' : 'Trace one period');
    }
  }
  button.addEventListener('click', () => {
    if (reducedMotion.matches) {
      step = (step + 1) % stops.length;
      display(stops[step]);
      steppedAction();
      status.textContent = isProjection ? (step ? '312 projects to 132.' : 'Six chambers before projection.') :
        'The path is at '+path[step]+'.';
    } else if (startedAt !== null) {
      pause();
    } else {
      if (elapsed >= duration) elapsed = 0;
      startedAt = performance.now() - elapsed;
      setAction('playing', 'Pause');
      status.textContent = isProjection ? 'Projecting 312.' : 'Tracing the cycle.';
      tick(performance.now());
    }
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });
  reducedMotion.addEventListener('change', applyPreference);
  if (reducedMotion.matches) steppedAction();
}

for (const figure of document.querySelectorAll('[data-study]')) {
  const kind = figure.dataset.study;
  const board = figure.querySelector('.figure-artboard');
  const canvas = figure.querySelector('canvas');
  const ctx = canvas.getContext('2d');
  if (!ctx) continue;
  const cycle = figure.dataset.cycle ? JSON.parse(figure.dataset.cycle) : null;
  const compactView = window.matchMedia(board.querySelector('source[media]').media);
  let current = kind === 'pure-loss' ? .5 : 1;
  function render(value) {
    current = value;
    const width = Math.round(board.clientWidth * Math.min(window.devicePixelRatio || 1, 2.5));
    if (!width) return;
    const logicalHeight = compactView.matches ? compactHeight : figureHeight;
    const height = Math.round(width * logicalHeight / figureWidth);
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
    }
    ctx.setTransform(width / figureWidth, 0, 0, height / logicalHeight, 0, 0);
    if (kind === 'tito-join') {
      ctx.clearRect(0, 0, figureWidth, logicalHeight);
      drawTitoTracer(ctx, value, compactView.matches);
    } else {
      drawResearchFigure(ctx, kind, value, cycle, compactView.matches);
    }
    canvas.hidden = false;
  }
  // The responsive poster remains in place until the reader uses a control.
  if ('ResizeObserver' in window) {
    new ResizeObserver(() => { if (!canvas.hidden) render(current); }).observe(board);
  }
  if (kind === 'pure-loss') {
    const range = figure.querySelector('input');
    const output = figure.querySelector('.parameter-value');
    function setValue() {
      const eta = range.valueAsNumber;
      output.textContent = eta.toFixed(2);
      range.style.setProperty('--position', (eta - .1) / .8 * 100 + '%');
      range.setAttribute('aria-valuetext', eta.toFixed(2)+', coefficient gap '+coefficientGap(eta).toFixed(2)+' at ten percent error');
    }
    setValue();
    if (range.valueAsNumber !== current) render(range.valueAsNumber);
    range.addEventListener('input', () => {
      setValue();
      render(range.valueAsNumber);
    });
  } else {
    addPlayback(figure, kind, cycle, render);
  }
  figure.querySelector('.figure-controls').hidden = false;
}
