#!/usr/bin/env python3
"""Build the HWPX edition of Heurēsis Vol.01 from export/out/ir.json

Usage: python3 export/make_hwpx.py
"""
from __future__ import annotations

import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)

from hwpx.document import HwpxDocument  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IR_PATH = ROOT / "export" / "out" / "ir.json"
IMG_DIR = ROOT / "export" / "out" / "img"
OUT_PATH = ROOT / "dist" / "Heuresis_Vol01_창간특집호.hwpx"

HEADER_TEXT = "Heurēsis Vol.01 창간특집호"

MM = 7200 / 25.4  # HWP units per mm
PX_MM = 0.2646
CONTENT_MM = 170.0
CELL_PAD_MM = 4.0

SERIF = "Noto Serif KR"
SANS = "Noto Sans KR"
MONO = "IBM Plex Mono"

INK = "#1A1A1A"
ACCENT = {"": "#C8372D", "clinic": "#15606A", "teacher": "#A97A22"}
BOX_FILL = {
    "sand": "#F1EADF",
    "navy": "#1B2A41",
    "teal": "#E1EEEE",
    "ochre": "#F4EAD4",
    "line": "#FFFFFF",
    "card": "#FFFFFF",
}

# block style name -> (font, size pt, bold, color)
TEXT_STYLES = {
    "p": (SERIF, 10, False, INK),
    "lead": (SERIF, 11, False, INK),
    "li": (SERIF, 10, False, INK),
    "h1": (SERIF, 22, True, INK),
    "h2": (SERIF, 16, True, INK),
    "h3": (SANS, 11.5, True, INK),
    "h4": (SANS, 11, True, INK),
    "label": (MONO, 7.5, False, None),  # accent color
    "dek": (SANS, 12, False, "#34322F"),
    "small": (SANS, 8, False, "#6F6A63"),
    "quote": (SERIF, 13, True, INK),
    "cite": (SANS, 7.5, False, "#6F6A63"),
    "cell": (SANS, 8.5, False, INK),
    "toc": (SERIF, 11, False, INK),
}

# block style name -> paragraph format
PARA_STYLES = {
    "p": dict(alignment="JUSTIFY", line=160, after=4),
    "lead": dict(alignment="JUSTIFY", line=160, after=6),
    "li": dict(alignment="JUSTIFY", line=160, after=2, left=5, intent=-5),
    "h1": dict(alignment="LEFT", line=130, before=6, after=8, keep=True),
    "h2": dict(alignment="LEFT", line=130, before=10, after=6, keep=True),
    "h3": dict(alignment="LEFT", line=140, before=8, after=4, keep=True),
    "h4": dict(alignment="LEFT", line=140, before=6, after=3, keep=True),
    "label": dict(alignment="LEFT", line=130, before=8, after=2, keep=True),
    "dek": dict(alignment="LEFT", line=150, after=8),
    "small": dict(alignment="LEFT", line=140, after=4),
    "quote": dict(alignment="LEFT", line=150, before=8, after=2, left=8),
    "cite": dict(alignment="LEFT", line=130, after=8, left=8),
    "cell": dict(alignment="LEFT", line=140),
    "toc": dict(alignment="LEFT", line=160, after=6),
    "img": dict(alignment="CENTER", line=100, before=4, after=4),
    "host": dict(alignment="LEFT", line=100, before=3, after=6),
    "cover": dict(alignment="CENTER", line=100),
}


def run_text(runs) -> str:
    return "".join(r.get("t", "") for r in runs or [])


class Builder:
    def __init__(self) -> None:
        self.doc = HwpxDocument.new()
        self.header = self.doc._root.headers[0]
        self._char_cache: dict[tuple, str] = {}
        self._para_cache: dict[tuple, str] = {}
        self._bf_cache: dict[tuple, str] = {}
        self._img_cache: dict[str, str] = {}
        self.pending_break = False
        self.base_para = self.doc.paragraphs[0].para_pr_id_ref
        self.counts = {"pictures": 0, "tables": 0, "boxes": 0}

    # ---------- styles ----------
    def char_id(self, font, size, bold=False, italic=False, color=INK) -> str:
        key = (font, float(size), bool(bold), bool(italic), color)
        if key not in self._char_cache:
            self._char_cache[key] = str(
                self.doc.ensure_run_style(
                    font=font, size=size, bold=bold, italic=italic, color=color
                )
            )
        return self._char_cache[key]

    def para_id(self, name: str, extra_left_mm: float = 0.0) -> str:
        key = (name, extra_left_mm)
        if key in self._para_cache:
            return self._para_cache[key]
        spec = PARA_STYLES[name]
        margins = {
            "left": round((spec.get("left", 0) + extra_left_mm) * MM),
            "right": 0,
            "intent": round(spec.get("intent", 0) * MM),
            "prev": round(spec.get("before", 0) * 100),
            "next": round(spec.get("after", 0) * 100),
        }
        brk = {"keep_with_next": True} if spec.get("keep") else None
        pid = self.header.ensure_paragraph_format(
            base_para_pr_id=self.base_para,
            alignment=spec["alignment"],
            line_spacing_percent=spec["line"],
            margins=margins,
            break_setting=brk,
        )
        self._para_cache[key] = str(pid)
        return self._para_cache[key]

    def border_fill(self, kind: str, fill: str | None = None) -> str:
        key = (kind, fill)
        if key in self._bf_cache:
            return self._bf_cache[key]
        d = self.doc
        if kind == "grid":  # thin table grid
            bid = d.ensure_border_fill(border_color="#8C877F", border_width="0.12 mm", fill_color=fill)
        elif kind == "line":
            bid = d.ensure_border_fill(border_color="#000000", border_width="0.5 mm", fill_color="#FFFFFF")
        elif kind == "card":
            bid = d.ensure_border_fill(border_color="#D6D1C8", border_width="0.12 mm", fill_color="#FFFFFE")
            self._thicken_top(bid, "1.0 mm", "#1B2A41")
        else:  # filled box, no visible border
            bid = d.ensure_border_fill(border_color=fill, border_width="0.12 mm", fill_color=fill)
        self._bf_cache[key] = str(bid)
        return self._bf_cache[key]

    def _thicken_top(self, bid: str, width: str, color: str) -> None:
        el = self.header.element
        for bf in el.iter():
            if bf.tag.endswith("}borderFill") and bf.get("id") == str(bid):
                for child in bf:
                    if child.tag.endswith("}topBorder"):
                        child.set("width", width)
                        child.set("color", color)
                self.header.mark_dirty()
                return

    # ---------- paragraphs ----------
    def top_par(self, pstyle: str, extra_left_mm: float = 0.0):
        p = self.doc.add_paragraph(
            "", include_run=False, para_pr_id_ref=self.para_id(pstyle, extra_left_mm)
        )
        if self.pending_break:
            p.element.set("pageBreak", "1")
            self.pending_break = False
        return p

    def add_runs(self, p, runs, tstyle: str, ctx: dict, prefix: str = "") -> None:
        font, size, bold, color = TEXT_STYLES[tstyle]
        if color is None:
            color = ctx["accent"]
        if ctx.get("inverse"):
            color = "#FFFFFF" if tstyle != "label" else "#E9C77B"
        if prefix:
            p.add_run(prefix, char_pr_id_ref=self.char_id(font, size, bold, False, color))
        wrote = False
        for r in runs or []:
            text = r.get("t", "")
            if not text:
                continue
            rfont = MONO if r.get("m") else font
            cid = self.char_id(rfont, size, bold or r.get("b"), r.get("i"), color)
            p.add_run(text, char_pr_id_ref=cid, expand_special_characters=("\n" in text))
            wrote = True
        if not wrote and not prefix:
            p.add_run("", char_pr_id_ref=self.char_id(font, size, bold, False, color))

    # ---------- images ----------
    def image_item(self, img_id: str) -> str | None:
        if img_id in self._img_cache:
            return self._img_cache[img_id]
        path = IMG_DIR / f"{img_id}.png"
        if not path.exists():
            print(f"warning: missing image {path}", file=sys.stderr)
            return None
        iid = str(self.doc.add_image(path.read_bytes(), "png"))
        self._img_cache[img_id] = iid
        return iid

    def place_image(self, p, block, avail_mm: float) -> None:
        iid = self.image_item(block["id"])
        if iid is None:
            return
        w_px, h_px = float(block["w"]), float(block["h"])
        if block.get("kind") == "band":
            w_mm = avail_mm
        else:
            w_mm = min(w_px * PX_MM, avail_mm)
        h_mm = w_mm * h_px / w_px
        max_h = 240.0
        if h_mm > max_h:
            w_mm, h_mm = w_mm * max_h / h_mm, max_h
        p.add_picture(iid, width=round(w_mm * MM), height=round(h_mm * MM))
        self.counts["pictures"] += 1

    # ---------- containers ----------
    def render_blocks(self, blocks, target, ctx) -> None:
        """target: callable(pstyle, extra_left) -> paragraph; plus ctx['avail']"""
        ord_counter = 0
        for b in blocks:
            t = b["t"]
            if t == "li" and b.get("ord"):
                ord_counter += 1
            elif t != "li":
                ord_counter = 0
            self.render_block(b, target, ctx, ord_counter)

    def render_block(self, b, target, ctx, ord_n: int = 0) -> None:
        t = b["t"]
        if t == "h":
            lvl = min(max(int(b.get("l", 2)), 1), 4)
            p = target(f"h{lvl}")
            self.add_runs(p, b.get("r"), f"h{lvl}", ctx)
        elif t in ("label", "dek", "small"):
            p = target(t)
            self.add_runs(p, b.get("r"), t, ctx)
        elif t == "p":
            style = "lead" if b.get("lead") else ("toc" if b.get("toc") else "p")
            p = target(style)
            self.add_runs(p, b.get("r"), style, ctx)
        elif t == "li":
            if b.get("check"):
                prefix = "☐ "
            elif b.get("ord"):
                prefix = f"{ord_n}. "
            else:
                prefix = "• "
            p = target("li")
            self.add_runs(p, b.get("r"), "li", ctx, prefix=prefix)
        elif t == "quote":
            p = target("quote")
            self.add_runs(p, b.get("r"), "quote", ctx)
            cite = b.get("cite")
            if cite:
                c = target("cite")
                text = cite if isinstance(cite, str) else run_text(cite)
                self.add_runs(c, [{"t": text}], "cite", ctx)
        elif t == "img":
            p = target("img")
            self.place_image(p, b, ctx["avail"])
        elif t == "table":
            self.render_table(b, target, ctx)
        elif t == "box":
            self.render_box(b, target, ctx)
        else:
            text = run_text(b.get("r"))
            if text:
                p = target("p")
                self.add_runs(p, b.get("r"), "p", ctx)

    def new_table(self, host, rows, cols, width_mm, bf):
        tbl = host.add_table(rows, cols, width=round(width_mm * MM), border_fill_id_ref=bf)
        self.counts["tables"] += 1
        return tbl

    def cell_target(self, cell, ctx_inner):
        state = {"first": True}

        def target(pstyle, extra_left=0.0):
            pid = self.para_id(pstyle, extra_left)
            if state["first"]:
                state["first"] = False
                p = cell.paragraphs[0]
                p.para_pr_id_ref = pid
                return p
            return cell.add_paragraph("", para_pr_id_ref=pid)

        return target

    def render_table(self, b, target, ctx) -> None:
        rows = b.get("rows") or []
        if not rows:
            return
        ncols = max(len(r) for r in rows)
        host = target("host")
        width = ctx["avail"]
        tbl = self.new_table(host, len(rows), ncols, width, self.border_fill("grid"))
        head_bf = self.border_fill("grid", "#EEEAE3")
        weights = []
        for c in range(ncols):
            lens = [len(run_text(r[c].get("r"))) for r in rows if c < len(r)]
            weights.append(min(max(max(lens or [1]), 4), 40))
        try:
            tbl.set_column_widths(weights)
        except Exception as exc:  # pragma: no cover
            print(f"warning: column widths: {exc}", file=sys.stderr)
        cctx = dict(ctx, inverse=False)
        for ri, row in enumerate(rows):
            for ci in range(ncols):
                cell = tbl.cell(ri, ci)
                cell.set_margins(left=round(1.8 * MM), right=round(1.8 * MM), top=round(1.0 * MM), bottom=round(1.0 * MM))
                p = cell.paragraphs[0]
                p.para_pr_id_ref = self.para_id("cell")
                if ci >= len(row):
                    continue
                c = row[ci]
                runs = c.get("r") or []
                if c.get("th"):
                    runs = [dict(r, b=True) for r in runs]
                    tbl.set_cell_border_fill(ri, ci, head_bf)
                self.add_runs(p, runs, "cell", cctx)

    def render_box(self, b, target, ctx) -> None:
        v = b.get("v", "sand")
        if v == "line":
            bf = self.border_fill("line")
        elif v == "card":
            bf = self.border_fill("card")
        else:
            bf = self.border_fill("fill", BOX_FILL.get(v, "#F1EADF"))
        host = target("host")
        width = ctx["avail"]
        tbl = self.new_table(host, 1, 1, width, bf)
        self.counts["boxes"] += 1
        cell = tbl.cell(0, 0)
        pad = round(CELL_PAD_MM * MM)
        cell.set_margins(left=pad, right=pad, top=round(3 * MM), bottom=round(3 * MM))
        inner = dict(ctx, avail=width - 2 * CELL_PAD_MM - 1.0, inverse=(v == "navy") or ctx.get("inverse", False))
        if v != "navy" and ctx.get("inverse"):
            inner["inverse"] = False
        self.render_blocks(b.get("c") or [], self.cell_target(cell, inner), inner)

    # ---------- document ----------
    def build(self, ir) -> None:
        d = self.doc
        d.set_page_setup(
            paper_size="A4",
            margins_mm=dict(left=20, right=20, top=20, bottom=20),
            header_margin_mm=10,
            footer_margin_mm=10,
        )
        d.set_header_text(HEADER_TEXT)
        d.set_page_number(position="BOTTOM_CENTER")

        pages = {p["n"]: p for p in ir}

        # page 1 cover into the first existing paragraph (holds secPr)
        first = d.paragraphs[0]
        first.para_pr_id_ref = self.para_id("cover")
        first.add_page_hiding(header=True, footer=True, page_num=True)
        cover = pages[1]
        ctx = {"accent": ACCENT[""], "avail": CONTENT_MM}
        for blk in cover["b"]:
            if blk["t"] == "img":
                self.place_image(first, dict(blk, kind="page"), CONTENT_MM)
                break

        # static contents page
        self.pending_break = True
        p = self.top_par("label")
        self.add_runs(p, [{"t": "In This Issue"}], "label", ctx)
        p = self.top_par("h1")
        self.add_runs(p, [{"t": "차례", "b": True}], "h1", ctx)
        for page in ir:
            if not page.get("sec") or page["n"] in (1, 2, 3):
                continue
            label = next((run_text(b.get("r")) for b in page["b"] if b["t"] == "label"), "")
            head = next((run_text(b.get("r")) for b in page["b"] if b["t"] == "h"), "")
            head = " ".join(head.split())
            label = " ".join(label.split())
            # drop in-story page counters such as 1/14 so the list carries no page numbers
            label = re.sub(r"\s*·\s*\d+\s*/\s*\d+\s*$", "", label)
            p = self.top_par("toc")
            if label:
                self.add_runs(p, [{"t": label, "m": True}, {"t": " · "}, {"t": head, "b": True}], "toc", ctx)
            else:
                self.add_runs(p, [{"t": head, "b": True}], "toc", ctx)

        # magazine pages
        for page in ir:
            n = page["n"]
            if n in (1, 2, 3):
                continue
            if page.get("sec"):
                self.pending_break = True
            ctx = {"accent": ACCENT.get(page.get("theme") or "", ACCENT[""]), "avail": CONTENT_MM}
            self.render_blocks(page["b"], self.top_par, ctx)


def main() -> int:
    ir = json.loads(IR_PATH.read_text(encoding="utf-8"))
    b = Builder()
    b.build(ir)

    report = b.doc.validate()
    print("validate:", report)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    b.doc.save_to_path(str(OUT_PATH))
    print("saved:", OUT_PATH, OUT_PATH.stat().st_size, "bytes")
    print("built:", b.counts)

    # reopen check
    doc = HwpxDocument.open(str(OUT_PATH))
    rv = doc.validate()
    print("reopen validate:", rv)
    xml_counts = {"p": 0, "tbl": 0, "pic": 0}
    for sec in doc.sections:
        for el in sec.element.iter():
            tag = el.tag.rsplit("}", 1)[-1]
            if tag in xml_counts:
                xml_counts[tag] += 1
    print(
        "reopened: sections=%d body_paragraphs=%d all_paragraphs=%d tables=%d pictures=%d images=%d"
        % (len(doc.sections), len(doc.paragraphs), xml_counts["p"], xml_counts["tbl"], xml_counts["pic"], len(doc.list_images()))
    )
    text = doc.export_text()
    missing = [s for s in ("정답 이후의 수학", "수학클리닉", "참고문헌과 자료 출처", "차례") if s not in text]
    print("text export chars:", len(text), "missing:", missing or "none")
    return 0 if not missing and not getattr(rv, "issues", ()) else 1


if __name__ == "__main__":
    sys.exit(main())
