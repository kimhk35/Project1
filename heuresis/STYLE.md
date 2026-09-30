# Heurēsis 조판·집필 가이드  작업자용

Heurēsis는 수학교육 연구와 교실 실천을 잇는 한국어 월간지다  창간특집호 Vol.01은 A4 약 112쪽이며 연구의 깊이와 대중지의 읽는 맛을 함께 갖춘다

## 1  파일과 도구

- 조판 스타일  `heuresis/heuresis-vol01.css`  수정하지 말 것  필요한 변형은 요소의 style 속성으로
- 그래픽  `heuresis/heuresis-art.js`  `<svg data-art="이름">`으로 호출  cover tangent contour steps eye waffle trajectories efficacy  새 차트는 인라인 SVG나 HTML div 막대로 직접 그린다
- 기존 초안  `heuresis/src/draft/*.html`  28쪽 버전  구조와 컴포넌트 예시로 참고하고 자기 섹션 초안은 확장의 출발점으로 쓴다
- 자기 섹션 파일  `heuresis/src/sections/NN-이름.html`  `.page` section 여러 개를 이어 쓴 조각
- 검사  `cd heuresis && NODE_PATH=$(npm root -g) node check.js src/sections/NN-이름.html <스크래치 PNG 폴더>`
  - OVERFLOW는 반드시 0  STYLE 위반도 0  bottom whitespace 경고는 가능한 한 없애기
  - PNG를 Read로 열어 눈으로 확인할 것  글이 잘리거나 겹치면 안 된다
- 원천 자료  `/tmp/claude-0/-home-user-Project1/f0f25d68-6cd3-5d7b-9a69-213fcfdd4f27/scratchpad/sources/`
  - `daily_2026-09-DD.txt` 30일치 수학교육 연구 데일리 브리핑
  - `clinic_weekly_vol01~03.txt` 수학클리닉 위클리 브리핑
  - `monthly_report_2026-09.txt` 9월 월말 동향 보고서
  - `mathed_signal_2026-09-28.txt` AI 디지털 교육 주간 인사이트

## 2  문체 규칙  절대 규칙

1. **쌍따옴표를 쓰지 않는다**  인용과 강조는 홑따옴표 ' ' 또는 「 」
2. **문장 끝에 온점을 쓰지 않는다**  문장과 문장 사이는 공백 두 칸으로 구분하고 단락은 `<p>`로 나눈다  숫자 소수점 DOI URL 약어 Vol.01 안의 점은 괜찮다  et al. 대신 '외'
3. 본문은 한국어  학술 용어는 필요하면 영어 병기  noticing 같은 정착된 용어는 그대로
4. 연구자 톤과 대중지 톤의 균형  장면으로 시작하고 숫자로 붙잡고 한계로 마무리한다  교사가 내일 무엇을 다르게 할지와 연구자가 무엇을 다르게 설계할지를 함께 말한다
5. 존칭 없는 평서문  -다 체

## 3  사실 규칙  절대 규칙

- 원천 자료에 있는 사실만 쓴다  표본 수 효과크기 날짜 저자 학술지를 바꾸거나 지어내지 않는다  소속 기관도 자료에 없으면 쓰지 않는다
- 실존 인물의 발언을 지어내지 않는다  인터뷰를 꾸미지 않는다  pull quote는 '편집부 해석' 또는 '○○ 연구의 요지'로 출처를 밝힌다
- 가상의 교실 장면을 쓸 때는 가상 사례임을 작게 표시한다
- 근거 수준 배지를 붙인다  `<span class="ev e1"><i></i>실증</span>` 동료심사 실험·종단·대규모  `e2` 종합 체계적 고찰·메타·척도  `e3` 질적·개념·프리프린트  `e4` 현장 운영자료·보도·제품
- 인과를 과장하지 않는다  관찰연구는 관련으로  프리프린트는 후속 검증 필요로
- PISA 2025 성취 하락처럼 원문에서 확인되지 않은 주장은 쓰지 않는다
- 본문에서 인용한 모든 자료를 `heuresis/refs/NN-이름.tsv`에 한 줄씩 적는다  형식  `저자\t연도\t제목\t출처(학술지·기관)\tDOI 또는 URL\t원천 브리핑 파일명`  맨 뒤 통합 참고문헌과 자료 출처는 편집장이 이것으로 만든다  섹션 안에 참고문헌 쪽을 따로 만들지 말 것  섹션 끝의 Further Reading 상자는 괜찮다

## 4  쪽 구조

```html
<section class="page" data-sec="cover">            <!-- 특집이면 class="page clinic" 또는 "page teacher" -->
  <div class="rh"><span><b>Heurēsis</b> · Cover Story</span><span class="sec">정답 이후의 수학 · 2/14</span></div>
  <div class="inner">
    ... 내용 ...
  </div>
  <div class="folio"><span class="n">00</span><span>COVER STORY · 정답 이후의 수학</span></div>
</section>
```

- 쪽 번호 `.folio .n`은 자동으로 채워지므로 00으로 둔다
- 섹션 첫 쪽의 section에는 `id="sec-이름"`을 붙인다  차례가 이 id로 쪽 번호를 찾는다  그 밖의 id는 `이름-의미` 식으로 섹션 접두어를 붙여 충돌을 피한다
- 오프너 쪽은 `.opener-band` + `.opener-text` 패턴  `.inner`의 top을 밴드 아래로 내린다  초안 참고
- 쪽마다 고정 높이다  내용이 넘치면 잘리고 모자라면 빈다  check.js로 반복 확인하며 문단을 옮기거나 상자·표·도식을 넣어 채운다  한 쪽이 꽉 차도록
- 레이아웃을 단조롭게 하지 말 것  2단 본문 3단 카드 표 통계 타일 flow 도식 pull quote 사이드바 SVG 차트를 섞는다  문단으로만 된 쪽이 연속 2쪽을 넘지 않게
- 여러 쪽에 걸친 기사는 `.cont` 로 다음 쪽에서 계속 → 을 표시하고 러닝헤드에 n/N을 적는다

## 5  컴포넌트 요약

kicker  h1.title  h2.head  h3(.no)  .dek  .byline  .body(.cols2 .cols3)  p.lead(드롭캡)  em.hl  .pq  .box(.navy .teal .ochre .line)  .bt  .stats/.stat(.v .l .s)  table.t(td.k)  .ev  .cards/.card(.meta .num h4 .src p .take)  .flow/.st(.hot)/.ar  .checklist  .lab-app  .verdict .dots  .rule  .spacer  .cont  .sp-badge
