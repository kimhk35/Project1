#!/usr/bin/env python3
import os
BASE = "c:/upstage"

p2 = """
  <section class="section framework-section" id="framework">
    <div class="container">
      <div class="section-label"><span class="label-line" aria-hidden="true"></span>02 — 분류 체계</div>
      <div class="framework-intro">
        <h2 class="section-title">7대 대분류 체계</h2>
        <p>수학교육 연구를 <strong class="highlight">내용의 초점</strong>에 따라 다음과 같이 대분류합니다. 하나의 연구 프로젝트가 여러 분류에 걸치는 경우도 흔하며, 이 체계는 연구를 기술하기 위한 <strong class="highlight">참조 틀</strong>입니다.</p>
      </div>
      <div class="framework-timeline" id="frameworkTimeline"></div>
    </div>
  </section>

  <section class="section domains-section" id="domains">
    <div class="container">
      <div class="section-label"><span class="label-line" aria-hidden="true"></span>03 — 연구 영역 상세</div>
      <div class="domains-header">
        <h2 class="section-title">각 연구 영역 깊이 보기</h2>
        <p>대분류를 선택하면 해당 영역의 중분류 주제, 주요 연구 질문, 대표 방법론을 확인할 수 있습니다.</p>
      </div>
      <div class="domain-tabs" id="domainTabs" role="tablist" aria-label="연구 영역 탭"></div>
      <div class="domain-panel" id="domainPanel" aria-live="polite"></div>
    </div>
  </section>

  <section class="section flow-section" id="flow">
    <div class="container">
      <div class="section-label"><span class="label-line" aria-hidden="true"></span>04 — 연구 흐름</div>
      <div class="flow-grid">
        <div class="flow-text">
          <h2 class="section-title">수학교육 연구의 역사적 흐름</h2>
          <p>수학교육 연구는 20세기 초 수학교육학에서 출발하여, 1960–70년대 구조주의·새수학, 1980–90년대 구성주의·메타인지 연구를 거쳐, 2000년대 이후 사회문화적 접근, 설계 기반 연구(DBR), 신경과학적 접근으로 확장되었습니다.</p>
          <div class="flow-eradec">
            <div class="era-card"><div class="era-year">1900–1950</div><div class="era-title">태동기</div><div class="era-desc">수와 연산 교육, 기하 교육 방법론 모색. 유럽 중심 초기 수학교육학 형성.</div></div>
            <div class="era-card"><div class="era-year">1960–1970</div><div class="era-title">구조주의 · 새수학</div><div class="era-desc">수학의 구조적 이해 강조(새로운 수학 운동). 집합론 기반 교육과정. 반성적 비판 등장.</div></div>
            <div class="era-card"><div class="era-year">1980–1990</div><div class="era-title">구성주의 · 메타인지</div><div class="era-desc">피아제·비고츠키 영향. 학습자 중심, 문제 해결, 메타인지, 다중 표상 연구 활발.</div></div>
            <div class="era-card"><div class="era-year">2000–2010</div><div class="era-title">사회문화 · DBR</div><div class="era-desc">상황화 학습, 협력 학습, 설계 기반 연구 방법론 정착. 디지털 도구 활용 연구 확대.</div></div>
            <div class="era-card"><div class="era-year">2010–현재</div><div class="era-title">융합 · 실천 · 신경과학</div><div class="era-desc">STEAM, 수학적 모델링, 체화된 인지, 신경과학 접근, AI·디지털 전환 시대 수학교육 연구.</div></div>
          </div>
        </div>
        <div class="flow-visual" id="flowVisual"></div>
      </div>
    </div>
  </section>

  <section class="section refs-section" id="references">
    <div class="container">
      <div class="section-label"><span class="label-line" aria-hidden="true"></span>05 — 참고문헌</div>
      <div class="refs-grid">
        <div class="refs-column">
          <h2 class="refs-heading">국제 주요 문헌</h2>
          <ol class="refs-list" id="refsInternational"></ol>
        </div>
        <div class="refs-column">
          <h2 class="refs-heading">국내 주요 문헌</h2>
          <ol class="refs-list" id="refsDomestic"></ol>
        </div>
      </div>
    </div>
  </section>

  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <span class="logo-icon">∑</span>
        <div>
          <div class="footer-title">수학교육 연구 분류</div>
          <div class="footer-subtitle">Mathematics Education Research Classification</div>
        </div>
      </div>
      <div class="footer-nav">
        <span class="footer-label">탐색</span>
        <a href="#overview">개요</a><a href="#framework">분류 체계</a>
        <a href="#domains">연구 영역</a><a href="#flow">연구 흐름</a>
        <a href="#references">참고문헌</a>
      </div>
      <p class="footer-note">본 분류 체계는 교육학 연구 목적의 참고 자료이며, 절대적 분류 기준이 아닙니다. 연구 주제는 관점에 따라 여러 분류에 중복하여 속할 수 있습니다.</p>
    </div>
  </footer>

  <script src="script_data.js"></script>
  <script src="script_domains.js"></script>
  <script src="script_render.js"></script>
  <script src="script_util.js"></script>
</body>
</html>
"""
with open(os.path.join(BASE, "index.html"), "a", encoding="utf-8") as f:
    f.write(p2)
print("index.html part2 완료")
