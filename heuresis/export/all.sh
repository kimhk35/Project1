#!/usr/bin/env bash
# Heurēsis Vol.01 전 형식 내보내기  PDF HTML e-book DOCX HWPX
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
python3 build_refs.py
python3 build.py
node render.js
mkdir -p dist && cp Heuresis_Vol01_창간특집호.pdf dist/
python3 export/export_web.py
node export/extract.js
python3 export/make_docx.py
python3 export/make_hwpx.py
ls -la dist
