// 조판된 잡지에서 DOCX·HWPX용 흐름 문서 구조를 뽑는다
// 글은 문단 제목 표 상자로 옮기고 차트 도식 타일처럼 모양이 의미인 요소는 그림으로 캡처한다
// 사용법  NODE_PATH=$(npm root -g) node export/extract.js  →  export/out/ir.json, export/out/img/*.png
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const root = path.dirname(__dirname);
  const out = path.join(__dirname, 'out');
  if (process.env.CLEAN) fs.rmSync(out, { recursive: true, force: true });
  fs.mkdirSync(path.join(out, 'img'), { recursive: true });
  const exe = process.env.CHROMIUM_PATH || fs.readdirSync('/opt/pw-browsers').filter(d => d.startsWith('chromium-')).map(d => `/opt/pw-browsers/${d}/chrome-linux/chrome`)[0];
  const browser = await chromium.launch({ executablePath: exe });
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 2.5 });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await page.goto('file://' + path.join(root, 'heuresis-vol01.html'), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'print' });

  const ir = await page.evaluate(() => {
    let nimg = 0;
    const pages = [...document.querySelectorAll('.page')];
    const BLOCK = 'P,LI,TABLE,H1,H2,H3,H4,UL,OL';
    const SKIP = el => el.matches('.rh,.folio,.cont,[aria-hidden="true"],script,style') || getComputedStyle(el).display === 'none';
    const markImg = (el, kind) => { const id = 'i' + String(++nimg).padStart(3, '0'); el.setAttribute('data-ximg', id); const r = el.getBoundingClientRect(); return { t: 'img', id, w: r.width, h: r.height, kind }; };

    const isVisual = el => {
      if (el.tagName === 'svg' || el.matches('.flow,.stats,[data-art]')) return true;
      if (el.tagName !== 'DIV') return false;
      if (el.querySelector(BLOCK + ',.box,.card,.lab-app,.pq')) return false;
      const cs = getComputedStyle(el);
      const kids = el.children.length;
      if ((cs.display === 'grid' || cs.display === 'flex') && kids >= 2) return true;
      if (el.querySelector('svg')) return true;
      // 배경색 막대로 그린 차트
      const bars = [...el.querySelectorAll('div')].filter(d => { const c = getComputedStyle(d).backgroundColor; return c !== 'rgba(0, 0, 0, 0)' && d.textContent.trim().length < 12; });
      return bars.length >= 2;
    };

    const runs = el => {
      const out = [];
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
      let n;
      while ((n = walker.nextNode())) {
        if (n.nodeType === 1) { if (n.tagName === 'BR') { const l = out[out.length - 1]; if (l) l.t += '\n'; } continue; }
        const p = n.parentElement;
        if (p.closest('.rh,.folio,[data-pageof]')) continue;
        let t = n.textContent.replace(/[\n\t\r]+/g, ' ').replace(/ {2,}/g, ' ');
        if (!t) continue;
        const cs = getComputedStyle(p);
        const bold = parseInt(cs.fontWeight, 10) >= 600;
        const ital = cs.fontStyle === 'italic';
        const mono = /Plex/.test(cs.fontFamily);
        const last = out[out.length - 1];
        if (last && last.b === bold && last.i === ital && last.m === mono) last.t += t; else out.push({ t, b: bold, i: ital, m: mono });
      }
      if (out.length) { out[0].t = out[0].t.replace(/^\s+/, ''); out[out.length - 1].t = out[out.length - 1].t.replace(/\s+$/, ''); }
      return out.filter(r => r.t);
    };
    const text = el => el.textContent.replace(/\s+/g, ' ').trim();

    function walk(el, acc) {
      if (SKIP(el)) return;
      if (el.querySelector('[data-pageof]') && !el.querySelector(BLOCK)) { if (text(el)) acc.push({ t: 'p', toc: true, r: runs(el) }); return; }
      if (isVisual(el)) { if (el.getBoundingClientRect().height > 4) acc.push(markImg(el, 'figure')); return; }
      const tag = el.tagName;
      if (tag === 'H1' || el.matches('.title')) return acc.push({ t: 'h', l: 1, r: runs(el) });
      if (tag === 'H2' || el.matches('.head')) return acc.push({ t: 'h', l: 2, r: runs(el) });
      if (tag === 'H3') return acc.push({ t: 'h', l: 3, r: runs(el) });
      if (tag === 'H4') return acc.push({ t: 'h', l: 4, r: runs(el) });
      if (el.matches('.kicker,.bt,.sp-badge')) return text(el) && acc.push({ t: 'label', r: runs(el) });
      if (el.matches('.dek')) return acc.push({ t: 'dek', r: runs(el) });
      if (el.matches('.byline,.src')) return acc.push({ t: 'small', r: runs(el) });
      if (tag === 'UL' || tag === 'OL') {
        [...el.children].forEach(li => { if (li.tagName === 'LI' && text(li)) acc.push({ t: 'li', ord: tag === 'OL', check: el.matches('.checklist'), r: runs(li) }); });
        return;
      }
      if (tag === 'P' || tag === 'LI') { if (text(el)) acc.push({ t: 'p', lead: el.matches('.lead'), r: runs(el) }); return; }
      if (tag === 'TABLE') {
        const rows = [...el.rows].map(tr => [...tr.cells].map(c => ({ r: runs(c), th: c.tagName === 'TH' })));
        const imgs = [...el.querySelectorAll('.ev')].length;
        return acc.push({ t: 'table', rows, badges: imgs });
      }
      if (el.matches('.pq')) { const p = el.querySelector('p'), c = el.querySelector('cite'); return acc.push({ t: 'quote', r: p ? runs(p) : runs(el), cite: c ? text(c) : '' }); }
      if (el.matches('.box,.card,.lab-app,.take,.verdict')) {
        const kids = [];
        if (el.matches('.take,.verdict')) kids.push({ t: 'p', r: runs(el) });
        else [...el.childNodes].forEach(ch => { if (ch.nodeType === 1) walk(ch, kids); else if (ch.textContent.trim()) kids.push({ t: 'p', r: [{ t: ch.textContent.trim(), b: false }] }); });
        const cs = getComputedStyle(el);
        const variant = el.matches('.navy') ? 'navy' : el.matches('.teal') ? 'teal' : el.matches('.ochre') ? 'ochre' : el.matches('.line') ? 'line' : el.matches('.card,.lab-app') ? 'card' : 'sand';
        return kids.length && acc.push({ t: 'box', v: variant, bg: cs.backgroundColor, c: kids });
      }
      if (el.matches('.ev')) return; // 근거 배지는 주변 표나 카드에 글로 남는다
      // 블록 자식이 없는 말단 div는 문단으로
      const blockKids = [...el.children].filter(c => { const d = getComputedStyle(c).display; return d !== 'inline' && d !== 'inline-block' && d !== 'inline-flex' && c.tagName !== 'BR' && c.tagName !== 'B' && c.tagName !== 'STRONG' && c.tagName !== 'EM' && c.tagName !== 'SPAN' && c.tagName !== 'I' && c.tagName !== 'A'; });
      if (!blockKids.length) { if (text(el)) acc.push({ t: 'p', r: runs(el) }); return; }
      [...el.childNodes].forEach(ch => { if (ch.nodeType === 1) walk(ch, acc); else if (ch.textContent.trim()) acc.push({ t: 'p', r: [{ t: ch.textContent.trim(), b: false }] }); });
    }

    return pages.map((pg, i) => {
      const acc = [];
      const sec = pg.id && pg.id.startsWith('sec-') ? pg.id : null;
      const theme = pg.classList.contains('clinic') ? 'clinic' : pg.classList.contains('teacher') ? 'teacher' : '';
      const rh = pg.querySelector('.rh .sec');
      const inner = pg.querySelector('.inner');
      if (!inner) { acc.push(markImg(pg, 'page')); return { n: i + 1, sec, theme, rh: '', b: acc }; }
      const band = pg.querySelector('.opener-band');
      if (band) {
        const ot = band.querySelector('.opener-text');
        acc.push(markImg(band.querySelector('svg') || band, 'band'));
        if (ot) walk(ot, acc);
      }
      walk(inner, acc);
      return { n: i + 1, sec, theme, rh: rh ? rh.textContent.trim() : '', b: acc };
    });
  });

  // 그림 캡처  밴드는 제목 글자를 숨기고 배경만 찍는다
  await page.addStyleTag({ content: '.opener-text,.rh{visibility:hidden}' });
  const ids = await page.$$eval('[data-ximg]', els => els.map(e => e.getAttribute('data-ximg')));
  for (const id of ids) {
    const el = await page.$(`[data-ximg="${id}"]`);
    try { await el.screenshot({ path: path.join(out, 'img', id + '.png') }); } catch (e) { console.error('skip', id, e.message); }
  }
  fs.writeFileSync(path.join(out, 'ir.json'), JSON.stringify(ir));
  const count = t => ir.reduce((s, p) => s + p.b.filter(b => b.t === t).length, 0);
  console.log(`pages ${ir.length}  images ${ids.length}  paragraphs ${count('p')}  tables ${count('table')}  boxes ${count('box')}`);
  await browser.close();
})();
