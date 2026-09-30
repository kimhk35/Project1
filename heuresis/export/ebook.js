// Heurēsis e-book 뷰어  펼침과 단면 보기 차례 키보드 스와이프 주소 해시를 지원한다
(function () {
  const pages = [...document.querySelectorAll('body > .page')];
  const N = pages.length, W = 794, H = 1123;
  const spread = document.getElementById('eb-spread'), stage = document.getElementById('eb-stage');
  const count = document.getElementById('eb-count'), range = document.getElementById('eb-range');
  const modeBtn = document.getElementById('eb-mode'), toc = document.getElementById('eb-toc');
  const home = document.createElement('div'); home.id = 'eb-home'; home.hidden = true; document.body.appendChild(home);
  pages.forEach(p => home.appendChild(p));
  range.max = N;
  let two = matchMedia('(min-aspect-ratio: 5/4)').matches && innerWidth > 900;
  let cur = Math.min(Math.max(parseInt((location.hash.match(/\d+/) || ['1'])[0], 10) || 1, 1), N);

  // 펼침에서는 표지를 홀로 두고 2-3 4-5 식으로 짝을 짓는다
  const group = i => { if (!two || i === 1) return [i]; const a = i % 2 === 0 ? i : i - 1; return a + 1 <= N ? [a, a + 1] : [a]; };

  // 확대 배율 z는 화면 맞춤 배율에 곱한다  z=1이 맞춤
  const sizer = document.getElementById('eb-sizer'), zlabel = document.getElementById('eb-zlabel');
  let z = 1; const ZMIN = 0.5, ZMAX = 4;
  function fitScale() { const g = group(cur).length; return Math.min((stage.clientWidth - 40) / (W * g), (stage.clientHeight - 32) / H); }
  function fit(anchor) {
    const g = group(cur).length, s = fitScale() * z;
    // 기준점을 유지하며 확대하도록 확대 전 비율 위치를 기억한다
    let rx = 0.5, ry = 0.5;
    if (anchor) { const r = sizer.getBoundingClientRect(); rx = (anchor.x - r.left + stage.scrollLeft * 0) / r.width; ry = (anchor.y - r.top) / r.height; }
    else if (stage.scrollWidth > stage.clientWidth || stage.scrollHeight > stage.clientHeight) {
      rx = (stage.scrollLeft + stage.clientWidth / 2) / stage.scrollWidth; ry = (stage.scrollTop + stage.clientHeight / 2) / stage.scrollHeight; }
    spread.style.transform = `scale(${s})`;
    sizer.style.width = (W * g * s) + 'px'; sizer.style.height = (H * s) + 'px';
    stage.classList.toggle('zoomed', z > 1.001);
    zlabel.textContent = z === 1 ? '맞춤' : Math.round(z * 100) + '%';
    const ax = anchor ? anchor.x - stage.getBoundingClientRect().left : stage.clientWidth / 2;
    const ay = anchor ? anchor.y - stage.getBoundingClientRect().top : stage.clientHeight / 2;
    stage.scrollLeft = rx * stage.scrollWidth - ax; stage.scrollTop = ry * stage.scrollHeight - ay;
  }
  function setZoom(v, anchor) { z = Math.min(ZMAX, Math.max(ZMIN, Math.round(v * 100) / 100)); fit(anchor); }
  function show(i, instant) {
    cur = Math.min(Math.max(i, 1), N);
    const g = group(cur);
    const render = () => {
      while (spread.firstChild) home.appendChild(spread.firstChild);
      g.forEach(n => spread.appendChild(pages[n - 1]));
      spread.classList.toggle('two', g.length === 2);
      count.textContent = g.length === 2 ? `${g[0]}–${g[1]} / ${N}` : `${g[0]} / ${N}`;
      range.value = g[0];
      history.replaceState(null, '', '#' + g[0]);
      document.querySelectorAll('#eb-toc-list a').forEach(a => a.classList.toggle('cur', +a.dataset.p <= g[g.length - 1] && +a.dataset.end >= g[0]));
      fit(); stage.scrollTop = 0;
      spread.classList.remove('fade');
    };
    if (instant) render(); else { spread.classList.add('fade'); setTimeout(render, 140); }
  }
  const step = d => { const g = group(cur); show(d > 0 ? g[g.length - 1] + 1 : (two && g[0] > 2 ? g[0] - 2 : g[0] - 1)); };

  // 차례  본문 차례 쪽의 data-pageof 항목을 그대로 가져온다
  const list = document.getElementById('eb-toc-list');
  const items = [...document.querySelectorAll('.toc-row')].filter(r => pages.indexOf(r.closest('.page')) < 3).map(r => {
    const id = r.querySelector('[data-pageof]')?.dataset.pageof; const t = id && document.getElementById(id);
    return t ? { p: pages.indexOf(t.closest('.page')) + 1, c: r.querySelector('.c')?.textContent || '', h: r.querySelector('.h')?.textContent || '' } : null;
  }).filter(Boolean);
  items.unshift({ p: 1, c: 'Cover', h: '표지' }, { p: 2, c: 'Contents', h: '차례' });
  items.sort((a, b) => a.p - b.p);
  items.forEach((it, k) => {
    const end = (items[k + 1] ? items[k + 1].p : N + 1) - 1;
    const li = document.createElement('li');
    li.innerHTML = `<a href="#${it.p}" data-p="${it.p}" data-end="${end}"><span class="n">${String(it.p).padStart(2, '0')}</span><span><span class="c"></span><span class="h"></span></span></a>`;
    li.querySelector('.c').textContent = it.c; li.querySelector('.h').textContent = it.h;
    li.querySelector('a').addEventListener('click', e => { e.preventDefault(); toc.hidden = true; show(it.p); });
    list.appendChild(li);
  });

  document.getElementById('eb-prev').onclick = () => step(-1);
  document.getElementById('eb-next').onclick = () => step(1);
  document.getElementById('eb-hit-l').onclick = () => step(-1);
  document.getElementById('eb-hit-r').onclick = () => step(1);
  document.getElementById('eb-toc-btn').onclick = () => { toc.hidden = !toc.hidden; };
  document.getElementById('eb-toc-close').onclick = () => { toc.hidden = true; };
  const setMode = v => { two = v; modeBtn.textContent = two ? '펼침' : '단면'; show(cur, true); };
  modeBtn.onclick = () => setMode(!two);
  document.getElementById('eb-full').onclick = () => document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen?.();
  range.oninput = () => show(+range.value, true);
  const ZSTEPS = [0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4];
  const zstep = d => { const i = ZSTEPS.findIndex(v => v >= z - 0.001); const k = d > 0 ? (ZSTEPS[i] > z + 0.001 ? i : i + 1) : i - 1; setZoom(ZSTEPS[Math.min(Math.max(k, 0), ZSTEPS.length - 1)]); };
  document.getElementById('eb-zin').onclick = () => zstep(1);
  document.getElementById('eb-zout').onclick = () => zstep(-1);
  zlabel.onclick = () => setZoom(1);
  // Ctrl 또는 Cmd와 휠로 커서 위치를 기준으로 확대한다
  stage.addEventListener('wheel', e => { if (!e.ctrlKey && !e.metaKey) return; e.preventDefault(); setZoom(z * Math.exp(-e.deltaY * 0.0022), { x: e.clientX, y: e.clientY }); }, { passive: false });
  // 두 번 클릭하면 그 지점을 2배로 확대하고 다시 두 번 클릭하면 맞춤으로 돌아간다
  stage.addEventListener('dblclick', e => { e.preventDefault(); setZoom(z > 1.001 ? 1 : 2, { x: e.clientX, y: e.clientY }); });
  // 확대 중에는 끌어서 화면을 옮긴다
  let drag = null;
  stage.addEventListener('pointerdown', e => { if (z <= 1.001 || e.pointerType === 'touch') return; drag = { x: e.clientX, y: e.clientY, l: stage.scrollLeft, t: stage.scrollTop }; stage.classList.add('dragging'); stage.setPointerCapture(e.pointerId); });
  stage.addEventListener('pointermove', e => { if (!drag) return; stage.scrollLeft = drag.l - (e.clientX - drag.x); stage.scrollTop = drag.t - (e.clientY - drag.y); });
  const endDrag = () => { drag = null; stage.classList.remove('dragging'); };
  stage.addEventListener('pointerup', endDrag); stage.addEventListener('pointercancel', endDrag);
  // 두 손가락으로 벌리고 오므려 확대 축소한다
  let pinch = null;
  const dist = t => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
  stage.addEventListener('touchstart', e => { if (e.touches.length === 2) pinch = { d: dist(e.touches), z }; }, { passive: true });
  stage.addEventListener('touchmove', e => { if (pinch && e.touches.length === 2) { e.preventDefault(); const t = e.touches; setZoom(pinch.z * dist(t) / pinch.d, { x: (t[0].clientX + t[1].clientX) / 2, y: (t[0].clientY + t[1].clientY) / 2 }); } }, { passive: false });
  stage.addEventListener('touchend', e => { if (e.touches.length < 2) pinch = null; });
  addEventListener('resize', fit);
  addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT' && e.key !== 'Escape') return;
    const k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ') { e.preventDefault(); step(1); }
    else if (k === 'ArrowLeft' || k === 'PageUp') { e.preventDefault(); step(-1); }
    else if (k === 'Home') show(1); else if (k === 'End') show(N);
    else if (k === 's' || k === 'S') setMode(!two);
    else if (k === 't' || k === 'T') toc.hidden = !toc.hidden;
    else if (k === 'f' || k === 'F') document.getElementById('eb-full').click();
    else if (k === '+' || k === '=') zstep(1); else if (k === '-' || k === '_') zstep(-1); else if (k === '0') setZoom(1);
    else if (k === 'Escape') toc.hidden = true;
  });
  let sx = null;
  stage.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
  stage.addEventListener('touchend', e => { if (sx === null || z > 1.001 || pinch) { sx = null; return; } const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) step(dx < 0 ? 1 : -1); sx = null; });
  addEventListener('hashchange', () => { const n = parseInt(location.hash.slice(1), 10); if (n && !group(cur).includes(n)) show(n, true); });
  // 인쇄할 때는 모든 쪽을 순서대로 되돌린다
  addEventListener('beforeprint', () => { pages.forEach(p => spread.appendChild(p)); spread.style.transform = 'none'; });
  addEventListener('afterprint', () => show(cur, true));
  modeBtn.textContent = two ? '펼침' : '단면';
  show(cur, true);
})();
