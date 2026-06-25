const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const root = path.join(__dirname, '..');
const artDir = path.join(root, 'art');
const wwwArtDir = path.join(root, 'www', 'art');
const tempMediaDir = `C:\\Users\\User\\.gemini\\antigravity\\brain\\80f6a430-21e4-4b82-8b61-de530470d5f9\\.tempmediaStorage`;

const mapping = {
  "Gemini_Generated_Image_31qt2031qt2031qt_seo.jpg": { "size": 780775, "type": "animal", "id": "dog_husky", "stage": "legendary" },
  "Gemini_Generated_Image_3m8iow3m8iow3m8i_seo.jpg": { "size": 486826, "type": "animal", "id": "dog_retriever", "stage": "child" },
  "Gemini_Generated_Image_5qpyh65qpyh65qpy_seo.jpg": { "size": 468732, "type": "animal", "id": "dog_retriever", "stage": "baby" },
  "Gemini_Generated_Image_62gwku62gwku62gw_seo.jpg": { "size": 301742, "type": "animal", "id": "cat", "stage": "baby" },
  "Gemini_Generated_Image_6z29le6z29le6z29_seo.jpg": { "size": 517565, "type": "animal", "id": "cat", "stage": "teen" },
  "Gemini_Generated_Image_7gmvsn7gmvsn7gmv_seo.jpg": { "size": 304272, "type": "animal", "id": "fox", "stage": "baby" },
  "Gemini_Generated_Image_8by338by338by338_seo.jpg": { "size": 509427, "type": "animal", "id": "hamster", "stage": "child" },
  "Gemini_Generated_Image_8kzuuj8kzuuj8kzu_seo.jpg": { "size": 626751, "type": "animal", "id": "dog_husky", "stage": "adult" },
  "Gemini_Generated_Image_93z92o93z92o93z9_seo.jpg": { "size": 592566, "type": "animal", "id": "fox", "stage": "teen" },
  "Gemini_Generated_Image_dkq0l8dkq0l8dkq0_seo.jpg": { "size": 515782, "type": "animal", "id": "hamster", "stage": "teen" },
  "Gemini_Generated_Image_hkyn5khkyn5khkyn_seo.jpg": { "size": 659511, "type": "animal", "id": "fox", "stage": "child" },
  "Gemini_Generated_Image_iiwvcviiwvcviiwv_seo.jpg": { "size": 552386, "type": "animal", "id": "dog_pomeranian", "stage": "child" },
  "Gemini_Generated_Image_j6io6kj6io6kj6io_seo.jpg": { "size": 1174339, "type": "animal", "id": "dog_pomeranian", "stage": "legendary" },
  "Gemini_Generated_Image_kbl20zkbl20zkbl2_seo.jpg": { "size": 539738, "type": "animal", "id": "dog_husky", "stage": "baby" },
  "Gemini_Generated_Image_kzcu6hkzcu6hkzcu_seo.jpg": { "size": 569300, "type": "animal", "id": "dog_pomeranian", "stage": "teen" },
  "Gemini_Generated_Image_mo2vjrmo2vjrmo2v_seo.jpg": { "size": 763854, "type": "animal", "id": "fox", "stage": "adult" },
  "Gemini_Generated_Image_my5d9pmy5d9pmy5d_seo.jpg": { "size": 337650, "type": "animal", "id": "hamster", "stage": "baby" },
  "Gemini_Generated_Image_ne11june11june11_seo.jpg": { "size": 854436, "type": "animal", "id": "cat", "stage": "legendary" },
  "Gemini_Generated_Image_pge2bipge2bipge2_seo.jpg": { "size": 539230, "type": "animal", "id": "hamster", "stage": "legendary" },
  "Gemini_Generated_Image_thy9zjthy9zjthy9_seo.jpg": { "size": 513198, "type": "animal", "id": "cat", "stage": "child" },
  "Gemini_Generated_Image_tisclxtisclxtisc_seo.jpg": { "size": 518686, "type": "animal", "id": "dog_husky", "stage": "teen" },
  "Gemini_Generated_Image_tq2msatq2msatq2m_seo.jpg": { "size": 862156, "type": "animal", "id": "fox", "stage": "legendary" },
  "Gemini_Generated_Image_w1v8zww1v8zww1v8_seo.jpg": { "size": 537437, "type": "animal", "id": "dog_husky", "stage": "child" },
  "Gemini_Generated_Image_w9vvww9vvww9vvww_seo.jpg": { "size": 551529, "type": "animal", "id": "cat", "stage": "adult" },
  "Gemini_Generated_Image_x1um8gx1um8gx1um_seo.jpg": { "size": 477595, "type": "animal", "id": "dog_pomeranian", "stage": "baby" },
  "Gemini_Generated_Image_y5vagzy5vagzy5va_seo.jpg": { "size": 492878, "type": "animal", "id": "hamster", "stage": "adult" },
  "chrome_7o9kufT4eb_seo.jpg": { "size": 20841, "type": "animal", "id": "dog_retriever", "stage": "teen" },
  "chrome_CPMvzfjN7x_seo.jpg": { "size": 48705, "type": "animal", "id": "dog_pomeranian", "stage": "adult" },
  "chrome_aD4nb4pUYH_seo.jpg": { "size": 57827, "type": "animal", "id": "dog_retriever", "stage": "legendary" },
  "chrome_cCkKEmi36w_seo.jpg": { "size": 39563, "type": "animal", "id": "dog_retriever", "stage": "adult" }
};

// Step 1: Find tempmedia files and recover them to art/
console.log('🔄 Restoring original files from tempmediaStorage...');
const tempFiles = fs.readdirSync(tempMediaDir).map(name => {
  const filePath = path.join(tempMediaDir, name);
  const stat = fs.statSync(filePath);
  return { name, path: filePath, size: stat.size };
});

for (const [origName, info] of Object.entries(mapping)) {
  // Find a temp file with matching size
  const found = tempFiles.find(tf => tf.size === info.size);
  if (!found) {
    console.error(`❌ Could not find a backup file with size ${info.size} for ${origName}`);
    continue;
  }
  
  const destPath = path.join(artDir, origName);
  fs.copyFileSync(found.path, destPath);
  console.log(`✓ Restored: art/${origName} (from ${found.name})`);
}

// Step 2: Convert restored files with fit:contain and background: transparent
console.log('\n⏳ Converting images with fit:contain (transparent backgrounds)...');
async function convert() {
  for (const [filename, info] of Object.entries(mapping)) {
    const srcPath = path.join(artDir, filename);
    if (!fs.existsSync(srcPath)) {
      console.warn(`⚠️ Source file not found: art/${filename}`);
      continue;
    }

    const dstName = `char_${info.id}_${info.stage}.webp`;
    const dstPath = path.join(artDir, dstName);

    try {
      console.log(`⏳ Converting art/${filename} → art/${dstName}...`);
      await sharp(srcPath)
        .resize(256, 320, { 
          fit: 'contain', 
          background: { r: 0, g: 0, b: 0, alpha: 0 } 
        })
        .webp({ quality: 90 })
        .toFile(dstPath);

      console.log(`✓ Created art/${dstName}`);
      fs.unlinkSync(srcPath); // Clean up original
    } catch (err) {
      console.error(`❌ Failed to convert ${filename}:`, err);
    }
  }

  // Step 3: Delete obsolete files
  console.log('\n🗑️ Deleting obsolete files from art/ and www/art/...');
  const obsoleteFiles = [
    'char_dog_adult.webp',
    'char_dog_baby.webp',
    'char_dog_child.webp',
    'char_dog_legendary.webp',
    'char_dog_teen.webp',
    'char_fish_adult.webp',
    'char_fish_baby.webp',
    'char_fish_child.webp',
    'char_fish_legendary.webp',
    'char_fish_teen.webp'
  ];

  obsoleteFiles.forEach(file => {
    [artDir, wwwArtDir].forEach(dir => {
      const filePath = path.join(dir, file);
      if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
        console.log(`🗑️ Deleted obsolete file: ${path.relative(root, filePath)}`);
      }
    });
  });

  // Step 4: Sync to www
  console.log('\n⏳ Syncing to www folder...');
  try {
    require('./copy-web.js');
    console.log('✨ Done! Image conversion and sync completed successfully.');
  } catch (err) {
    console.error('❌ Sync failed:', err);
  }
}

convert();
