// Image pipeline for pitch prototypes. Usage: node tools/images.js images.json
// images.json: { "src": "assets-src", "out": "assets/img",
//   "photos": { "hero": ["file.jpg", [800, 1280, 1920]], "service-1": ["x.jpg", [640, 1000, 1400]] },
//   "logo": "logo.jpg", "favicon": "favicon.png",
//   "og": { "photo": "file.jpg", "title": "Lawn care & pest control", "subtitle": "City, State", "phone": "(000) 000-0000", "accent": "#5fb944" } }
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");
const cfg = JSON.parse(fs.readFileSync(process.argv[2] || "images.json", "utf8"));
const src = (f) => path.join(cfg.src, f);
fs.mkdirSync(cfg.out, { recursive: true });

(async () => {
  for (const [name, [file, widths]] of Object.entries(cfg.photos || {})) {
    for (const w of widths) {
      const q = name === "hero" ? 58 : 70; // the hero is the largest image on the page
      const info = await sharp(src(file)).resize({ width: w, withoutEnlargement: true }).webp({ quality: q }).toFile(path.join(cfg.out, `${name}-${w}.webp`));
      console.log(name, w, `${info.width}x${info.height}`, Math.round(info.size / 1024) + "KB");
    }
  }
  if (cfg.logo) {
    // Turn a white JPG background into real transparency (color-to-alpha against white).
    const { data, info } = await sharp(src(cfg.logo)).removeAlpha().raw().toBuffer({ resolveWithObject: true });
    const out = Buffer.alloc(info.width * info.height * 4);
    for (let i = 0, j = 0; i < data.length; i += 3, j += 4) {
      const [r, g, b] = [data[i], data[i + 1], data[i + 2]];
      const a = Math.max(255 - r, 255 - g, 255 - b);
      const alpha = a < 10 ? 0 : a;
      const un = (c) => (alpha === 0 ? 0 : Math.max(0, Math.min(255, Math.round((c - 255 * (1 - alpha / 255)) / (alpha / 255)))));
      out[j] = un(r); out[j + 1] = un(g); out[j + 2] = un(b); out[j + 3] = alpha;
    }
    const logo = await sharp(out, { raw: { width: info.width, height: info.height, channels: 4 } }).trim().png().toBuffer();
    await sharp(logo).resize({ height: 160 }).webp({ quality: 90, alphaQuality: 100 }).toFile(path.join(cfg.out, "logo.webp"));
    await sharp(logo).resize({ height: 160 }).png().toFile(path.join(cfg.out, "logo.png"));
    const m = await sharp(path.join(cfg.out, "logo.png")).metadata();
    console.log("logo", `${m.width}x${m.height}`, "(use these as the <img> width/height)");
  }
  if (cfg.favicon) {
    await sharp(src(cfg.favicon)).resize(32, 32).png().toFile(path.join(cfg.out, "favicon-32.png"));
    await sharp(src(cfg.favicon)).resize(180, 180).flatten({ background: "#ffffff" }).png().toFile(path.join(cfg.out, "apple-touch-icon.png"));
  }
  if (cfg.og) {
    const o = cfg.og;
    const bg = await sharp(src(o.photo)).resize(1200, 630, { fit: "cover" }).modulate({ brightness: 0.55 }).toBuffer();
    const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;");
    const svg = Buffer.from(`<svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
      <text x="70" y="420" font-family="Arial" font-weight="800" font-size="62" fill="#fff">${esc(o.title)}</text>
      <text x="70" y="485" font-family="Arial" font-weight="700" font-size="34" fill="${o.accent || "#fff"}">${esc(o.subtitle)}</text>
      <text x="70" y="545" font-family="Arial" font-size="30" fill="#fff">${esc(o.phone)}</text></svg>`);
    const layers = [{ input: svg, left: 0, top: 0 }];
    if (fs.existsSync(path.join(cfg.out, "logo.png"))) {
      const l = await sharp(path.join(cfg.out, "logo.png")).resize({ width: 240, height: 170, fit: "inside" }).toBuffer();
      const tile = await sharp({ create: { width: 290, height: 200, channels: 4, background: "#ffffff" } }).composite([{ input: l, gravity: "center" }]).png().toBuffer();
      layers.unshift({ input: tile, left: 70, top: 70 });
    }
    await sharp(bg).composite(layers).jpeg({ quality: 82 }).toFile(path.join(cfg.out, "og-image.jpg"));
  }
  console.log("done");
})();
