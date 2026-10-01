# PRAXIS 창간특집호 · 섹션 작성 가이드

잡지 PRAXIS(프락시스, 실천) 창간특집호 2026년 9월호 · 편집장 McKay
독자는 교사, 대학원생·연구자, 학교·교육청 정책담당자, 에듀테크 개발자다. 전문 연구지처럼 정확하고 대중지처럼 읽히게 쓴다
대상기간은 2026-09-01 ~ 2026-09-30, 자료 마감은 2026-09-30 10:29 KST다

## 1 절대 규칙 · 표기

1. **한국어 문장 끝에 온점(.)을 쓰지 않는다** 문장과 문장은 띄어쓰기로만 구분하고 문단은 새 `<p>`로 나눈다
   - 숫자의 소수점(0.64, p=.149), URL, DOI, 영문 약어 안의 점은 괜찮다
   - 저자 이니셜(M. D.)은 쓰지 말고 `Koretsky 외`처럼 쓴다
   - 목록 항목 끝에도 온점 없음
2. **쌍따옴표(" “ ”)를 절대 쓰지 않는다** 인용·제목·강조는 「 」 또는 ' ' 로 한다 (HTML 속성값의 따옴표는 당연히 괜찮다)
3. 사실을 지어내지 않는다 수치·표본·저자·날짜·결과는 소스 파일(아래 4절)에 있는 것만 쓴다 소스에 없는 수치는 쓰지 않거나 「미확인」으로 쓴다
   - 가상 사례·예시 대화·설계안은 반드시 `편집부 예시` 또는 `가상 사례`라고 명시한다
   - 인터뷰나 인물 발언을 만들어내지 않는다
4. 공급사 발표는 효과 근거가 아니다 발표와 검증을 구분해 쓴다 의학교육·대학 결과를 K-12에 곧바로 일반화하지 않는다
5. 문체는 신문·잡지 기사체 평서문 (…다 …한다) 단정 대신 근거 수준에 맞는 표현을 쓴다
6. 개인 연구 포트폴리오 언급(「사용자 연구 연결」, 「김홍겸 연구」, 「교수님」 등 소스 속 개인화 문구)은 옮기지 않는다 대신 일반 독자용 「연구 아이디어」로 바꾼다

## 2 페이지 구조

A4 고정 페이지(210×297mm)다 한 `<section class="page">`가 한 면이다
```html
<section class="page" data-sec="SPECIAL 05 · 교사의 AI 역량" data-title="교사의 AI 역량" id="p-teacher"
         data-toc="SPECIAL 05|교사의 AI 역량|판단노동을 가르치는 연수" data-toc-cls="sp">
  ...
</section>
```
- `id` 전체에서 고유 · 접두어를 섹션별로 정해 쓴다 (p-teacher, p-teacher2 …)
- `data-sec` 러닝헤드에 대문자로 표시되는 섹션명 · `data-title` 폴리오 옆 제목
- `data-toc` 는 **섹션 첫 면에만** 붙인다 형식 `분류|제목|부제` · `data-toc-cls="sp"`는 SPECIAL 코너, `big`은 대형 기사
- 러닝헤드·폴리오(쪽번호)는 빌드가 자동으로 넣는다 직접 쓰지 않는다
- 배경 변형 `class="page dark"`(네이비) · `class="page tint"`(짙은 종이색)
- 여러 면에 걸친 기사 · 첫 면 끝에 `<div class="cont">→ {{next}}면에 계속</div>`, 다음 면 맨 위에 `<div class="cont from">← {{prev}}면에서 계속</div>`
- 다른 면 참조는 `{{pg:p-clinic2}}면` 처럼 토큰을 쓴다 (빌드가 쪽번호로 바꾼다)

## 3 컴포넌트 (praxis.css 에 정의됨 · 새 CSS가 꼭 필요하면 섹션 파일 안 `<style>`에 섹션 접두어 클래스로만 추가)

```html
<div class="kicker">한글 분류<span class="sep">/</span>ENGLISH LABEL</div>
<h1 class="headline">제목</h1>            <!-- .xl 40pt .m 22pt .s 17pt -->
<div class="cs-sub">부제</div>
<p class="dek">리드문</p>
<div class="byline">글 <b>PRAXIS 편집부</b> · 근거 …</div>
<span class="special-tag">SPECIAL 05 · …</span>   <!-- .teal .navy .gold 변형 -->
<h3 class="sub"><span class="no">01</span>소제목</h3>
<p class="dropcap">첫 문단</p>   <p class="lead">큰 본문</p>   <em class="hl">형광 강조</em>
<div class="cols-2"> … </div>  <div class="cols-3"> … </div>   <!-- 다단 -->
<div class="grid g2|g3|g4|g-7-5|g-5-7|g-8-4" style="gap:6mm"> … </div>
<div class="pull">인용문<small>출처</small></div>
<div class="box"> <h4><span class="tag">TAG</span>제목</h4> <p class="small">…</p> </div>  <!-- .acc .teal .dark -->
<ul class="list small"><li>…</li></ul>   <ol class="list num small">   <ul class="list check small">
<table class="tbl"><thead><tr><th>…</th></tr></thead><tbody><tr><td class="k">키</td><td>…</td></tr></tbody></table>
<div class="stat"><div class="v">87<small>%</small></div><div class="l">라벨</div><div class="s">설명</div></div>
<!-- 근거 미터 · data-l 1~5 -->
<span class="ev" data-l="5"><i><b></b><b></b><b></b><b></b><b></b></i>무작위 시험</span>
<span class="stat-badge">라벨</span>  <!-- .t .n .g 색 변형 -->
<!-- 연구 카드 -->
<div class="card">
  <div class="meta"><span class="note">저널 · 날짜</span><span class="ev" data-l="4"><i><b></b><b></b><b></b><b></b><b></b></i>체계적 고찰</span></div>
  <span class="num">01</span><h4>기사형 제목</h4>
  <div class="src">저자 외 · 저널 권호 · 2026-09-xx</div>
  <dl><dt>무엇을</dt><dd>…</dd><dt>발견</dt><dd>…</dd><dt>주의</dt><dd>…</dd><dt>교실로</dt><dd>…</dd></dl>
</div>
<!-- 도구 카드 -->
<div class="app"> <div class="top"><div style="display:flex;gap:3mm"><span class="rank">01</span><div><h4>이름</h4><div class="who">개발사 · 국가 · 날짜 · 유형</div></div></div>
  <div class="scores"><b>교사</b><span class="dots">●●●<span class="off">●●</span></span><br><b>연구</b><span class="dots">●●●●<span class="off">●</span></span></div></div>
  <dl><dt>무엇인가</dt><dd>…</dd> …</dl></div>      <!-- .mini 작은 카드 -->
<figure class="figure" id="fig-고유id"><svg viewBox="0 0 680 200" role="img" aria-label="…">…</svg>
  <figcaption><b>그림 제목</b> 설명</figcaption></figure>
```
근거 미터 기준 · 5 무작위 시험·메타분석 · 4 준실험·체계적 고찰 · 3 대규모 조사·종단·혼합방법·신뢰도 검증 · 2 질적·서지계량·설계·개발·서사적 리뷰·가능성 연구 · 1 개념·논평·정책·기업 발표

SVG 도표 · 색은 #14223A(네이비) #C8412A(주홍) #E0735A #4F8F88(청록) #B08A3E(금) #EFE8DA(종이) #6B6F77(회색) 글꼴 `font-family="Noto Sans KR"` · 모든 figure에 고유 id · 데이터 도표는 소스 수치만 사용하고 개념도는 「개념도」라고 캡션에 쓴다

## 4 소스 자료 (텍스트로 변환됨)

`/tmp/claude-0/-home-user-Project1/6ea381e4-8f95-5ae5-8c38-ecf3530a34db/scratchpad/txt/`
- `research_2026-09-DD.txt` 교육 AI 연구·뉴스 데일리 브리핑 30개 (각 6~10건 · 저자·저널·DOI·설계·결과)
- `monthly_research.txt` 9월 월말 동향 보고서
- `EdTech_Radar_2026-09-DD.txt` 에듀테크 레이더 20개 · `EdTech_Weekly_Review_2026-W37~39.txt` · `EdTech_Monthly_Landscape_2026-09.txt`
원본 docx 의 하이퍼링크가 필요하면 같은 폴더의 .docx 를 zip 으로 열어 `word/_rels/document.xml.rels` 를 본다

이미 다른 기사에서 크게 다룬 연구·도구 (카드로 반복하지 말고 필요하면 한 줄 언급과 `{{pg:…}}` 참조만)
Koretsky 외 · Colson·Ballard · Sheng-Tun Li · 권태현 · Liang 외 BJET · UNESCO IESALC 87/26 · Köroğlu 외 · Zhang·Li 교사권한 · Chin-Siang Ang · AFT/UFT/Microsoft · UNESCO Algorithm in the Room · Molemane 외 · 가나 GPT-4o 가능성 연구 · Ed.ai · Scientific Reports 대화 스캐폴딩 · 해석가능 문제추천 · Moradi·Evans · 박주현 외 SEL · Broughton 외 WIDA · Oreopoulos NUMI · 리빙 메타분석 arXiv 2601.18685 · Bassner Iris · Connell Pensky · Thoeni·Fryer · Hai Li 음성 · Jiayue Zhang EEG · Deduwela GPT-5 · Kiliç Şafak · Zhengdao Li · 류경희 · 우길주·양지원 · 이효정 · Lodén 외 · Höper·Schulte · 하오선·정주원 · Hur 외 · Sadegh 외 · Amiruddin 외 · Satmaz 외 · Google Learning Interactives · Learning Commons · Project Helix · Makit · Pearson ITS · Ellucian · WhalesBot · Kahoot! · Assessable · EduverseSTEM · Glite · ScholarSail · QwenWork · Florida · Multiverse
주요 면 id · p-cover-story(커버스토리) p-feature(특집 거버넌스) p-clinic p-clinic2~4(수학클리닉) p-spot~3(스포트라이트) p-radar~4(레이더) p-literacy p-affect p-evidence p-practice p-agenda p-sources(참고문헌)

## 5 참고문헌

본문에는 짧은 출처(저자 외 연도 · 저널)만 쓰고 전체 서지는 맨 뒤 참고문헌에 모은다
섹션마다 `refs_<섹션>.txt` 를 만들고 한 줄에 하나씩 쓴다
`분류 | 서지 | URL` · 분류는 `국외논문` `국내논문` `정책기관` `에듀테크` `보도` 중 하나 · 서지 형식 예 `Oreopoulos 외 2026 Making AI Tutoring Productive · NBER Working Paper 35621`
URL 은 소스에 있는 것만 · 없으면 비워 둔다 · 서지 안에도 온점과 쌍따옴표 금지

## 6 검증 (반드시 끝까지)

```bash
cd /home/user/Project1/praxis/src
python3 build.py p12_teachers.html     # 내 파일만 빌드 → _build/preview_p12_teachers.html + 표기 규칙 검사 (둘 다 0이어야 한다)
HTML=preview_p12_teachers.html NODE_PATH=$(npm root -g) node render.js check   # 넘침 검사 · overflowing 0
HTML=preview_p12_teachers.html NODE_PATH=$(npm root -g) node render.js shots   # 스크린샷 → _build/shots_preview_p12_teachers/p001.png …
```
- 스크린샷을 Read 도구로 **모든 면을 직접 보고** 확인한다 · 넘침 · 겹침 · 아래쪽에 큰 빈 공간(면의 15% 이상)이 없도록 분량을 조절한다
- 여러 에이전트가 동시에 작업한다 · 미리보기 파일과 스크린샷 폴더는 파일 이름별로 분리된다 · 미리보기에서 쪽번호와 {{pg:…}} 참조는 ?? 나 임시 번호로 보여도 괜찮다 · 다른 섹션 파일·praxis.css·build.py·render.js 는 수정하지 않는다
- git 커밋·푸시는 하지 않는다
