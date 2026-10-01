// 그림 확대  e-book 쪽 안의 도표와 그림을 눌러 따로 크게 본다
// 쪽을 통째로 복제해 그림 영역만 잘라 보여 주므로 지면과 똑같은 모양으로 확대된다
// 창 안에서  휠 · + − 0 키 · 두 손가락 · 두 번 누르기로 확대 축소  끌어서 이동  Esc · × · 바깥 누르기로 닫기
(function () {
  'use strict';
  const PAD = 10, ZMIN = 0.5, ZMAX = 8, FIT_MAX = 6;
  const SKIP = '.rh,.folio,.runhead,.ev,button,a';
  const DECOR = '.cv-book,.cv-mast,.logo-row,.sigsvg,.sign-row,.portrait,.opener-band'; // 로고 서명 배경 그림
  const LABEL = /^\s*(chart|figure|fig\.?|map|diagram|graph|그림|도표|차트)\b/i;

  // 1  확대할 대상 찾기
  function isBar(el) {
    const s = el.getAttribute('style') || '';
    return /width:\s*[\d.]+%/.test(s) && /background/.test(s) && /position:\s*absolute|height:/.test(s);
  }
  function findTargets() {
    const set = new Set();
    const pages = [...document.querySelectorAll('.page')];
    pages.forEach(pg => {
      // figure 요소
      pg.querySelectorAll('figure').forEach(f => set.add(f));
      // 'Chart 1' 'Figure 2' 같은 이름표로 시작하는 묶음
      pg.querySelectorAll('.kicker,.bt,.fig-t').forEach(k => {
        const box = k.parentElement;
        if (!LABEL.test(k.textContent) || !box || box.classList.contains('inner') || box.classList.contains('page')) return;
        if (box.querySelector('svg,img,canvas') || [...box.querySelectorAll('[style]')].filter(isBar).length >= 2) set.add(box);
      });
      // 따로 놓인 SVG 그림  배경용 밴드와 아이콘은 뺀다
      pg.querySelectorAll('svg').forEach(s => {
        if (s.closest(SKIP + ',' + DECOR) || s.parentElement.closest('svg')) return;
        const vb = (s.getAttribute('viewBox') || '').split(/[\s,]+/).map(Number);
        const w = vb.length === 4 ? vb[2] : +s.getAttribute('width') || 0, h = vb.length === 4 ? vb[3] : +s.getAttribute('height') || 0;
        if (w >= 60 && h >= 40) set.add(s);
      });
      // 이름표 없는 막대그래프  막대가 셋 이상 모인 가장 작은 묶음
      const bars = [...pg.querySelectorAll('[style]')].filter(isBar);
      bars.forEach(b => {
        let a = b.parentElement;
        while (a && a !== pg && !a.classList.contains('inner')) {
          if (bars.filter(x => a.contains(x)).length >= 3) { set.add(a); return; }
          a = a.parentElement;
        }
      });
    });
    // 다른 대상 안에 든 것은 바깥 하나만 남긴다
    const all = [...set];
    return all.filter(t => !t.closest(SKIP) && !all.some(o => o !== t && o.contains(t)));
  }

  function captionOf(t) {
    const fc = t.querySelector('figcaption');
    if (fc) return fc.textContent.trim();
    const k = t.querySelector('.kicker,.bt,.fig-t,h3,h4');
    if (k && LABEL.test(k.textContent)) return k.textContent.trim();
    const tt = t.matches('svg') ? (t.getAttribute('aria-label') || t.querySelector('title')?.textContent) : '';
    if (tt) return tt.trim();
    const near = t.closest('.box,.card,figure');
    const h = near && near.querySelector('.bt,h3,h4,.kicker');
    return h ? h.textContent.trim() : '그림';
  }

  // 2  확대 창
  const ov = document.createElement('div');
  ov.id = 'fz'; ov.hidden = true;
  ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', '그림 확대');
  ov.innerHTML = '<div class="fz-view"><div class="fz-clip"><div class="fz-sheet"></div></div></div>' +
    '<div class="fz-bar"><span class="fz-cap"></span><span class="fz-tools">' +
    '<button class="fz-b" data-z="-1" aria-label="축소" title="축소 ( − )">−</button>' +
    '<button class="fz-b fz-val" data-z="0" title="창에 맞춤 ( 0 )">맞춤</button>' +
    '<button class="fz-b" data-z="1" aria-label="확대" title="확대 ( + )">+</button>' +
    '<button class="fz-b fz-x" aria-label="닫기" title="닫기 ( Esc )">×</button></span></div>';
  document.body.appendChild(ov);
  const view = ov.querySelector('.fz-view'), clip = ov.querySelector('.fz-clip'), sheet = ov.querySelector('.fz-sheet');
  const cap = ov.querySelector('.fz-cap'), val = ov.querySelector('.fz-val');

  let st = null; // { fx, fy, fw, fh, fit, s, ox, oy }
  let opener = null, openedAt = 0;

  function viewSize() { return { w: view.clientWidth, h: view.clientHeight }; }
  function clamp() {
    const { w, h } = viewSize(), cw = st.fw * st.s, ch = st.fh * st.s;
    st.ox = cw <= w ? (w - cw) / 2 : Math.min(0, Math.max(w - cw, st.ox));
    st.oy = ch <= h ? (h - ch) / 2 : Math.min(0, Math.max(h - ch, st.oy));
  }
  function paint() {
    clamp();
    clip.style.width = st.fw * st.s + 'px'; clip.style.height = st.fh * st.s + 'px';
    clip.style.transform = `translate(${st.ox}px,${st.oy}px)`;
    sheet.style.transform = `scale(${st.s}) translate(${-st.fx}px,${-st.fy}px)`;
    const r = st.s / st.fit;
    val.textContent = Math.abs(r - 1) < 0.01 ? '맞춤' : Math.round(r * 100) + '%';
    view.classList.toggle('pan', st.fw * st.s > viewSize().w + 1 || st.fh * st.s > viewSize().h + 1);
  }
  function zoomTo(s, cx, cy) {
    s = Math.min(st.fit * ZMAX, Math.max(st.fit * ZMIN, s));
    const vr = view.getBoundingClientRect();
    if (cx === undefined) { cx = vr.left + vr.width / 2; cy = vr.top + vr.height / 2; }
    const px = cx - vr.left, py = cy - vr.top;
    const ux = (px - st.ox) / st.s, uy = (py - st.oy) / st.s; // 기준점의 그림 좌표
    st.s = s; st.ox = px - ux * s; st.oy = py - uy * s;
    paint();
  }
  const STEPS = [0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8];
  function zstep(d) {
    const r = st.s / st.fit;
    let t = r;
    if (d > 0) t = STEPS.find(v => v > r + 0.01) || ZMAX;
    else t = [...STEPS].reverse().find(v => v < r - 0.01) || ZMIN;
    zoomTo(t * st.fit);
  }
  function refit() {
    const { w, h } = viewSize();
    st.fit = Math.min((w - 24) / st.fw, (h - 24) / st.fh, FIT_MAX);
    st.s = st.fit; st.ox = st.oy = 0; paint();
  }

  function open(t) {
    const pg = t.closest('.page');
    const pr = pg.getBoundingClientRect(), tr = t.getBoundingClientRect();
    const k = pr.width / pg.offsetWidth || 1;
    const W = pg.offsetWidth, H = pg.offsetHeight;
    const x0 = Math.max(0, (tr.left - pr.left) / k - PAD), y0 = Math.max(0, (tr.top - pr.top) / k - PAD);
    const x1 = Math.min(W, (tr.right - pr.left) / k + PAD), y1 = Math.min(H, (tr.bottom - pr.top) / k + PAD);
    const c = pg.cloneNode(true);
    c.classList.remove('hidden', 'left', 'right', 'enter-n', 'enter-p');
    c.querySelectorAll('.fz-target').forEach(e => { e.classList.remove('fz-target'); e.removeAttribute('title'); e.removeAttribute('tabindex'); e.removeAttribute('role'); });
    c.removeAttribute('id'); c.setAttribute('aria-hidden', 'true');
    c.style.cssText += ';position:absolute;left:0;top:0;margin:0;box-shadow:none;animation:none;transform:none;display:block';
    sheet.replaceChildren(c);
    sheet.style.width = W + 'px'; sheet.style.height = H + 'px';
    st = { fx: x0, fy: y0, fw: x1 - x0, fh: y1 - y0, fit: 1, s: 1, ox: 0, oy: 0 };
    cap.textContent = captionOf(t);
    opener = t; openedAt = Date.now();
    ov.hidden = false; document.documentElement.classList.add('fz-open');
    refit();
    ov.querySelector('.fz-x').focus({ preventScroll: true });
  }
  function close() {
    if (ov.hidden) return;
    ov.hidden = true; document.documentElement.classList.remove('fz-open');
    sheet.replaceChildren(); st = null;
    if (opener) opener.focus({ preventScroll: true });
  }

  // 3  쪽 안의 그림 누르기
  const targets = findTargets();
  targets.forEach(t => {
    t.classList.add('fz-target');
    t.setAttribute('title', '눌러서 그림 확대');
    t.setAttribute('tabindex', '0'); t.setAttribute('role', 'button');
  });
  let down = null;
  document.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY }; }, true);
  document.addEventListener('click', e => {
    const t = e.target.closest && e.target.closest('.fz-target');
    if (!t || !ov.hidden || e.target.closest('a')) return;
    const moved = down && Math.abs(e.clientX - down.x) + Math.abs(e.clientY - down.y) > 5;
    if (moved) return;
    e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation();
    open(t);
  }, true);
  // 그림 위에서 두 번 누르면 쪽 확대가 아니라 그림 확대가 먼저 열린다
  document.addEventListener('dblclick', e => { if (e.target.closest && (e.target.closest('.fz-target') || e.target.closest('#fz'))) { e.stopPropagation(); e.stopImmediatePropagation(); } }, true);

  // 4  확대 창 조작
  ov.querySelectorAll('[data-z]').forEach(b => b.addEventListener('click', () => { const d = +b.dataset.z; d ? zstep(d) : refit(); }));
  ov.querySelector('.fz-x').addEventListener('click', close);
  view.addEventListener('wheel', e => { e.preventDefault(); zoomTo(st.s * Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0022)), e.clientX, e.clientY); }, { passive: false });
  view.addEventListener('dblclick', e => {
    if (Date.now() - openedAt < 500) return;
    const r = st.s / st.fit; zoomTo(st.fit * (r > 1.05 ? 1 : 2.5), e.clientX, e.clientY);
  });
  const pts = new Map(); let g = null, movedInView = false;
  const mid = () => { const a = [...pts.values()]; return { x: (a[0].x + a[1].x) / 2, y: (a[0].y + a[1].y) / 2, d: Math.hypot(a[0].x - a[1].x, a[0].y - a[1].y) }; };
  view.addEventListener('pointerdown', e => {
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY }); view.setPointerCapture(e.pointerId);
    if (pts.size === 1) { g = { x: e.clientX, y: e.clientY, ox: st.ox, oy: st.oy }; movedInView = false; }
    else if (pts.size === 2) { const m = mid(); g = { pinch: true, d: m.d, s: st.s }; }
  });
  view.addEventListener('pointermove', e => {
    if (!pts.has(e.pointerId) || !g) return;
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (g.pinch && pts.size === 2) { const m = mid(); movedInView = true; zoomTo(g.s * m.d / g.d, m.x, m.y); }
    else if (!g.pinch) {
      const dx = e.clientX - g.x, dy = e.clientY - g.y;
      if (Math.abs(dx) + Math.abs(dy) > 4) movedInView = true;
      st.ox = g.ox + dx; st.oy = g.oy + dy; paint(); view.classList.add('dragging');
    }
  });
  const up = e => {
    pts.delete(e.pointerId); view.classList.remove('dragging');
    if (pts.size === 1) { const p = [...pts.values()][0]; g = { x: p.x, y: p.y, ox: st.ox, oy: st.oy }; } else if (!pts.size) g = null;
  };
  view.addEventListener('pointerup', e => {
    // 그림 바깥 빈 곳을 누르면 닫는다
    const cr = clip.getBoundingClientRect();
    const inClip = e.clientX >= cr.left && e.clientX <= cr.right && e.clientY >= cr.top && e.clientY <= cr.bottom;
    if (!movedInView && !inClip && pts.size === 1 && Date.now() - openedAt > 300) { up(e); close(); return; }
    up(e);
  });
  view.addEventListener('pointercancel', up);
  // 창이 열린 동안의 키는 뷰어로 넘기지 않는다
  addEventListener('keydown', e => {
    if (ov.hidden) {
      if ((e.key === 'Enter' || e.key === ' ') && document.activeElement && document.activeElement.classList.contains('fz-target')) {
        e.preventDefault(); e.stopImmediatePropagation(); open(document.activeElement);
      }
      return;
    }
    const k = e.key;
    if (k === 'Tab') { // 창 안에서만 돈다
      const f = [...ov.querySelectorAll('button')], i = f.indexOf(document.activeElement);
      e.preventDefault(); f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    } else if (k === 'Escape') close();
    else if (k === '+' || k === '=') zstep(1);
    else if (k === '-' || k === '_') zstep(-1);
    else if (k === '0') refit();
    else if (k.startsWith('Arrow')) { const d = 60; if (k === 'ArrowLeft') st.ox += d; if (k === 'ArrowRight') st.ox -= d; if (k === 'ArrowUp') st.oy += d; if (k === 'ArrowDown') st.oy -= d; paint(); }
    else if ((k === 'Enter' || k === ' ') && document.activeElement && document.activeElement.tagName === 'BUTTON') return;
    else return e.stopImmediatePropagation();
    e.preventDefault(); e.stopImmediatePropagation();
  }, true);
  addEventListener('resize', () => { if (st) refit(); });
  window.FigZoom = { open, close, count: targets.length };
})();
