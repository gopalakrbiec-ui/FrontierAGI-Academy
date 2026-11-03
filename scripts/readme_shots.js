// Refreshes the README pictures in assets/readme/ (run from the repo root):
//   python3 -m http.server 8765 &   then   node scripts/readme_shots.js
// Needs Playwright (Chromium) and ffmpeg. Stills are PNG converted to WebP by ffmpeg; 🎞️ maps are short GIFs.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
const BASE = process.env.BASE || 'http://localhost:8765/';
const OUT = path.join(__dirname, '..', 'assets', 'readme'), TMP = fs.mkdtempSync('/tmp/rs-');
const M = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'readme-maps.json'), 'utf8'));
fs.mkdirSync(OUT, { recursive: true });
const webp = (png, out, w) => execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', png, '-vf', 'scale=' + w + ':-1', '-quality', '72', out]);
const GIF = { // page: how to animate it
  'maestro-journey': async p => { await p.goto(BASE + 'pages/maestro-journey.html?embed=1'); await p.waitForTimeout(1200); await p.click('#jrPlay'); },
  'software-stack-live': async p => { await p.goto(BASE + 'pages/software-stack-live.html?embed=1'); await p.waitForTimeout(2500); },
  'ai-factory-3d': async p => { await p.goto(BASE + 'pages/ai-factory-3d.html?embed=1'); await p.waitForTimeout(2500); }
};
(async () => {
  const b = await chromium.launch();
  const shoot = async (page, file, w) => {
    const p = await b.newPage({ viewport: { width: 1280, height: 794 } });
    await p.goto(BASE + (page === 'home' ? 'index.html' : 'pages/' + page + '.html')); await p.waitForTimeout(2500);
    const png = path.join(TMP, file + '.png'); await p.screenshot({ path: png, clip: { x: 0, y: 94, width: 1280, height: 700 } });
    webp(png, path.join(OUT, file), w); await p.close(); console.log('still', file);
  };
  await shoot('home', 'home.webp', 1100);
  for (const [, items] of M.groups) for (const m of items) {
    if (!m.gif) { await shoot(m.page, m.shot, 900); continue; }
    const p = await b.newPage({ viewport: { width: 1000, height: 620 } }); await GIF[m.page](p);
    const dir = fs.mkdtempSync(path.join(TMP, m.page));
    for (let i = 0; i < 36; i++) {
      if (m.page === 'ai-factory-3d') { await p.mouse.move(500, 310); await p.mouse.down({ button: 'right' }); await p.mouse.move(530, 310, { steps: 3 }); await p.mouse.up({ button: 'right' }); }
      await p.screenshot({ path: path.join(dir, String(i).padStart(3, '0') + '.png') }); await p.waitForTimeout(m.page === 'maestro-journey' ? 900 : 160);
    }
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', m.page === 'maestro-journey' ? '3' : '7', '-i', path.join(dir, '%03d.png'), '-vf', 'scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4', path.join(OUT, m.shot)]);
    await p.close(); console.log('gif', m.shot);
  }
  for (const h of M.hubs) await shoot(h.page, h.shot, 600);
  await b.close();
})();
