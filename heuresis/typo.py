"""조판 직전 가독성 보정  원고는 그대로 두고 빌드 결과에만 적용한다

1  문장 사이의 공백 두 칸을 반각 공백(U+2002) 하나로 바꿔 온점 없이도 문장 경계가 보이게 한다
2  인라인으로 지정된 6.6pt 미만 글자는 0.4pt 키워 작은 메타 정보도 읽히게 한다
"""
import re

SENT_GAP = ' '
_tag = re.compile(r'(<[^>]+>)')
_raw = re.compile(r'<(script|style)\b.*?</\1>', re.S | re.I)


def _texts(html, fn):
    out, pos = [], 0
    for m in _raw.finditer(html):
        out.append(_apply(html[pos:m.start()], fn))
        out.append(m.group(0))
        pos = m.end()
    out.append(_apply(html[pos:], fn))
    return ''.join(out)


def _apply(chunk, fn):
    return ''.join(p if p.startswith('<') else fn(p) for p in _tag.split(chunk))


def sentence_gaps(text):
    return re.sub(r'(?<=\S) {2,}(?=\S)', SENT_GAP, text)


def bump_small(html):
    def up(m):
        v = float(m.group(1))
        return f'font-size:{v + 0.4:.1f}pt' if v < 6.6 else m.group(0)
    return re.sub(r'font-size:(\d+(?:\.\d+)?)pt', up, html)


def polish(body):
    return bump_small(_texts(body, sentence_gaps))
