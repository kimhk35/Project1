"""refs/*.tsv를 모아 권말 참고문헌과 자료 출처 쪽(src/sections/99-back.html)을 만든다
사용법  python3 build_refs.py [쪽당 항목 수]"""
import glob, html, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
PER_PAGE = int(sys.argv[1]) if len(sys.argv) > 1 else 42

SECTION = {'10-month': 'The Month', '20-cover': 'Cover Story', '30-anxiety': 'Feature 1', '40-data': 'Feature 2',
           '50-spotlight': 'Spotlight', '60-edtech': 'EdTech Lab', '70-clinic': 'Math Clinic', '80-teacher': "Teacher's Eye",
           '90-agenda': 'Agenda', '95-glossary': 'Glossary'}

def key(title, doi):
    d = (doi or '').lower()
    m = re.search(r'10\.\d{4,9}/\S+', d)
    if m:
        return m.group(0).rstrip('.')
    return re.sub(r'\W+', '', title.lower())[:60]

entries = {}
for f in sorted(glob.glob(os.path.join(here, 'refs', '*.tsv'))):
    sec = SECTION.get(os.path.basename(f)[:-4], '')
    for line in open(f, encoding='utf-8'):
        cols = [c.strip() for c in line.rstrip('\n').split('\t')]
        if len(cols) < 3 or not cols[0] or cols[0].startswith('#') or cols[0] in ('저자', 'author'):
            continue
        cols += [''] * (6 - len(cols))
        author, year, title, venue, link, src = cols[:6]
        k = key(title, link)
        e = entries.setdefault(k, dict(author=author, year=year, title=title, venue=venue, link=link, src=set(), secs=[]))
        if src:
            e['src'].update(s.strip() for s in re.split(r'[,;/ ]+', src) if s.strip())
        if sec and sec not in e['secs']:
            e['secs'].append(sec)
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
chunks = [allitems[i:i + PER_PAGE] for i in range(0, len(allitems), PER_PAGE)]
total = len(chunks) + 1
out = []
for i, ch in enumerate(chunks):
    out.append(page(head1 if i == 0 else '    <div class="kicker" style="margin-bottom:3mm">References · 계속</div>', ch, i + 1, total, 'sec-refs' if i == 0 else None))

sources = open(os.path.join(here, 'src', 'sources_page.html'), encoding='utf-8').read().replace('{N}', str(total))
out.append(sources)
open(os.path.join(here, 'src', 'sections', '99-back.html'), 'w', encoding='utf-8').write('\n'.join(out))
print(f'{len(papers)} papers, {len(field)} field items, {total} pages')
