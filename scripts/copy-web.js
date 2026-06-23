// Copies the app's web assets into www/ (the folder we deploy / Capacitor's webDir).
// Edit the app at the project-root index.html; this mirrors everything into www/.
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const www = path.join(root, 'www');
fs.mkdirSync(www, { recursive: true });

// single files
['index.html', 'manifest.webmanifest', 'sw.js'].forEach(f => {
  fs.copyFileSync(path.join(root, f), path.join(www, f));
  console.log('✓ ' + f);
});

// asset folders (copied recursively)
function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  fs.readdirSync(src).forEach(f => {
    const s = path.join(src, f), d = path.join(dst, f);
    if (fs.statSync(s).isDirectory()) copyDir(s, d);
    else { fs.copyFileSync(s, d); console.log('✓ ' + path.relative(root, d)); }
  });
}
['icons', 'vendor', 'art'].forEach(dir => {
  const src = path.join(root, dir);
  if (!fs.existsSync(src)) return;
  copyDir(src, path.join(www, dir));
});

console.log('→ www/ ready to deploy');
