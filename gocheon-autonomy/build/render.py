# -*- coding: utf-8 -*-
"""SVG 도식과 표지를 PNG로 렌더링  python3 build/render.py [cover|figs]"""
import os, sys, re
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIGS = os.path.join(ROOT, "figs")


def render_figs(page):
    for fn in sorted(os.listdir(FIGS)):
        if not fn.endswith(".svg"):
            continue
        svg = open(os.path.join(FIGS, fn), encoding="utf-8").read()
        w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
        page.set_viewport_size({"width": int(w), "height": int(h)})
        page.set_content(f'<html><body style="margin:0">{svg}</body></html>')
        page.evaluate("document.fonts.ready")
        page.screenshot(path=os.path.join(FIGS, fn[:-4] + ".png"), clip={"x": 0, "y": 0, "width": w, "height": h})
        print("png", fn)


def render_cover(page):
    # A4 794x1123 css px  ×3.125 → 2481x3509 (300dpi)
    page.set_viewport_size({"width": 794, "height": 1123})
    page.goto("file://" + os.path.join(ROOT, "build", "cover.html"))
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(FIGS, "cover.png"), clip={"x": 0, "y": 0, "width": 794, "height": 1123})
    print("png cover")


if __name__ == "__main__":
    what = sys.argv[1:] or ["figs", "cover"]
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        if "figs" in what:
            pg = br.new_page(device_scale_factor=2)
            render_figs(pg)
        if "cover" in what:
            pg = br.new_page(device_scale_factor=3.125)
            render_cover(pg)
        br.close()
