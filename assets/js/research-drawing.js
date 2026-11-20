// The site and the static posters share these drawings. Coordinates are in
// figure space, independent of the display size and device pixel ratio.
export const figureWidth = 720;
export const figureHeight = 432;
export const compactHeight = 500;
const TAU = Math.PI * 2;
const ink = '#1c3148';
const muted = '#486075';
const serif = 'Georgia, "Times New Roman", serif';
const sans = '"Helvetica Neue", Arial, sans-serif';
const mono = 'Menlo, Consolas, monospace';

function line(ctx, points, color, width = 1, dash = []) {
  ctx.beginPath();
  points.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.setLineDash(dash);
  ctx.stroke();
  ctx.setLineDash([]);
}

function polygon(ctx, points, fill) {
  ctx.beginPath();
  points.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
}

function dot(ctx, x, y, radius, color) {
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, TAU);
  ctx.fillStyle = color;
  ctx.fill();
}

function label(ctx, text, x, y, font, color = ink, align = 'left') {
  ctx.font = font;
  ctx.fillStyle = color;
  ctx.textAlign = align;
  ctx.textBaseline = 'alphabetic';
  ctx.fillText(text, x, y);
}

function blend(start, end, t) {
  const rgb = start.map((value, i) => Math.round(value + (end[i] - value) * t));
  return 'rgb(' + rgb.join(',') + ')';
}

// Positive gap between the fixed-photon and candidate √n coefficients, N_S=1.
// Parametrizing by z = -Φ⁻¹(ε) avoids inverting the CDF for every vertex.
function errorProbability(z) {
  const t = 1 / (1 + .2316419 * z);
  const series = t * (.319381530 + t * (-.356563782 + t *
    (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
  return z === 0 ? .5 : Math.exp(-z * z / 2) / Math.sqrt(TAU) * series;
}

const errorSamples = Array.from({ length: 73 }, (_, i) => {
  const z = 1.64485362695147 * (1 - i / 72);
  return [errorProbability(z), z];
});
const probeError = .1;
const probeZ = 1.28155156554460;

export function coefficientGap(eta, z = probeZ) {
  const rootVariance = Math.sqrt(eta * (eta + 1)) * Math.log2(1 + 1 / eta);
  return z * rootVariance * (1 - Math.sqrt((1 - eta) / (1 + eta)));
}

function quantumPoint(error, eta, gap = 0) {
  const depth = (eta - .1) / .8;
  return [68 + 478 * (error - .05) / .45 + 111 * depth,
    334 - 117 * depth - 91 * gap];
}

function quantum(ctx, eta, compact) {
  const blue = '#184cba';
  if (compact) ctx.translate(0, 62);
  polygon(ctx, [quantumPoint(.05, .1), quantumPoint(.5, .1),
    quantumPoint(.5, .9), quantumPoint(.05, .9)], '#f4f7fa');
  for (const error of [.1, .2, .3, .4, .5]) {
    line(ctx, [quantumPoint(error, .1), quantumPoint(error, .9)], '#d4dce5', .9);
  }

  // Back-to-front sections expose how the entire counterexample family varies.
  // The selected section has its own ink, independent of its depth.
  for (let i = 16; i >= 0; i--) {
    const layer = .1 + i * .05;
    const selected = Math.abs(eta - layer) < .001;
    const ridge = errorSamples.map(([e, z]) => quantumPoint(e, layer, coefficientGap(layer, z)));
    const base = quantumPoint(.05, layer);
    const fill = ctx.createLinearGradient(0, ridge[0][1], 0, base[1]);
    if (selected) {
      fill.addColorStop(0, '#1958d7');
      fill.addColorStop(.55, '#588be3');
      fill.addColorStop(1, '#aec6f0');
    } else {
      fill.addColorStop(0, blend([169, 192, 217], [81, 123, 188], i / 16));
      fill.addColorStop(.55, '#e0eaf6');
      fill.addColorStop(1, '#f4f7fb');
    }
    polygon(ctx, [...ridge, base], fill);
    line(ctx, [base, ridge[0]], selected ? blue : '#7698c5', selected ? 1.8 : .85);
    line(ctx, ridge, selected ? '#103f9f' : '#416da6', selected ? 3.5 : 1.45);
    line(ctx, ridge.map(([x, y]) => [x, y + 1.8]), 'rgba(255,255,255,.68)', .85);
  }

  const pin = quantumPoint(probeError, eta, coefficientGap(eta));
  const base = quantumPoint(probeError, eta);
  line(ctx, [pin, base], '#354e7a', 1.25, [2.3, 4.5]);
  dot(ctx, ...pin, 8, 'white');
  dot(ctx, ...pin, 5, '#b44228');
  if (compact) {
    label(ctx, 'Coefficient gap', 52, -3, '28px ' + sans, muted);
    label(ctx, '+' + coefficientGap(eta).toFixed(2), 282, 1, '47px ' + serif, '#113767');
    label(ctx, 'ε = 0.10', 665, -3, '25px ' + mono, muted, 'right');
  } else {
    label(ctx, 'Coefficient gap', 472, 63, '21px ' + sans, muted);
    label(ctx, '+' + coefficientGap(eta).toFixed(2), 467, 122, '54px ' + serif, '#113767');
    label(ctx, 'at ε = 0.10', 474, 149, '19px ' + mono, muted);
  }

  line(ctx, [quantumPoint(.05, .1), quantumPoint(.5, .1)], '#788da3', 1.2);
  for (const error of compact ? [.1, .3, .5] : [.1, .2, .3, .4, .5]) {
    const [x, y] = quantumPoint(error, .1);
    line(ctx, [[x,y],[x,y+6]], '#788da3', 1);
    label(ctx, error.toFixed(1), x, y + (compact ? 36 : 29), (compact ? '25px ' : '17px ') + mono, muted, 'center');
  }
  label(ctx, 'Error probability ε', 309, 404, (compact ? '27px ' : '21px ') + sans, ink, 'center');
  for (const layer of [.1, .5, .9]) {
    const [x, y] = quantumPoint(.5, layer);
    label(ctx, layer.toFixed(1), x + 9, y - 1, (compact ? '23px ' : '16px ') + mono, muted);
  }
  const [endX, endY] = quantumPoint(.5,.9);
  label(ctx, 'η', endX + 15, endY - 27, 'italic 25px ' + serif, blue);
}

// Adjacent chambers around the A₂ Coxeter arrangement, beginning just above
// the positive horizontal ray. The Cambrian fan forgets the 312/132 wall.
const chambers = ['312', '132', '123', '213', '231', '321'];
const coolPleats = [
  [[199, 200, 233], [133, 135, 198]],
  [[223, 225, 236], [162, 173, 205]],
  [[210, 217, 237], [151, 160, 205]],
  [[238, 238, 244], [177, 181, 207]],
];
const centerX = 252;
const centerY = 213;
const radius = 157;
function polar(angle, r) {
  return [centerX + r * Math.cos(angle), centerY + r * Math.sin(angle)];
}
function fanArc(ctx, r, start, end, color, width, dash = []) {
  ctx.beginPath();
  ctx.arc(centerX, centerY, r, start, end);
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.setLineDash(dash);
  ctx.stroke();
  ctx.setLineDash([]);
}

function cambrian(ctx, progress, compact) {
  const sector = TAU / 6;
  const purple = '#5d479e';
  if (compact) ctx.translate(-3,32);
  // A cut edge makes the paper thickness visible only on the lower rim.
  for (let thickness = 5; thickness >= 1; thickness--) {
    ctx.save();
    ctx.translate(0, thickness);
    fanArc(ctx, radius, 0, Math.PI, '#9ca4bc', 1.5);
    ctx.restore();
  }
  for (let i = 0; i < 6; i++) {
    const start = (i - 1) * sector;
    const end = i * sector;
    const mid = (start + end) / 2;
    const lit = i < 2;
    const [light, shade] = lit ? [[235, 221, 249], [139, 112, 181]] : coolPleats[i-2];
    const leftEdge = lit ? start + progress * (-sector - start) : start;
    const rightEdge = lit ? end + progress * (sector - end) : end;
    const across = ctx.createLinearGradient(...polar(leftEdge,radius), ...polar(rightEdge,radius));
    across.addColorStop(0, blend(light, shade, .76));
    across.addColorStop(.30, blend(light, shade, .10));
    across.addColorStop(.72, blend(light, shade, .22));
    across.addColorStop(1, blend(light, shade, .72));
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, start, end);
    ctx.closePath();
    ctx.fillStyle = across;
    ctx.fill();
    ctx.save();
    ctx.clip();
    // One direction of fine parallel hatching per facet. The clipping keeps
    // the paper's contour crisp at both the origin and the perimeter.
    for (let distance = 4; distance < radius * 1.2; distance += 4.3) {
      line(ctx, [polar(start,distance), polar(end,distance)],
        lit ? 'rgba(83,53,124,.37)' : 'rgba(56,66,110,.29)', .82);
      line(ctx, [polar(start,distance+1.1), polar(end,distance+1.1)],
        'rgba(255,255,255,.60)', .75);
    }
    ctx.restore();
    if (i !== 1) line(ctx, [[centerX,centerY],polar(start,radius)], '#58577e', 1.35);
    const [x,y] = polar(mid, radius + (compact ? 37 : 26));
    label(ctx, chambers[i], x, y + 6, (lit ? 'bold ' : '')+(compact ? '27px ' : '19px ')+mono,
      lit ? '#533f85' : muted, 'center');
  }
  fanArc(ctx, radius, 0, TAU, '#686b8d', 1.1);
  // Show the former wall as a trace, keeping the contracted pair legible.
  line(ctx, [[centerX,centerY],polar(0,radius)], 'rgba(70,42,95,'+(1-.62*progress)+')',
    1.8, progress > .55 ? [3,5] : []);
  if (progress > 0 && progress < 1) {
    line(ctx, [[centerX,centerY],polar(-sector*progress,radius)],
      'rgba(70,42,95,'+(.7*(1-progress))+')', 1.75);
  }
  fanArc(ctx, radius - 3.8, -sector, sector, '#6e4e9d', 3.5);
  const head = -sector / 2 + sector * progress;
  const pathRadius = 121;
  const vertices = chambers.map((_, i) => polar((i - .5)*sector, pathRadius));
  const fixedChain = [...vertices.slice(1), vertices[0]];
  line(ctx, fixedChain, 'rgba(255,255,255,.86)', 4.4);
  line(ctx, fixedChain, '#696580', 1.25);
  for (const point of vertices.slice(2)) {
    dot(ctx,...point,5.4,'white');
    dot(ctx,...point,3.2,'#535372');
  }
  fanArc(ctx, pathRadius, -sector / 2, sector / 2, 'rgba(255,255,255,.88)', 5.2);
  if (progress > .001) fanArc(ctx, pathRadius, -sector/2, head, '#843e33', 2.5);
  const startPoint = polar(-sector/2,pathRadius);
  dot(ctx,...startPoint,6.1,'white');
  dot(ctx,...startPoint,3.7,'#754035');
  const [x,y] = polar(head,pathRadius);
  dot(ctx,x,y,8.4,'#fff');
  dot(ctx,x,y,5.6,'#b44f36');
  dot(ctx,centerX,centerY,4,'#444763');
  if (compact) {
    label(ctx, 'Cambrian', 474, 110, '28px '+sans, muted);
    label(ctx, 'projection', 474, 144, '28px '+sans, muted);
  } else {
    label(ctx, 'Cambrian projection', 475, 139, '21px '+sans, muted);
  }
  label(ctx, '312', 477, 204, '58px '+serif, '#605770');
  line(ctx, [[494,221],[494,249],[515,249]], '#966957', 2);
  polygon(ctx, [[515,245],[522,249],[515,253]], '#966957');
  label(ctx, '132', 533, 272, '60px '+serif, purple);
  label(ctx, 'c = s₁s₂', 477, 320, (compact ? '26px ' : '20px ')+mono, muted);
}

// Unwrap the minimum-weight lift 2 → 3 → 4 → 8. One full rotation advances
// by a period. Slicing the ribbon by depth gives its turns real occlusion.
function helix(turn, across = 0, inset = 0) {
  const theta = turn * TAU - 1.03;
  return [
    70 + 244 * turn + (91-inset) * Math.cos(theta) + 55 * across,
    237 - 30 * turn - (99-inset)*Math.sin(theta) + 17*Math.cos(theta) - 6.8*across,
    Math.cos(theta),
  ];
}
function tito(ctx, cycle, compact) {
  if (compact) ctx.translate(0,32);
  const period = cycle.reduce((sum, edge) => sum + edge.weight, 0);
  const starts = [];
  let increment = 0;
  for (const edge of cycle) {
    starts.push(increment / period);
    increment += edge.weight;
  }
  const chalk = [250,252,251];
  const palettes = {
    A: [[15,81,85],[45,153,145],[164,218,194]],
    B: [[126,63,57],[206,118,92],[245,195,161]],
  };
  const slices = 240;
  const bands = Array.from({length:slices}, (_,i) => {
    const turn = (i+.5) * 2 / slices;
    return {i, turn, depth:helix(turn)[2]};
  }).sort((a,b) => a.depth-b.depth);
  const bandFor = turn => {
    const phase = turn % 1;
    for (let j = starts.length - 1; j >= 0; j--) {
      if (phase >= starts[j]) return cycle[j].operand;
    }
    return cycle[0].operand;
  };
  for (const {i,turn,depth} of bands) {
    const a = 2*i/slices, b = 2*(i+1)/slices + .00024;
    const [dark, mid, light] = palettes[bandFor(turn)];
    const lum = (depth + 1) / 2;
    const glint = Math.max(0, Math.sin(TAU*turn + .5));
    const a0 = helix(a,-.5), a1 = helix(a,.5);
    const b0 = helix(b,-.5), b1 = helix(b,.5);
    const face = ctx.createLinearGradient(a0[0],a0[1],a1[0],a1[1]);
    face.addColorStop(0, blend(mid,light,.28 + lum*.65));
    face.addColorStop(.15, blend(mid,light,.12 + glint*.37));
    face.addColorStop(.70, blend(dark,mid,.22 + lum*.7));
    face.addColorStop(1, blend(dark,mid,.10 + lum*.48));
    polygon(ctx,[a0,b0,b1,a1],face);
    polygon(ctx,[a1,b1,helix(b,.5,4),helix(a,.5,4)],blend(dark,mid,lum*.32));
    // Silk-like engraved longitudinal rules follow the lifted path itself.
    for (const strand of [-.48,-.31,-.15,.01,.17,.33,.47]) {
      line(ctx,[helix(a,strand),helix(b,strand)],
        strand < -.45 ? blend(light,chalk,.44) : 'rgba(245,255,249,.37)',
        strand < -.45 ? 1.45 : .72);
    }
  }
  label(ctx, 'One turn', 50, 65, (compact ? '28px ' : '21px ')+sans, muted);
  label(ctx, '+'+period, 47, 122, '56px '+serif, '#1a5955');
  // Color encodes the contributing input order, not the magnitude of a weight.
  for (const [index,key] of ['A','B'].entries()) {
    const lx = 415+index*140;
    line(ctx,[[lx,63],[lx+20,63]],key==='A'?'#277f76':'#ba735f',3.1);
    label(ctx,'Input '+key,lx+28,69,(compact ? '25px ' : '19px ')+sans,muted);
  }
  for (let lap=0; lap<=2; lap++) {
    const [x,y]=helix(lap);
    line(ctx,[[x,y+4],[x,y+23],[x+11,y+31]],'#738d8a',1.15);
    dot(ctx,x,y,6.7,'#fff');
    dot(ctx,x,y,4.1,'#205e58');
    label(ctx,String(cycle[0].source+period*lap),x+14,y+44,(compact ? '30px ' : '23px ')+mono,'#244e4d');
  }
  for (let j=1; j<starts.length; j++) {
    const [x,y] = helix(starts[j],-.49);
    const labelX = j === 1 ? 94 : 77;
    line(ctx,[[x,y],[labelX+17,y-3],[labelX+6,y-3]],'#738d89',1.2);
    dot(ctx,x,y,3.1,'#fff');
    label(ctx,String(cycle[j].source),labelX,y+3,(compact ? '23px ' : '17px ')+mono,muted,'right');
  }
  const [endX, endY] = helix(1);
  dot(ctx, endX, endY, 8.2, 'white');
  dot(ctx, endX, endY, 6, '#a14c36');
  dot(ctx, endX, endY, 3.1, 'white');
}

// The ribbon in the responsive poster never moves. Redraw only the tracer
// above it during playback, including when the page switches poster sizes.
export function drawTitoTracer(ctx, progress, compact) {
  if (progress === 1) return;
  const [x, y] = helix(progress);
  const markerY = y + (compact ? 32 : 0);
  dot(ctx, x, markerY, 9.2, 'white');
  dot(ctx, x, markerY, 6, '#a14c36');
}

export function drawResearchFigure(ctx, kind, value, cycle, compact = false) {
  ctx.save();
  ctx.fillStyle = '#fff';
  ctx.fillRect(0,0,figureWidth,compact ? compactHeight : figureHeight);
  ctx.lineJoin = 'round';
  ctx.lineCap = 'round';
  if (kind === 'pure-loss') quantum(ctx,value,compact);
  if (kind === 'cambrian') cambrian(ctx,value,compact);
  if (kind === 'tito-join') tito(ctx,cycle,compact);
  ctx.restore();
  if (kind === 'tito-join') drawTitoTracer(ctx, value, compact);
}
