#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
BASE = "c:/upstage"

index_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>수학교육 연구 분류 | Mathematics Education Research Classification</title>
  <link rel="stylesheet" href="style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600;700;900&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%231B2A4A'/><text x='16' y='22' font-size='18' text-anchor='middle' fill='%23D4A853' font-family='serif'>∑</text></svg>">
</head>
<body>
  <header class="site-header" id="header">
    <div class="container header-inner">
      <a href="#" class="logo" aria-label="수학교육 연구 분류 홈">
        <span class="logo-icon">∑</span>
        <span class="logo-text">수학교육 연구 분류</span>
      </a>
      <nav class="main-nav" id="mainNav">
        <ul class="nav-list">
          <li><a href="#overview" class="nav-link">개요</a></li>
          <li><a href="#framework" class="nav-link">분류 체계</a></li>
          <li><a href="#domains" class="nav-link">연구 영역</a></li>
          <li><a href="#flow" class="nav-link">연구 흐름</a></li>
          <li><a href="#references" class="nav-link">참고문헌</a></li>
        </ul>
      </nav>
      <button class="menu-toggle" id="menuToggle" aria-label="메뉴 열기" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
  <section class="hero" id="hero">
    <div class="hero-bg-grid" aria-hidden="true"></div>
    <div class="hero-shape hero-shape-1" aria-hidden="true"></div>
    <div class="hero-shape hero-shape-2" aria-hidden="true"></div>
    <div class="container hero-content">
      <div class="hero-badge">
        <span class="badge-dot" aria-hidden="true"></span>
        교육학 연구 분류 체계
      </div>
      <h1 class="hero-title">
        수학교육 연구<br>
        <span class="title-accent">분류 체계</span>
      </h1>
      <p class="hero-subtitle">
        수학 교육의 연구 영역을 구조적으로 분류하고,<br>
        각 영역의 주요 주제, 방법론, 흐름을 한눈에 조망합니다.
      </p>
      <div class="hero-actions">
        <a href="#framework" class="btn btn-primary">분류 체계 보기</a>
        <a href="#domains" class="btn btn-outline">연구 영역 탐색</a>
      </div>
      <div class="hero-stats">
        <div class="stat">
          <span class="stat-number" data-count="7">0</span>
          <span class="stat-label">대분류 영역</span>
        </div>
        <div class="stat-divider" aria-hidden="true"></div>
        <div class="stat">
          <span class="stat-number" data-count="23">0</span>
          <span class="stat-label">중분류 주제</span>
        </div>
        <div class="stat-divider" aria-hidden="true"></div>
        <div class="stat">
          <span class="stat-number" data-count="32">0</span>
          <span class="stat-label">주요 문헌</span>
        </div>
      </div>
    </div>
  </section>
  <section class="section overview-section" id="overview">
    <div class="container">
      <div class="section-label">
        <span class="label-line" aria-hidden="true"></span>
        01 — 개요
      </div>
      <div class="overview-grid">
        <div class="overview-text">
          <h2 class="section-title">수학교육 연구 분류란 무엇인가</h2>
          <p class="lead-paragraph">
            수학교육 연구는 수학 교수·학습의 현상을 과학적으로 규명하고, 더 나은 교육 실천을 모색하는 학문 분야입니다.
            연구 주제가 방대해짐에 따라, 연구 결과를 체계적으로 조직하고 소통할 수 있는 <strong class="highlight">분류 체계</strong>가 필요해졌습니다.
          </p>
          <p>
            본 페이지는 국내외 수학교육 연구 문헌에서 다루어지는 주요 연구 영역을 <strong class="highlight">7개 대분류</strong>로 나누고,
            각 대분류 아래 중분류 주제를 배치하여 수학교육 연구의 지형도를 제시합니다.
            이 분류는 절대적인 위계가 아니라 연구자의 관점에 따른 <strong class="highlight">분석적 렌즈</strong>로 이해하는 것이 적절합니다.
          </p>
          <div class="overview-cards-mini">
            <div class="mini-card">
              <div class="mini-card-icon">🎯</div>
              <div>
                <div class="mini-card-title">목적 지향</div>
                <div class="mini-card-desc">연구 목적별로 기초·응용·실천 연구로 구분</div>
              </div>
            </div>
            <div class="mini-card">
              <div class="mini-card-icon">🔬</div>
              <div>
                <div class="mini-card-title">방법 지향</div>
                <div class="mini-card-desc">양적·질적·혼합·설계 기반 연구 방법론</div>
              </div>
            </div>
            <div class="mini-card">
              <div class="mini-card-icon">📐</div>
              <div>
                <div class="mini-card-title">내용 지향</div>
                <div class="mini-card-desc">수학 내용 영역별 학습·교수 연구</div>
              </div>
            </div>
          </div>
        </div>
        <div class="overview-visual">
          <div class="venn-diagram">
            <div class="venn-circle venn-a" style="top:5%; left:10%;">
              <div class="venn-label">수학</div>
              <div class="venn-sub">학문으로서의 수학</div>
            </div>
            <div class="venn-circle venn-b" style="top:30%; right:8%;">
              <div class="venn-label">교육</div>
              <div class="venn-sub">교수·학습 과학</div>
            </div>
            <div class="venn-circle venn-c" style="bottom:8%; left:36%;">
              <div class="venn-label">인지</div>
              <div class="venn-sub">학습자의 마음</div>
            </div>
            <div class="venn-center">
              <span class="venn-center-text">수학교육 연구</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
"""  <!-- ====== FRAMEWORK ====== -->
  <section class="section framework-section" id="framework">
    <div class="container">
      <div class="section-label">
        <span class="label-line" aria-hidden="true"></span>
        02 — 분류 체계
      </div>
      <div class="framework-intro">
        <h2 class="section-title">7대 대분류 체계</h2>
        <p>
          수학교육 연구를 <strong class="highlight">내용의 초점</strong>에 따라 다음과 같이 대분류합니다.
          하나의 연구 프로젝트가 여러 분류에 걸치는 경우도 흔하며, 이 체계는 연구를 기술하기 위한 <strong class="highlight">참조 틀</strong>입니다.
        </p>
      </div>
      <div class="framework-timeline" id="frameworkTimeline"></div>
    </div>
  </section>
  <section class="section domains-section" id="domains">
    <div class="container">
      <div class="section-label">
        <span class="label-line" aria-hidden="true"></span>
        03 — 연구 영역 상세
      </div>
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
      <div class="section-label">
        <span class="label-line" aria-hidden="true"></span>
        04 — 연구 흐름
      </div>
      <div class="flow-grid">
        <div class="flow-text">
          <h2 class="section-title">수학교육 연구의 역사적 흐름</h2>
          <p>
            수학교육 연구는 20세기 초 수학교육학에서 출발하여, 1960–70년대 구조주의·새수학, 1980–90년대 구성주의·메타인지 연구를 거쳐,
            2000년대 이후 사회문화적 접근, 설계 기반 연구(DBR), 신경과학적 접근으로 확장되었습니다.
          </p>
          <div class="flow-eradec">
            <div class="era-card">
              <div class="era-year">1900–1950</div>
              <div class="era-title">태동기</div>
              <div class="era-desc">수와 연산 교육, 기하 교육 방법론 모색. 유럽 중심 초기 수학교육학 형성.</div>
            </div>
            <div class="era-card">
              <div class="era-year">1960–1970</div>
              <div class="era-title">구조주의 · 새수학</div>
              <div class="era-desc">수학의 구조적 이해 강조(새로운 수학 운동). 집합론 기반 교육과정. 반성적 비판 등장.</div>
            </div>
            <div class="era-card">
              <div class="era-year">1980–1990</div>
              <div class="era-title">구성주의 · 메타인지</div>
              <div class="era-desc">피아제·비고츠키 영향. 학습자 중심, 문제 해결, 메타인지, 다중 표상 연구 활발.</div>
            </div>
            <div class="era-card">
              <div class="era-year">2000–2010</div>
              <div class="era-title">사회문화 · DBR</div>
              <div class="era-desc">상황화 학습, 협력 학습, 설계 기반 연구 방법론 정착. 디지털 도구 활용 연구 확대.</div>
            </div>
            <div class="era-card">
              <div class="era-year">2010–현재</div>
              <div class="era-title">융합 · 실천 · 신경과학</div>
              <div class="era-desc">STEAM, 수학적 모델링, 체화된 인지, 신경과학 접근, AI·디지털 전환 시대 수학교육 연구.</div>
            </div>
          </div>
        </div>
        <div class="flow-visual" id="flowVisual"></div>
      </div>
    </div>
  </section>
  <section class="section refs-section" id="references">
    <div class="container">
      <div class="section-label">
        <span class="label-line" aria-hidden="true"></span>
        05 — 참고문헌
      </div>
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
        <a href="#overview">개요</a>
        <a href="#framework">분류 체계</a>
        <a href="#domains">연구 영역</a>
        <a href="#flow">연구 흐름</a>
        <a href="#references">참고문헌</a>
      </div>
      <p class="footer-note">
        본 분류 체계는 교육학 연구 목적의 참고 자료이며, 절대적 분류 기준이 아닙니다.<br>
        연구 주제는 관점에 따라 여러 분류에 중복하여 속할 수 있습니다.
      </p>
    </div>
  </footer>
  <script src="script.js"></script>
</body>
</html>
"""
with open(os.path.join(BASE, "index.html"), "a", encoding="utf-8") as f:
    f.write(tail)
print("✓ index.html part2 완료")

print("✓ index.html part1 완료")
