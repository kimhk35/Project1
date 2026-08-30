# 수학교육 연구 분류

Mathematics Education Research Classification — 수학교육 연구 영역을 구조적으로 분류한 정적 웹사이트입니다.

## 프로젝트 구조

```
.
├── index.html          # 메인 페이지
├── style.css           # 전체 스타일링
├── script_data.js      # FRAMEWORK, INT_REFS, DOM_REFS 데이터
├── script_domains.js   # DOMAINS 데이터 (7개 영역, 26개 중분류)
├── script_render.js    # DOM 렌더링 (타임라인, 탭, SVG, 참고문헌)
├── script_util.js      # 유틸리티 (스크롤 리빌, 카운터, 모바일 메뉴)
├── verify_all.js       # Node.js 검증 스크립트
├── verify_all.py       # Python 검증 스크립트
├── .gitignore          # 버전관리 제외 파일
└── README.md           # 이 파일
```

## 기술 스택

- **HTML5 / CSS3 / Vanilla JavaScript** — 빌드 도구 없이 브라우저에서 직접 실행
- **Google Fonts (Noto Sans KR, Noto Serif KR)** — CDN 링크
- **Intersection Observer API** — 스크롤 리빌 애니메이션
- **SVG** — 연구 흐름 다이어그램 (인라인)

### 사용 중인 외부 라이브러리

없음 — 모든 기능이 바닐라 JavaScript로 구현되어 있습니다.

## 로컬 실행

별도의 서버 없이 브라우저에서 직접 열 수 있습니다.

```bash
# 방법 1: 파일 직접 열기
# index.html을 더블클릭하거나 브라우저에 드래그

# 방법 2: 간단한 로컬 서버 (권장 - CORS 등 문제 방지)
python -m http.server 8000
# 또는
npx serve .
# 그 후 http://localhost:8000 접속
```

## 데이터 검증

데이터 일관성과 렌더링 로직을 검증합니다.

```bash
# Node.js
node verify_all.js

# Python
python verify_all.py
```

## 배포

### Cloudflare Pages

1. GitHub 저장소에 푸시된 상태에서 Cloudflare 대시보드 접속
2. **Workers & Pages** → **Create Application** → **Pages** → **Connect to Git**
3. `kimhk35/mckay` 저장소 선택
4. 빌드 설정:
   - **Build command**: 비워두기 (또는 `echo "no build"`)
   - **Build output directory**: 비워두기 (루트에 index.html 있음)
5. **Save and Deploy**

또는 CLI로 배포:

```bash
# wrangler CLI 설치 (처음 한 번)
npm install -g wrangler

# Cloudflare Pages에 배포
npx wrangler pages deploy . --project-name=mckay
```

### GitHub Pages

1. GitHub 저장소 설정 → **Pages** 메뉴
2. **Source**: `Deploy from a branch`
3. **Branch**: `main` / `root` 선택
4. **Save**

또는 액션으로 배포:

```yaml
# .github/workflows/pages.yml (자동 생성됨)
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - uses: actions/deploy-pages@v4
```

### Netlify

```bash
# netlify CLI
npm install -g netlify-cli
netlify deploy --prod --dir=.
```

## 주의사항

- **상대경로**를 사용하므로 어떤 서브디렉토리에서 호스팅해도 정상 동작합니다.
- **API Key, .env 파일 없음** — 정적 사이트이므로 서버 사이드 비밀 정보가 없습니다.
- **Node.js 의존성 없음** — npm install 이 필요 없습니다.
- **모바일 대응** — CSS media query 및 햄버거 메뉴 포함.

## 브라우저 호환성

- Chrome/Edge 90+
- Firefox 88+
- Safari 15+
- 모바일 브라우저 최신 버전

Intersection Observer, backdrop-filter 등 최신 API 사용 (폴리필 불필요 — 타겟 브라우저에서 지원).

## 라이센스

교육 목적의 참고 자료입니다.
