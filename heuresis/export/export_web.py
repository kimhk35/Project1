"""단일 파일 HTML과 HTML e-book을 만든다  폰트는 실제로 쓰인 글자만 남겨 woff2로 파일 안에 넣는다
사용법  python3 export/export_web.py   (먼저 build.py로 heuresis-vol01.html을 만든다)
"""
import base64, io, os, re, sys
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(HERE, 'dist')
FONT_DIR = os.environ.get('FONT_DIR', '/root/.fonts/praxis')

FONTS = [  # (family, weight, style, file)
    ('Noto Serif KR', 400, 'normal', 'f1.ttf'), ('Noto Serif KR', 600, 'normal', 'f2.ttf'), ('Noto Serif KR', 900, 'normal', 'f3.ttf'),
    ('Noto Sans KR', 300, 'normal', 'f4.ttf'), ('Noto Sans KR', 400, 'normal', 'f5.ttf'), ('Noto Sans KR', 500, 'normal', 'f6.ttf'),
    ('Noto Sans KR', 700, 'normal', 'f7.ttf'), ('Noto Sans KR', 900, 'normal', 'f8.ttf'),
    ('Playfair Display', 400, 'normal', 'f11.ttf'), ('Playfair Display', 700, 'normal', 'f12.ttf'), ('Playfair Display', 900, 'normal', 'f13.ttf'),
    ('Playfair Display', 400, 'italic', 'f9.ttf'), ('Playfair Display', 700, 'italic', 'f10.ttf'),
    ('IBM Plex Mono', 400, 'normal', 'f14.ttf'), ('IBM Plex Mono', 500, 'normal', 'f15.ttf'),
]


def font_faces(text):
    chars = set(text) | set(chr(c) for c in range(0x20, 0x250)) | set('–—‘’“”…·•→←↑↓×−≤≥±√∑πβηα²³₀₁₂「」『』①②③④⑤⑥⑦⑧⑨⑩●○◐□■★☆')
    unicodes = sorted(ord(c) for c in chars if ord(c) > 0x1f)
    css = []
    for fam, wt, st, fn in FONTS:
        font = TTFont(os.path.join(FONT_DIR, fn))
        opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['*']; opts.name_IDs = ['*']
        sub = subset.Subsetter(opts); sub.populate(unicodes=unicodes); sub.subset(font)
        buf = io.BytesIO(); font.flavor = 'woff2'; font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:{st};font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return '\n'.join(css)


def standalone(html, css, js, faces, extra_head='', extra_body=''):
    head_end = html.index('</head>')
    head = html[:head_end]
    head = re.sub(r'<link[^>]+fonts\.googleapis[^>]*>\s*', '', head)
    head = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', head)
    head = re.sub(r'<link rel="stylesheet" href="heuresis-vol01.css">', '', head)
    body = html[head_end:]
    body = body.replace('<script src="heuresis-art.js"></script>', f'<script>\n{js}\n</script>{extra_body}')
    return head + f'<style>\n{faces}\n{css}\n</style>\n{extra_head}' + body


def main():
    src = os.path.join(HERE, 'heuresis-vol01.html')
    html = open(src, encoding='utf-8').read()
    css = open(os.path.join(HERE, 'heuresis-vol01.css'), encoding='utf-8').read()
    js = open(os.path.join(HERE, 'heuresis-art.js'), encoding='utf-8').read()
    faces = font_faces(re.sub(r'<[^>]+>', ' ', html) + js)
    os.makedirs(DIST, exist_ok=True)

    web = standalone(html, css, js, faces, extra_head='<style>@media screen{body{padding:8mm 0}}</style>\n')
    open(os.path.join(DIST, 'Heuresis_Vol01_창간특집호.html'), 'w', encoding='utf-8').write(web)

    viewer_css = open(os.path.join(HERE, 'export', 'ebook.css'), encoding='utf-8').read()
    viewer_js = open(os.path.join(HERE, 'export', 'ebook.js'), encoding='utf-8').read()
    shell = open(os.path.join(HERE, 'export', 'ebook_shell.html'), encoding='utf-8').read()
    book = standalone(html, css, js, faces, extra_head=f'<style>\n{viewer_css}\n</style>\n',
                      extra_body=f'\n{shell}\n<script>\n{viewer_js}\n</script>')
    book = book.replace('<body>', '<body class="ebook">', 1).replace('<title>Heurēsis Vol.01 창간특집호</title>', '<title>Heurēsis Vol.01 창간특집호 · e-book</title>')
    open(os.path.join(DIST, 'Heuresis_Vol01_창간특집호_ebook.html'), 'w', encoding='utf-8').write(book)
    for n in ('Heuresis_Vol01_창간특집호.html', 'Heuresis_Vol01_창간특집호_ebook.html'):
        print(n, round(os.path.getsize(os.path.join(DIST, n)) / 1e6, 1), 'MB')


if __name__ == '__main__':
    main()
