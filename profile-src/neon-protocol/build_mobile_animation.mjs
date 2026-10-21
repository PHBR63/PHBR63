#!/usr/bin/env node
/**
 * Terminal mobile de @phbr63: revelação breve + pausa de leitura.
 * Lê somente assets/neon-protocol/terminal-mobile.svg; não altera o SVG.
 * Saída: assets/neon-protocol/terminal-mobile.gif (600 × 260, loop de 10 s).
 * Uso: node profile-src/neon-protocol/build_mobile_animation.mjs
 * Dependência: sharp, local ou em CODEX_PRIMARY_RUNTIME_NODE_MODULES.
 * A imagem SVG estática permanece como alternativa sem movimento no README.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
let sharp;
try {
  sharp = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
    ? require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, 'sharp'))
    : require('sharp');
} catch (error) {
  if (!process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES) throw error;
  sharp = require('sharp');
}

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const sourcePath = path.join(root, 'assets/neon-protocol/terminal-mobile.svg');
const outputPath = path.join(root, 'assets/neon-protocol/terminal-mobile.gif');
const stagingPath = `${outputPath}.${process.pid}.tmp`;
const source = await fs.readFile(sourcePath, 'utf8');
const width = 600;
const height = 260;
const fps = 10;
const seconds = 10;
const totalFrames = fps * seconds;
const cellWidth = 21.674;
const rows = [
  { text: 'CRIANDO.', baseline: 123, start: 0.4 },
  { text: 'EXPERIMENTANDO.', baseline: 171, start: 1.1 },
  { text: 'EVOLUINDO.', baseline: 219, start: 2.2 },
];
const cursorPattern = /<rect x="545" y="200" width="23" height="30" fill="#FF375A"\s*\/>/;
if (!source.includes('width="600" height="260"') || !cursorPattern.test(source)) {
  throw new Error('O SVG base mudou de geometria; revise o gerador antes de continuar.');
}
for (const row of rows) {
  if ((source.match(new RegExp(`>${row.text.replace('.', '\\.')}<`, 'g')) || []).length !== 1) {
    throw new Error(`Texto ausente ou duplicado no SVG: ${row.text}`);
  }
}

const clamp = (n) => Math.max(0, Math.min(1, n));
const smooth = (n) => { const x = clamp(n); return x * x * (3 - 2 * x); };
function frameSvg(t) {
  // A retirada final dura 0,7 s; não há piscadas nem alternância de cores.
  const opacity = 1 - smooth((t - 9.2) / 0.7);
  let svg = source;
  const clips = [];
  rows.forEach((row, index) => {
    const count = Math.max(0, Math.min(row.text.length, Math.floor((t - row.start) / 0.07) + 1));
    const clipWidth = count === row.text.length ? 532 : count * cellWidth;
    clips.push(`<clipPath id="reveal-${index}"><rect x="34" y="${row.baseline - 38}" width="${clipWidth.toFixed(3)}" height="48"/></clipPath>`);
    const pattern = new RegExp(`(<text\\b[^>]*>)(${row.text.replace('.', '\\.')})(<\\/text>)`);
    svg = svg.replace(pattern, `<g opacity="${opacity.toFixed(3)}" clip-path="url(#reveal-${index})">$1$2$3</g>`);
  });
  // Um cursor sempre aceso acompanha lentamente a revelação e depois repousa.
  // O ciclo vertical longo é decorativo; não representa status de atividade.
  const cursorY = t < 3.1 ? 104 + 96 * smooth(t / 3.1) : 200;
  const cursorX = t < 3.1 ? 545 : 545 + 9 * Math.sin((t - 3.1) / 6.1 * Math.PI * 2);
  svg = svg.replace(cursorPattern, `<rect x="${cursorX.toFixed(3)}" y="${cursorY.toFixed(3)}" width="23" height="30" fill="#FF375A" opacity="${opacity.toFixed(3)}"/>`);
  return svg.replace('</desc>', `</desc><defs>${clips.join('')}</defs>`);
}

const frames = new Array(totalFrames);
for (let start = 0; start < totalFrames; start += 8) {
  await Promise.all(Array.from({ length: Math.min(8, totalFrames - start) }, async (_, offset) => {
    const index = start + offset;
    frames[index] = await sharp(Buffer.from(frameSvg(index / fps)))
      .ensureAlpha().raw().toBuffer();
  }));
}
await sharp(Buffer.concat(frames), {
  raw: { width, height: height * totalFrames, channels: 4, pageHeight: height },
}).gif({
  delay: Array(totalFrames).fill(1000 / fps),
  loop: 0,
  colours: 128,
  dither: 0,
  effort: 7,
  keepDuplicateFrames: false,
}).toFile(stagingPath);
const metadata = await sharp(stagingPath, { animated: true }).metadata();
const bytes = (await fs.stat(stagingPath)).size;
const durationMs = (metadata.delay || []).reduce((sum, delay) => sum + delay, 0);
if (metadata.width !== width || metadata.pageHeight !== height || durationMs !== seconds * 1000) {
  throw new Error('A saída GIF não corresponde às dimensões/duração esperadas.');
}
await fs.rename(stagingPath, outputPath);
console.log(JSON.stringify({ file: path.relative(root, outputPath), width, height,
  frames: metadata.pages, sourceFps: fps, durationMs, loop: metadata.loop, bytes }));
