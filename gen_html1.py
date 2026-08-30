#!/usr/bin/env python3
import os
BASE = "c:/upstage"

p1 = """<!DOCTYPE html>
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
      <div class="hero-badge"><span class="badge-dot" aria-hidden="true"></span>교육학 연구 분류 체계</div>
      <h1 class="hero-title">수학교육 연구<br><span class="title-accent">분류 체계</span></h1>
      <p class="hero-subtitle">수학 교육의 연구 영역을 구조적으로 분류하고,<br>각 영역의 주요 주제, 방법론, 흐름을 한눈에 조망합니다.</p>
      <div class="hero-actions">
        <a href="#framework" class="btn btn-primary">분류 체계 보기</a>
        <a href="#domains" class="btn btn-outline">연구 영역 탐색</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><span class="stat-number" data-count="7">0</span><span class="stat-label">대분류 영역</span></div>
        <div class="stat-divider" aria-hidden="true"></div>
        <div class="stat"><span class="stat-number" data-count="28">0</span><span class="stat-label">중분류 주제</span></div>
        <div class="stat-divider" aria-hidden="true"></div>
        <div class="stat"><span class="stat-number" data-count="32">0</span><span class="stat-label">주요 문헌</span></div>
      </div>
    </div>
  </section>

  <section class="section overview-section" id="overview">
    <div class="container">
      <div class="section-label"><span class="label-line" aria-hidden="true"></span>01 — 개요</div>
      <div class="overview-grid">
        <div class="overview-text">
          <h2 class="section-title">수학교육 연구 분류란 무엇인가</h2>
          <p class="lead-paragraph">수학교육 연구는 수학 교수·학습의 현상을 과학적으로 규명하고, 더 나은 교육 실천을 모색하는 학문 분야입니다. 연구 주제가 방대해짐에 따라, 연구 결과를 체계적으로 조직하고 소통할 수 있는 <strong class="highlight">분류 체계</strong>가 필요해졌습니다.</p>
          <p>본 페이지는 국내외 수학교육 연구 문헌에서 다루어지는 주요 연구 영역을 <strong class="highlight">7개 대분류</strong>로 나누고, 각 대분류 아래 중분류 주제를 배치하여 수학교육 연구의 지형도를 제시합니다. 이 분류는 절대적인 위계가 아니라 연구자의 관점에 따른 <strong class="highlight">분석적 렌즈</strong>로 이해하는 것이 적절합니다.</p>
          <div class="overview-cards-mini">
            <div class="mini-card"><div class="mini-card-icon">🎯</div><div><div class="mini-card-title">목적 지향</div><div class="mini-card-desc">연구 목적별로 기초·응용·실천 연구로 구분</div></div></div>
            <div class="mini-card"><div class="mini-card-icon">🔬</div><div><div class="mini-card-title">방법 지향</div><div class="mini-card-desc">양적·질적·혼합·설계 기반 연구 방법론</div></div></div>
            <div class="mini-card"><div class="mini-card-icon">📐</div><div><div class="mini-card-title">내용 지향</div><div class="mini-card-desc">수학 내용 영역별 학습·교수 연구</div></div></div>
          </div>
        </div>
        <div class="overview-visual">
          <div class="venn-diagram">
            <div class="venn-circle venn-a" style="top:5%;left:10%;"><div class="venn-label">수학</div><div class="venn-sub">학문으로서의 수학</div></div>
            <div class="venn-circle venn-b" style="top:30%;right:8%;"><div class="venn-label">교육</div><div class="venn-sub">교수·학습 과학</div></div>
            <div class="venn-circle venn-c" style="bottom:8%;left:36%;"><div class="venn-label">인지</div><div class="venn-sub">학습자의 마음</div></div>
            <div class="venn-center"><span class="venn-center-text">수학교육 연구</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(p1)
print("index.html part1 완료")
