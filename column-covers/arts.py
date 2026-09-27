"""표지 일러스트 모음

칼럼마다 art_<이름>(theme) 함수 하나를 두고 600x420 viewBox SVG 문자열을 돌려준다
theme 키는 bg ink acc acc2 mute dark
새 칼럼 표지를 만들 때 이 파일 끝에 함수를 추가한다
"""
import json, math, os, subprocess

KATEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.katex')


def tex(expr, x, y, w, h, color, size=30):
    """LaTeX 수식을 KaTeX로 조판해 SVG foreignObject로 돌려준다 (처음 실행 때 .katex에 katex 설치)"""
    dist = os.path.join(KATEX, 'node_modules', 'katex', 'dist')
    if not os.path.exists(dist):
        subprocess.run(['npm', 'install', '--silent', '--prefix', KATEX, 'katex@0.16'], check=True)
    js = f"process.stdout.write(require('katex').renderToString({json.dumps(expr)}, {{output: 'html'}}))"
    out = subprocess.run(['node', '-e', js], cwd=KATEX, capture_output=True, text=True, check=True).stdout
    css = open(os.path.join(dist, 'katex.min.css')).read().replace('url(fonts/', f'url(file://{dist}/fonts/')
    return (f'<foreignObject x="{x}" y="{y}" width="{w}" height="{h}"><div xmlns="http://www.w3.org/1999/xhtml" '
            f'style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:{color};font-size:{size}px;white-space:nowrap">'
            f'<style>{css}</style>{out}</div></foreignObject>')

def art_prologue(c):
    # dot lattice: explicit structure (solid) vs implicit (faint)
    cols, rows = 9, 7
    sx, sy, ox, oy = 62, 62, 40, 30
    pts = {(i, j): (ox + i * sx, oy + j * sy) for i in range(cols) for j in range(rows)}
    explicit = [(2,1),(4,1),(3,2),(5,2),(2,3),(4,3),(6,3),(3,4),(5,4),(4,5)]
    edges = [((2,1),(3,2)),((4,1),(3,2)),((4,1),(5,2)),((3,2),(2,3)),((3,2),(4,3)),
             ((5,2),(4,3)),((5,2),(6,3)),((2,3),(3,4)),((4,3),(3,4)),((4,3),(5,4)),
             ((6,3),(5,4)),((3,4),(4,5)),((5,4),(4,5)),((2,1),(4,1))]
    s = []
    # faint implicit haze
    for (i, j), (x, y) in pts.items():
        if (i, j) not in explicit:
            s.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{c["ink"]}" opacity=".16"/>')
    s.append(f'<path d="M70 360 C 160 300, 220 420, 330 350 S 500 300, 560 380" fill="none" stroke="{c["ink"]}" stroke-width="1.2" stroke-dasharray="3 6" opacity=".35"/>')
    s.append(f'<path d="M60 80 C 150 20, 260 120, 360 60 S 520 30, 560 90" fill="none" stroke="{c["ink"]}" stroke-width="1.2" stroke-dasharray="3 6" opacity=".35"/>')
    for a, b in edges:
        (x1, y1), (x2, y2) = pts[a], pts[b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["ink"]}" stroke-width="2.2"/>')
    for p in explicit:
        x, y = pts[p]
        hl = p == (4, 3)
        s.append(f'<circle cx="{x}" cy="{y}" r="{15 if hl else 9}" fill="{c["acc"] if hl else c["bg"]}" stroke="{c["ink"]}" stroke-width="2.2"/>')
    x, y = pts[(4, 3)]
    s.append(f'<circle cx="{x}" cy="{y}" r="30" fill="none" stroke="{c["acc"]}" stroke-width="1.5" stroke-dasharray="2 5"/>')
    for (p, t, dx, dy) in [((2,1),'개체',-18,-22),((6,3),'관계',20,6),((4,5),'제약',20,8),((4,3),'검증',38,6)]:
        px, py = pts[p]
        s.append(f'<text x="{px+dx}" y="{py+dy}" class="lbl" fill="{c["acc"] if t=="검증" else c["ink"]}" text-anchor="{"end" if dx<0 else "start"}">{t}</text>')
    s.append(f'<text x="560" y="410" class="lbl" fill="{c["ink"]}" opacity=".55" text-anchor="end">implicit → explicit</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'


def art_screen(c):
    ink, acc, bg = c['ink'], c['acc'], c['bg']
    s = []
    # screen
    s.append(f'<rect x="230" y="40" width="330" height="230" rx="18" fill="{ink}"/>')
    s.append(f'<rect x="246" y="56" width="298" height="198" rx="8" fill="{acc}" opacity=".95"/>')
    for k in range(6):
        w = [200, 150, 230, 120, 180, 90][k]
        s.append(f'<rect x="270" y="{78+k*14}" width="{w}" height="5" rx="2.5" fill="{bg}" opacity=".35"/>')
    s.append(f'<text x="270" y="220" font-family="Playfair Display" font-weight="900" font-size="64" fill="{bg}">x = 3</text>')
    s.append(f'<path d="M478 188 l18 20 l36 -44" fill="none" stroke="{bg}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<rect x="370" y="270" width="50" height="34" fill="{ink}"/><rect x="330" y="302" width="130" height="10" rx="5" fill="{ink}"/>')
    # speech bubble 왜
    s.append(f'<path d="M40 90 h140 a22 22 0 0 1 22 22 v70 a22 22 0 0 1 -22 22 h-80 l-30 30 v-30 h-30 a22 22 0 0 1 -22 -22 v-70 a22 22 0 0 1 22 -22z" fill="{bg}" stroke="{ink}" stroke-width="3"/>')
    s.append(f'<text x="110" y="172" font-family="Noto Serif KR" font-weight="900" font-size="64" fill="{ink}" text-anchor="middle">왜?</text>')
    # glance arrows
    s.append(f'<path d="M120 300 C 170 380, 330 390, 420 330" fill="none" stroke="{ink}" stroke-width="2" stroke-dasharray="6 7"/>')
    s.append(f'<path d="M412 322 l14 6 l-6 14" fill="none" stroke="{ink}" stroke-width="2"/>')
    s.append(f'<path d="M150 250 C 200 290, 260 260, 300 280" fill="none" stroke="{c["acc2"]}" stroke-width="3"/>')
    s.append(f'<path d="M290 270 l12 10 l-14 6" fill="none" stroke="{c["acc2"]}" stroke-width="3" stroke-linejoin="round"/>')
    s.append(f'<circle cx="120" cy="300" r="7" fill="{ink}"/>')
    s.append(f'<text x="136" y="398" class="lbl" fill="{ink}">두 번째로 화면을 보는 동작</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'


def art_ontology(c):
    ink, acc, bg, a2 = c['ink'], c['acc'], c['bg'], c['acc2']
    nodes = {'개념': (300, 205, 48), '정의': (120, 90, 34), '관계': (480, 85, 34),
             '예시': (110, 330, 30), '제약': (490, 330, 34), '성질': (300, 45, 24), '반례': (300, 380, 24)}
    edges = [('개념','정의','is-defined-by'),('개념','관계','relates-to'),('개념','예시','instance-of'),
             ('개념','제약','constrained-by'),('정의','성질','has'),('관계','성질',''),('예시','반례','vs'),('제약','반례','')]
    s = []
    s.append(f'<circle cx="300" cy="205" r="180" fill="none" stroke="{ink}" stroke-width="1" stroke-dasharray="2 6" opacity=".4"/>')
    for a, b, t in edges:
        x1, y1, _ = nodes[a]; x2, y2, _ = nodes[b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ink}" stroke-width="2"/>')
        if t:
            mx, my = (x1+x2)/2, (y1+y2)/2
            w = len(t)*7.2+14
            s.append(f'<rect x="{mx-w/2}" y="{my-11}" width="{w}" height="22" rx="11" fill="{bg}" stroke="{ink}" stroke-width="1.2"/>')
            s.append(f'<text x="{mx}" y="{my+4.5}" class="mono" fill="{ink}" text-anchor="middle">{t}</text>')
    for n, (x, y, r) in nodes.items():
        main = n == '개념'
        fill = acc if main else (a2 if n in ('제약',) else bg)
        tc = bg if main or n == '제약' else ink
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{ink}" stroke-width="2.4"/>')
        fs = 22 if main else (16 if r > 26 else 13)
        s.append(f'<text x="{x}" y="{y+fs*0.36}" font-family="Noto Serif KR" font-weight="900" font-size="{fs}" fill="{tc}" text-anchor="middle">{n}</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'


def art_split(c):
    ink, acc, bg, a2 = c['ink'], c['acc'], c['bg'], c['acc2']
    s = []
    # left: agent grid
    for i in range(5):
        for j in range(6):
            x, y = 50 + i*48, 50 + j*56
            s.append(f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="{ink}"/>')
            if i < 4:
                s.append(f'<line x1="{x+5}" y1="{y}" x2="{x+43}" y2="{y}" stroke="{ink}" stroke-width="1.4"/>')
            if j < 5:
                s.append(f'<line x1="{x}" y1="{y+5}" x2="{x}" y2="{y+51}" stroke="{ink}" stroke-width="1.4"/>')
    s.append(f'<rect x="133" y="157" width="30" height="30" fill="{acc}"/>')
    # divider
    s.append(f'<line x1="300" y1="20" x2="300" y2="400" stroke="{ink}" stroke-width="2"/>')
    s.append(f'<circle cx="300" cy="210" r="30" fill="{bg}" stroke="{ink}" stroke-width="2"/>')
    s.append(f'<text x="300" y="224" font-family="Playfair Display" font-weight="900" font-size="40" fill="{ink}" text-anchor="middle">≠</text>')
    # right: organic contour lines
    for k in range(9):
        o = k*11
        s.append(f'<path d="M{340+o*0.3} {380-o} C {360+o} {300-o}, {420-o*0.5} {330-o*1.2}, {450} {250-o*0.6} S {560-o*0.4} {150+o*0.2}, {520-o*0.5} {70+o*0.6} S {400} {40+o}, {380+o*0.4} {110+o*0.8}" fill="none" stroke="{a2 if k==4 else ink}" stroke-width="{2.6 if k==4 else 1.1}" opacity="{1 if k==4 else .55}"/>')
    s.append(f'<text x="50" y="405" class="lbl" fill="{ink}">AGENT · 명세된 요건</text>')
    s.append(f'<text x="560" y="405" class="lbl" fill="{ink}" text-anchor="end">HUMAN · 몸과 상황</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'


def art_click(c):
    ink, acc, bg = c['ink'], c['acc'], c['bg']
    s = []
    cx, cy = 250, 180
    for k, r in enumerate([40, 80, 125, 175, 230]):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{acc}" stroke-width="{3-k*0.45}" opacity="{1-k*0.17}"/>')
    # polished object with empty core (bottom right)
    s.append(f'<g transform="translate(380 230)">'
             f'<polygon points="80,0 160,45 80,90 0,45" fill="{acc}"/>'
             f'<polygon points="0,45 80,90 80,180 0,135" fill="{acc}" opacity=".7"/>'
             f'<polygon points="160,45 80,90 80,180 160,135" fill="{acc}" opacity=".45"/>'
             f'<polygon points="80,30 118,52 80,74 42,52" fill="{bg}"/>'
             f'<text x="80" y="206" class="lbl" fill="{ink}" text-anchor="middle" opacity=".7">산출물 ≠ 이해</text></g>')
    # cursor
    s.append(f'<g transform="translate({cx-8} {cy-6}) rotate(-8)"><path d="M0 0 L0 120 L30 92 L50 140 L72 130 L52 84 L92 84 Z" fill="{bg}" stroke="{ink}" stroke-width="5" stroke-linejoin="round"/></g>')
    s.append(f'<text x="40" y="70" font-family="Noto Serif KR" font-weight="900" font-size="54" fill="{ink}" transform="rotate(-8 40 70)">딸깍!</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'


def art_fluid(c):
    s = ['<defs>'
         '<linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7B6CFF"/><stop offset="1" stop-color="#3FD0C9"/></linearGradient>'
         '<linearGradient id="g2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF7AB6"/><stop offset="1" stop-color="#7B6CFF"/></linearGradient>'
         '<filter id="bl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="18"/></filter>'
         '</defs>']
    s.append('<path d="M120 90 C 220 10, 380 60, 430 150 S 520 330, 380 360 S 120 380, 90 280 S 40 150, 120 90Z" fill="url(#g1)" opacity=".85" filter="url(#bl)"/>')
    s.append('<path d="M330 120 C 420 60, 560 120, 540 230 S 430 380, 350 300 S 260 170, 330 120Z" fill="url(#g2)" opacity=".75" filter="url(#bl)"/>')
    for k in range(7):
        y = 70 + k*46
        s.append(f'<path d="M20 {y} C 140 {y-40+k*6}, 260 {y+40-k*4}, 380 {y-10} S 540 {y+30}, 590 {y-10}" fill="none" stroke="#EEF0FF" stroke-width="1" opacity=".35"/>')
    nodes = [(170, 170), (250, 120), (300, 210), (230, 270), (380, 250), (420, 160)]
    for a, b in [(0,1),(1,2),(0,3),(2,3),(2,4),(4,5),(1,5)]:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFFFFF" stroke-width="2" opacity=".9"/>')
    for i, (x, y) in enumerate(nodes):
        s.append(f'<circle cx="{x}" cy="{y}" r="{11 if i==2 else 7}" fill="{"#FFFFFF" if i!=2 else "#0E1230"}" stroke="#FFFFFF" stroke-width="3"/>')
    s.append('<circle cx="480" cy="330" r="6" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="2 3"/>')
    s.append('<line x1="380" y1="250" x2="480" y2="330" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="3 5" opacity=".8"/>')
    s.append('<text x="560" y="358" class="lbl" fill="#EEF0FF" opacity=".8" text-anchor="end">다음 판단에 충분한 구조</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'


def art_elephant(c):
    ink, bg = c['ink'], c['bg']
    T, D, P = '#C8553D', '#2E5C8A', '#D99A1E'
    s = []
    dash = f'fill="none" stroke="{ink}" stroke-width="2.4" stroke-dasharray="7 7" stroke-linecap="round"'
    s.append(f'<path d="M215 128 C 250 92, 340 84, 405 94 C 470 104, 505 155, 500 215 C 497 250, 486 272, 474 284 L474 352 L436 352 L431 294 C 385 302, 325 302, 285 294 L281 352 L243 352 L239 282 C 222 270, 210 250, 206 232" {dash}/>')
    s.append(f'<path d="M215 128 C 190 100, 125 100, 110 150 C 98 192, 108 222, 124 238 C 120 278, 100 318, 82 334 C 74 342, 84 354, 94 347 C 124 324, 148 286, 158 252 C 176 256, 196 248, 206 232" {dash}/>')
    s.append(f'<path d="M186 124 C 238 112, 268 170, 250 222 C 240 250, 212 256, 196 236" {dash}/>')
    s.append(f'<path d="M500 200 C 520 210, 526 236, 518 262 l-6 12 l14 -4" {dash}/>')
    s.append(f'<circle cx="142" cy="162" r="4.5" fill="{ink}"/>')
    # three touches
    def touch(x, y, col, label, lx, ly, anchor='start'):
        return (f'<circle cx="{x}" cy="{y}" r="34" fill="{col}" opacity=".9"/>'
                f'<circle cx="{x}" cy="{y}" r="50" fill="none" stroke="{col}" stroke-width="2"/>'
                f'<text x="{lx}" y="{ly}" font-family="Noto Serif KR" font-weight="900" font-size="22" fill="{ink}" text-anchor="{anchor}">{label}</text>')
    s.append(touch(96, 322, T, '교사', 40, 405))
    s.append(touch(232, 180, D, '개발자', 205, 92, 'end'))
    s.append(touch(455, 322, P, '정부', 520, 405, 'start'))
    s.append(f'<text x="330" y="40" class="lbl" fill="{ink}" opacity=".6" text-anchor="middle">아무도 전체를 보지 않는다</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'


def art_translate(c):
    ink, bg = c['ink'], c['bg']
    D, P, T = '#2E5C8A', '#D99A1E', '#C8553D'
    s = []
    cx, cy = 360, 210
    groups = [(D, 60, '개발의 언어', '&lt;/&gt;'), (P, 210, '정책의 언어', '§'), (T, 360, '수업의 언어', '가')]
    for col, y0, lab, glyph in groups:
        for k in range(6):
            dy = (k - 2.5) * 7
            s.append(f'<path d="M70 {y0+dy} C 190 {y0+dy}, 230 {cy+dy*0.35}, {cx-58} {cy+dy*0.35}" fill="none" stroke="{col}" stroke-width="2" opacity="{0.45+k*0.09}"/>')
        s.append(f'<circle cx="46" cy="{y0}" r="22" fill="{col}"/>')
        s.append(f'<text x="46" y="{y0+7}" font-family="JetBrains Mono" font-weight="500" font-size="{17 if glyph.startswith("&") else 21}" fill="{bg}" text-anchor="middle">{glyph}</text>')
        s.append(f'<text x="76" y="{y0-26}" class="lbl" fill="{ink}">{lab}</text>')
    # braided output
    for k, col in enumerate([D, P, T]):
        for j in range(2):
            o = (k*2 + j - 2.5) * 5
            s.append(f'<path d="M{cx+58} {cy+o*0.6} C 450 {cy+o*0.6}, 470 {cy-40+o}, 510 {cy-40+o} S 560 {cy+o}, 600 {cy+o}" fill="none" stroke="{col}" stroke-width="2.2"/>')
    # table
    s.append(f'<circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="{ink}" stroke-width="1.2" stroke-dasharray="2 5"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="58" fill="{ink}"/>')
    s.append(f'<text x="{cx}" y="{cy+11}" font-family="Noto Serif KR" font-weight="900" font-size="32" fill="{bg}" text-anchor="middle">번역</text>')
    for ang, col in [(-90, D), (30, P), (150, T)]:
        x = cx + 74*math.cos(math.radians(ang)); y = cy + 74*math.sin(math.radians(ang))
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{col}" stroke="{bg}" stroke-width="3"/>')
    s.append(f'<text x="600" y="{cy+48}" class="lbl" fill="{ink}" text-anchor="end">공통 언어</text>')
    s.append(f'<text x="{cx}" y="{cy+118}" class="lbl" fill="{ink}" opacity=".6" text-anchor="middle">같은 테이블에 앉는다</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'


def art_blank(c):
    ink, acc, bg, a2 = c['ink'], c['acc'], c['bg'], c['acc2']
    s = []
    # worksheet
    s.append(f'<g transform="rotate(-4 200 150)">')
    s.append(f'<rect x="60" y="20" width="300" height="250" rx="4" fill="#FFFDF8" stroke="{ink}" stroke-width="2"/>')
    s.append(f'<text x="84" y="54" font-family="Noto Serif KR" font-weight="900" font-size="15" fill="{ink}">활동지</text>')
    for k, w in enumerate([240, 200]):
        s.append(f'<rect x="84" y="{70+k*14}" width="{w}" height="5" rx="2.5" fill="{ink}" opacity=".25"/>')
    s.append(f'<text x="84" y="124" class="lbl" fill="{ink}" style="font-size:12px">AI의 답을 비판적으로 검토하고</text>')
    s.append(f'<text x="84" y="142" class="lbl" fill="{ink}" style="font-size:12px">문제점을 적어 보시오</text>')
    s.append(f'<rect x="84" y="156" width="252" height="92" fill="none" stroke="{ink}" stroke-width="1.6" stroke-dasharray="6 5"/>')
    s.append(f'<text x="210" y="210" font-family="Playfair Display" font-style="italic" font-size="20" fill="{a2}" text-anchor="middle">(blank)</text>')
    s.append('</g>')
    # 확인 도장
    s.append(f'<g transform="rotate(10 470 120)"><circle cx="470" cy="120" r="58" fill="none" stroke="{a2}" stroke-width="3"/>'
             f'<circle cx="470" cy="120" r="49" fill="none" stroke="{a2}" stroke-width="1.2"/>'
             f'<text x="470" y="113" font-family="Noto Serif KR" font-weight="900" font-size="17" fill="{a2}" text-anchor="middle">특별한</text>'
             f'<text x="470" y="136" font-family="Noto Serif KR" font-weight="900" font-size="17" fill="{a2}" text-anchor="middle">문제 없음</text></g>')
    # timeline
    y = 340
    s.append(f'<line x1="30" y1="{y}" x2="575" y2="{y}" stroke="{ink}" stroke-width="2"/>')
    s.append(f'<path d="M565 {y-7} l12 7 l-12 7" fill="none" stroke="{ink}" stroke-width="2"/>')
    s.append(f'<rect x="170" y="{y-26}" width="16" height="52" fill="{acc}"/>')
    s.append(f'<text x="178" y="{y+48}" class="lbl" fill="{acc}" text-anchor="middle">AI 답 출력</text>')
    s.append(f'<circle cx="95" cy="{y}" r="8" fill="{bg}" stroke="{ink}" stroke-width="2"/>')
    s.append(f'<text x="95" y="{y-18}" class="lbl" style="font-size:12px" fill="{ink}" text-anchor="middle">프롬프트</text>')
    for k, t in enumerate(['의심', '출처 확인', '환각 점검', '비교', '최종 판단']):
        x = 250 + k*66
        s.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{ink}"/>')
        s.append(f'<text x="{x}" y="{y-18}" class="lbl" style="font-size:12px" fill="{ink}" text-anchor="middle">{t}</text>')
    s.append(f'<path d="M236 {y+18} q0 10 10 10 h300 q10 0 10 -10" fill="none" stroke="{ink}" stroke-width="1.2"/>')
    s.append(f'<text x="396" y="{y+50}" class="lbl" fill="{ink}" text-anchor="middle">지침 전체가 사후에 몰려 있다</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'




def art_goal(c):
    ink, acc, bg, a2 = c['ink'], c['acc'], c['bg'], c['acc2']
    s = []
    # 통째로 붙여 넣은 프롬프트
    s.append(f'<text x="40" y="34" class="lbl" fill="{ink}" opacity=".55">통째로 붙여 넣기</text>')
    s.append(f'<rect x="30" y="48" width="250" height="178" rx="10" fill="none" stroke="{ink}" stroke-width="2" opacity=".55"/>')
    for k, w in enumerate([210, 190, 214, 170, 200, 150, 120]):
        s.append(f'<rect x="50" y="{68+k*16}" width="{w}" height="5" rx="2.5" fill="{ink}" opacity=".2"/>')
    s.append(f'<text x="50" y="206" class="lbl" fill="{a2}">+ 풀어 줘</text>')
    # 한 줄 목표 카드
    s.append(f'<g transform="rotate(-3 445 120)">')
    s.append(f'<rect x="318" y="58" width="258" height="130" rx="4" fill="#FFFDF8" stroke="{ink}" stroke-width="2.2"/>')
    s.append(f'<rect x="318" y="58" width="258" height="10" fill="{acc}"/>')
    s.append(f'<text x="338" y="102" class="lbl" fill="{ink}">내가 이 문제에서</text>')
    s.append(f'<text x="338" y="124" class="lbl" fill="{ink}">알아내려는 것은</text>')
    s.append(f'<path d="M338 160 C 380 152, 430 166, 470 156 S 530 150, 556 158" fill="none" stroke="{acc}" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<text x="556" y="178" class="lbl" fill="{ink}" text-anchor="end">이다</text>')
    s.append('</g>')
    s.append(f'<text x="447" y="34" class="lbl" fill="{acc}" text-anchor="middle">AI를 켜기 전에 한 줄</text>')
    # 답
    s.append(f'<rect x="175" y="282" width="250" height="74" rx="37" fill="{ink}"/>')
    s.append(tex(r'x=-1 \ \text{또는}\ x=3', 175, 282, 250, 74, bg, 20))
    # 붙여 넣기 → 답 : 대조할 기준 없음
    s.append(f'<path d="M150 232 C 150 270, 170 300, 186 312" fill="none" stroke="{ink}" stroke-width="2" stroke-dasharray="4 6" opacity=".55"/>')
    s.append(f'<text x="118" y="298" font-family="Noto Serif KR" font-weight="900" font-size="34" fill="{a2}" text-anchor="middle">?</text>')
    # 목표 카드 ↔ 답 : 대조
    s.append(f'<path d="M450 196 C 452 250, 446 292, 428 312" fill="none" stroke="{acc}" stroke-width="3"/>')
    s.append(f'<path d="M444 188 l6 -10 l6 10" fill="none" stroke="{acc}" stroke-width="3" stroke-linejoin="round"/>')
    s.append(f'<path d="M438 298 l-12 16 l18 2" fill="none" stroke="{acc}" stroke-width="3" stroke-linejoin="round"/>')
    s.append(f'<text x="466" y="262" class="lbl" fill="{acc}">대조</text>')
    # 판정 칸
    for k, t in enumerate(['예', '일부만', '아니오']):
        x = 170 + k * 94
        on = k == 1
        s.append(f'<rect x="{x}" y="378" width="82" height="30" rx="15" fill="{acc if on else "none"}" stroke="{acc if on else ink}" stroke-width="1.6" opacity="{1 if on else .6}"/>')
        s.append(f'<text x="{x+41}" y="398" class="lbl" fill="{bg if on else ink}" text-anchor="middle">{t}</text>')
    return '<svg viewBox="0 0 600 420">' + ''.join(s) + '</svg>'
