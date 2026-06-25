const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const root = path.join(__dirname, '..');
const artDir = path.join(root, 'art');
const mappingFile = path.join(root, 'mapping.json');

async function processImages() {
  if (!fs.existsSync(mappingFile)) {
    console.error('❌ mapping.json file not found! Please place it in the project root.');
    process.exit(1);
  }

  const mapping = JSON.parse(fs.readFileSync(mappingFile, 'utf8'));
  console.log(`🔍 Read mapping.json: ${Object.keys(mapping).length} images to process.`);

  for (const [filename, info] of Object.entries(mapping)) {
    const srcPath = path.join(artDir, filename);
    if (!fs.existsSync(srcPath)) {
      console.warn(`⚠️ Source file not found: art/${filename}`);
      continue;
    }

    let dstName = '';
    let targetWidth = 0;
    let targetHeight = 0;

    if (info.type === 'animal') {
      dstName = `char_${info.id}_${info.stage}.webp`;
      targetWidth = 256;
      targetHeight = 320;
    } else if (info.type === 'bg') {
      dstName = `bg-${info.tier}.webp`;
      targetWidth = 832;
      targetHeight = 1216;
    } else {
      console.log(`⏭️ Skipping art/${filename}`);
      continue;
    }

    const dstPath = path.join(artDir, dstName);

    try {
      console.log(`⏳ Converting art/${filename} → art/${dstName}...`);
      await sharp(srcPath)
        .resize(targetWidth, targetHeight, { fit: 'cover' })
        .webp({ quality: 90 })
        .toFile(dstPath);

      console.log(`✓ Created art/${dstName}`);
      
      // Delete original JPG file
      fs.unlinkSync(srcPath);
      console.log(`🗑️ Deleted original art/${filename}`);
    } catch (err) {
      console.error(`❌ Failed to convert ${filename}:`, err);
    }
  }

  console.log('✨ Image conversion completed.');

  // Re-run copy script to mirror to www/
  try {
    console.log('⏳ Syncing assets to www/ folder...');
    require('./copy-web.js');
    console.log('✓ Assets synchronized successfully!');
  } catch (err) {
    console.error('❌ Failed to run copy-web.js:', err);
  }
}

processImages();
