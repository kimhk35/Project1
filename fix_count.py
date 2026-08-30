path = 'c:/upstage/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('data-count="28"', 'data-count="26"')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('교체 완료')
