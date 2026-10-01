// Heurēsis 조판 파일을 PDF와 쪽별 미리보기 PNG로 렌더링하고 넘침을 검사한다
// 사용법  NODE_PATH=$(npm root -g) node render.js [--png]
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const src = path.join(__dirname, 'heuresis-vol01.html');
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  // 로컬에 설치된 폰트를 쓰도록 웹폰트 요청은 막는다
  await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await page.goto('file://' + src, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  // 넘침 검사  .inner 안의 요소가 영역 밖으로 나가거나 다단이 가로로 넘치면 보고한다
  const issues = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.page').forEach(pg => {
      const inner = pg.querySelector('.inner');
      if (!inner) return;
      const box = inner.getBoundingClientRect();
      inner.querySelectorAll('*').forEach(e => {
        const r = e.getBoundingClientRect();
        if (r.height && r.bottom > box.bottom + 1) out.push(`${pg.id}: ${e.tagName}.${e.className} bottom +${(r.bottom - box.bottom).toFixed(0)}px`);
      });
      inner.querySelectorAll('.cols2,.cols3').forEach(c => {
        if (c.scrollWidth > c.clientWidth + 2) out.push(`${pg.id}: columns overflow ${c.scrollWidth - c.clientWidth}px`);
      });
    });
    return [...new Set(out)].slice(0, 80);
  });
  console.log(issues.length ? issues.join('\n') : 'no overflow');

  await page.pdf({ path: path.join(__dirname, 'Heuresis_Vol01_창간특집호.pdf'), width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });

  if (process.argv.includes('--png')) {
    const dir = process.env.PNG_DIR || path.join(__dirname, 'preview');
    require('fs').mkdirSync(dir, { recursive: true });
    await page.emulateMedia({ media: 'print' });
    const pages = await page.$$('.page');
    for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(dir, `p${String(i + 1).padStart(2, '0')}.png`) });
  }
  await browser.close();
})();
