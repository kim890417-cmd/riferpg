// Generates PWA / launcher icons (PNG) from an inline SVG using sharp.
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const out = path.join(__dirname, '..', 'icons');
fs.mkdirSync(out, { recursive: true });

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#10b981"/>
      <stop offset="1" stop-color="#0ea5e9"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="112" fill="#0f172a"/>
  <rect x="36" y="36" width="440" height="440" rx="92" fill="url(#g)"/>
  <g fill="none" stroke="#ffffff" stroke-width="42" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="160,300 256,212 352,300"/>
    <polyline points="160,372 256,284 352,372" opacity="0.5"/>
  </g>
</svg>`;

const buf = Buffer.from(svg);
const sizes = [192, 512];

Promise.all(sizes.map(s =>
  sharp(buf).resize(s, s).png().toFile(path.join(out, `icon-${s}.png`))
    .then(() => console.log(`✓ icons/icon-${s}.png`))
)).then(() =>
  // apple-touch-icon (no transparency, 180px)
  sharp(buf).resize(180, 180).flatten({ background: '#0f172a' }).png()
    .toFile(path.join(out, 'apple-touch-icon.png'))
    .then(() => console.log('✓ icons/apple-touch-icon.png'))
).catch(e => { console.error(e); process.exit(1); });
