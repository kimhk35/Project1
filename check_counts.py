# DOMAINS 하위 subsection 수 (직접 문자열 카운트)
t = open('c:/upstage/script_domains.js', encoding='utf-8').read()
subs = t.count('[[')
print('DOMAINS 하위 섹션 배열 수 ([[):', subs)

# INT_REFS, DOM_REFS 개수 (인용부호로 감싸진 문자열 개수)
t2 = open('c:/upstage/script_data.js', encoding='utf-8').read()
int_block = t2.split('INT_REFS')[1].split('DOM_REFS')[0]
dom_block = t2.split('DOM_REFS')[1]
intRefs = int_block.count("',")
domRefs = dom_block.count("',")
print('INT_REFS 항목 수:', intRefs)
print('DOM_REFS 항목 수:', domRefs)
print('문헌 총합:', intRefs + domRefs)

# FRAMEWORK 항목 수
fw_block = t2.split('const FRAMEWORK')[1].split('INT_REFS')[0]
fw_count = fw_block.count('{')
print('FRAMEWORK 항목 수:', fw_count)
