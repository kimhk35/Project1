# -*- coding: utf-8 -*-
"""개선안 도식 SVG 생성기  build/figs.py

python3 build/figs.py  →  figs/<id>.svg 생성 (PNG 변환은 render.py)
"""
import os, math, re
from content import COLORS as C

FONT = "Pretendard, 'Pretendard Variable', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"
OUT = os.path.join(os.path.dirname(__file__), "..", "figs")


# ── 기본 도형 ───────────────────────────────────────────
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rect(x, y, w, h, fill="none", stroke="none", sw=1.5, rx=12, dash=None, op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>'


_SENT = re.compile(r"[가-힣](?<![마보])다$")
_QUES = re.compile(r"(인가|는가)$")


def punct(s):
    """도식 속 문장은 온점, 의문문은 물음표로 끝낸다"""
    if _SENT.search(s):
        return s + "."
    if _QUES.search(s):
        return s + "?"
    return s


def text(x, y, s, size=16, weight=500, fill=None, anchor="middle", ls=None):
    s = punct(s)
    fill = fill or C["text"]
    l = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" dominant-baseline="central" style="white-space:pre"{l}>{esc(s)}</text>')


def lines(x, y, arr, size=15, weight=500, fill=None, anchor="middle", lh=1.45):
    out = []
    for i, s in enumerate(arr):
        out.append(text(x, y + i * size * lh, s, size, weight, fill, anchor))
    return "".join(out)


def line(x1, y1, x2, y2, stroke=None, sw=2, dash=None, arrow=None):
    stroke = stroke or C["muted"]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ""
    if arrow:
        m = f' marker-end="url(#ah-{arrow})"'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d}{m}/>'


def path(d, stroke=None, sw=2, fill="none", arrow=None, dash=None):
    stroke = stroke or C["muted"]
    m = f' marker-end="url(#ah-{arrow})"' if arrow else ""
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"{m}{ds}/>'


def pill(cx, cy, w, h, label, fill, color="#fff", size=15, weight=700):
    return rect(cx - w / 2, cy - h / 2, w, h, fill, rx=h / 2) + text(cx, cy, label, size, weight, color)


def person(cx, cy, s=1.0, fill="#fff"):
    return (f'<circle cx="{cx}" cy="{cy - 9 * s}" r="{7 * s}" fill="{fill}"/>'
            f'<path d="M{cx - 13 * s},{cy + 14 * s} a{13 * s},{12 * s} 0 0 1 {26 * s},0 z" fill="{fill}"/>')


def svg(w, h, body, title=""):
    markers = "".join(
        f'<marker id="ah-{k}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{C[k] if k in C else k}"/></marker>'
        for k in ["muted", "del", "raon", "lead", "ink", "ok", "gold"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="{FONT}" role="img" aria-label="{esc(title)}">'
            f'<defs>{markers}</defs>'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')


# ── 그림 0  전체 구조 ────────────────────────────────────
def fig0():
    W, H = 1000, 640
    b = []
    # 학교
    b.append(rect(330, 14, 340, 70, "#fff", C["ink"], 2, 14))
    b.append(text(500, 38, "학교", 19, 800, C["ink"]))
    b.append(text(500, 64, "교장, 교직원회의, 학교운영위원회", 14, 500, C["muted"]))
    b.append(line(470, 86, 470, 126, C["ink"], 2, arrow="ink"))
    b.append(line(530, 126, 530, 86, C["ink"], 2, arrow="ink"))
    b.append(text(458, 106, "건의, 협의", 12.5, 600, C["muted"], "end"))
    b.append(text(542, 106, "답변, 지원", 12.5, 600, C["muted"], "start"))

    # 두 조직 패널
    for x, key, name, sub, items in [
        (30, "del", "대의원회", "심의와 의결 기구", ["총 31명, 회장단 3 + 학급 임원 28", "안건 심의와 의결", "학생참여예산 심의", "라온하제 사업 승인, 평가"]),
        (570, "raon", "라온하제", "기획과 집행 기구", ["총 26명, 회장단 3 + 부원 23", "연간 사업 기획과 실행", "행사, 캠페인, 홍보", "의결 사항 이행, 결과 보고"]),
    ]:
        b.append(rect(x, 160, 400, 230, C[key + "_l"], C[key], 2, 18))
        tx = x + 28
        b.append(text(tx, 222, name, 26, 800, C[key], "start"))
        b.append(text(tx, 252, sub, 14.5, 600, C["muted"], "start"))
        for i, it in enumerate(items):
            yy = 288 + i * 25
            b.append(f'<circle cx="{tx + 5}" cy="{yy}" r="3.5" fill="{C[key]}"/>')
            b.append(text(tx + 18, yy, it, 14.5, 500, C["text"], "start"))
    # 회장단 (두 패널 위에 걸침)
    b.append(rect(335, 128, 330, 62, C["lead"], rx=31))
    b.append(text(500, 150, "학생회장단", 19, 800, "#fff"))
    b.append(text(500, 172, "회장 1, 부회장 2, 두 조직 당연직", 12.5, 500, "#EDE6FF"))
    # 가운데 화살표
    b.append(line(440, 270, 560, 270, C["del"], 2.5, arrow="del"))
    b.append(text(500, 256, "의결 사항", 13, 700, C["del"]))
    b.append(line(560, 330, 440, 330, C["raon"], 2.5, arrow="raon"))
    b.append(text(500, 346, "실행 결과", 13, 700, C["raon"]))
    # 자치운영위원회
    b.append(path("M230,390 L230,432 L378,432", C["lead"], 2, dash="5 5"))
    b.append(path("M770,390 L770,432 L622,432", C["lead"], 2, dash="5 5"))
    b.append(rect(378, 408, 244, 50, "#fff", C["lead"], 2, 25))
    b.append(text(500, 427, "자치운영위원회", 16, 800, C["lead"]))
    b.append(text(500, 446, "통합 집행부 회의, 격주", 11.5, 600, C["muted"]))
    # 학급자치회
    b.append(rect(30, 496, 940, 96, C["soft"], C["line"], 1.5, 16))
    b.append(text(58, 526, "학급자치회", 18, 800, C["ink"], "start"))
    b.append(text(58, 552, "교육과정 속 학급자치 시간", 13, 600, C["ok"], "start"))
    b.append(text(58, 572, "월 2회, 연 17시간", 13, 500, C["muted"], "start"))
    b.append(text(930, 522, "14개 학급", 12.5, 700, C["ink"], "end"))
    for c in range(14):
        xx = 300 + c * 45
        b.append(rect(xx, 536, 38, 38, "#fff", C["line"], 1.2, 8))
        b.append(person(xx + 12, 557, 0.5, C["muted"]) + person(xx + 26, 557, 0.5, C["muted"]))
    b.append(line(200, 494, 200, 394, C["del"], 2.5, arrow="del"))
    b.append(text(212, 470, "대의원 선출, 건의 전달", 12.5, 700, C["del"], "start"))
    b.append(line(800, 394, 800, 494, C["raon"], 2.5, arrow="raon"))
    b.append(text(788, 470, "활동 참여, 결과 공유", 12.5, 700, C["raon"], "end"))
    b.append(text(500, 618, "전교생이 학생회장단을 직접 선출하고 각 학급은 학급회장과 부회장을 선출한다.", 13.5, 500, C["muted"]))
    return svg(W, H, "".join(b), "학생자치 전체 구조")


# ── 그림 1  역할 구분 개념도 ─────────────────────────────
def fig1():
    W, H = 1000, 600
    b = []
    cols = [
        (30, "del", "대의원회", "목소리를 모아 결정한다", "학교 속 의회",
         [("대표", "학급이 뽑은 대표가 모인다"), ("심의", "안건을 따지고 토론한다"), ("의결", "전교생 사안을 결정한다"), ("평가", "실행 결과를 평가한다")],
         "무엇을 할 것인가"),
        (610, "raon", "라온하제", "결정을 실행하고 만든다", "학교 속 실행부",
         [("기획", "사업과 행사를 설계한다"), ("실행", "부서별로 실천한다"), ("홍보", "과정과 결과를 알린다"), ("보고", "결과를 대의원회에 보고한다")],
         "어떻게 실현할 것인가"),
    ]
    for x, k, name, tag, meta, steps, q in cols:
        b.append(rect(x, 20, 360, 560, "#fff", C[k], 2, 20))
        b.append(f'<path d="M{x},{40} a20,20 0 0 1 20,-20 h320 a20,20 0 0 1 20,20 v92 h-360 z" fill="{C[k]}"/>')
        b.append(text(x + 180, 58, name, 30, 800, "#fff"))
        b.append(text(x + 180, 94, tag, 15.5, 600, "#fff"))
        b.append(text(x + 180, 118, meta, 12.5, 500, "#ffffffcc"))
        for i, (kw, desc) in enumerate(steps):
            yy = 160 + i * 86
            b.append(rect(x + 24, yy, 312, 70, C[k + "_l"], "none", 0, 12))
            b.append(f'<circle cx="{x + 62}" cy="{yy + 35}" r="24" fill="{C[k]}"/>')
            b.append(text(x + 62, yy + 35, kw, 15, 800, "#fff"))
            b.append(text(x + 100, yy + 35, desc, 15, 600, C["text"], "start"))
            if i < 3:
                b.append(line(x + 62, yy + 60, x + 62, yy + 96, C[k], 2))
        b.append(rect(x + 24, 510, 312, 50, "none", C[k], 1.5, 25, dash="4 4"))
        b.append(text(x + 180, 535, "핵심 질문  " + q, 15, 800, C[k]))
    # 가운데
    b.append(line(402, 210, 596, 210, C["del"], 3, arrow="del"))
    b.append(text(499, 190, "의결 사항, 사업 승인", 13.5, 700, C["del"]))
    b.append(line(598, 470, 404, 470, C["raon"], 3, arrow="raon"))
    b.append(text(501, 492, "실행 결과 보고", 13.5, 700, C["raon"]))
    b.append(f'<circle cx="500" cy="340" r="84" fill="{C["lead"]}"/>')
    b.append(f'<circle cx="500" cy="340" r="92" fill="none" stroke="{C["lead"]}" stroke-width="1.5" stroke-dasharray="3 5"/>')
    b.append(text(500, 312, "학생회장단", 18, 800, "#fff"))
    b.append(text(500, 342, "의장과 대표", 14, 600, "#EDE6FF"))
    b.append(text(500, 366, "양쪽 당연직", 12.5, 500, "#EDE6FF"))
    return svg(W, H, "".join(b), "대의원회와 라온하제의 역할 구분")


# ── 그림 2  회장단 벤 다이어그램 ─────────────────────────
def fig2():
    W, H = 1000, 560
    cy, r, cl, cr = 262, 215, 385, 615
    b = []
    b.append(f'<circle cx="{cl}" cy="{cy}" r="{r}" fill="{C["del_l"]}" stroke="{C["del"]}" stroke-width="2.5"/>')
    b.append(f'<circle cx="{cr}" cy="{cy}" r="{r}" fill="{C["raon_l"]}" stroke="{C["raon"]}" stroke-width="2.5"/>')
    d = cr - cl
    hy = math.sqrt(r * r - (d / 2) ** 2)
    top, bot = cy - hy, cy + hy
    b.append(f'<path d="M500,{top:.1f} A{r},{r} 0 0,1 500,{bot:.1f} A{r},{r} 0 0,1 500,{top:.1f} z" '
             f'fill="{C["lead"]}" stroke="{C["lead"]}" stroke-width="2"/>')
    # 왼쪽
    b.append(text(275, 150, "대의원회", 26, 800, C["del"]))
    b.append(text(275, 182, "31명, 심의와 의결", 14.5, 700, C["muted"]))
    b.append(lines(265, 232, ["학급회장과 부회장 23", "학년대의원장과 서기 포함", ""], 15, 600, C["text"]))
    b.append(text(265, 332, "학급 선거로 선출", 13, 600, C["del"]))
    # 오른쪽
    b.append(text(725, 150, "라온하제", 26, 800, C["raon"]))
    b.append(text(725, 182, "26명, 기획과 집행", 14.5, 700, C["muted"]))
    b.append(lines(735, 232, ["부서 부원 18", "부서장 6 포함", ""], 15, 600, C["text"]))
    b.append(text(735, 332, "공개 모집으로 선발", 13, 600, C["raon"]))
    # 교집합
    b.append(person(470, 170, 1.0) + person(500, 160, 1.15) + person(530, 170, 1.0))
    b.append(text(500, 222, "두 조직 공통", 16, 800, "#fff"))
    b.append(text(500, 254, "학생회장단 3", 14, 700, "#fff"))
    b.append(text(500, 274, "당연직", 12, 500, "#EDE6FF"))
    b.append(text(500, 306, "겸직 5", 14, 700, "#fff"))
    b.append(text(500, 326, "학급회장과 부회장", 12, 500, "#EDE6FF"))
    # 역할 태그
    b.append(pill(340, 520, 250, 40, "대의원회에서  의장단 3, 학급 대표 5", C["del"], size=14))
    b.append(pill(660, 520, 250, 40, "라온하제에서  대표단 3, 부원 5", C["raon"], size=14))
    b.append(path("M480,410 C470,470 420,480 400,500", C["lead"], 2, arrow="lead"))
    b.append(path("M520,410 C530,470 580,480 600,500", C["lead"], 2, arrow="lead"))
    return svg(W, H, "".join(b), "학생회장단의 이중 소속")


# ── 조직도 공통 박스 ─────────────────────────────────────
def obox(cx, y, w, h, title, sub, key, filled=True, badge=None):
    fill = C[key] if filled else "#fff"
    col = "#fff" if filled else C[key]
    s = rect(cx - w / 2, y, w, h, fill, C[key], 2, 12)
    if sub:
        s += text(cx, y + h / 2 - 10, title, 16, 800, col) + text(cx, y + h / 2 + 12, sub, 12.5, 500, "#ffffffdd" if filled else C["muted"])
    else:
        s += text(cx, y + h / 2, title, 16, 800, col)
    if badge:
        s += pill(cx + w / 2 - 30, y, 58, 22, badge, C["gold"], size=11)
    return s


def fig3():
    W, H = 1000, 660
    b = []
    L = C["line"]
    # 의장
    b.append(obox(500, 20, 230, 62, "의장", "학생회장", "lead", badge="당연직"))
    b.append(obox(170, 30, 170, 44, "지도교사", "", "muted" if False else "ink", filled=False))
    b[-1] = rect(85, 30, 170, 44, "#fff", C["muted"], 1.5, 12, dash="5 4") + text(170, 52, "대의원회 지도교사", 13.5, 700, C["muted"])
    b.append(line(255, 52, 385, 52, C["muted"], 1.5, dash="5 4"))
    b.append(rect(745, 30, 170, 44, "#fff", C["del"], 1.5, 12) + text(830, 46, "서기 2", 15, 800, C["del"]) + text(830, 64, "회의록, 의결서", 11.5, 500, C["muted"]))
    b.append(line(615, 52, 745, 52, C["del"], 1.5))
    # 부의장
    b.append(line(500, 82, 500, 112, L, 2))
    b.append(line(370, 112, 630, 112, L, 2))
    for x, s in [(370, "부회장 (기획)"), (630, "부회장 (소통)")]:
        b.append(line(x, 112, x, 124, L, 2))
        b.append(obox(x, 124, 200, 56, "부의장", s, "lead", badge="당연직"))
    # 학년
    b.append(line(500, 180, 500, 220, L, 2))
    b.append(line(170, 220, 830, 220, L, 2))
    for i, x in enumerate([170, 500, 830]):
        g = i + 1
        b.append(line(x, 220, x, 236, L, 2))
        b.append(obox(x, 236, 220, 52, f"{g}학년 대의원장", f"{g}학년 협의회 대표", "del"))
        b.append(line(x, 288, x, 304, C["del"], 2))
    b.append(rect(30, 304, 940, 176, C["del_l"], C["del"], 1.5, 14))
    b.append(text(500, 332, "학급 대의원 28명  (14개 학급 × 학급회장과 부회장)", 16, 800, C["del"]))
    for c in range(14):
        cx = 92 + c * 63
        b.append(rect(cx - 25, 356, 50, 58, "#fff", C["del"], 1.2, 10))
        b.append(person(cx - 9, 388, 0.62, C["del"]) + person(cx + 9, 388, 0.62, C["del"]))
    b.append(text(500, 446, "학년협의회는 학년별 학급회장과 부회장으로 구성하고, 학년대의원장과 서기는 학급 대의원 중에서 뽑는다", 12.5, 600, C["muted"]))
    # 특별위원회
    b.append(rect(30, 510, 940, 130, C["soft"], C["line"], 1.5, 16))
    b.append(text(58, 540, "특별위원회", 17, 800, C["ink"], "start"))
    b.append(text(58, 564, "대의원 중 지원, 지명", 12.5, 500, C["muted"], "start"))
    b.append(text(58, 584, "각 5명 내외", 12.5, 500, C["muted"], "start"))
    for x, t, s in [(420, "규정검토위원회", "학생생활인권규정 개정 의견 검토"), (735, "참여예산위원회", "학생참여예산 심의, 집행 점검")]:
        b.append(rect(x - 140, 532, 280, 84, "#fff", C["del"], 1.8, 12))
        b.append(text(x, 560, t, 16, 800, C["del"]))
        b.append(text(x, 588, s, 12.5, 500, C["muted"]))
    b.append(text(970, 500, "대의원회 총 31명, 의장단 3 + 학급 대의원 28", 12.5, 700, C["del"], "end"))
    return svg(W, H, "".join(b), "대의원회 조직도")


def fig4():
    W, H = 1000, 600
    b = []
    L = C["line"]
    b.append(obox(500, 20, 230, 62, "대표", "학생회장", "lead", badge="당연직"))
    b.append(rect(85, 30, 170, 44, "#fff", C["muted"], 1.5, 12, dash="5 4") + text(170, 52, "라온하제 지도교사", 13.5, 700, C["muted"]))
    b.append(line(255, 52, 385, 52, C["muted"], 1.5, dash="5 4"))
    b.append(rect(745, 30, 170, 44, "#fff", C["raon"], 1.5, 12) + text(830, 46, "대의원 겸직 5", 15, 800, C["raon"]) + text(830, 64, "학급회장과 부회장", 11.5, 500, C["muted"]))
    b.append(line(615, 52, 745, 52, C["raon"], 1.5))
    b.append(line(500, 82, 500, 112, L, 2))
    b.append(line(258, 112, 742, 112, L, 2))
    groups = [(258, "기획 총괄", "부회장", ["기획부", "문화체육부", "학습나눔부"]),
              (742, "소통 총괄", "부회장", ["소통홍보부", "생활인권부", "환경복지부"])]
    duties = {"기획부": ["연간 사업계획", "대형 행사 기획"], "문화체육부": ["스포츠 리그", "문화 예술 행사"],
              "학습나눔부": ["또래 멘토링", "자습 공간 운영"], "소통홍보부": ["의견 게시판, SNS", "월간 소식지"],
              "생활인권부": ["생활협약 캠페인", "존중 문화 조성"], "환경복지부": ["환경 개선, 쉼터", "급식, 복지 의견"]}
    for gx, t, s, depts in groups:
        b.append(line(gx, 112, gx, 124, L, 2))
        b.append(obox(gx, 124, 210, 56, t, s, "lead", badge="당연직"))
        b.append(line(gx, 180, gx, 212, L, 2))
        xs = [gx - 158, gx, gx + 158]
        b.append(line(xs[0], 212, xs[2], 212, L, 2))
        for x, dname in zip(xs, depts):
            b.append(line(x, 212, x, 228, L, 2))
            b.append(rect(x - 74, 228, 148, 250, "#fff", C["raon"], 1.8, 14))
            b.append(f'<path d="M{x - 74},{242} a14,14 0 0 1 14,-14 h120 a14,14 0 0 1 14,14 v34 h-148 z" fill="{C["raon"]}"/>')
            b.append(text(x, 254, dname, 16, 800, "#fff"))
            for i, dd in enumerate(duties[dname]):
                b.append(text(x, 304 + i * 24, dd, 13, 600, C["text"]))
            b.append(line(x - 54, 360, x + 54, 360, C["raon_l"], 2))
            b.append(lines(x, 384, ["부장 1", "부원 2~3", "3~4명"], 12.5, 600, C["muted"], lh=1.55))
    b.append(rect(30, 504, 940, 76, C["raon_l"], "none", 0, 16))
    b.append(text(500, 530, "학생회장단 3 (대표단) + 6개 부서 부원 23 = 26명", 16, 800, C["raon"]))
    b.append(text(500, 556, "부원 중 5명은 대의원회를 겸직하는 학급회장과 부회장이고, 학생회장단 3명은 두 조직의 당연직이다", 13.5, 600, C["muted"]))
    return svg(W, H, "".join(b), "라온하제 조직도")


# ── 그림 5  자치운영위원회 ───────────────────────────────
def fig5():
    W, H = 1000, 540
    cx, cy = 330, 270
    b = []
    b.append(f'<circle cx="{cx}" cy="{cy}" r="214" fill="{C["soft"]}"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="112" fill="#fff" stroke="{C["lead"]}" stroke-width="2.5"/>')
    b.append(text(cx, cy - 30, "자치운영위원회", 20, 800, C["lead"]))
    b.append(text(cx, cy - 2, "통합 집행부 회의", 13.5, 600, C["muted"]))
    b.append(pill(cx, cy + 36, 150, 30, "격주 월요일 점심", C["lead"], size=12.5))
    seats = [("lead", "회장")] + [("del", "1학년")] + [("raon", "기획")] + [("raon", "문체")] + [("del", "2학년")] + \
            [("raon", "학습")] + [("lead", "부회장")] + [("raon", "소통")] + [("del", "3학년")] + [("raon", "인권")] + \
            [("raon", "환경")] + [("lead", "부회장")]
    n = len(seats)
    for i, (k, lab) in enumerate(seats):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + 165 * math.cos(a), cy + 165 * math.sin(a)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="31" fill="{C[k]}"/>')
        b.append(text(x, y, lab, 12.5, 800, "#fff"))
    for i, a in enumerate([math.radians(-35), math.radians(215)]):
        x, y = cx + 238 * math.cos(a), cy + 238 * math.sin(a)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="24" fill="#fff" stroke="{C["muted"]}" stroke-width="1.5" stroke-dasharray="4 3"/>')
        b.append(text(x, y, "교사", 11.5, 700, C["muted"]))
    # 범례
    lx = 610
    items = [("lead", "학생회장단 3", "회장(위원장), 부회장 2"), ("del", "학년대의원장 3", "대의원회 대표"),
             ("raon", "라온하제 부서장 6", "부서 실행 책임"), ("muted", "지도교사 2 (배석)", "대의원회, 라온하제")]
    for i, (k, t, s) in enumerate(items):
        y = 70 + i * 78
        if k == "muted":
            b.append(f'<circle cx="{lx + 20}" cy="{y + 20}" r="18" fill="#fff" stroke="{C["muted"]}" stroke-width="1.5" stroke-dasharray="4 3"/>')
        else:
            b.append(f'<circle cx="{lx + 20}" cy="{y + 20}" r="18" fill="{C[k]}"/>')
        b.append(text(lx + 52, y + 10, t, 17, 800, C[k] if k != "muted" else C["muted"], "start"))
        b.append(text(lx + 52, y + 34, s, 13.5, 500, C["muted"], "start"))
    b.append(rect(lx, 392, 360, 92, C["lead_l"], "none", 0, 14))
    b.append(text(lx + 20, 418, "의결권 없는 조정 기구", 15.5, 800, C["lead"], "start"))
    b.append(text(lx + 20, 444, "안건 분류, 업무 배분, 진행 점검", 13.5, 600, C["text"], "start"))
    b.append(text(lx + 20, 466, "결정은 반드시 대의원회에서", 13.5, 600, C["text"], "start"))
    b.append(text(lx, 30, "위원 12명", 22, 800, C["ink"], "start"))
    return svg(W, H, "".join(b), "자치운영위원회 구성")


# ── 그림 6  안건 분류 흐름 ───────────────────────────────
def fig6():
    W, H = 1000, 450
    b = []
    b.append(rect(20, 180, 150, 90, C["soft"], C["ink"], 1.8, 14))
    b.append(text(95, 212, "학급 건의", 17, 800, C["ink"]))
    b.append(text(95, 240, "학급자치 시간", 12.5, 600, C["muted"]))
    b.append(line(172, 225, 214, 225, C["ink"], 2, arrow="ink"))
    b.append(f'<path d="M300,150 L382,225 L300,300 L218,225 z" fill="{C["lead"]}"/>')
    b.append(text(300, 212, "자치운영", 14.5, 800, "#fff"))
    b.append(text(300, 234, "위원회 분류", 14.5, 800, "#fff"))
    rows = [
        (70, "raon", "A  즉시 처리", "기존 사업 범위, 단순 개선", "라온하제 부서 실행"),
        (225, "del", "B  대의원회 상정", "전교생 영향, 예산, 규칙", "심의와 의결 → 라온하제 실행"),
        (380, "ink", "C  학교 전달", "시설, 교육과정, 학교 규정", "학교 답변 14일 이내"),
    ]
    for y, k, t, s, r in rows:
        b.append(path(f"M384,225 C430,225 420,{y} 470,{y}", C[k], 2.2, arrow=k))
        b.append(rect(476, y - 44, 250, 88, C[k + "_l"] if k != "ink" else C["soft"], C[k], 1.8, 14))
        b.append(text(496, y - 16, t, 16, 800, C[k], "start"))
        b.append(text(496, y + 10, s, 13, 600, C["muted"], "start"))
        b.append(text(496, y + 30, r, 13, 700, C["text"], "start"))
        b.append(path(f"M728,{y} C770,{y} 770,225 812,225", C["ok"], 2, arrow="ok" if y == 225 else None))
    b.append(rect(816, 170, 166, 110, C["ok"], rx=16))
    b.append(text(899, 206, "결과 공개", 17, 800, "#fff"))
    b.append(text(899, 232, "학급 환류", 17, 800, "#fff"))
    b.append(text(899, 258, "다음 학급자치 시간", 11.5, 600, "#E4F4EF"))
    return svg(W, H, "".join(b), "안건 분류 흐름")


# ── 그림 7  월간 사이클 ─────────────────────────────────
def fig7():
    W, H = 1000, 600
    cx, cy, R = 500, 300, 205
    b = []
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{C["soft"]}" stroke-width="18"/>')
    # 호 화살표
    def arc(a1, a2, k):
        x1, y1 = cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1))
        x2, y2 = cx + R * math.cos(math.radians(a2)), cy + R * math.sin(math.radians(a2))
        return path(f"M{x1:.1f},{y1:.1f} A{R},{R} 0 0,1 {x2:.1f},{y2:.1f}", C[k], 3.5, arrow=k)
    nodes = [(-90, "ok", "1주", "학급자치 시간 ①", "건의 수렴, 지난 결과 공유"),
             (0, "del", "2주", "운영위원회 → 대의원회", "안건 분류와 심의, 의결"),
             (90, "raon", "3주", "학급자치 시간 ②, 실행", "결과 전달, 라온하제 착수"),
             (180, "lead", "4주", "점검, 결과 공개", "운영위원회, 소식지 발행")]
    for i, (a, k, *_ ) in enumerate(nodes):
        a1, a2 = (a + 40, a + 72) if a in (-90, 90) else (a + 17, a + 49)
        b.append(arc(a1, a2, nodes[(i + 1) % 4][1]))
    for a, k, wk, t, s in nodes:
        x, y = cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))
        w, h = 250, 96
        b.append(rect(x - w / 2, y - h / 2, w, h, "#fff", C[k], 2.5, 16))
        b.append(pill(x - w / 2 + 34, y - h / 2 + 2, 52, 26, wk, C[k], size=13))
        b.append(text(x, y - 6, t, 16.5, 800, C[k]))
        b.append(text(x, y + 22, s, 13, 600, C["muted"]))
    b.append(text(cx, cy - 22, "월간 자치 순환", 24, 800, C["ink"]))
    b.append(text(cx, cy + 12, "학급에서 시작해", 15, 600, C["muted"]))
    b.append(text(cx, cy + 34, "학급으로 돌아온다", 15, 600, C["muted"]))
    return svg(W, H, "".join(b), "월간 자치 4주 사이클")


# ── 그림 8  학급자치 45분 ───────────────────────────────
def fig8():
    W, H = 1000, 300
    b = []
    segs = [(5, "열기", "지난 결과 공유", "학급회장", C["ink"]), (10, "안건 발표", "건의, 대의원회 전달 사항", "제안 학생", C["del"]),
            (20, "토의", "모둠 토의, 전체 토론", "학급 전체", C["lead"]), (7, "결정", "표결, 합의 정리", "학급회장", C["raon"]),
            (3, "닫기", "회의록, 건의서 확정", "학급부회장", C["ok"])]
    x = 30
    total = 45
    Wb = 940
    b.append(text(30, 30, "45분", 22, 800, C["ink"], "start"))
    b.append(text(100, 30, "진행  학급회장    |    기록  학급부회장    |    담임  조력자", 14, 600, C["muted"], "start"))
    for m, t, s, who, col in segs:
        w = Wb * m / total
        b.append(rect(x + 2, 64, w - 4, 70, col, rx=12))
        b.append(text(x + w / 2, 88, t, 15 if w > 70 else 13, 800, "#fff"))
        b.append(text(x + w / 2, 112, f"{m}분", 13, 600, "#ffffffdd"))
        b.append(line(x + w / 2, 136, x + w / 2, 160, col, 2))
        b.append(f'<circle cx="{x + w / 2:.1f}" cy="164" r="4" fill="{col}"/>')
        x += w
    # 설명 (좁은 구간은 엇갈리게)
    x = 30
    for i, (m, t, s, who, col) in enumerate(segs):
        w = Wb * m / total
        mx = min(x + w / 2, 905)
        yy = 196 if i % 2 == 0 else 246
        if i % 2 == 1:
            b.append(line(mx, 168, mx, yy - 22, col, 1.2, dash="3 3"))
        b.append(text(mx, yy, s, 13.5, 700, C["text"]))
        b.append(text(mx, yy + 20, who, 12, 600, col))
        x += w
    return svg(W, H, "".join(b), "학급자치 시간 운영 모형")


# ── 그림 9  7대 지원 영역 ───────────────────────────────
def fig9():
    W, H = 1000, 470
    cx, cy = 500, 235
    b = []
    items = [("시간", "학급자치 연 17시간", "ok"), ("공간", "자치실, 의견 게시판", "del"), ("예산", "학생참여예산제", "raon"),
             ("사람", "지도교사 분리 지정", "lead"), ("역량", "리더십 캠프 연 2회", "del"), ("제도", "자치회 규칙 개정", "raon"),
             ("소통", "답변 14일 이내", "lead")]
    n = len(items)
    for i, (t, s, k) in enumerate(items):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + 380 * math.cos(a), cy + 178 * math.sin(a)
        b.append(line(cx + 100 * math.cos(a), cy + 100 * math.sin(a) * 0.9, x - 60 * math.cos(a), y - 26 * math.sin(a), C["line"], 2))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="96" fill="{C["ink"]}"/>')
    b.append(text(cx, cy - 14, "학생자치", 22, 800, "#fff"))
    b.append(text(cx, cy + 16, "지속 가능성", 14, 600, C["gold"]))
    for i, (t, s, k) in enumerate(items):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + 380 * math.cos(a), cy + 178 * math.sin(a)
        b.append(rect(x - 95, y - 32, 190, 64, "#fff", C[k], 2, 14))
        b.append(f'<circle cx="{x - 64:.1f}" cy="{y:.1f}" r="20" fill="{C[k]}"/>')
        b.append(text(x - 64, y, t, 13, 800, "#fff"))
        b.append(text(x - 36, y, s, 13.5, 700, C["text"], "start"))
    return svg(W, H, "".join(b), "학생자치 7대 지원 영역")


# ── 그림 10  로드맵 ──────────────────────────────────────
def fig10():
    W, H = 1000, 330
    b = []
    phases = [("설계", "2026년 10~12월", ["개선안 공유, 의견 수렴", "자치회 규칙 개정안", "학교운영위원회 심의"], C["ink"]),
              ("준비", "2027년 1~2월", ["학급자치 시간 편성", "학사일정 반영", "운영 가이드북 제작"], C["del"]),
              ("출범", "2027년 3월", ["대의원 선출", "라온하제 공개 모집", "리더십 캠프"], C["lead"]),
              ("운영과 환류", "2027년 4~12월", ["4주 사이클 정례 운영", "운영위원회 격주 개최", "학기별 성과 점검"], C["raon"])]
    w = 232
    for i, (t, d, its, col) in enumerate(phases):
        x = 20 + i * w
        tip = 26
        pts = f"{x},{30} {x + w - 6},{30} {x + w - 6 + tip},{76} {x + w - 6},{122} {x},{122}"
        if i > 0:
            pts += f" {x + tip},{76}"
        b.append(f'<polygon points="{pts}" fill="{col}"/>')
        b.append(text(x + w / 2 + 6, 62, t, 19, 800, "#fff"))
        b.append(text(x + w / 2 + 6, 92, d, 13.5, 600, "#ffffffdd"))
        for j, it in enumerate(its):
            yy = 160 + j * 38
            b.append(f'<circle cx="{x + 26}" cy="{yy}" r="4" fill="{col}"/>')
            b.append(text(x + 40, yy, it, 14, 600, C["text"], "start"))
    b.append(line(20, 290, 980, 290, C["line"], 2))
    b.append(text(980, 312, "2027학년도 3월 새 체제 출범", 13, 700, C["lead"], "end"))
    return svg(W, H, "".join(b), "추진 로드맵")


FIGS = {
    "fig0_structure": fig0, "fig1_roles": fig1, "fig2_leaders": fig2, "fig3_del_org": fig3, "fig4_raon_org": fig4,
    "fig5_council": fig5, "fig6_triage": fig6, "fig7_cycle": fig7, "fig8_classmeeting": fig8,
    "fig9_support": fig9, "fig10_roadmap": fig10,
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, f in FIGS.items():
        with open(os.path.join(OUT, k + ".svg"), "w", encoding="utf-8") as fp:
            fp.write(f())
    print("svg", len(FIGS))
