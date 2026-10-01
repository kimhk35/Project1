// 섹션 조각 하나를 단독으로 렌더링해 넘침과 문체 규칙을 검사하고 미리보기 PNG를 만든다
// 사용법  NODE_PATH=$(npm root -g) node check.js src/sections/20-cover.html <png-dir>
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

(async () => {
  const frag = path.resolve(process.argv[2]);
  const outDir = process.argv[3] ? path.resolve(process.argv[3]) : null;
  const tmp = path.join(__dirname, `_check_${path.basename(frag)}`);
  execFileSync('python3', [path.join(__dirname, 'build.py'), frag], { env: { ...process.env, OUT: tmp } });

  const exe = process.env.CHROMIUM_PATH || fs.readdirSync('/opt/pw-browsers').filter(d => d.startsWith('chromium-')).map(d => `/opt/pw-browsers/${d}/chrome-linux/chrome`)[0];
  const browser = await chromium.launch({ executablePath: exe });
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await page.goto('file://' + tmp, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  const report = await page.evaluate(() => {
    const out = [];
    const pages = [...document.querySelectorAll('.page')];
    pages.forEach((pg, i) => {
      const tag = `page ${i + 1}`;
      const inner = pg.querySelector('.inner');
      if (inner) {
        const box = inner.getBoundingClientRect();
        let worst = 0;
        inner.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.height && r.bottom - box.bottom > worst) worst = r.bottom - box.bottom; });
        if (worst > 1) out.push(`${tag}: OVERFLOW bottom +${worst.toFixed(0)}px`);
        inner.querySelectorAll('.cols2,.cols3').forEach(c => { if (c.scrollWidth > c.clientWidth + 2) out.push(`${tag}: OVERFLOW columns (text runs into hidden extra column)`); });
        // 빈 공간 추정  .inner 하단에서 가장 아래 요소까지 거리
        let lowest = box.top;
        inner.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.height && r.bottom > lowest) lowest = r.bottom; });
        const gap = box.bottom - lowest;
        if (gap > 90) out.push(`${tag}: bottom whitespace ${gap.toFixed(0)}px (fill it)`);
      } else out.push(`${tag}: (no .inner)`);
      // 문체 규칙  본문 텍스트의 쌍따옴표와 한글 뒤 마침표
      const walker = document.createTreeWalker(pg, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = walker.nextNode())) {
        const t = n.textContent;
        if (/["“”]/.test(t)) out.push(`${tag}: STYLE double quote in "${t.trim().slice(0, 50)}"`);
        const m = t.match(/[가-힣)\]]\.(\s|$)/);
        if (m) out.push(`${tag}: STYLE sentence period in "${t.trim().slice(Math.max(0, m.index - 30), m.index + 3)}"`);
      }
    });
    return { count: pages.length, issues: out };
  });
  console.log(`pages: ${report.count}`);
  console.log(report.issues.length ? report.issues.join('\n') : 'OK  no overflow, no style violations');

  if (outDir) {
    fs.mkdirSync(outDir, { recursive: true });
    await page.emulateMedia({ media: 'print' });
    const pages = await page.$$('.page');
    for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(outDir, `p${String(i + 1).padStart(3, '0')}.png`) });
    console.log(`png -> ${outDir}`);
  }
  await browser.close();
  fs.unlinkSync(tmp);
})();
