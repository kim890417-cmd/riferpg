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
['icons', 'vendor', 'art'].forEach(dir => {
  const src = path.join(root, dir);
  if (!fs.existsSync(src)) return;
  const dst = path.join(www, dir);
  fs.mkdirSync(dst, { recursive: true });
  fs.readdirSync(src).forEach(f => {
    fs.copyFileSync(path.join(src, f), path.join(dst, f));
    console.log('✓ ' + dir + '/' + f);
  });
});

console.log('→ www/ ready to deploy');
