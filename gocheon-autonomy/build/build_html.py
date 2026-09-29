# -*- coding: utf-8 -*-
"""HTML 본문, 표지, PDF 생성  python3 build/build_html.py

out/고천중_학생자치_개선안.html  웹 배포용 (웹폰트 링크)
out/고천중_학생자치_개선안.pdf   인쇄용 (표지 + 본문, 쪽번호)
build/cover.html               표지 단독 (render.py가 cover.png로 변환)
"""
import os, re, io, html
from content import META, COLORS as C, TOC, SUMMARY, BLOCKS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD = os.path.join(ROOT, "build")
OUT = os.path.join(ROOT, "out")
FIGS = os.path.join(ROOT, "figs")
NAME = "고천중_학생자치_개선안"
SERIF_DIR = "/tmp/claude-0/-home-user-Project1/4f344351-ba79-556c-86d5-e6bebf97c7d4/scratchpad/fonts/package/files"

WEB_FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.min.css">"""


def local_fonts():
    out = []
    for w in (600, 700, 900):
        for sub in ("korean", "latin"):
            f = os.path.join(SERIF_DIR, f"noto-serif-kr-{sub}-{w}-normal.woff2")
            if os.path.exists(f):
                out.append(f"@font-face{{font-family:'Noto Serif KR';font-weight:{w};src:url('file://{f}') format('woff2')}}")
    return "<style>" + "".join(out) + "</style>"


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s.replace("\n", "<br>")


# ── 표지 ───────────────────────────────────────────────
def cover_html():
    kw_cols = [C["del"], C["raon"], C["lead"], C["ok"]]
    kws = "".join(f'<span class="kw"><i style="background:{c}"></i>{k}</span>' for k, c in zip(META["keywords"], kw_cols))
    return f"""
<section class="cover">
  <svg class="cv-art" viewBox="0 0 600 600" aria-hidden="true">
    <defs><clipPath id="cvL"><circle cx="215" cy="300" r="170"/></clipPath></defs>
    <circle cx="215" cy="300" r="232" fill="none" stroke="#ffffff" stroke-opacity=".06" stroke-width="1"/>
    <circle cx="385" cy="300" r="262" fill="none" stroke="#ffffff" stroke-opacity=".045" stroke-width="1"/>
    <circle cx="215" cy="300" r="170" fill="{C['del']}" fill-opacity=".10" stroke="{C['del']}" stroke-width="2.5"/>
    <circle cx="385" cy="300" r="170" fill="{C['raon']}" fill-opacity=".08" stroke="{C['raon']}" stroke-width="2.5"/>
    <circle cx="385" cy="300" r="170" fill="{C['lead']}" clip-path="url(#cvL)"/>
    <text x="300" y="292" text-anchor="middle" fill="#fff" font-size="20" font-weight="800" font-family="Pretendard">학생회장단</text>
    <text x="300" y="318" text-anchor="middle" fill="#E9E1FF" font-size="12.5" font-weight="500" font-family="Pretendard">두 조직의 연결</text>
    <text x="128" y="306" text-anchor="middle" fill="#9FB6F2" font-size="17" font-weight="700" font-family="Pretendard">대의원회</text>
    <text x="472" y="306" text-anchor="middle" fill="#F6B39A" font-size="17" font-weight="700" font-family="Pretendard">라온하제</text>
  </svg>
  <div class="cv-top">
    <div class="cv-eyebrow">{META['school_en']}  |  STUDENT AUTONOMY</div>
  </div>
  <div class="cv-main">
    <div class="cv-year">{META['year']}</div>
    <h1 class="cv-title">{META['school']}<br><span>{META['title']}</span></h1>
    <div class="cv-rule"></div>
    <p class="cv-sub">{META['subtitle']}</p>
    <div class="cv-kws">{kws}</div>
  </div>
  <div class="cv-foot">
    <div class="cv-date">{META['date']}</div>
    <div class="cv-org"><b>{META['school']}</b>{META['dept']}</div>
  </div>
</section>"""


# ── 블록 렌더러 ─────────────────────────────────────────
def figure_svg(fid):
    p = os.path.join(FIGS, fid + ".svg")
    s = open(p, encoding="utf-8").read()
    return re.sub(r'width="\d+" height="\d+"', 'width="100%" height="auto"', s, count=1)


def table_html(t):
    tone = t.get("tone", "ink")
    cols = t["cols"]
    ws = t.get("widths")
    cg = "".join(f'<col style="width:{w}%">' for w in ws) if ws else ""
    th = []
    for i, c in enumerate(cols):
        cls = ""
        if tone == "split":
            cls = ["t-ink", "t-del", "t-raon"][min(i, 2)]
        elif tone == "split2":
            cls = ["t-del", "t-raon"][min(i, 1)]
        th.append(f'<th class="{cls}">{inline(c)}</th>')
    rows = []
    for r in t["rows"]:
        tds = []
        for i, v in enumerate(r):
            ind = v.startswith("  ")
            cls = ' class="sub"' if ind else ""
            tds.append(f"<td{cls}>{inline(v.strip())}</td>")
        rows.append("<tr>" + "".join(tds) + "</tr>")
    note = f'<p class="tnote">{inline(t["note"])}</p>' if t.get("note") else ""
    return (f'<div class="tbl-wrap"><table class="tbl tone-{tone}"><colgroup>{cg}</colgroup>'
            f'<thead><tr>{"".join(th)}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>{note}')


def body_html():
    out, sec_open = [], False
    fig_no = 0
    for b in BLOCKS:
        k = b[0]
        if k == "h1":
            if sec_open:
                out.append("</section>")
            sid = "sec-" + re.sub(r"\W", "", b[1]) if b[1] != "부록" else "sec-appx"
            out.append(f'<section class="chapter" id="{sid}">')
            sec_open = True
            out.append(f'<header class="ch-head"><div class="ch-num">{b[1]}</div>'
                       f'<div><h2 class="ch-title">{inline(b[2])}</h2><p class="ch-lead">{inline(b[3])}</p></div></header>')
        elif k == "h2":
            out.append(f'<h3 class="h2">{inline(b[1])}</h3>')
        elif k == "p":
            out.append(f'<p class="p">{inline(b[1])}</p>')
        elif k == "bullets":
            out.append('<ul class="ul">' + "".join(f"<li>{inline(x)}</li>" for x in b[1]) + "</ul>")
        elif k == "table":
            out.append(table_html(b[1]))
        elif k == "figure":
            fig_no += 1
            out.append(f'<figure class="fig" id="{b[1]}">{figure_svg(b[1])}<figcaption>{inline(b[2])}</figcaption></figure>')
        elif k == "callout":
            out.append(f'<aside class="callout c-{b[1]}"><div class="c-title">{inline(b[2])}</div><p>{inline(b[3])}</p></aside>')
        elif k == "pagebreak":
            pass  # 장마다 새 쪽 (CSS)
    if sec_open:
        out.append("</section>")
    return "\n".join(out)


def toc_html():
    ids = []
    for num, t in TOC:
        sid = "sec-appx" if num == "부록" else "sec-" + num
        ids.append(f'<li><a href="#{sid}"><span class="tn">{num}</span><span class="tt">{t}</span></a></li>')
    summ = "".join(f'<div class="sum-item"><div class="sum-k">{k}</div><div class="sum-v">{inline(v)}</div></div>' for k, v in SUMMARY)
    return f"""
<section class="front" id="front">
  <div class="front-grid">
    <div>
      <div class="eyebrow">CONTENTS</div>
      <h2 class="front-h">목차</h2>
      <ol class="toc">{''.join(ids)}</ol>
    </div>
    <div>
      <div class="eyebrow">EXECUTIVE SUMMARY</div>
      <h2 class="front-h">핵심 요약</h2>
      <div class="sum">{summ}</div>
    </div>
  </div>
</section>"""


CSS = r"""
:root{
  --ink:%(ink)s;--text:%(text)s;--muted:%(muted)s;--line:%(line)s;--soft:%(soft)s;
  --del:%(del)s;--del-l:%(del_l)s;--raon:%(raon)s;--raon-l:%(raon_l)s;--lead:%(lead)s;--lead-l:%(lead_l)s;
  --gold:%(gold)s;--ok:%(ok)s;--ok-l:%(ok_l)s;--paper:#ffffff;--bg:#EEF1F6;
  --sans:Pretendard,'Pretendard Variable','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  --serif:'Noto Serif KR','Nanum Myeongjo',serif;
  color-scheme: light;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--sans);font-size:15.5px;line-height:1.75;word-break:keep-all;overflow-wrap:break-word}
.doc{max-width:900px;margin:0 auto;padding:32px 16px 80px}
.sheet{background:var(--paper);border-radius:6px;box-shadow:0 1px 2px rgba(21,33,59,.06),0 8px 28px rgba(21,33,59,.07);margin:0 0 28px;overflow:hidden}

/* 표지 */
.cover{position:relative;aspect-ratio:210/297;background:
  radial-gradient(120%% 80%% at 90%% 0%%,#22325A 0%%,rgba(34,50,90,0) 60%%),var(--ink);color:#fff;overflow:hidden;
  display:flex;flex-direction:column;padding:8.5%% 9%% 7%%;container-type:inline-size}
.cv-art{position:absolute;right:-6%%;top:3%%;width:84%%;height:auto}
.cv-top{position:relative}
.cv-eyebrow{font-size:1.75cqw;letter-spacing:.32em;color:var(--gold);font-weight:600}
.cv-main{position:relative;margin-top:auto;margin-bottom:9%%}
.cv-year{display:inline-block;font-size:2.1cqw;font-weight:700;letter-spacing:.08em;padding:.45em 1.1em;border:1px solid rgba(196,162,106,.7);color:var(--gold);border-radius:999px;margin-bottom:4.2cqw}
.cv-title{font-family:var(--serif);font-weight:700;font-size:5cqw;line-height:1.28;margin:0;letter-spacing:-.01em;color:#DCE3F2}
.cv-title span{display:block;font-size:8.6cqw;font-weight:900;color:#fff;letter-spacing:-.02em;margin-top:.5cqw}
.cv-rule{width:12cqw;height:3px;background:var(--gold);margin:5cqw 0 3.6cqw}
.cv-sub{font-size:3cqw;font-weight:500;margin:0 0 6cqw;color:#E6EAF3;letter-spacing:-.01em}
.cv-kws{display:flex;flex-wrap:wrap;gap:1.4cqw 3.4cqw}
.kw{display:inline-flex;align-items:center;gap:1.2cqw;font-size:2.15cqw;font-weight:600;color:#C9D2E4}
.kw i{display:inline-block;width:1.5cqw;height:1.5cqw;border-radius:50%%}
.cv-foot{position:relative;display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid rgba(255,255,255,.18);padding-top:3.2cqw}
.cv-date{font-size:2.3cqw;color:#AEB8CC;font-weight:500;letter-spacing:.04em}
.cv-org{text-align:right;font-size:2.2cqw;color:#AEB8CC;line-height:1.5}
.cv-org b{display:block;font-family:var(--serif);font-size:3.8cqw;color:#fff;font-weight:700;letter-spacing:.06em}

/* 목차와 요약 */
.front{padding:56px 56px 48px}
.front-grid{display:grid;grid-template-columns:1fr;gap:40px}
.eyebrow{font-size:11.5px;letter-spacing:.28em;color:var(--gold);font-weight:700}
.front-h{font-family:var(--serif);font-size:30px;margin:4px 0 18px;color:var(--ink)}
.toc{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;column-gap:28px}
.toc li a{display:flex;gap:14px;align-items:baseline;padding:11px 2px;border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink)}
.toc .tn{font-family:var(--serif);font-weight:700;color:var(--del);min-width:2.4em}
.toc .tt{font-weight:600}
.toc li a:hover .tt{color:var(--del)}
.sum{display:grid;gap:10px}
.sum-item{display:grid;grid-template-columns:120px 1fr;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.sum-k{background:var(--ink);color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;padding:12px;font-size:14.5px}
.sum-item:nth-child(1) .sum-k{background:linear-gradient(90deg,var(--del),var(--raon))}
.sum-item:nth-child(2) .sum-k{background:var(--lead)}
.sum-item:nth-child(3) .sum-k{background:var(--lead)}
.sum-item:nth-child(4) .sum-k{background:var(--ok)}
.sum-v{padding:12px 18px;font-size:14.5px;line-height:1.65}
.sum-v strong{color:var(--ink)}

/* 장 */
.chapter{padding:56px 56px 40px}
.ch-head{display:flex;gap:22px;align-items:flex-start;padding-bottom:22px;margin-bottom:28px;border-bottom:2px solid var(--ink);position:relative}
.ch-head:after{content:"";position:absolute;left:0;bottom:-2px;width:88px;height:2px;background:var(--del)}
.ch-num{font-family:var(--serif);font-size:46px;font-weight:900;color:var(--del);line-height:1;min-width:64px}
#sec-appx .ch-num{font-size:26px;padding-top:10px}
.ch-title{font-size:27px;font-weight:800;color:var(--ink);margin:2px 0 6px;letter-spacing:-.02em;line-height:1.35}
.ch-lead{margin:0;color:var(--muted);font-size:15px}
.h2{font-size:18.5px;font-weight:800;color:var(--ink);margin:34px 0 12px;display:flex;align-items:center;gap:10px;letter-spacing:-.01em}
.h2:before{content:"";width:5px;height:19px;border-radius:2px;background:var(--del)}
.p{margin:0 0 14px;text-align:justify}
.p strong,.ul strong,td strong,.callout strong{color:var(--ink);font-weight:800}
.ul{margin:0 0 16px;padding:0;list-style:none}
.ul li{position:relative;padding-left:20px;margin:6px 0}
.ul li:before{content:"";position:absolute;left:4px;top:.72em;width:6px;height:6px;border-radius:50%%;background:var(--del)}

/* 표 */
.tbl-wrap{overflow-x:auto;margin:6px 0 18px;border-radius:10px;border:1px solid var(--line)}
.tbl{width:100%%;border-collapse:collapse;font-size:14px;line-height:1.6;min-width:560px}
.tbl th{background:var(--ink);color:#fff;font-weight:700;text-align:left;padding:11px 14px;font-size:13.5px;letter-spacing:.01em}
.tone-del th{background:var(--del)}.tone-raon th{background:var(--raon)}.tone-lead th{background:var(--lead)}.tone-ok th{background:var(--ok)}
.tbl th.t-ink{background:var(--ink)}.tbl th.t-del{background:var(--del)}.tbl th.t-raon{background:var(--raon)}
.tbl td{padding:10px 14px;border-top:1px solid var(--line);vertical-align:top}
.tbl tbody tr:nth-child(even) td{background:#FAFBFD}
.tbl td:first-child{font-weight:700;color:var(--ink)}
.tbl td.sub{padding-left:28px;font-weight:500;color:var(--muted)}
.tone-split td:nth-child(2){background:linear-gradient(0deg,rgba(42,86,198,.035),rgba(42,86,198,.035))}
.tone-split td:nth-child(3){background:linear-gradient(0deg,rgba(224,100,58,.04),rgba(224,100,58,.04))}
.tone-split2 td:first-child{font-weight:500;color:var(--text)}
.tnote{font-size:12.5px;color:var(--muted);margin:-10px 0 18px;padding-left:2px}

/* 강조 상자 */
.callout{border-radius:12px;padding:16px 20px;margin:8px 0 20px;background:var(--soft);border-left:5px solid var(--ink)}
.callout .c-title{font-weight:800;font-size:14px;letter-spacing:.02em;margin-bottom:4px;color:var(--ink)}
.callout p{margin:0;font-size:15px}
.c-del{background:var(--del-l);border-color:var(--del)}.c-del .c-title{color:var(--del)}
.c-lead{background:var(--lead-l);border-color:var(--lead)}.c-lead .c-title{color:var(--lead)}
.c-ok{background:var(--ok-l);border-color:var(--ok)}.c-ok .c-title{color:var(--ok)}

/* 그림 */
.fig{margin:14px 0 24px;text-align:center}
.fig svg{display:block;width:100%%;height:auto;max-width:100%%}
.fig figcaption{font-size:12.5px;color:var(--muted);margin-top:8px;font-weight:600;letter-spacing:.01em}

/* 화면 전용 */
.topbar{position:sticky;top:0;z-index:5;background:rgba(21,33,59,.94);backdrop-filter:blur(6px);color:#fff}
.topbar .in{max-width:900px;margin:0 auto;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px;font-size:13px}
.topbar b{font-weight:700;letter-spacing:.02em}
.topbar nav{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none}
.topbar nav a{color:#C9D2E4;text-decoration:none;padding:4px 8px;border-radius:6px;white-space:nowrap;font-family:var(--serif);font-weight:700}
.topbar nav a:hover{background:rgba(255,255,255,.1);color:#fff}

@media screen and (max-width:720px){
  body{font-size:15px}
  .doc{padding:16px 16px 60px}
  .front,.chapter{padding:32px 20px 24px}
  .toc{grid-template-columns:1fr}
  .sum-item{grid-template-columns:1fr}
  .ch-head{gap:14px}.ch-num{font-size:34px;min-width:44px}.ch-title{font-size:22px}
  .topbar b{display:none}
}

/* 인쇄 */
@page{size:A4;margin:17mm 18mm 18mm}
@media print{
  body{background:#fff;font-size:10.4pt;line-height:1.68}
  .topbar{display:none}
  .doc{max-width:none;padding:0;margin:0}
  .sheet{box-shadow:none;border-radius:0;margin:0;overflow:visible}
  .front,.chapter{padding:0;break-before:page}
  .front-grid{gap:26px}
  .toc li a{padding:7px 2px}
  .front-h{font-size:22pt;margin-bottom:10px}
  .ch-head{margin-bottom:18px;padding-bottom:14px}
  .ch-num{font-size:32pt}.ch-title{font-size:19pt}.ch-lead{font-size:10.5pt}
  .h2{font-size:13pt;margin:20px 0 8px;break-after:avoid}
  .tbl{font-size:9.2pt;min-width:0}.tbl th{font-size:9pt;padding:7px 10px}.tbl td{padding:6px 10px}
  .tbl tr{break-inside:avoid}.tbl thead{display:table-header-group}
  .tbl-wrap{overflow:visible;border-radius:6px}
  .callout{break-inside:avoid;padding:11px 16px}.callout p{font-size:10.2pt}
  .fig{break-inside:avoid;margin:8px 0 16px}
  .fig svg{max-height:128mm;width:auto;margin:0 auto}
  .tnote{font-size:8.5pt}
  a{color:inherit}
}
""" % C


def page(fonts, with_cover=True, with_body=True, screen_bar=True):
    nav = "".join(f'<a href="#{"sec-appx" if n == "부록" else "sec-" + n}">{n}</a>' for n, _ in TOC)
    bar = (f'<div class="topbar"><div class="in"><b>{META["school"]} {META["title"]}</b><nav>{nav}</nav></div></div>'
           if screen_bar else "")
    parts = []
    if with_cover:
        parts.append(f'<div class="sheet">{cover_html()}</div>')
    if with_body:
        parts.append(f'<div class="sheet">{toc_html()}</div>')
        parts.append(f'<div class="sheet body">{body_html()}</div>')
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{META['school']} {META['title']}</title>
<meta name="description" content="{META['year']} {META['school']} {META['title']}  {META['subtitle']}">
{fonts}
<style>{CSS}</style></head>
<body>{bar}<main class="doc">{''.join(parts)}</main></body></html>"""


COVER_ONLY_CSS = """<style>
html,body{margin:0;background:#15213B}
.doc{padding:0!important;max-width:none!important}
.sheet{margin:0!important;border-radius:0!important;box-shadow:none!important}
.cover{width:794px;height:1123px;aspect-ratio:auto}
@page{size:A4;margin:0}
</style>"""


def build():
    os.makedirs(OUT, exist_ok=True)
    web = page(WEB_FONTS)
    open(os.path.join(OUT, NAME + ".html"), "w", encoding="utf-8").write(web)
    lf = local_fonts()
    open(os.path.join(BUILD, "cover.html"), "w", encoding="utf-8").write(
        page(lf + COVER_ONLY_CSS, with_body=False, screen_bar=False))
    open(os.path.join(BUILD, "print_body.html"), "w", encoding="utf-8").write(
        page(lf, with_cover=False, screen_bar=False))
    print("html ok")


def build_pdf():
    from playwright.sync_api import sync_playwright
    import fitz
    foot = (f'<div style="width:100%;font-family:Pretendard;font-size:7.5pt;color:{C["muted"]};padding:0 18mm;'
            f'display:flex;justify-content:space-between"><span>{META["school"]}  {META["title"]}</span>'
            f'<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = br.new_page()
        pg.goto("file://" + os.path.join(BUILD, "cover.html"))
        pg.evaluate("document.fonts.ready")
        cov = pg.pdf(format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                     page_ranges="1")
        pg.goto("file://" + os.path.join(BUILD, "print_body.html"))
        pg.evaluate("document.fonts.ready")
        body = pg.pdf(format="A4", print_background=True, display_header_footer=True,
                      header_template="<span></span>", footer_template=foot,
                      margin={"top": "17mm", "bottom": "18mm", "left": "18mm", "right": "18mm"})
        br.close()
    doc = fitz.open(stream=cov, filetype="pdf")
    doc.insert_pdf(fitz.open(stream=body, filetype="pdf"))
    doc.set_metadata({"title": f"{META['school']} {META['title']}", "author": f"{META['school']} {META['dept']}",
                      "subject": META["subtitle"]})
    doc.save(os.path.join(OUT, NAME + ".pdf"), garbage=3, deflate=True)
    print("pdf ok")


if __name__ == "__main__":
    import sys
    build()
    if "pdf" in sys.argv:
        build_pdf()
