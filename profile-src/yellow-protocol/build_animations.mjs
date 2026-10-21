#!/usr/bin/env node
/**
 * Animações vetoriais originais para @phbr63.
 * Saída: SVG autossuficiente + PNG estático + GIF animado.
 * Uso: node profile-src/yellow-protocol/build_animations.mjs
 * Dependência de geração: sharp (librsvg + libvips). Os SVGs não dependem dela.
 * NODE_MODULES: CODEX_PRIMARY_RUNTIME_NODE_MODULES, ou sharp instalado localmente.
 * Nenhum bitmap externo ou imagem gerada por IA é usado neste gerador.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const sharp = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
  ? require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, 'sharp'))
  : require('sharp');

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const dest = path.join(root, 'assets', 'yellow-protocol', 'animacoes');
const C = { bg: '#080C12', yellow: '#FCEE09', cyan: '#00F0FF', red: '#FF375A', white: '#DEE5EE', line: '#202D3D' };
const fps = 20;

function svgOpen(width, height, title, description) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="title desc"><title id="title">${title}</title><desc id="desc">${description}</desc>`;
}

function dividerSvg({ animated = true, t = 5 } = {}) {
  const period = 12;
  const x = -160 + (1520 * (t % period) / period);
  const opacity = Math.min(1, Math.max(0, Math.min(t % period, period - (t % period)) / 0.8));
  const geometry = 'M0 40H54L74 20H200L218 38H972L990 20H1124L1144 40H1200';
  return svgOpen(1200, 64, 'Divisória — pulso de criação', 'Uma linha angular amarela recebe um pulso ciano lento. Animação decorativa, sem flashes.') + `
  <defs>
    <linearGradient id="scan" gradientUnits="userSpaceOnUse" x1="${animated ? -80 : x - 80}" y1="0" x2="${animated ? 80 : x + 80}" y2="0">
      <stop offset="0" stop-color="${C.cyan}" stop-opacity="0"/><stop offset="0.35" stop-color="${C.cyan}" stop-opacity="0.4"/><stop offset="0.5" stop-color="${C.cyan}"/><stop offset="0.65" stop-color="${C.cyan}" stop-opacity="0.4"/><stop offset="1" stop-color="${C.cyan}" stop-opacity="0"/>
      ${animated ? '<animateTransform attributeName="gradientTransform" type="translate" values="-160 0;1360 0" dur="12s" repeatCount="indefinite"/>' : ''}
    </linearGradient>
  </defs>
  <rect width="1200" height="64" fill="${C.bg}"/>
  <path d="${geometry}" fill="none" stroke="${C.line}" stroke-width="7"/>
  <path d="${geometry}" fill="none" stroke="${C.yellow}" stroke-width="1.6" opacity="0.76"/>
  <path d="${geometry}" fill="none" stroke="url(#scan)" stroke-width="4" opacity="${animated ? 1 : opacity}">
    ${animated ? '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.067;0.933;1" dur="12s" repeatCount="indefinite"/>' : ''}
  </path>
  <path d="M90 31H148M1050 31H1108" stroke="${C.line}" stroke-width="2"/>
  <path d="M165 27L171 21M175 27L181 21" stroke="${C.red}" stroke-width="2"/>
  <path d="M1010 21L1016 27M1020 21L1026 27" stroke="${C.yellow}" stroke-width="2" opacity="0.65"/>
</svg>`;
}

const phrase = 'CRIANDO. EXPERIMENTANDO. EVOLUINDO.';
const charWidth = 19.3;
const lineWidth = phrase.length * charWidth;
const phraseStart = 64;
function terminalState(t) {
  t %= 10;
  const count = t < 0.8 ? 0 : t >= 2.6 ? phrase.length : Math.min(phrase.length, Math.floor((t - 0.8) / 1.8 * phrase.length));
  const opacity = t < 9.5 ? 1 : Math.max(0, (10 - t) / 0.5);
  return { width: count * charWidth, opacity };
}
function revealAnimation(attribute, offset = 0) {
  const times = [0, 0.08];
  const values = [offset, offset];
  for (let i = 1; i <= phrase.length; i++) {
    times.push((0.8 + 1.8 * i / phrase.length) / 10);
    values.push(offset + i * charWidth);
  }
  times.push(1);
  values.push(offset + lineWidth);
  return `<animate attributeName="${attribute}" values="${values.map(n => n.toFixed(2)).join(';')}" keyTimes="${times.map(n => n.toFixed(5)).join(';')}" calcMode="discrete" dur="10s" repeatCount="indefinite"/>`;
}
function terminalSvg({ animated = true, t = 5 } = {}) {
  const state = terminalState(t);
  const width = animated ? lineWidth : state.width;
  return svgOpen(1200, 180, 'Terminal de criação de @phbr63', '@phbr63. Criando. Experimentando. Evoluindo. A frase é revelada brevemente e permanece legível durante uma pausa longa; nenhum status ou indicador de atividade real é representado.') + `
  <defs><clipPath id="reveal"><rect x="${phraseStart}" y="87" width="${width}" height="42">${animated ? revealAnimation('width') : ''}</rect></clipPath></defs>
  <rect width="1200" height="180" fill="${C.bg}"/>
  <path d="M20 1H1168L1199 32V159L1179 179H1V20Z" fill="none" stroke="${C.line}" stroke-width="2"/>
  <path d="M1 52V20L20 1H168M1032 179H1179L1199 159V128" fill="none" stroke="${C.yellow}" stroke-width="2"/>
  <path d="M1150 1H1168L1199 32V59" fill="none" stroke="${C.cyan}" stroke-width="2" opacity="0.8"/>
  <path d="M20 155H32M20 161H32M20 167H32" stroke="${C.red}" stroke-width="2"/>
  <path d="M1088 149H1120L1133 136H1166" fill="none" stroke="${C.line}" stroke-width="2"/>
  <g font-family="DejaVu Sans Mono,monospace">
    <text x="34" y="65" fill="${C.cyan}" font-size="26" font-weight="700">&gt;</text>
    <text x="${phraseStart}" y="65" fill="${C.yellow}" font-size="29" font-weight="700">@phbr63</text>
    <text x="1135" y="40" fill="#798698" font-size="13" letter-spacing="2" text-anchor="end">PEDRO / ZAMPRONHA</text>
    <g opacity="${animated ? 1 : state.opacity}">
      ${animated ? '<animate attributeName="opacity" values="1;1;0" keyTimes="0;0.95;1" dur="10s" repeatCount="indefinite"/>' : ''}
      <text x="${phraseStart}" y="118" fill="${C.white}" font-size="32" textLength="${lineWidth}" lengthAdjust="spacingAndGlyphs" clip-path="url(#reveal)">${phrase}</text>
      <rect x="${phraseStart + width + 7}" y="95" width="2" height="28" fill="${C.cyan}" opacity="0.78">
        ${animated ? revealAnimation('x', phraseStart + 7) : ''}
      </rect>
    </g>
    <text x="${phraseStart}" y="155" fill="#657386" font-size="12" letter-spacing="2">IDEIAS EM MOVIMENTO</text>
  </g>
</svg>`;
}

async function writeAsset(name, generator, duration, fallbackTime) {
  await fs.writeFile(path.join(dest, `${name}.svg`), generator({ animated: true }), 'utf8');
  await sharp(Buffer.from(generator({ animated: false, t: fallbackTime }))).png().toFile(path.join(dest, `${name}.png`));
  const total = duration * fps;
  const frames = new Array(total);
  let info;
  for (let start = 0; start < total; start += 8) {
    await Promise.all(Array.from({ length: Math.min(8, total - start) }, async (_, j) => {
      const i = start + j;
      const rendered = await sharp(Buffer.from(generator({ animated: false, t: i / fps }))).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
      frames[i] = rendered.data;
      info = rendered.info;
    }));
  }
  const gifPath = path.join(dest, `${name}.gif`);
  await sharp(Buffer.concat(frames), { raw: { width: info.width, height: info.height * total, channels: 4, pageHeight: info.height } })
    .gif({ delay: Array(total).fill(1000 / fps), loop: 0, colours: 128, dither: 0, effort: 7, keepDuplicateFrames: false })
    .toFile(gifPath);
  const files = await Promise.all(['svg', 'png', 'gif'].map(async ext => {
    const nameWithExt = `${name}.${ext}`;
    return { file: nameWithExt, bytes: (await fs.stat(path.join(dest, nameWithExt))).size };
  }));
  console.log(JSON.stringify({ asset: name, durationSeconds: duration, fps, files }));
}

await fs.mkdir(dest, { recursive: true });
await writeAsset('divisoria-scan', dividerSvg, 12, 6);
await writeAsset('terminal-conexao', terminalSvg, 10, 5);
