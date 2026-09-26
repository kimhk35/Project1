---
name: column-cover
description: AI Insight Column 칼럼 원고(PDF DOCX)에 시리즈 테마 표지를 만들어 원고 앞에 붙이고 zip으로 돌려준다 사용자가 칼럼 파일을 올리며 표지를 부탁하면 사용
---

# AI Insight Column 표지 만들기

사용자가 칼럼 원고를 올리고 표지를 부탁하면 이 절차를 따른다 도구는 `column-covers/`에 있다

## 시리즈와 번호 규칙 (바꾸지 않는다)

| 시리즈 | 키 | 번호 표기 | 테마 | 알아보는 법 |
|---|---|---|---|---|
| 본연재 〈에이전틱 사고 · 온톨로지〉 | main | 00 01 02 … (00은 PROLOGUE) | 미색 종이 + 청록 | 본문 첫머리 `연재 〈에이전틱 사고 · 온톨로지〉 제N회` |
| Spin-Off | spinoff | S1 S2 … | 먹색 + 주황 | 제목이나 파일명에 Spin-Off |
| Policy Lens | policy | PL1 PL2 … | 크림 + 청색 | `AI Insight Column – Policy Lens` |
| 번외편 | special | EX1 EX2 … | 남색 + 보라 청록 그라데이션 | 번외편 |

- 본연재 번호는 원고에 적힌 제N회를 그대로 쓴다 나머지는 원고에 번호가 있으면 그 번호 없으면 `python column-covers/build.py next`가 알려 주는 다음 번호
- 테마 색 레이아웃 글꼴은 `series.py` `build.py`에 고정되어 있다 새 칼럼에서 바꾸지 않는다
- 시리즈를 알 수 없거나 새 시리즈로 보이면 만들기 전에 사용자에게 묻는다

## 표지 문구 규칙

- 사용자 선호 쌍따옴표와 온점을 쓰지 않는다 인용은 ‘ ’ 또는 「 」 제목 끝 온점은 뺀다
- 제목은 원고 제목 그대로 2~3줄로 끊는다 (한 줄 최대 13자 안팎)
- meta 두 항목 본연재는 `N부`, `부 제목` 부제 한 줄 태그 3~4개는 원고 핵심 개념에서 뽑는다
- 필자 이름은 사용자가 알려 주기 전에는 넣지 않는다

## 작업 순서

1. 원고 전체를 읽고 시리즈 번호 제목 부제 핵심 장면을 정한다
2. `column-covers/arts.py` 끝에 `art_<이름>(c)` 함수를 새로 만든다 600x420 viewBox SVG 문자열 반환 원고의 핵심 장면이나 개념을 한눈에 보여 주는 일러스트로 기존 함수들의 선 굵기 라벨 크기(`class="lbl"`) 색 사용 방식을 따른다 한글 라벨에 `mono` 클래스는 쓰지 않는다
3. `column-covers/registry.py`에 항목을 추가한다 (`src`는 업로드 파일을 옮긴 이름과 같게)
4. 업로드 파일을 스크래치 폴더에 알아보기 쉬운 이름으로 복사하고 빌드
   ```
   pip install pymupdf python-docx playwright   # 없으면
   python column-covers/build.py build --src <원고폴더> --out <결과폴더>
   ```
   글꼴은 처음 실행 때 Google Fonts에서 `column-covers/.fonts`로 받는다 Chromium은 `/opt/pw-browsers`의 것을 쓴다
5. `_work/<id>.png`를 직접 열어 보고 겹침 넘침 어색한 그림을 고친 뒤 다시 빌드한다
6. zip을 사용자에게 보내고 registry arts 변경을 커밋 푸시한다 (원고 파일과 결과물은 커밋하지 않는다)

## 결과물 형식

- `AI_Insight_Column_표지/칼럼_표지포함/` 원본 이름 형식 그대로 맨 앞에 표지 한 장
  - PDF 원고 첫 페이지 크기에 맞춰 표지를 앞에 붙인다
  - DOCX 여백 0짜리 첫 구역에 표지 이미지를 한 쪽 가득 넣는다 본문 서식은 건드리지 않는다
- `AI_Insight_Column_표지/표지_이미지/` 고해상도 PNG
- 원고에 이미 자체 표지가 있으면 지우지 않고 새 표지를 앞에 붙인 뒤 사용자에게 알린다
