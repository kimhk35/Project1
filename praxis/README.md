# PRAXIS 창간특집호

연구와 실천이 만나는 교육 AI 잡지 PRAXIS 제1권 제1호 창간특집호 (2026년 10월 · 편집장 McKay)
2026년 9월 교육 AI 연구 브리핑과 EdTech Radar 자료를 바탕으로 만들었다

## 결과물

| 파일 | 설명 |
| --- | --- |
| `PRAXIS_Vol01_창간특집호.pdf` | A4 인쇄판 |
| `PRAXIS_Vol01_창간특집호.docx` | 편집 가능한 Word 흐름형 문서 (도표는 이미지) |
| `PRAXIS_Vol01_창간특집호.html` | 웹판 · 데스크톱은 지면 보기 모바일은 반응형 흐름 |
| `PRAXIS_Vol01_창간특집호_ebook.html` | HTML e-book · 펼침면 넘김 차례 서랍 키보드와 스와이프 |

## 소스 구조 (`src/`)

- `p[0-9]*.html` 지면 조각 · 파일 이름 순서대로 합쳐진다 · 한 `<section class="page">` 가 A4 한 면
- `praxis.css` 공용 스타일 · `ebook_viewer.html` e-book 뷰어 틀
- `refs_*.txt` 섹션별 참고문헌 · 빌드가 모아 맨 뒤 참고문헌과 자료 출처 면을 만든다
- `STYLE.md` 필자용 작성 가이드 (표기 규칙 · 컴포넌트 · 검증 절차)
- 쪽번호 러닝헤드 차례 면 참조(`{{pg:id}}`) 계속 표시(`{{next}}` `{{prev}}`)는 빌드 때 자동으로 채워진다

## 빌드

```bash
cd src
python3 build.py                                        # print.html · 웹판 · e-book + 표기 규칙 검사
NODE_PATH=$(npm root -g) node render.js check           # 지면 넘침 검사
NODE_PATH=$(npm root -g) node render.js charts          # DOCX용 도표 이미지
NODE_PATH=$(npm root -g) node render.js pdf             # PDF
python3 pdf_optimize.py                                 # PDF 재압축과 문서 정보
python3 docx_build.py                                   # DOCX
```

필요 도구 · Python 3 (beautifulsoup4 python-docx pikepdf) · Node.js와 Playwright Chromium · 글꼴 Noto Serif KR Noto Sans KR Playfair Display
