// Heurēsis Vol.01 — 표지와 오프너의 수학적 그래픽을 인라인 SVG로 그린다
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const el = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };

  // 표지  두 겹의 실 그림(string art)  선들의 포락선은 제어점이 모서리인 2차 베지어 곡선이다
  function cover(svg) {
    const S = 400, N = 28;
    for (let x = 20; x < S; x += 20) for (let y = 20; y < S; y += 11.4)
      el('ellipse', { cx: x, cy: y, rx: 1, ry: 0.56, fill: '#16161A', opacity: 0.25 }, svg);
    for (let i = 0; i <= N; i++) {
      const t = (i / N) * S;
      el('line', { x1: 0, y1: t, x2: t, y2: S, stroke: '#1B2A41', 'stroke-width': 0.7, opacity: 0.85, 'vector-effect': 'non-scaling-stroke' }, svg);
      el('line', { x1: S, y1: S - t, x2: S - t, y2: 0, stroke: '#1B2A41', 'stroke-width': 0.7, opacity: 0.35, 'vector-effect': 'non-scaling-stroke' }, svg);
    }
    el('path', { d: `M0,0 Q0,${S} ${S},${S}`, fill: 'none', stroke: '#C8372D', 'stroke-width': 3.2, 'vector-effect': 'non-scaling-stroke' }, svg);
    el('path', { d: `M${S},${S} Q${S},0 0,0`, fill: 'none', stroke: '#C8372D', 'stroke-width': 1.2, 'stroke-dasharray': '4 5', 'vector-effect': 'non-scaling-stroke' }, svg);
  }

  // 커버스토리  곡선과 접선 다발
  function tangent(svg) {
    const W = 800, H = 600;
    for (let x = 0; x <= W; x += 40) el('line', { x1: x, y1: 0, x2: x, y2: H, stroke: '#fff', opacity: 0.06 }, svg);
    for (let y = 0; y <= H; y += 40) el('line', { x1: 0, y1: y, x2: W, y2: y, stroke: '#fff', opacity: 0.06 }, svg);
    const f = x => 330 - 150 * Math.sin((x - 60) / 130) * Math.exp(-((x - 430) ** 2) / 90000) - 0.12 * (x - 400);
    const df = x => (f(x + 0.5) - f(x - 0.5));
    for (let i = 0; i < 34; i++) {
      const x0 = 40 + i * 22, y0 = f(x0), m = df(x0);
      el('line', { x1: x0 - 120, y1: y0 - 120 * m, x2: x0 + 120, y2: y0 + 120 * m, stroke: '#fff', 'stroke-width': 0.7, opacity: 0.28 }, svg);
    }
    let d = '';
    for (let x = 0; x <= W; x += 4) d += (x ? 'L' : 'M') + x + ',' + f(x).toFixed(1);
    el('path', { d, fill: 'none', stroke: '#F3A89F', 'stroke-width': 3 }, svg);
    [180, 430, 640].forEach(x => el('circle', { cx: x, cy: f(x), r: 6, fill: '#C8372D', stroke: '#fff', 'stroke-width': 2 }, svg));
  }

  // 기획  불안의 등고선
  function contour(svg) {
    const cx = 560, cy = 250;
    for (let k = 1; k <= 22; k++) {
      let d = '';
      for (let a = 0; a <= 360; a += 4) {
        const r = k * 17 * (1 + 0.16 * Math.sin((a * Math.PI) / 60 + k * 0.5) + 0.08 * Math.cos((a * Math.PI) / 45));
        const x = cx + r * Math.cos((a * Math.PI) / 180) * 1.35, y = cy + r * Math.sin((a * Math.PI) / 180);
        d += (a ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1);
      }
      el('path', { d: d + 'Z', fill: 'none', stroke: k === 7 ? '#F3A89F' : '#fff', 'stroke-width': k === 7 ? 2.4 : 0.8, opacity: k === 7 ? 1 : 0.3 }, svg);
    }
  }

  // 수학클리닉  계단형 성장과 회기 점
  function steps(svg) {
    const W = 800;
    for (let r = 0; r < 12; r++) for (let c = 0; c < 33; c++) {
      const on = (c * 7 + r * 3) % 11 > 2;
      el('circle', { cx: 30 + c * 23, cy: 40 + r * 23, r: on ? 3 : 1.4, fill: '#fff', opacity: on ? 0.32 : 0.18 }, svg);
    }
    let d = 'M30,330', y = 330;
    for (let i = 0; i < 12; i++) { const x = 30 + (i + 1) * 62; y -= 12 + (i % 3) * 6; d += ` H${x} V${y}`; }
    el('path', { d, fill: 'none', stroke: '#BFE3E3', 'stroke-width': 3 }, svg);
    el('path', { d: 'M30,330 L' + (W - 20) + ',120', fill: 'none', stroke: '#fff', 'stroke-width': 1, 'stroke-dasharray': '6 6', opacity: 0.6 }, svg);
  }

  // 교사의 시선  시야각을 이루는 동심호
  function eye(svg) {
    const cx = 620, cy = 330;
    for (let k = 1; k <= 18; k++) {
      const r = k * 26;
      el('path', { d: `M${cx - r},${cy} A${r},${r * 0.62} 0 0 1 ${cx + r},${cy}`, fill: 'none', stroke: '#fff', 'stroke-width': k === 5 ? 2.6 : 0.8, opacity: k === 5 ? 0.95 : 0.3 }, svg);
    }
    for (let i = 0; i < 13; i++) {
      const a = Math.PI + (i / 12) * Math.PI;
      el('line', { x1: cx, y1: cy, x2: cx + 520 * Math.cos(a), y2: cy + 320 * Math.sin(a), stroke: '#fff', opacity: 0.16 }, svg);
    }
    el('circle', { cx, cy, r: 16, fill: '#fff' }, svg);
    el('circle', { cx, cy, r: 7, fill: '#16161A' }, svg);
  }

  // 84개 프롬프트 와플 차트  Bulut & Borromeo Ferri 2026
  function waffle(svg) {
    const groups = [[49, '#1B2A41'], [16, '#7A8CA8'], [2, '#A97A22'], [1, '#C8372D'], [16, '#E7DDCD']];
    const cols = 10, s = 22, g = 2.5;
    let i = 0;
    groups.forEach(([n, c]) => {
      for (let k = 0; k < n; k++, i++) {
        const x = (i % cols) * (s + g), y = Math.floor(i / cols) * (s + g);
        el('rect', { x, y, width: s, height: s, fill: c }, svg);
        if (c === '#C8372D') el('rect', { x: x - 2, y: y - 2, width: s + 4, height: s + 4, fill: 'none', stroke: '#C8372D', 'stroke-width': 1.5 }, svg);
      }
    });
  }

  // 성취 궤적 도식  Guo 외 2026  비율만 실제 값이고 곡선 모양은 도식이다
  function trajectories(svg) {
    const X = [60, 170, 280, 390], lab = ['3학년', '4학년', '5학년', '6학년'];
    el('line', { x1: 50, y1: 200, x2: 410, y2: 200, stroke: '#16161A', 'stroke-width': 1 }, svg);
    X.forEach((x, i) => { const t = el('text', { x, y: 216, 'text-anchor': 'middle', 'font-family': 'Noto Sans KR', 'font-size': 10, fill: '#6F6A63' }, svg); t.textContent = lab[i]; });
    const lines = [
      { y: [60, 52, 44, 36], c: '#1B2A41', w: 3, n: '고성취 안정상승형 9.3%' },
      { y: [130, 108, 88, 70], c: '#C8372D', w: 5, n: '중간수준 빠른상승형 81.4%' },
      { y: [172, 170, 168, 167], c: '#A97A22', w: 3, n: '저성취 안정형 9.3%' }
    ];
    lines.forEach(L => {
      el('path', { d: X.map((x, i) => (i ? 'L' : 'M') + x + ',' + L.y[i]).join(''), fill: 'none', stroke: L.c, 'stroke-width': L.w }, svg);
      X.forEach((x, i) => el('circle', { cx: x, cy: L.y[i], r: 3.2, fill: '#FBF8F3', stroke: L.c, 'stroke-width': 1.6 }, svg));
      const t = el('text', { x: 400, y: L.y[3] - 7, 'text-anchor': 'end', 'font-family': 'Noto Sans KR', 'font-weight': 700, 'font-size': 10.5, fill: L.c }, svg); t.textContent = L.n;
    });
  }

  // 난이도 표시와 여학생 자기효능감  Herset & Bjerke 2026
  function efficacy(svg) {
    const base = 190, scale = v => (v - 60) * 7;
    [['표시 없음', 81.21, '#1B2A41'], ['어려움 표시', 75.82, '#C8372D']].forEach(([n, v, c], i) => {
      const x = 40 + i * 120, h = scale(v);
      el('rect', { x, y: base - h, width: 70, height: h, fill: c }, svg);
      const t = el('text', { x: x + 35, y: base - h - 8, 'text-anchor': 'middle', 'font-family': 'Playfair Display', 'font-weight': 900, 'font-size': 20, fill: c }, svg); t.textContent = v.toFixed(2);
      const l = el('text', { x: x + 35, y: base + 16, 'text-anchor': 'middle', 'font-family': 'Noto Sans KR', 'font-size': 10.5, fill: '#34322F' }, svg); l.textContent = n;
    });
    el('line', { x1: 30, y1: base, x2: 270, y2: base, stroke: '#16161A' }, svg);
    const n = el('text', { x: 30, y: 12, 'font-family': 'IBM Plex Mono', 'font-size': 9, fill: '#6F6A63' }, svg); n.textContent = '여학생 자기효능감  축은 60에서 시작';
  }

  const map = { cover, tangent, contour, steps, eye, waffle, trajectories, efficacy };
  document.querySelectorAll('svg[data-art]').forEach(svg => { const fn = map[svg.dataset.art]; if (fn) fn(svg); });
})();

// 쪽 번호와 차례 번호를 문서 순서대로 자동으로 매긴다
(function () {
  const pages = [...document.querySelectorAll('.page')];
  pages.forEach((pg, i) => { const n = pg.querySelector('.folio .n'); if (n) n.textContent = String(i + 1).padStart(2, '0'); });
  document.querySelectorAll('[data-pageof]').forEach(e => {
    const t = document.getElementById(e.dataset.pageof);
    const pg = t && t.closest('.page');
    if (pg) e.textContent = String(pages.indexOf(pg) + 1).padStart(2, '0');
  });
})();
