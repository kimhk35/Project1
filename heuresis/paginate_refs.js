// 참고문헌 항목을 실제로 렌더링하며 쪽마다 넘치기 직전까지 채워 99-back.html을 만든다
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const pageHtml = (n, headHtml, body, sid) => `<section class="page"${sid ? ` id="${sid}"` : ''}>
  <div class="rh"><span><b>Heurēsis</b> · Vol.01</span><span class="sec">References &amp; Sources · ${n}/{TOTAL}</span></div>
  <div class="inner">
${headHtml}
    <div class="refs cols3" style="flex:1;min-height:0;column-fill:auto">
${body}
    </div>
  </div>
  <div class="folio"><span class="n">00</span><span>REFERENCES &amp; SOURCES</span></div>
</section>
`;

(async () => {
  const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'src', 'refs_items.json'), 'utf8'));
  const head = fs.readFileSync(path.join(__dirname, 'src', 'head.html'), 'utf8');
  const exe = process.env.CHROMIUM_PATH || fs.readdirSync('/opt/pw-browsers').filter(d => d.startsWith('chromium-')).map(d => `/opt/pw-browsers/${d}/chrome-linux/chrome`)[0];
  const browser = await chromium.launch({ executablePath: exe });
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  const tmp = path.join(__dirname, '_paginate.html');
  fs.writeFileSync(tmp, head + '<body><div id="host"></div></body></html>');
  await page.goto('file://' + tmp);
  await page.evaluate(() => document.fonts.ready);

  const cont = '    <div class="kicker" style="margin-bottom:3mm">References · 계속</div>';
  const pages = await page.evaluate(({ items, head1, cont }) => {
    const host = document.getElementById('host');
    const out = [];
    let i = 0;
    while (i < items.length) {
      const first = out.length === 0;
      host.innerHTML = `<section class="page"><div class="inner">${first ? head1 : cont}<div class="refs cols3" style="flex:1;min-height:0;column-fill:auto"></div></div></section>`;
      const col = host.querySelector('.cols3');
      const taken = [];
      while (i < items.length) {
        col.insertAdjacentHTML('beforeend', items[i]);
        if (col.scrollWidth > col.clientWidth + 1) { col.lastElementChild.remove(); break; }
        taken.push(items[i]); i++;
      }
      if (!taken.length) { taken.push(items[i]); i++; }
      out.push(taken);
    }
    return out;
  }, { items: data.items, head1: data.head, cont });
  await browser.close();
  fs.unlinkSync(tmp);

  const total = pages.length + 1;
  let html = pages.map((items, k) => pageHtml(k + 1, k === 0 ? data.head : cont, items.join('\n'), k === 0 ? 'sec-refs' : null)).join('\n');
  html = html.replace(/\{TOTAL\}/g, total) + '\n' + data.sources.replace(/\{N\}/g, total);
  fs.writeFileSync(path.join(__dirname, 'src', 'sections', '99-back.html'), html);
  console.log(`references: ${pages.length} pages + sources page`);
})();
