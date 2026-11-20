// Run with Node 22 and @napi-rs/canvas available. The browser uses the same
// drawing functions, so the first interaction never switches illustration styles.
import { createRequire } from 'node:module';
import { readFile, writeFile } from 'node:fs/promises';
import { compactHeight, drawResearchFigure, figureWidth, figureHeight } from '../assets/js/research-drawing.js';

const require = createRequire(import.meta.url);
const { createCanvas } = require('@napi-rs/canvas');
const artwork = new URL('../images/research/', import.meta.url);
const example = JSON.parse(await readFile(new URL('../_data/tito_join.json', import.meta.url)));

for (const [kind, value] of [['pure-loss', .5], ['cambrian', 1], ['tito-join', 1]]) {
  for (const width of [480, 720, 1080]) {
    const compact = width === 720;
    const canvas = createCanvas(width, width * (compact ? compactHeight : figureHeight) / figureWidth);
    const ctx = canvas.getContext('2d');
    ctx.scale(width / figureWidth, width / figureWidth);
    drawResearchFigure(ctx, kind, value, example.cycle, compact);
    const suffix = compact ? 'compact' : String(width);
    await writeFile(new URL(kind+'-'+suffix+'.webp', artwork), await canvas.encode('webp', 94));
    if (width === 1080) {
      await writeFile(new URL(kind+'.png', artwork), await canvas.encode('png'));
    }
  }
}
