//= render.mjs  version 0.1.0 (2026-11-09)
//= Renders docs/mockups/*.html to docs/screenshots/<name>.png at 2x with Playwright (Chromium). The pictures are illustrations.
//= Usage: node scripts/mockups/render.mjs [SRC_DIR] [OUT_DIR]      (needs `playwright`; in this repo: npm i --no-save playwright)
import { createRequire } from "node:module";
import { readdirSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) { console.error("render.mjs: playwright not found (npm i --no-save playwright, or set NODE_PATH)"); process.exit(66); }
const here = dirname(fileURLToPath(import.meta.url));
const src = resolve(process.argv[2] ?? join(here, "../../docs/mockups"));
const out = resolve(process.argv[3] ?? join(here, "../../docs/screenshots"));
const files = readdirSync(src).filter((f) => f.endsWith(".html")).sort();
if (files.length === 0) { console.error(`render.mjs: no .html files in ${src}`); process.exit(66); }

const browser = await chromium.launch();
const ctx = await browser.newContext({ deviceScaleFactor: 2, viewport: { width: 1400, height: 900 } });
const pg = await ctx.newPage();
for (const f of files) {
  await pg.goto(pathToFileURL(join(src, f)).href);
  await pg.evaluate(() => document.fonts.ready);
  const box = await pg.locator(".stage").boundingBox();
  await pg.screenshot({ path: join(out, f.replace(/\.html$/, ".png")), fullPage: true, clip: box });
  console.log(`rendered ${f}`);
}
await browser.close();
