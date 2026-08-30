# 데이터 일관성 및 렌더링 로직 검증
import re, json

base = 'c:/upstage'

# 데이터 로드
data_code = open(f'{base}/script_data.js', encoding='utf-8').read()
domains_code = open(f'{base}/script_domains.js', encoding='utf-8').read()


def extract_array(code, var_name):
    """const VAR_NAME = <array_or_object>; 패턴에서 전체를 추출해 파이썬 객체로 변환.

    중첩된 [], {} 를 올바르게 처리하기 위해 괄호 깊이를 추적한다.
    """
    # const VAR_NAME =  찾기
    header = rf'const\s+{re.escape(var_name)}\s*=\s*'
    start = re.search(header, code)
    if not start:
        return None
    pos = start.end()

    # 첫 문자 확인: [ (배열) 또는 { (객체)
    first = code[pos]
    if first == '[':
        opener, closer = '[', ']'
    elif first == '{':
        opener, closer = '{', '}'
    else:
        return None

    depth = 0
    in_string = False
    string_char = None
    escape = False
    end = pos
    for i in range(pos, len(code)):
        ch = code[i]
        if escape:
            escape = False
            continue
        if in_string:
            if ch == '\\':
                escape = True
            elif ch == string_char:
                in_string = False
            continue
        if ch in ('"', "'"):
            in_string = True
            string_char = ch
            continue
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    raw = code[pos:end]
    # 세미콜론 제거 (마지막 문자)
    if raw.endswith(';'):
        raw = raw[:-1]
    # JS 싱글쿼트 → JSON 더블쿼트 치환 (문자열 내부만)
    # 간단 치환: 문자열 밖은 신경 쓰지 않고 전체 치환 ( 현행 데이터는 문자열만 싱글쿼트 사용 )
    fixed = raw.replace("'", '"')
    return json.loads(fixed)


FRAMEWORK = extract_array(data_code, 'FRAMEWORK')
INT_REFS = extract_array(data_code, 'INT_REFS')
DOM_REFS = extract_array(data_code, 'DOM_REFS')
DOMAINS = extract_array(domains_code, 'DOMAINS')

print('=== 데이터 검증 ===')
print(f'FRAMEWORK: {len(FRAMEWORK)}개 항목')
for i, f in enumerate(FRAMEWORK, 1):
    print(f'  {i}. {f["order"]} {f["title"]} — 태그 {len(f["tags"])}개')

print(f'\nDOMAINS: {len(DOMAINS)}개 영역')
total_sub = 0
for d in DOMAINS:
    sub_count = len(d[4])
    total_sub += sub_count
    print(f'  {d[0]} {d[2]} — 하위 {sub_count}개')
print(f'총 하위 주제: {total_sub}개')

print(f'\n참고문헌: 국제 {len(INT_REFS)}개 + 국내 {len(DOM_REFS)}개 = {len(INT_REFS)+len(DOM_REFS)}개')

# HTML data-count 검증
html = open(f'{base}/index.html', encoding='utf-8').read()
dc7 = len(re.findall(r'data-count="7"', html))
dc26 = len(re.findall(r'data-count="26"', html))
dc32 = len(re.findall(r'data-count="32"', html))

print('\n=== HTML data-count 검증 ===')
print(f'대분류 영역 data-count="7": {dc7}개 발견 → {"OK" if dc7 > 0 else "MISSING"} (실제 {len(FRAMEWORK)}개)')
print(f'중분류 주제 data-count="26": {dc26}개 발견 → {"OK" if dc26 > 0 else "MISSING"} (실제 {total_sub}개)')
print(f'주요 문헌 data-count="32": {dc32}개 발견 → {"OK" if dc32 > 0 else "MISSING"} (실제 {len(INT_REFS)+len(DOM_REFS)}개)')

# 스크립트 로드 순서 검증
scripts = re.findall(r'<script src="([^"]+)"', html)
print(f'\n=== 스크립트 로드 순서 ===')
for i, s in enumerate(scripts, 1):
    print(f'  {i}. {s}')

# SVG 렌더링 로직 검증 (script_render.js)
render_code = open(f'{base}/script_render.js', encoding='utf-8').read()
svg_bug_fixed = 'N[a]' in render_code and 'N[b]' in render_code
print(f'\n=== 버그 수정 검증 ===')
print(f'SVG N[a]/N[b] 수정: {"OK" if svg_bug_fixed else "NOT FIXED"}')

util_code = open(f'{base}/script_util.js', encoding='utf-8').read()
reveal_added = '.reveal' in util_code
print(f'스크롤 리빌 .reveal 클래스 추가: {"OK" if reveal_added else "NOT FIXED"}')

print('\n=== 최종 판정 ===')
all_ok = (dc7 > 0 and dc26 > 0 and dc32 > 0 and svg_bug_fixed and reveal_added and
          len(scripts) == 4 and scripts[0] == 'script_data.js' and
          scripts[1] == 'script_domains.js' and scripts[2] == 'script_render.js' and
          scripts[3] == 'script_util.js')
print('모든 검증 통과!' if all_ok else '일부 검증 실패 — 상세 확인 필요')
