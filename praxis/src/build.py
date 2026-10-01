#!/usr/bin/env python3
"""PRAXIS 창간특집호 빌드 스크립트

페이지 조각(p0*.html)과 praxis.css 로부터 세 가지 HTML 을 만든다
  - print.html   PDF 렌더링용 (로컬 폰트)
  - web edition  반응형 웹판
  - e-book       페이지 넘김 뷰어
PDF 와 DOCX 는 render.js 와 docx_build.py 가 이어서 만든다
"""
import glob
import os
import re
import sys

from bs4 import BeautifulSoup

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(SRC, '..'))
BUILD = os.path.join(SRC, '_build')
NAME = 'PRAXIS_Vol01_창간특집호'
TITLE = 'PRAXIS 창간특집호'
DESC = 'PRAXIS 제1권 제1호 창간특집호 · 교육 AI 에듀테크 학습과학 · 2026년 9월'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;800;900'
         '&family=Noto+Serif+KR:wght@400;500;600;700;800;900'
         '&family=Playfair+Display:ital,wght@0,400;0,700;0,800;1,400;1,700&display=swap" rel="stylesheet">')
BOOK_ICON = ('<svg viewBox="0 0 64 48" width="26" height="20" aria-hidden="true"><path d="M32 10C25 5 14 4 4 6v34c10-2 21-1 28 4 '
             '7-5 18-6 28-4V6c-10-2-21-1-28 4z" fill="none" stroke="#E0735A" stroke-width="4" stroke-linejoin="round"/>'
             '<path d="M32 10v34" stroke="#E0735A" stroke-width="4"/></svg>')


def source_files(only=None):
    files = sorted(glob.glob(os.path.join(SRC, 'p[0-9]*.html')))
    if only:
        files = [f for f in files if os.path.basename(f) in only]
    return files


def resolve_tokens(html, pages):
    ids = {p.get('id'): int(p['data-n']) for p in pages if p.get('id')}
    out = []
    for p in pages:
        n = int(p['data-n'])
        t = str(p).replace('{{next}}', f'{n + 1:02d}').replace('{{prev}}', f'{n - 1:02d}')
        out.append(t)
    t = '\n'.join(out)
    def pg(m):
        k = m.group(1)
        return f'{ids[k]:02d}' if k in ids else '??'
    return re.sub(r'\{\{pg:([\w-]+)\}\}', pg, t)


SENT_SKIP = {'svg', 'style', 'script', 'h1', 'h2', 'h3', 'h4', 'h5', 'title', 'a'}


def sentence_gaps(pages):
    """온점 없는 문장 사이에 조금 넓은 간격을 둔다 (…다 · …까 뒤의 띄어쓰기)"""
    from bs4 import NavigableString
    pat = re.compile(r'([가-힣](?:다|까))\s+(?=[가-힣A-Za-z0-9「(‘\'])')
    for sec in pages:
        if (sec.get('id') or '').startswith('p-sources'):
            continue
        for node in list(sec.find_all(string=True)):
            if isinstance(node, NavigableString) and node.parent and not any(
                    p.name in SENT_SKIP for p in [node.parent, *node.parent.parents] if p is not None and p.name):
                t = str(node)
                if pat.search(t):
                    node.replace_with(NavigableString(pat.sub(lambda m: m.group(1) + '\u2002', t)))


def number_figures(html):
    n = [0]
    def rep(m):
        n[0] += 1
        title = re.sub(r'^\s*그림\s*(?:\d+(?![년월일]))?\s*', '', m.group(2))
        title = re.sub(r'^P(\d)[a-z]?\s+', r'제안 \1 ', title)
        title = re.sub(r'^(?:[A-Z]\d?[a-z]?|\d{2})\s+', '', title)
        return f'{m.group(1)}<b>그림 {n[0]} {title}</b>'
    return re.sub(r'(<figcaption[^>]*>\s*)<b[^>]*>(.*?)</b>', rep, html, flags=re.S)


def build_toc(pages):
    items = []
    for p in pages:
        if p.get('data-toc'):
            parts = p['data-toc'].split('|') + ['', '']
            cls = p.get('data-toc-cls', '')
            items.append(f'<li class="{cls}"><span class="pg">{int(p["data-n"]):02d}</span><span class="sec">{parts[0]}</span>'
                         f'<b>{parts[1]}</b>' + (f'<i>{parts[2]}</i>' if parts[2] else '') + '</li>')
    return items


REF_ORDER = [('참고문헌', '학술 논문 · 국외', '국외논문'), ('참고문헌', '학술 논문 · 국내', '국내논문'),
             ('자료 출처', '정책 · 기관', '정책기관'), ('자료 출처', '언론 보도', '보도'),
             ('자료 출처', '에듀테크 공식 발표와 제품 자료', '에듀테크'), ('자료 출처', 'PRAXIS 편집부 내부 자료', '내부자료')]
REF_PER_PAGE = (30, 40)


def load_refs():
    seen, refs = set(), {}
    for fn in sorted(glob.glob(os.path.join(SRC, 'refs_*.txt'))):
        for line in open(fn, encoding='utf-8'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 2 or not parts[1]:
                continue
            cat, text, url = parts[0], parts[1], (parts[2] if len(parts) > 2 else '')
            text = text.replace('"', '').replace('“', '').replace('”', '').rstrip('.')
            key = url.lower().rstrip('/') or re.sub(r'\W', '', text.lower())[:60]
            if key in seen:
                continue
            seen.add(key)
            refs.setdefault(cat, []).append((text, url))
    return refs


def refs_pages():
    refs = load_refs()
    items = []
    for part, head, cat in REF_ORDER:
        lst = sorted(refs.get(cat, []), key=lambda r: r[0].lower())
        if not lst:
            continue
        items.append(('part', part, head))
        for text, url in lst:
            short = re.sub(r'^https?://(www\.)?', '', url)
            link = f' · <a href="{url}">{short}</a>' if url else ''
            items.append(('ref', text + link, cat))
    pages, cur, cap, n = [], [], REF_PER_PAGE[0], 0
    for it in items:
        cur.append(it)
        if it[0] == 'ref':
            n += 1
        if len([c for c in cur if c[0] == 'ref']) >= cap:
            pages.append(cur); cur = []; cap = REF_PER_PAGE[1]
    if cur:
        pages.append(cur)
    out, num, shown_parts = [], 0, set()
    for i, pg in enumerate(pages):
        body = []
        for it in pg:
            if it[0] == 'part':
                if it[1] not in shown_parts:
                    body.append(f'<h4 class="refpart">{it[1]}</h4>')
                    shown_parts.add(it[1])
                body.append(f'<h5>{it[2]}</h5>')
            else:
                num += 1
                body.append(f'<p class="ref"><span class="rn">{num}</span><span>{it[1]}</span></p>')
        sid = 'p-sources' if i == 0 else f'p-sources{i + 1}'
        toc = ' data-toc="참고문헌과 자료 출처|이번 호가 인용한 {{nrefs}}건"' if i == 0 else ''
        head = ('<div class="kicker">참고문헌과 자료 출처<span class="sep">/</span>REFERENCES AND SOURCES</div>'
                '<h1 class="headline s">이번 호가 인용한 자료</h1>'
                '<p class="note">본문의 짧은 출처 표기에 대응하는 전체 목록이다 학술 논문은 참고문헌으로 정책 보도 에듀테크 발표와 편집부 내부 자료는 자료 출처로 나누었다 URL은 원문 확인 당시의 주소다</p>') if i == 0 else '<div class="cont from">← {{prev}}면에서 계속</div>'
        out.append(f'<section class="page" data-sec="REFERENCES" data-title="참고문헌과 자료 출처" id="{sid}"{toc}>{head}'
                   f'<div class="cols-2 refs2">{"".join(body)}</div></section>')
    return '\n'.join(out).replace('{{nrefs}}', str(num))


def load_pages(only=None):
    files = source_files(only)
    chunks = []
    for f in files:
        chunks.append(open(f, encoding='utf-8').read())
        if os.path.basename(f).startswith('p18') and not only:
            chunks.append(refs_pages())
    if only and 'refs' in sys.argv:
        chunks.append(refs_pages())
    html = ''.join(chunks)
    html = html.replace('Heurēsis', 'PRAXIS').replace('HEURĒSIS', 'PRAXIS')
    # 가독성 하한 · 6.5pt 미만 글자 크기는 6.6pt로 올린다
    html = re.sub(r'font-size:\s*(?:[1-5](?:\.\d+)?|6(?:\.[0-4]\d*)?)pt', 'font-size:6.6pt', html)
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('section', class_='page')
    for i, sec in enumerate(pages, 1):
        sec['data-n'] = str(i)
        if sec.get('data-bare'):
            continue
        even = i % 2 == 0
        cls = sec.get('class', [])
        if even and 'even' not in cls:
            cls.append('even')
        if not even and 'even' in cls:
            cls.remove('even')
        sec['class'] = cls
        brand = 'PRAXIS · VOL 01 · 2026 09'
        s = sec.get('data-sec', '')
        left, right = (f'<b>{s}</b>', brand) if even else (brand, f'<b>{s}</b>')
        rh = BeautifulSoup(f'<div class="runhead"><span>{left}</span><span>{right}</span></div>', 'html.parser')
        fo = BeautifulSoup(f'<div class="folio"><span class="n">{i:02d}</span>'
                           f'<span>PRAXIS 창간특집호 · {sec.get("data-title", "")}</span></div>', 'html.parser')
        sec.insert(0, rh)
        sec.append(fo)
    return pages


def page(title, head, body, body_cls=''):
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><meta name="description" content="{DESC}">'
            f'{head}</head><body class="{body_cls}">{body}</body></html>')


def main():
    os.makedirs(BUILD, exist_ok=True)
    css = open(os.path.join(SRC, 'praxis.css'), encoding='utf-8').read()
    only = [a for a in sys.argv[1:] if a.endswith('.html')]
    pages = load_pages(only)
    sentence_gaps(pages)
    pages_html = resolve_tokens(None, pages)
    toc = build_toc(pages)
    half = (len(toc) + 1) // 2
    pages_html = pages_html.replace('<!--TOC1-->', ''.join(toc[:half])).replace('<!--TOC2-->', ''.join(toc[half:]))
    pages_html = pages_html.replace('{{npages}}', str(len(pages)))
    pages_html = number_figures(pages_html)
    m = re.search(r'이번 호가 인용한 (\d+)건', pages_html)
    pages_html = pages_html.replace('{{nrefs}}', m.group(1) if m else '')
    print(f'pages: {len(pages)}')
    if only:
        pv = 'preview_' + os.path.splitext(os.path.basename(only[0]))[0] + '.html'
        with open(os.path.join(BUILD, pv), 'w', encoding='utf-8') as f:
            f.write(page('preview', f'<style>{css}</style>', pages_html))
        print(f'preview written: _build/{pv}')
        style_check(pages_html)
        return

    # 1 print
    with open(os.path.join(BUILD, 'print.html'), 'w', encoding='utf-8') as f:
        f.write(page(TITLE, f'<style>{css}</style>', pages_html))

    # 2 web edition
    toc = [(p['data-n'], p.get('data-title')) for p in pages]
    seen, nav = set(), []
    for n, t in toc:
        if t not in seen and t not in ('표지', '뒤표지'):
            seen.add(t)
            nav.append(f'<a href="#{pages[int(n) - 1]["id"]}">{t}</a>')
    bar = (f'<header class="web-bar"><span class="brand">{BOOK_ICON}PRAXIS</span>'
           f'<nav><a class="keep" href="#p-contents">차례</a>{"".join(nav[1:6])}'
           f'<a class="keep" href="{NAME}_ebook.html">e-book으로 보기</a></nav></header>')
    web_css = css + '\nhtml{scroll-behavior:smooth}\n'
    with open(os.path.join(OUT, f'{NAME}.html'), 'w', encoding='utf-8') as f:
        f.write(page(TITLE + ' · 웹판', FONTS + f'<style>{web_css}</style>', bar + pages_html, 'web'))

    # 3 e-book
    viewer = open(os.path.join(SRC, 'ebook_viewer.html'), encoding='utf-8').read()
    toc_items = []
    seen = set()
    for n, t in toc:
        if t not in seen:
            seen.add(t)
            toc_items.append(f'<li><button data-go="{n}"><span>{int(n):02d}</span>{t}</button></li>')
    ebook = (viewer.replace('/*__CSS__*/', css)
             .replace('<!--__PAGES__-->', pages_html)
             .replace('<!--__TOC__-->', ''.join(toc_items))
             .replace('__FONTS__', FONTS)
             .replace('__BOOK__', BOOK_ICON)
             .replace('__TITLE__', TITLE + ' · e-book')
             .replace('__DESC__', DESC)
             .replace('__WEB__', f'{NAME}.html')
             .replace('/*__FZCSS__*/', open(os.path.join(SRC, 'figzoom.css'), encoding='utf-8').read())
             .replace('/*__FZJS__*/', open(os.path.join(SRC, 'figzoom.js'), encoding='utf-8').read()))
    with open(os.path.join(OUT, f'{NAME}_ebook.html'), 'w', encoding='utf-8') as f:
        f.write(ebook)

    style_check(pages_html)


def style_check(pages_html):
    # 사용자 표기 규칙 · 본문 문장 끝 온점과 쌍따옴표 금지
    text = BeautifulSoup(pages_html, 'html.parser')
    for t in text(['style', 'script', 'svg']):
        t.decompose()
    plain = text.get_text('\n')
    bad_q = [l for l in plain.split('\n') if '"' in l or '“' in l or '”' in l]
    bad_p = [l.strip() for l in plain.split('\n') if re.search(r'[가-힣]\.(\s|$)', l)]
    print('double quotes:', len(bad_q), bad_q[:5])
    print('korean sentence periods:', len(bad_p), bad_p[:5])


if __name__ == '__main__':
    main()
