# 고천중학교 학생자치 활성화 개선안

2027학년도 학생자치 개선안  대의원회와 라온하제의 역할 정립을 중심으로 (14학급, 대의원회 31명, 라온하제 27명 내외, 겸직 7명)

## 결과물 (out/)

| 형식 | 파일 | 용도 |
|---|---|---|
| HWPX | 고천중_학생자치_개선안.hwpx | 한글 문서 편집과 결재용 |
| DOCX | 고천중_학생자치_개선안.docx | MS Word 편집용 |
| PDF | 고천중_학생자치_개선안.pdf | 배포·인쇄용 |
| HTML | 고천중_학생자치_개선안.html | 웹 열람·공유용 |

## 구성

- 표지, 목차와 핵심 요약
- Ⅰ 개선의 배경과 방향
- Ⅱ 대의원회와 라온하제의 역할 구분
- Ⅲ 두 조직에 함께 속한 학생회장단
- Ⅳ 조직 예시 (대의원회, 라온하제 조직도)
- Ⅴ 통합 집행부 회의 : 자치운영위원회
- Ⅵ 월간 자치 순환 체계
- Ⅶ 학급자치 시간의 교육과정 정례화
- Ⅷ 그 밖의 지원 방안
- Ⅸ 추진 일정과 기대 효과
- 부록 학생자치회 규칙 개정 조문 예시

## 다시 만들기 (build/)

모든 형식은 `build/content.py` 하나를 원본으로 삼는다. 내용을 고치면 아래 순서로 다시 생성한다.

```bash
cd gocheon-autonomy
python3 build/figs.py            # 도식 SVG
python3 build/build_html.py      # HTML과 표지 원본
python3 build/render.py          # 도식 PNG와 표지 PNG
python3 build/build_html.py pdf  # PDF
python3 build/build_docx.py      # DOCX
python3 build/build_hwpx.py      # HWPX
```

필요 도구  Python 3, playwright(Chromium), python-docx, PyMuPDF, lxml, Pillow, Pretendard와 Noto Serif KR 글꼴

문서 표기 원칙

- 쌍따옴표를 쓰지 않고 인용은 「 」로 표기한다.
- 문장 끝에는 반드시 온점을, 의문문에는 물음표를 쓴다. content.py의 punctuate()와 figs.py의 punct()가 자동으로 붙인다.
- 가운데 점은 공식 명칭(자율·자치활동, 초·중등교육법) 외에는 쓰지 않는다.
