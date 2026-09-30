// PRAXIS render · overflow check, screenshots, chart PNGs, PDF
// usage: node render.js [check|shots|pdf|charts|all] [pages e.g. 1,5-7]
const { chromium } = require(process.env.PW || 'playwright');
const path = require('path'), fs = require('fs');
const mode = process.argv[2] || 'all', sel = process.argv[3] || '';
const B = path.join(__dirname, '_build'), OUT = path.join(__dirname, '..');
const NAME = 'PRAXIS_Vol01_창간특집호';
function want(n){ if(!sel) return true; return sel.split(',').some(r=>{const [a,b]=r.split('-').map(Number);return b?n>=a&&n<=b:n===a}); }
(async () => {
  const browser = await chromium.launch({ executablePath: fs.existsSync('/opt/pw-browsers/chromium') ? undefined : undefined });
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(B, process.env.HTML || 'print.html'));
  await page.evaluate(() => document.fonts.ready);
  if (['check','all','shots'].includes(mode)) {
    const res = await page.evaluate(() => [...document.querySelectorAll('section.page')].map((s, i) => {
      const r = s.getBoundingClientRect(); let worst = 0, who = '';
      s.querySelectorAll('*').forEach(el => { if (el.closest('.runhead,.folio,.cv-art')) return;
        const b = el.getBoundingClientRect(); if (b.width === 0) return;
        const over = Math.max(b.bottom - (r.bottom - 12 * 3.78), b.right - r.right + 1);
        if (over > worst) { worst = over; who = el.tagName + '.' + el.className + ' ' + (el.textContent || '').slice(0, 40); } });
      const cols = [...s.querySelectorAll('.cols-2,.cols-3')].filter(c => c.scrollWidth > c.clientWidth + 2).length;
      return { n: i + 1, id: s.id, over: Math.round(worst), who, colsOverflow: cols };
    }));
    const bad = res.filter(r => r.over > 0 || r.colsOverflow);
    console.log('pages', res.length, 'overflowing', bad.length);
    bad.forEach(b => console.log(`  p${b.n} ${b.id} over=${b.over}px cols=${b.colsOverflow} :: ${b.who}`));
  }
  if (['shots','all'].includes(mode)) {
    const SD = 'shots' + (process.env.HTML ? '_' + process.env.HTML.replace(/\.html$/, '') : ''); fs.mkdirSync(path.join(B, SD), { recursive: true });
    const secs = await page.$$('section.page');
    for (let i = 0; i < secs.length; i++) if (want(i + 1)) await secs[i].screenshot({ path: path.join(B, SD, `p${String(i + 1).padStart(3, '0')}.png`) });
  }
  if (['charts','all'].includes(mode)) {
    fs.mkdirSync(path.join(B, 'charts'), { recursive: true });
    const p2 = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 2.5 });
    await p2.goto('file://' + path.join(B, process.env.HTML || 'print.html')); await p2.evaluate(() => document.fonts.ready);
    const figs = await p2.$$('figure[id] svg, .docx-img');
    for (const f of figs) { const id = await f.evaluate(e => (e.closest('[id]')||{}).id); if (id) await f.screenshot({ path: path.join(B, 'charts', id + '.png') }); }
    const cover = await p2.$('#p-cover'); await cover.screenshot({ path: path.join(B, 'charts', 'cover.png') });
    await p2.close();
  }
  if (['pdf','all'].includes(mode)) {
    await page.pdf({ path: path.join(OUT, NAME + '.pdf'), preferCSSPageSize: true, printBackground: true });
    console.log('pdf written');
  }
  await browser.close();
})();
