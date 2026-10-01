"""refs/*.tsv를 모아 권말 참고문헌과 자료 출처 쪽(src/sections/99-back.html)을 만든다
사용법  python3 build_refs.py  쪽 나눔은 paginate_refs.js가 실제 렌더링으로 정한다"""
import glob, html, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))

SECTION = {'10-month': 'The Month', '20-cover': 'Cover Story', '30-anxiety': 'Feature 1', '40-data': 'Feature 2',
           '50-spotlight': 'Spotlight', '60-edtech': 'EdTech Lab', '70-clinic': 'Math Clinic', '80-teacher': "Teacher's Eye",
           '90-agenda': 'Agenda', '95-glossary': 'Glossary'}

def key(author, year, title, venue, doi):
    d = (doi or '').lower()
    m = re.search(r'10\.\d{4,9}/\S+', d)
    if m:
        return m.group(0).rstrip('.')
    chunk = re.split(r'\s*(?:외|&|·|;| and )\s*', author.strip())[0]
    first = (chunk.split(',')[0] if ',' in chunk else (chunk.split() or [''])[-1]).lower()
    return first + year + re.sub(r'\W+', '', venue.lower())[:25]

def hangul(t):
    return bool(re.search('[가-힣]', t))

entries = {}
for f in sorted(glob.glob(os.path.join(here, 'refs', '*.tsv'))):
    sec = SECTION.get(os.path.basename(f)[:-4], '')
    for line in open(f, encoding='utf-8'):
        cols = [c.strip() for c in line.rstrip('\n').split('\t')]
        if len(cols) < 3 or not cols[0] or cols[0].startswith('#') or cols[0] in ('저자', 'author'):
            continue
        cols += [''] * (6 - len(cols))
        author, year, title, venue, link, src = cols[:6]
        if not re.search(r'10\.\d{4}|https?://|www\.', link):
            link = ''
        if re.search(r'브리핑|월말 동향|동향 및 연구주제|MathEd Signal', author + title):
            continue  # 편집에 쓴 원천 자료는 자료 출처 쪽에 따로 싣는다
        k = key(author, year, title, venue, link)
        e = entries.setdefault(k, dict(author=author, year=year, title=title, venue=venue, link=link, src=set(), secs=[]))
        if src:
            e['src'].update(s.strip() for s in re.split(r'[,;/ ]+', src) if s.strip())
        if sec and sec not in e['secs']:
            e['secs'].append(sec)
        if hangul(e['title']) and title and not hangul(title):
            e['title'] = title
        for fld, v in (('venue', venue), ('link', link), ('year', year)):
            if not e[fld] and v:
                e[fld] = v

def is_field(e):
    t = (e['venue'] + e['title'] + e['link']).lower()
    return not re.search(r'10\.\d{4}', t) and not re.search(r'arxiv|nber|journal|zdm|education|학회|학술|논문|review|psychology|kci|kiss', t)

papers = sorted((e for e in entries.values() if not is_field(e)), key=lambda e: e['author'].lower())
field = sorted((e for e in entries.values() if is_field(e)), key=lambda e: e['author'].lower())

def fmt(e):
    esc = html.escape
    link = e['link']
    if link.lower().startswith('10.'):
        link = 'doi ' + link
    secs = ' · '.join(e['secs'])
    parts = [f"<b>{esc(e['author'])}</b> ({esc(e['year'] or 'n.d')}) {esc(e['title'])}"]
    if e['venue']: parts.append(esc(e['venue']))
    if link: parts.append(f'<span style="word-break:break-all">{esc(link)}</span>')
    tail = f' <span class="muted">[{esc(secs)}]</span>' if secs else ''
    return '<p>' + '  '.join(parts) + tail + '</p>'

def page(title_html, items, n, total, sid=None):
    idattr = f' id="{sid}"' if sid else ''
    return f'''<section class="page"{idattr}>
  <div class="rh"><span><b>Heurēsis</b> · Vol.01</span><span class="sec">References &amp; Sources · {n}/{total}</span></div>
  <div class="inner">
{title_html}
    <div class="refs cols3">
{''.join(items)}
    </div>
  </div>
  <div class="folio"><span class="n">00</span><span>REFERENCES &amp; SOURCES</span></div>
</section>
'''

head1 = '''    <div class="kicker">References &amp; Sources</div>
    <h1 class="title" style="font-size:26pt;margin-bottom:2mm">참고문헌과 자료 출처</h1>
    <div class="dek" style="font-size:9pt;margin-bottom:4mm">이번 호에서 인용한 연구 문헌을 저자순으로 정리했다  대괄호 안은 해당 문헌이 등장한 섹션이다  학술 문헌 뒤에는 기관 자료 보도 제품 정보 같은 현장 자료를 따로 모았고 마지막 쪽에 편집에 사용한 원천 브리핑을 밝혔다  DOI가 없는 항목은 원문 확인 시 제목으로 검색하기 바란다</div>'''

items = [fmt(e) for e in papers]
field_items = ['<p style="text-indent:0;padding-left:0;margin-top:1mm"><b style="font-family:var(--mono);color:var(--red);letter-spacing:.1em">현장·정책·제품 자료</b></p>'] + [fmt(e) for e in field]
allitems = items + field_items
import json, subprocess
sources = open(os.path.join(here, 'src', 'sources_page.html'), encoding='utf-8').read().replace('{PAPERS}', str(len(papers))).replace('{FIELD}', str(len(field)))
json.dump({'head': head1, 'items': allitems, 'sources': sources}, open(os.path.join(here, 'src', 'refs_items.json'), 'w', encoding='utf-8'), ensure_ascii=False)
subprocess.run(['node', os.path.join(here, 'paginate_refs.js')], check=True, env={**os.environ, 'NODE_PATH': subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()})
print(f'{len(papers)} papers, {len(field)} field items')
