# -*- coding: utf-8 -*-
"""고천중학교 학생자치 개선안  HWPX (한컴오피스 OWPML) 생성기

사용법 (프로젝트 폴더에서)
    python3 build/build_hwpx.py
    python3 build/build_hwpx.py --figs <그림폴더> --out <출력파일>

원본 콘텐츠는 build/content.py 하나이며 그림은 figs/<그림ID>.png, 표지는 figs/cover.png 를 쓴다
요소 순서와 속성 표기는 한컴오피스 한글이 저장한 HWPX 를 그대로 따른다
외부 의존성  lxml, Pillow
"""

import argparse
import datetime
import io
import math
import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

from lxml import etree
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import content as C  # noqa: E402

# ─────────────────────────────────────────────── 단위와 쪽 설정 (HWPUNIT, 1mm = 283.46)
MM = 7200 / 25.4
PAGE_W, PAGE_H = 59528, 84188            # A4 세로
MARGIN_LR = round(20 * MM)               # 좌우 20mm
MARGIN_TOP = round(12 * MM)              # 위 12mm + 머리말 6mm  => 본문 시작 18mm
MARGIN_HEADER = round(6 * MM)
MARGIN_BOTTOM = round(10 * MM)           # 아래 10mm + 꼬리말 8mm => 본문 끝 18mm
MARGIN_FOOTER = round(8 * MM)
TEXT_W = PAGE_W - 2 * MARGIN_LR          # 48190
BODY_H = PAGE_H - MARGIN_TOP - MARGIN_HEADER - MARGIN_BOTTOM - MARGIN_FOOTER
FIG_MAX_H = int(BODY_H * 0.56)           # 그림 한 장이 제목과 함께 한 쪽에 들어가도록 높이 제한

COL = {k: v.upper() for k, v in C.COLORS.items()}
WHITE = "#FFFFFF"
FOOTER_TEXT = "%s %s" % (C.META["school"], C.META["title"])

NS_DECL = (
    'xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" '
    'xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph" '
    'xmlns:hp10="http://www.hancom.co.kr/hwpml/2016/paragraph" '
    'xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section" '
    'xmlns:hc="http://www.hancom.co.kr/hwpml/2011/core" '
    'xmlns:hh="http://www.hancom.co.kr/hwpml/2011/head" '
    'xmlns:hhs="http://www.hancom.co.kr/hwpml/2011/history" '
    'xmlns:hm="http://www.hancom.co.kr/hwpml/2011/master-page" '
    'xmlns:hpf="http://www.hancom.co.kr/schema/2011/hpf" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" '
    'xmlns:opf="http://www.idpf.org/2007/opf/" '
    'xmlns:ooxmlchart="http://www.hancom.co.kr/hwpml/2016/ooxmlchart" '
    'xmlns:hwpunitchar="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar" '
    'xmlns:epub="http://www.idpf.org/2007/ops" '
    'xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"'
)
XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
LANGS = ("hangul", "latin", "hanja", "japanese", "other", "symbol", "user")
FONT_LANGS = ("HANGUL", "LATIN", "HANJA", "JAPANESE", "OTHER", "SYMBOL", "USER")
HWPUNITCHAR_NS = "http://www.hancom.co.kr/hwpml/2016/HwpUnitChar"


def x(s):
    return escape(str(s), {'"': "&quot;"})


# ─────────────────────────────────────────────── 서식 레지스트리 (header.xml 로 직렬화)
class Registry:
    def __init__(self):
        # borderFill 은 1부터  (한글 저장본과 같이 1 = 선 없음, 2 = 선 없음 + 빈 채우기)
        self.bf = []          # (key, xml_body)
        self.bf_index = {}
        self.cp = []
        self.cp_index = {}
        self.pp = []
        self.pp_index = {}
        self.border_fill(None, None, None, None, fill=None)                 # id 1
        self.border_fill(None, None, None, None, fill="none")               # id 2

    # borderFill ----------------------------------------------------------
    def border_fill(self, left, right, top, bottom, fill=None):
        """각 변은 None(없음) 또는 (굵기mm문자열, 색) ; fill 은 None 또는 '#RRGGBB' 또는 'none'"""
        key = (left, right, top, bottom, fill)
        if key in self.bf_index:
            return self.bf_index[key]
        bid = len(self.bf) + 1

        def side(tag, v):
            if v is None:
                return '<hh:%s type="NONE" width="0.1 mm" color="#000000"/>' % tag
            return '<hh:%s type="SOLID" width="%s" color="%s"/>' % (tag, v[0], v[1])

        body = (
            '<hh:slash type="NONE" Crooked="0" isCounter="0"/>'
            '<hh:backSlash type="NONE" Crooked="0" isCounter="0"/>'
            + side("leftBorder", left) + side("rightBorder", right)
            + side("topBorder", top) + side("bottomBorder", bottom)
            + '<hh:diagonal type="SOLID" width="0.1 mm" color="#000000"/>'
        )
        if fill is not None:
            body += ('<hc:fillBrush><hc:winBrush faceColor="%s" hatchColor="#000000" alpha="0"/>'
                     '</hc:fillBrush>' % fill)
        xml = ('<hh:borderFill id="%d" threeD="0" shadow="0" centerLine="NONE" breakCellSeparateLine="0">'
               '%s</hh:borderFill>' % (bid, body))
        self.bf.append(xml)
        self.bf_index[key] = bid
        return bid

    # charPr --------------------------------------------------------------
    def char(self, size, color=None, bold=False, spacing=0):
        color = (color or COL["text"]).upper()
        key = (int(size * 100), color, bool(bold), spacing)
        if key in self.cp_index:
            return self.cp_index[key]
        cid = len(self.cp)

        def per_lang(tag, val):
            return "<hh:%s %s/>" % (tag, " ".join('%s="%s"' % (l, val) for l in LANGS))

        xml = (
            '<hh:charPr id="%d" height="%d" textColor="%s" shadeColor="none" useFontSpace="0" '
            'useKerning="0" symMark="NONE" borderFillIDRef="2">' % (cid, key[0], color)
            + per_lang("fontRef", 0) + per_lang("ratio", 100) + per_lang("spacing", spacing)
            + per_lang("relSz", 100) + per_lang("offset", 0)
            + ("<hh:bold/>" if bold else "")
            + '<hh:underline type="NONE" shape="SOLID" color="#000000"/>'
              '<hh:strikeout shape="NONE" color="#000000"/><hh:outline type="NONE"/>'
              '<hh:shadow type="NONE" color="#C0C0C0" offsetX="10" offsetY="10"/></hh:charPr>'
        )
        self.cp.append(xml)
        self.cp_index[key] = cid
        return cid

    # paraPr --------------------------------------------------------------
    def para(self, align="JUSTIFY", line=160, left=0, right=0, indent=0, prev=0, nxt=0,
             keep_next=False, keep_lines=False, valign="BASELINE", border=None):
        """border 는 (borderFillID, offL, offR, offT, offB) 또는 None"""
        key = (align, line, left, right, indent, prev, nxt, keep_next, keep_lines, valign, border)
        if key in self.pp_index:
            return self.pp_index[key]
        pid = len(self.pp)

        def margin(mult):
            return ('<hh:margin><hc:intent value="%d" unit="HWPUNIT"/><hc:left value="%d" unit="HWPUNIT"/>'
                    '<hc:right value="%d" unit="HWPUNIT"/><hc:prev value="%d" unit="HWPUNIT"/>'
                    '<hc:next value="%d" unit="HWPUNIT"/></hh:margin>'
                    '<hh:lineSpacing type="PERCENT" value="%d" unit="HWPUNIT"/>'
                    % (indent * mult, left * mult, right * mult, prev * mult, nxt * mult, line))

        b = border or (1, 0, 0, 0, 0)
        xml = (
            '<hh:paraPr id="%d" tabPrIDRef="0" condense="0" fontLineHeight="0" snapToGrid="0" '
            'suppressLineNumbers="0" checked="0">' % pid
            + '<hh:align horizontal="%s" vertical="%s"/>' % (align, valign)
            + '<hh:heading type="NONE" idRef="0" level="0"/>'
            + '<hh:breakSetting breakLatinWord="KEEP_WORD" breakNonLatinWord="KEEP_WORD" widowOrphan="0" '
              'keepWithNext="%d" keepLines="%d" pageBreakBefore="0" lineWrap="BREAK"/>'
              % (int(keep_next), int(keep_lines))
            + '<hh:autoSpacing eAsianEng="0" eAsianNum="0"/>'
            + '<hp:switch><hp:case hp:required-namespace="%s">%s</hp:case><hp:default>%s</hp:default></hp:switch>'
              % (HWPUNITCHAR_NS, margin(1), margin(2))
            + '<hh:border borderFillIDRef="%d" offsetLeft="%d" offsetRight="%d" offsetTop="%d" '
              'offsetBottom="%d" connect="0" ignoreMargin="0"/>' % b
            + '</hh:paraPr>'
        )
        self.pp.append(xml)
        self.pp_index[key] = pid
        return pid


R = Registry()

# 자주 쓰는 서식 (등록 순서가 곧 id)
CP_DEFAULT = R.char(10.5)                                     # 0  바탕글
PP_DEFAULT = R.para()                                         # 0  바탕글
LINE = ("0.12 mm", COL["line"])


def cell_bf(fill=None, sides=(LINE, LINE, LINE, LINE)):
    l, r, t, b = sides
    return R.border_fill(l, r, t, b, fill=fill)


BF_TABLE = cell_bf(None)

# 본문
CP_BODY = R.char(10.5, COL["text"])
CP_BODY_B = R.char(10.5, COL["ink"], bold=True)
PP_BODY = R.para("JUSTIFY", 160, nxt=560)

# 글머리 목록
BUL_LEFT, BUL_HANG = 560, 820
CP_BUL_MARK = R.char(10.5, COL["del"], bold=True)
PP_BUL = R.para("JUSTIFY", 160, left=BUL_LEFT, indent=-BUL_HANG, nxt=220)
PP_BUL_LAST = R.para("JUSTIFY", 160, left=BUL_LEFT, indent=-BUL_HANG, nxt=600)

# 장 제목 (h1)
CP_H1_NUM = R.char(24, WHITE, bold=True)
CP_H1_NUM_SM = R.char(17, WHITE, bold=True)
CP_H1_TITLE = R.char(20, COL["ink"], bold=True, spacing=-3)
CP_H1_LEAD = R.char(11, COL["muted"])
PP_H1_HOLD = R.para("LEFT", 100, prev=0, nxt=900, keep_next=True)
PP_CELL_CENTER_TIGHT = R.para("CENTER", 100, valign="CENTER")
PP_H1_TITLE = R.para("LEFT", 120, nxt=240)
PP_H1_LEAD = R.para("LEFT", 150)

# 절 제목 (h2)
CP_H2_BAR = R.char(13, COL["del"], bold=True)
CP_H2 = R.char(13, COL["ink"], bold=True, spacing=-2)
PP_H2 = R.para("LEFT", 140, prev=1300, nxt=480, keep_next=True)
PP_H2_FIRST = R.para("LEFT", 140, prev=200, nxt=480, keep_next=True)

# 표
CP_TH = R.char(9.5, WHITE, bold=True)
CP_TD = R.char(9.5, COL["text"])
CP_TD_B = R.char(9.5, COL["ink"], bold=True)
PP_TD_L = R.para("LEFT", 140, valign="CENTER")
PP_TD_C = R.para("CENTER", 140, valign="CENTER")
PP_TBL_HOLD = R.para("LEFT", 100, prev=160, nxt=640)
PP_TBL_HOLD_NOTE = R.para("LEFT", 100, prev=160, nxt=140)
CP_NOTE = R.char(8.5, COL["muted"])
PP_NOTE = R.para("LEFT", 140, left=0, nxt=640)

# 강조 상자
CP_CO_TEXT = R.char(10, COL["text"])
CP_CO_TEXT_B = R.char(10, COL["ink"], bold=True)
PP_CO_TITLE = R.para("LEFT", 140, nxt=160)
PP_CO_TEXT = R.para("JUSTIFY", 160)

# 그림
PP_FIG = R.para("CENTER", 100, prev=300, nxt=160, keep_next=True)
CP_CAP = R.char(9, COL["muted"])
PP_CAP = R.para("CENTER", 130, nxt=700)

# 꼬리말
CP_FOOT = R.char(8.5, COL["muted"])
CP_FOOT_NUM = R.char(8.5, COL["ink"], bold=True)
PP_FOOT = R.para("RIGHT", 100)

# 목차와 요약 쪽
CP_KICK = R.char(9.5, COL["del"], bold=True, spacing=10)
CP_PAGE_TITLE = R.char(22, COL["ink"], bold=True, spacing=-3)
PP_KICK = R.para("LEFT", 100, nxt=200)
PP_PAGE_TITLE = R.para("LEFT", 110, nxt=500)
CP_TOC_NUM = R.char(13, COL["del"], bold=True)
CP_TOC_NUM_APX = R.char(11, COL["raon"], bold=True)
CP_TOC_TXT = R.char(12, COL["ink"])
CP_SUM_LABEL = R.char(10, COL["del"], bold=True)
CP_SUM_TXT = R.char(10, COL["text"])
CP_SUM_TXT_B = R.char(10, COL["ink"], bold=True)
PP_CELL_L = R.para("LEFT", 150, valign="CENTER")
PP_CELL_J = R.para("JUSTIFY", 150, valign="CENTER")
PP_CELL_C = R.para("CENTER", 120, valign="CENTER")
PP_SPACER = R.para("LEFT", 100, nxt=900)

TONE = {"ink": COL["ink"], "del": COL["del"], "raon": COL["raon"], "lead": COL["lead"], "ok": COL["ok"]}
TONE_LIGHT = {"ink": COL["soft"], "del": COL["del_l"], "raon": COL["raon_l"], "lead": COL["lead_l"],
              "ok": COL["ok_l"]}

# ─────────────────────────────────────────────── 문단과 런
_ids = {"obj": 1000000000, "z": 0}


def next_obj_id():
    _ids["obj"] += 7
    return _ids["obj"]


def next_z():
    _ids["z"] += 1
    return _ids["z"]


def run(cp, text=None):
    if text is None or text == "":
        return '<hp:run charPrIDRef="%d"/>' % cp
    return '<hp:run charPrIDRef="%d"><hp:t>%s</hp:t></hp:run>' % (cp, x(text))


def rich_runs(text, cp, cp_bold):
    """**굵게** 표기를 런으로 나눈다 (표기 기호는 지운다)"""
    parts = re.split(r"(\*\*.+?\*\*)", text)
    out = []
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append(run(cp_bold, part[2:-2]))
        else:
            out.append(run(cp, part))
    return "".join(out) or run(cp)


def plain(text):
    return text.replace("**", "")


def para(pp, runs_xml, style=0, page_break=False, pid="2147483648"):
    # linesegarray 는 넣지 않는다  한글이 열 때 줄 배치를 새로 계산하며,
    # 실제 배치와 다른 캐시 값은 글자 겹침의 원인이 된다
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="%d" pageBreak="%d" columnBreak="0" merged="0">'
            '%s</hp:p>' % (pid, pp, style, int(page_break), runs_xml))


# ─────────────────────────────────────────────── 높이 추정 (한글이 다시 계산하므로 근사치)
def text_width(text, size_pt):
    w = 0.0
    for ch in text:
        o = ord(ch)
        if o >= 0x1100 and not (0x2000 <= o <= 0x206F):
            w += 1.0
        elif ch == " ":
            w += 0.3
        else:
            w += 0.55
    return w * size_pt * 100


def est_lines(text, size_pt, width):
    if width <= 0:
        return 1
    return max(1, math.ceil(text_width(plain(text), size_pt) / (width * 0.97)))


# ─────────────────────────────────────────────── 표
class Cell:
    def __init__(self, paras_xml, bf, height_hint, valign="CENTER", header=False):
        self.paras = paras_xml
        self.bf = bf
        self.h = height_hint
        self.valign = valign
        self.header = header


def split_widths(percents, total=TEXT_W):
    s = float(sum(percents))
    ws = [int(total * p / s) for p in percents]
    ws[-1] += total - sum(ws)
    return ws


def table_xml(rows, widths, margin=(510, 510, 340, 340), repeat_header=True, bf=None, min_row_h=0):
    """rows : [[Cell,...],...] ; margin : 셀 안 여백 (좌, 우, 위, 아래)"""
    ml, mr, mt, mb = margin
    heights = []
    for r in rows:
        h = max(c.h for c in r) + mt + mb
        heights.append(max(h, min_row_h))
    trs = []
    for ri, r in enumerate(rows):
        tcs = []
        for ci, c in enumerate(r):
            tcs.append(
                '<hp:tc name="" header="%d" hasMargin="1" protect="0" editable="0" dirty="0" borderFillIDRef="%d">'
                '<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="%s" linkListIDRef="0" '
                'linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">%s</hp:subList>'
                '<hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="1" rowSpan="1"/>'
                '<hp:cellSz width="%d" height="%d"/>'
                '<hp:cellMargin left="%d" right="%d" top="%d" bottom="%d"/></hp:tc>'
                % (int(c.header), c.bf, c.valign, "".join(c.paras), ci, ri, widths[ci], heights[ri],
                   ml, mr, mt, mb))
        trs.append("<hp:tr>%s</hp:tr>" % "".join(tcs))
    return (
        '<hp:tbl id="%d" zOrder="%d" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" '
        'lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="%d" rowCnt="%d" colCnt="%d" '
        'cellSpacing="0" borderFillIDRef="%d" noAdjust="0">'
        '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
        '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" '
        'vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
        '<hp:outMargin left="0" right="0" top="0" bottom="0"/>'
        '<hp:inMargin left="%d" right="%d" top="%d" bottom="%d"/>%s</hp:tbl>'
        % (next_obj_id(), next_z(), int(repeat_header), len(rows), len(widths), bf or BF_TABLE,
           sum(widths), sum(heights), ml, mr, mt, mb, "".join(trs))
    )


def holder(tbl, pp=PP_TBL_HOLD, page_break=False):
    """표/그림을 담는 문단  (한글 저장본과 같이 개체 뒤에 빈 hp:t)"""
    return para(pp, '<hp:run charPrIDRef="%d">%s<hp:t/></hp:run>' % (CP_BODY, tbl), page_break=page_break)


def cell_paras(text, cp, cp_b, pp, size, width):
    """셀 글  \\n 은 문단 나눔"""
    lines = str(text).split("\n")
    xmls, h = [], 0
    for ln in lines:
        xmls.append(para(pp, rich_runs(ln, cp, cp_b) if ln else run(cp)))
        h += est_lines(ln, size, width) * size * 100 * 1.32
    return xmls, int(h)


# ─────────────────────────────────────────────── 블록 렌더러
def render_h1(num, title, lead, page_break):
    num_w = round(26 * MM)
    widths = [num_w, TEXT_W - num_w]
    rule = ("0.5 mm", COL["del"])
    bf_num = R.border_fill(None, None, None, rule, fill=COL["ink"] if num == "부록" else COL["del"])
    bf_title = R.border_fill(None, None, None, rule, fill=None)
    cp_num = CP_H1_NUM_SM if len(num) > 1 else CP_H1_NUM
    num_cell = Cell([para(PP_CELL_CENTER_TIGHT, run(cp_num, num))], bf_num, 2400)
    tw = widths[1] - 1400 - 400
    title_h = est_lines(title, 20, tw) * 2000 * 1.25 + 240
    lead_h = est_lines(lead, 11, tw) * 1100 * 1.5
    title_cell = Cell([para(PP_H1_TITLE, run(CP_H1_TITLE, title)),
                       para(PP_H1_LEAD, run(CP_H1_LEAD, lead))], bf_title, int(title_h + lead_h))
    tbl = table_xml([[num_cell, title_cell]], widths, margin=(1400, 400, 700, 700), repeat_header=False)
    return holder(tbl, PP_H1_HOLD, page_break)


def render_h2(title, first=False, page_break=False):
    return para(PP_H2_FIRST if first else PP_H2,
                run(CP_H2_BAR, "▍") + run(CP_H2, title), style=3, page_break=page_break)


def render_p(text, page_break=False):
    return para(PP_BODY, rich_runs(text, CP_BODY, CP_BODY_B), style=1, page_break=page_break)


def render_bullets(items, page_break=False):
    out = []
    for i, it in enumerate(items):
        pp = PP_BUL_LAST if i == len(items) - 1 else PP_BUL
        out.append(para(pp, run(CP_BUL_MARK, "•  ") + rich_runs(it, CP_BODY, CP_BODY_B),
                        page_break=page_break and i == 0))
    return "".join(out)


def header_fill(tone, ci):
    if tone == "split":
        return [COL["ink"], COL["del"], COL["raon"]][ci] if ci < 3 else COL["ink"]
    if tone == "split2":
        return [COL["del"], COL["raon"]][ci] if ci < 2 else COL["ink"]
    return TONE.get(tone, COL["ink"])


def render_table(spec, page_break=False):
    cols, rows = spec["cols"], spec["rows"]
    tone = spec.get("tone", "ink")
    widths = split_widths(spec.get("widths") or [1] * len(cols))
    ml, mr, mt, mb = 450, 450, 300, 300
    # 짧은 글만 있는 열은 가운데 정렬
    center = []
    for ci in range(len(cols)):
        vals = [str(r[ci]) for r in rows]
        center.append(all(len(plain(v).strip()) <= 7 and "\n" not in v for v in vals))
    first_bold = tone != "split2"
    out_rows = []
    hdr = []
    for ci, name in enumerate(cols):
        ps, h = cell_paras(name, CP_TH, CP_TH, PP_TD_C, 9.5, widths[ci] - ml - mr)
        hdr.append(Cell(ps, cell_bf(header_fill(tone, ci)), h, header=True))
    out_rows.append(hdr)
    for ri, r in enumerate(rows):
        fill = COL["soft"] if ri % 2 == 1 else None
        cells = []
        for ci, val in enumerate(r):
            bold_col = first_bold and ci == 0
            cp = CP_TD_B if bold_col else CP_TD
            pp = PP_TD_C if center[ci] else PP_TD_L
            ps, h = cell_paras(val, cp, CP_TD_B, pp, 9.5, widths[ci] - ml - mr)
            cells.append(Cell(ps, cell_bf(fill), h))
        out_rows.append(cells)
    tbl = table_xml(out_rows, widths, margin=(ml, mr, mt, mb))
    note = spec.get("note")
    if note:
        return (holder(tbl, PP_TBL_HOLD_NOTE, page_break)
                + para(PP_NOTE, run(CP_NOTE, "※ " + note)))
    return holder(tbl, PP_TBL_HOLD, page_break)


def render_callout(tone, title, text, page_break=False):
    color = TONE.get(tone, COL["ink"])
    light = TONE_LIGHT.get(tone, COL["soft"])
    bf = R.border_fill(("1.5 mm", color), None, None, None, fill=light)
    cp_title = R.char(10.5, color, bold=True)
    ml, mr, mt, mb = 1100, 900, 650, 650
    w = TEXT_W - ml - mr
    h = 1050 * 1.4 + 160 + est_lines(text, 10, w) * 1000 * 1.6
    c = Cell([para(PP_CO_TITLE, run(cp_title, title)),
              para(PP_CO_TEXT, rich_runs(text, CP_CO_TEXT, CP_CO_TEXT_B))], bf, int(h))
    tbl = table_xml([[c]], [TEXT_W], margin=(ml, mr, mt, mb), repeat_header=False, bf=bf)
    return holder(tbl, PP_TBL_HOLD, page_break)


# ─────────────────────────────────────────────── 그림
class Images:
    def __init__(self):
        self.items = []   # (item_id, arcname, bytes)

    def add(self, path):
        with open(path, "rb") as f:
            data = f.read()
        im = Image.open(io.BytesIO(data))
        px_w, px_h = im.size
        dpi = im.info.get("dpi", (96, 96))[0] or 96
        try:
            dpi = float(dpi)
        except Exception:
            dpi = 96.0
        if dpi < 50:
            dpi = 96.0
        ext = os.path.splitext(path)[1].lower().lstrip(".")
        if ext == "jpeg":
            ext = "jpg"
        n = len(self.items) + 1
        item_id = "image%d" % n
        self.items.append((item_id, "BinData/%s.%s" % (item_id, ext), data, ext))
        return item_id, px_w, px_h, dpi


IMAGES = Images()


def pic_xml(item_id, px_w, px_h, dpi, w, h, inline=True, comment=""):
    org_w = int(round(px_w * 7200 / dpi))
    org_h = int(round(px_h * 7200 / dpi))
    sx, sy = w / float(org_w), h / float(org_h)
    if inline:
        wrap = "TOP_AND_BOTTOM"
        pos = ('<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" '
               'holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" '
               'vertOffset="0" horzOffset="0"/>')
    else:
        wrap = "BEHIND_TEXT"
        pos = ('<hp:pos treatAsChar="0" affectLSpacing="0" flowWithText="0" allowOverlap="1" '
               'holdAnchorAndSO="0" vertRelTo="PAPER" horzRelTo="PAPER" vertAlign="TOP" horzAlign="LEFT" '
               'vertOffset="0" horzOffset="0"/>')
    return (
        '<hp:pic id="%d" zOrder="%d" numberingType="PICTURE" textWrap="%s" textFlow="BOTH_SIDES" lock="0" '
        'dropcapstyle="None" href="" groupLevel="0" instid="%d" reverse="0">'
        '<hp:offset x="0" y="0"/><hp:orgSz width="%d" height="%d"/><hp:curSz width="%d" height="%d"/>'
        '<hp:flip horizontal="0" vertical="0"/>'
        '<hp:rotationInfo angle="0" centerX="%d" centerY="%d" rotateimage="1"/>'
        '<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
        '<hc:scaMatrix e1="%.6f" e2="0" e3="0" e4="0" e5="%.6f" e6="0"/>'
        '<hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
        '<hc:img binaryItemIDRef="%s" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/>'
        '<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="%d" y="0"/><hc:pt2 x="%d" y="%d"/><hc:pt3 x="0" y="%d"/>'
        '</hp:imgRect><hp:imgClip left="0" right="%d" top="0" bottom="%d"/>'
        '<hp:inMargin left="0" right="0" top="0" bottom="0"/><hp:imgDim dimwidth="%d" dimheight="%d"/>'
        '<hp:effects/><hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
        '%s<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:shapeComment>%s</hp:shapeComment></hp:pic>'
        % (next_obj_id(), next_z(), wrap, next_obj_id(), org_w, org_h, w, h, w // 2, h // 2, sx, sy, item_id,
           org_w, org_w, org_h, org_h, org_w, org_h, org_w, org_h, w, h, pos, x(comment))
    )


def render_figure(fig_id, caption, figdir, page_break=False):
    path = os.path.join(figdir, fig_id + ".png")
    if not os.path.exists(path):
        print("  [경고] 그림 없음 : %s  (자리 표시 문단으로 대체)" % path)
        return (para(PP_FIG, run(CP_CAP, "[그림 자리  %s]" % fig_id), page_break=page_break)
                + para(PP_CAP, run(CP_CAP, caption), style=9))
    item_id, pw, ph, dpi = IMAGES.add(path)
    w = TEXT_W
    h = int(round(w * ph / float(pw)))
    if h > FIG_MAX_H:
        h = FIG_MAX_H
        w = int(round(h * pw / float(ph)))
    pic = pic_xml(item_id, pw, ph, dpi, w, h, inline=True, comment=caption)
    return (para(PP_FIG, '<hp:run charPrIDRef="%d">%s<hp:t/></hp:run>' % (CP_CAP, pic), page_break=page_break)
            + para(PP_CAP, run(CP_CAP, caption), style=9))


# ─────────────────────────────────────────────── 쪽 설정 (첫 문단)
def sec_pr_xml():
    return (
        '<hp:secPr id="" textDirection="HORIZONTAL" spaceColumns="1134" tabStop="8000" tabStopVal="4000" '
        'tabStopUnit="HWPUNIT" outlineShapeIDRef="0" memoShapeIDRef="0" textVerticalWidthHead="0" '
        'masterPageCnt="0">'
        '<hp:grid lineGrid="0" charGrid="0" wonggojiFormat="0"/>'
        '<hp:startNum pageStartsOn="BOTH" page="0" pic="0" tbl="0" equation="0"/>'
        # 첫 쪽(표지)에는 머리말 꼬리말 쪽 번호를 감춘다
        '<hp:visibility hideFirstHeader="1" hideFirstFooter="1" hideFirstMasterPage="1" border="SHOW_ALL" '
        'fill="SHOW_ALL" hideFirstPageNum="1" hideFirstEmptyLine="1" showLineNumber="0"/>'
        '<hp:lineNumberShape restartType="0" countBy="0" distance="0" startNumber="0"/>'
        '<hp:pagePr landscape="WIDELY" width="%d" height="%d" gutterType="LEFT_RIGHT">'
        '<hp:margin header="%d" footer="%d" gutter="0" left="%d" right="%d" top="%d" bottom="%d"/></hp:pagePr>'
        '<hp:footNotePr><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" suffixChar=")" supscript="0"/>'
        '<hp:noteLine length="-1" type="SOLID" width="0.12 mm" color="#000000"/>'
        '<hp:noteSpacing betweenNotes="284" belowLine="568" aboveLine="852"/>'
        '<hp:numbering type="CONTINUOUS" newNum="1"/><hp:placement place="EACH_COLUMN" beneathText="0"/>'
        '</hp:footNotePr>'
        '<hp:endNotePr><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" suffixChar=")" supscript="0"/>'
        '<hp:noteLine length="0" type="NONE" width="0.12 mm" color="#000000"/>'
        '<hp:noteSpacing betweenNotes="0" belowLine="576" aboveLine="864"/>'
        '<hp:numbering type="CONTINUOUS" newNum="1"/><hp:placement place="END_OF_DOCUMENT" beneathText="0"/>'
        '</hp:endNotePr>'
        '<hp:pageBorderFill type="BOTH" borderFillIDRef="1" textBorder="PAPER" headerInside="0" footerInside="0" '
        'fillArea="PAPER"><hp:offset left="1417" right="1417" top="1417" bottom="1417"/></hp:pageBorderFill>'
        '<hp:pageBorderFill type="EVEN" borderFillIDRef="1" textBorder="PAPER" headerInside="0" footerInside="0" '
        'fillArea="PAPER"><hp:offset left="1417" right="1417" top="1417" bottom="1417"/></hp:pageBorderFill>'
        '<hp:pageBorderFill type="ODD" borderFillIDRef="1" textBorder="PAPER" headerInside="0" footerInside="0" '
        'fillArea="PAPER"><hp:offset left="1417" right="1417" top="1417" bottom="1417"/></hp:pageBorderFill>'
        '</hp:secPr>'
        % (PAGE_W, PAGE_H, MARGIN_HEADER, MARGIN_FOOTER, MARGIN_LR, MARGIN_LR, MARGIN_TOP, MARGIN_BOTTOM)
    )


def footer_ctrl_xml():
    body = para(
        PP_FOOT,
        run(CP_FOOT, FOOTER_TEXT + "   |   ")
        + '<hp:run charPrIDRef="%d"><hp:ctrl><hp:autoNum num="1" numType="PAGE">'
          '<hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" suffixChar="" supscript="0"/>'
          '</hp:autoNum></hp:ctrl><hp:t/></hp:run>' % CP_FOOT_NUM,
        style=4, pid="0")
    return (
        '<hp:ctrl><hp:footer id="1" applyPageType="BOTH">'
        '<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="BOTTOM" linkListIDRef="0" '
        'linkListNextIDRef="0" textWidth="%d" textHeight="%d" hasTextRef="0" hasNumRef="0">%s</hp:subList>'
        '</hp:footer></hp:ctrl>' % (TEXT_W, MARGIN_FOOTER, body)
    )


def first_paragraph(figdir):
    """쪽 설정 + 단 설정 + 꼬리말 + 표지 그림(종이 기준 전면 배치, 글 뒤)"""
    runs = ('<hp:run charPrIDRef="%d">%s<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="1" '
            'sameSz="1" sameGap="0"/></hp:ctrl></hp:run>' % (CP_DEFAULT, sec_pr_xml()))
    runs += '<hp:run charPrIDRef="%d">%s<hp:t/></hp:run>' % (CP_DEFAULT, footer_ctrl_xml())
    cover = os.path.join(figdir, "cover.png")
    if os.path.exists(cover):
        item_id, pw, ph, dpi = IMAGES.add(cover)
        pic = pic_xml(item_id, pw, ph, dpi, PAGE_W, PAGE_H, inline=False, comment="표지")
        runs += '<hp:run charPrIDRef="%d">%s<hp:t/></hp:run>' % (CP_DEFAULT, pic)
    else:
        print("  [경고] 표지 그림 없음 : %s  (글자 표지로 대체)" % cover)
        runs += run(CP_PAGE_TITLE, C.META["title"])
    return para(PP_DEFAULT, runs, pid="0")


# ─────────────────────────────────────────────── 목차와 핵심 요약 쪽
def render_front():
    out = []
    out.append(para(PP_KICK, run(CP_KICK, "CONTENTS"), page_break=True))
    out.append(para(PP_PAGE_TITLE, run(CP_PAGE_TITLE, "목차")))
    num_w = round(22 * MM)
    widths = [num_w, TEXT_W - num_w]
    row_line = ("0.12 mm", COL["line"])
    bf_row = R.border_fill(None, None, None, row_line)
    bf_top = R.border_fill(None, None, ("0.4 mm", COL["ink"]), row_line)
    rows = []
    for i, (num, title) in enumerate(C.TOC):
        bf = bf_top if i == 0 else bf_row
        cpn = CP_TOC_NUM_APX if num == "부록" else CP_TOC_NUM
        rows.append([Cell([para(PP_CELL_C, run(cpn, num))], bf, 1300),
                     Cell([para(PP_CELL_L, run(CP_TOC_TXT, title))], bf, 1300)])
    out.append(holder(table_xml(rows, widths, margin=(400, 400, 420, 420), repeat_header=False,
                                bf=BF_TABLE), R.para("LEFT", 100, nxt=1600)))

    out.append(para(PP_KICK, run(CP_KICK, "SUMMARY")))
    out.append(para(PP_PAGE_TITLE, run(CP_PAGE_TITLE, "핵심 요약")))
    lab_w = round(30 * MM)
    widths = [lab_w, TEXT_W - lab_w]
    bf_lab = cell_bf(COL["del_l"])
    bf_txt = cell_bf(None)
    rows = []
    ml, mr = 600, 600
    for label, text in C.SUMMARY:
        ps, h = cell_paras(text, CP_SUM_TXT, CP_SUM_TXT_B, PP_CELL_J, 10, widths[1] - ml - mr)
        rows.append([Cell([para(PP_CELL_C, run(CP_SUM_LABEL, label))], bf_lab, h),
                     Cell(ps, bf_txt, h)])
    out.append(holder(table_xml(rows, widths, margin=(ml, mr, 520, 520), repeat_header=False),
                      PP_TBL_HOLD))
    return "".join(out)


# ─────────────────────────────────────────────── 본문
def render_body(figdir):
    out = []
    pending_break = True        # 목차 쪽 다음 첫 장은 새 쪽에서
    after_h1 = False
    for blk in C.BLOCKS:
        kind = blk[0]
        pb = pending_break
        if kind == "pagebreak":
            pending_break = True
            continue
        pending_break = False
        if kind == "h1":
            out.append(render_h1(blk[1], blk[2], blk[3], pb))
            after_h1 = True
            continue
        if kind == "h2":
            out.append(render_h2(blk[1], first=after_h1, page_break=pb))
        elif kind == "p":
            out.append(render_p(blk[1], pb))
        elif kind == "bullets":
            out.append(render_bullets(blk[1], pb))
        elif kind == "table":
            out.append(render_table(blk[1], pb))
        elif kind == "figure":
            out.append(render_figure(blk[1], blk[2], figdir, pb))
        elif kind == "callout":
            out.append(render_callout(blk[1], blk[2], blk[3], pb))
        else:
            raise ValueError("알 수 없는 블록 : %r" % (kind,))
        after_h1 = False
    return "".join(out)


# ─────────────────────────────────────────────── header.xml
STYLES = [
    # (이름, 영문, paraPr, charPr)
    ("바탕글", "Normal", PP_DEFAULT, CP_DEFAULT),
    ("본문", "Body", PP_BODY, CP_BODY),
    ("개요 1", "Outline 1", PP_DEFAULT, CP_DEFAULT),
    ("개요 2", "Outline 2", PP_H2, CP_H2),
    ("쪽 번호", "Page Number", PP_FOOT, CP_FOOT),
    ("머리말", "Header", PP_FOOT, CP_FOOT),
    ("각주", "Footnote", PP_NOTE, CP_NOTE),
    ("미주", "Endnote", PP_NOTE, CP_NOTE),
    ("메모", "Memo", PP_NOTE, CP_NOTE),
    ("캡션", "Caption", PP_CAP, CP_CAP),
]


def header_xml():
    fonts = "".join(
        '<hh:fontface lang="%s" fontCnt="1"><hh:font id="0" face="맑은 고딕" type="TTF" isEmbedded="0">'
        '<hh:typeInfo familyType="FCAT_GOTHIC" weight="5" proportion="3" contrast="2" strokeVariation="0" '
        'armStyle="0" letterform="2" midline="0" xHeight="4"/></hh:font></hh:fontface>' % lang
        for lang in FONT_LANGS)
    styles = "".join(
        '<hh:style id="%d" type="PARA" name="%s" engName="%s" paraPrIDRef="%d" charPrIDRef="%d" '
        'nextStyleIDRef="%d" langID="1042" lockForm="0"/>' % (i, n, e, pp, cp, i)
        for i, (n, e, pp, cp) in enumerate(STYLES))
    return (
        XML_DECL + '<hh:head %s version="1.5" secCnt="1">' % NS_DECL
        + '<hh:beginNum page="1" footnote="1" endnote="1" pic="1" tbl="1" equation="1"/>'
        + '<hh:refList>'
        + '<hh:fontfaces itemCnt="%d">%s</hh:fontfaces>' % (len(FONT_LANGS), fonts)
        + '<hh:borderFills itemCnt="%d">%s</hh:borderFills>' % (len(R.bf), "".join(R.bf))
        + '<hh:charProperties itemCnt="%d">%s</hh:charProperties>' % (len(R.cp), "".join(R.cp))
        + '<hh:tabProperties itemCnt="2"><hh:tabPr id="0" autoTabLeft="0" autoTabRight="0"/>'
          '<hh:tabPr id="1" autoTabLeft="1" autoTabRight="0"/></hh:tabProperties>'
        + '<hh:paraProperties itemCnt="%d">%s</hh:paraProperties>' % (len(R.pp), "".join(R.pp))
        + '<hh:styles itemCnt="%d">%s</hh:styles>' % (len(STYLES), styles)
        + '</hh:refList>'
        + '<hh:compatibleDocument targetProgram="HWP201X"><hh:layoutCompatibility/></hh:compatibleDocument>'
        + '<hh:docOption><hh:linkinfo path="" pageInherit="1" footnoteInherit="0"/></hh:docOption>'
        + '<hh:trackchageConfig flags="56"/>'
        + '</hh:head>'
    )


# ─────────────────────────────────────────────── 패키지 부속 파일
VERSION_XML = (XML_DECL + '<hv:HCFVersion xmlns:hv="http://www.hancom.co.kr/hwpml/2011/version" '
               'tagetApplication="WORDPROCESSOR" major="5" minor="1" micro="1" buildNumber="0" os="1" '
               'xmlVersion="1.5" application="Hancom Office Hangul" appVersion="12, 0, 0, 3288 WIN32LEWindows_10"/>')

SETTINGS_XML = (
    XML_DECL + '<ha:HWPApplicationSetting xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" '
    'xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0">'
    '<ha:CaretPosition listIDRef="0" paraIDRef="0" pos="0"/>'
    '<config:config-item-set name="PrintInfo">'
    '<config:config-item name="PrintAutoFootNote" type="boolean">false</config:config-item>'
    '<config:config-item name="PrintAutoHeadNote" type="boolean">false</config:config-item>'
    '<config:config-item name="PrintMethod" type="short">0</config:config-item>'
    '<config:config-item name="OverlapSize" type="short">0</config:config-item>'
    '<config:config-item name="PrintCropMark" type="short">0</config:config-item>'
    '<config:config-item name="BinderHoleType" type="short">0</config:config-item>'
    '<config:config-item name="ZoomX" type="short">100</config:config-item>'
    '<config:config-item name="ZoomY" type="short">100</config:config-item>'
    '</config:config-item-set></ha:HWPApplicationSetting>')

CONTAINER_XML = (
    XML_DECL + '<ocf:container xmlns:ocf="urn:oasis:names:tc:opendocument:xmlns:container" '
    'xmlns:hpf="http://www.hancom.co.kr/schema/2011/hpf"><ocf:rootfiles>'
    '<ocf:rootfile full-path="Contents/content.hpf" media-type="application/hwpml-package+xml"/>'
    '<ocf:rootfile full-path="Preview/PrvText.txt" media-type="text/plain"/>'
    '<ocf:rootfile full-path="META-INF/container.rdf" media-type="application/rdf+xml"/>'
    '</ocf:rootfiles></ocf:container>')

CONTAINER_RDF = (
    XML_DECL + '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
    '<rdf:Description rdf:about=""><ns0:hasPart xmlns:ns0="http://www.hancom.co.kr/hwpml/2016/meta/pkg#" '
    'rdf:resource="Contents/header.xml"/></rdf:Description>'
    '<rdf:Description rdf:about="Contents/header.xml"><rdf:type '
    'rdf:resource="http://www.hancom.co.kr/hwpml/2016/meta/pkg#HeaderFile"/></rdf:Description>'
    '<rdf:Description rdf:about=""><ns0:hasPart xmlns:ns0="http://www.hancom.co.kr/hwpml/2016/meta/pkg#" '
    'rdf:resource="Contents/section0.xml"/></rdf:Description>'
    '<rdf:Description rdf:about="Contents/section0.xml"><rdf:type '
    'rdf:resource="http://www.hancom.co.kr/hwpml/2016/meta/pkg#SectionFile"/></rdf:Description>'
    '<rdf:Description rdf:about=""><rdf:type rdf:resource="http://www.hancom.co.kr/hwpml/2016/meta/pkg#Document"/>'
    '</rdf:Description></rdf:RDF>')

MANIFEST_XML = XML_DECL + '<odf:manifest xmlns:odf="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"/>'

MEDIA = {"png": "image/png", "jpg": "image/jpg", "bmp": "image/bmp", "gif": "image/gif"}


def content_hpf():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    items = '<opf:item id="header" href="Contents/header.xml" media-type="application/xml"/>'
    for item_id, arc, _data, ext in IMAGES.items:
        items += ('<opf:item id="%s" href="%s" media-type="%s" isEmbeded="1"/>'
                  % (item_id, arc, MEDIA.get(ext, "image/" + ext)))
    items += ('<opf:item id="section0" href="Contents/section0.xml" media-type="application/xml"/>'
              '<opf:item id="settings" href="settings.xml" media-type="application/xml"/>')
    return (
        XML_DECL + '<opf:package %s version="" unique-identifier="" id="">' % NS_DECL
        + '<opf:metadata><opf:title>%s</opf:title><opf:language>ko</opf:language>'
          % x("%s %s" % (C.META["school"], C.META["title"]))
        + '<opf:meta name="creator" content="text">%s</opf:meta>' % x("%s %s" % (C.META["school"], C.META["dept"]))
        + '<opf:meta name="subject" content="text">%s</opf:meta>' % x(C.META["subtitle"])
        + '<opf:meta name="description" content="text">%s</opf:meta>' % x(C.META["year"] + " " + C.META["title"])
        + '<opf:meta name="lastsaveby" content="text">%s</opf:meta>' % x(C.META["dept"])
        + '<opf:meta name="CreatedDate" content="text">%s</opf:meta>' % now
        + '<opf:meta name="ModifiedDate" content="text">%s</opf:meta>' % now
        + '<opf:meta name="date" content="text">%s</opf:meta>' % x(C.META["date"])
        + '<opf:meta name="keyword" content="text">%s</opf:meta>' % x(", ".join(C.META["keywords"]))
        + '</opf:metadata><opf:manifest>%s</opf:manifest>' % items
        + '<opf:spine><opf:itemref idref="header" linear="yes"/><opf:itemref idref="section0" linear="yes"/>'
          '</opf:spine></opf:package>'
    )


def preview_text():
    lines = [C.META["school"], C.META["year"] + " " + C.META["title"], C.META["subtitle"], "",
             C.META["date"] + "  " + C.META["dept"], "", "목차"]
    lines += ["%s  %s" % t for t in C.TOC]
    lines += ["", "핵심 요약"]
    lines += ["%s  %s" % (a, plain(b)) for a, b in C.SUMMARY]
    txt = "\r\n".join(lines)
    return txt[:2000]


def preview_image(figdir):
    cover = os.path.join(figdir, "cover.png")
    if not os.path.exists(cover):
        return None
    im = Image.open(cover).convert("RGB")
    im.thumbnail((724, 1024), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return buf.getvalue()


# ─────────────────────────────────────────────── 검증
HP = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"
HH = "{http://www.hancom.co.kr/hwpml/2011/head}"
HC = "{http://www.hancom.co.kr/hwpml/2011/core}"


def validate(parts, bin_names):
    errors = []
    trees = {}
    for name, data in parts.items():
        if name.endswith(".xml") or name.endswith(".hpf") or name.endswith(".rdf"):
            try:
                trees[name] = etree.fromstring(data)
            except etree.XMLSyntaxError as e:
                errors.append("XML 오류 %s : %s" % (name, e))
    if errors:
        return errors
    head = trees["Contents/header.xml"]
    sec = trees["Contents/section0.xml"]

    # itemCnt
    for tag, child in (("fontfaces", "fontface"), ("borderFills", "borderFill"),
                       ("charProperties", "charPr"), ("tabProperties", "tabPr"),
                       ("paraProperties", "paraPr"), ("styles", "style")):
        el = head.find(".//" + HH + tag)
        n = len(el.findall(HH + child))
        if int(el.get("itemCnt")) != n:
            errors.append("itemCnt 불일치 %s : %s != %d" % (tag, el.get("itemCnt"), n))
        ids = [int(c.get("id")) for c in el.findall(HH + child)] if child != "fontface" else []
        start = 1 if child == "borderFill" else 0
        if ids and ids != list(range(start, start + len(ids))):
            errors.append("id 가 연속이 아님 : %s" % tag)
    for ff in head.iter(HH + "fontface"):
        if int(ff.get("fontCnt")) != len(ff.findall(HH + "font")):
            errors.append("fontCnt 불일치 %s" % ff.get("lang"))

    def ids_of(tag):
        return {c.get("id") for c in head.iter(HH + tag)}

    bf, cp, pp, st = ids_of("borderFill"), ids_of("charPr"), ids_of("paraPr"), ids_of("style")
    # header 내부 참조
    for c in head.iter(HH + "charPr"):
        if c.get("borderFillIDRef") not in bf:
            errors.append("charPr borderFillIDRef 없음 %s" % c.get("id"))
    for b in head.iter(HH + "border"):
        if b.get("borderFillIDRef") not in bf:
            errors.append("paraPr border borderFillIDRef 없음")
    for s in head.iter(HH + "style"):
        if s.get("paraPrIDRef") not in pp or s.get("charPrIDRef") not in cp or s.get("nextStyleIDRef") not in st:
            errors.append("style 참조 오류 %s" % s.get("name"))
    # 본문 참조
    for p in sec.iter(HP + "p"):
        if p.get("paraPrIDRef") not in pp:
            errors.append("paraPrIDRef 없음 %s" % p.get("paraPrIDRef"))
        if p.get("styleIDRef") not in st:
            errors.append("styleIDRef 없음 %s" % p.get("styleIDRef"))
    for r in sec.iter(HP + "run"):
        if r.get("charPrIDRef") not in cp:
            errors.append("charPrIDRef 없음 %s" % r.get("charPrIDRef"))
    for tag in ("tbl", "tc", "pageBorderFill"):
        for e in sec.iter(HP + tag):
            if e.get("borderFillIDRef") not in bf:
                errors.append("%s borderFillIDRef 없음 %s" % (tag, e.get("borderFillIDRef")))
    # 표 구조
    for t in sec.iter(HP + "tbl"):
        trs = t.findall(HP + "tr")
        if int(t.get("rowCnt")) != len(trs):
            errors.append("rowCnt 불일치")
        for ri, tr in enumerate(trs):
            tcs = tr.findall(HP + "tc")
            if len(tcs) != int(t.get("colCnt")):
                errors.append("colCnt 불일치")
            for ci, tc in enumerate(tcs):
                order = [etree.QName(c).localname for c in tc]
                if order != ["subList", "cellAddr", "cellSpan", "cellSz", "cellMargin"]:
                    errors.append("tc 자식 순서 오류 %s" % order)
                a = tc.find(HP + "cellAddr")
                if (int(a.get("rowAddr")), int(a.get("colAddr"))) != (ri, ci):
                    errors.append("cellAddr 오류")
        order = [etree.QName(c).localname for c in t if etree.QName(c).localname != "tr"]
        if order != ["sz", "pos", "outMargin", "inMargin"]:
            errors.append("tbl 자식 순서 오류 %s" % order)
    # 그림 참조
    manifest = trees["Contents/content.hpf"]
    OPF = "{http://www.idpf.org/2007/opf/}"
    items = {i.get("id"): i.get("href") for i in manifest.iter(OPF + "item")}
    for img in sec.iter(HC + "img"):
        ref = img.get("binaryItemIDRef")
        if ref not in items:
            errors.append("binaryItemIDRef 가 manifest 에 없음 %s" % ref)
    for href in items.values():
        if href not in parts and href not in bin_names:
            errors.append("manifest 항목 파일 없음 %s" % href)
    for b in bin_names:
        if b not in items.values():
            errors.append("BinData 가 manifest 에 없음 %s" % b)
    # 표기 원칙  쌍따옴표와 문장 끝 온점 금지
    for t in sec.iter(HP + "t"):
        s = t.text or ""
        if '"' in s:
            errors.append("쌍따옴표 발견 : %s" % s[:40])
        if re.search(r"[^\d]\.(\s|$)", s):
            errors.append("온점 발견 : %s" % s[:40])
        if "**" in s:
            errors.append("굵게 표기 잔존 : %s" % s[:40])
    return errors


# ─────────────────────────────────────────────── 조립
def build(figdir, out_path):
    body_first = first_paragraph(figdir)
    front = render_front()
    body = render_body(figdir)
    section = XML_DECL + '<hs:sec %s>%s%s%s</hs:sec>' % (NS_DECL, body_first, front, body)
    header = header_xml()

    parts = {
        "Contents/header.xml": header.encode("utf-8"),
        "Contents/section0.xml": section.encode("utf-8"),
        "version.xml": VERSION_XML.encode("utf-8"),
        "settings.xml": SETTINGS_XML.encode("utf-8"),
        "META-INF/container.xml": CONTAINER_XML.encode("utf-8"),
        "META-INF/container.rdf": CONTAINER_RDF.encode("utf-8"),
        "META-INF/manifest.xml": MANIFEST_XML.encode("utf-8"),
        "Contents/content.hpf": content_hpf().encode("utf-8"),
    }
    bin_names = [arc for _i, arc, _d, _e in IMAGES.items]
    errs = validate(parts, bin_names)
    if errs:
        for e in errs[:50]:
            print("  [오류] " + e)
        raise SystemExit("검증 실패 (%d건)" % len(errs))

    prv_img = preview_image(figdir)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    tmp = out_path + ".tmp"
    with zipfile.ZipFile(tmp, "w") as z:
        def put(name, data, compress):
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
        # 한글 저장본과 같은 순서  mimetype 은 맨 앞, 압축 없이
        put("mimetype", b"application/hwp+zip", False)
        put("version.xml", parts["version.xml"], False)
        put("Contents/header.xml", parts["Contents/header.xml"], True)
        for _i, arc, data, _e in IMAGES.items:
            put(arc, data, False)
        put("Contents/section0.xml", parts["Contents/section0.xml"], True)
        put("Preview/PrvText.txt", preview_text().encode("utf-8"), True)
        put("settings.xml", parts["settings.xml"], True)
        if prv_img:
            put("Preview/PrvImage.png", prv_img, False)
        put("META-INF/container.rdf", parts["META-INF/container.rdf"], True)
        put("Contents/content.hpf", parts["Contents/content.hpf"], True)
        put("META-INF/container.xml", parts["META-INF/container.xml"], True)
        put("META-INF/manifest.xml", parts["META-INF/manifest.xml"], True)
    os.replace(tmp, out_path)

    # 저장 결과 재확인
    with zipfile.ZipFile(out_path) as z:
        infos = z.infolist()
        assert infos[0].filename == "mimetype" and infos[0].compress_type == zipfile.ZIP_STORED
        assert z.read("mimetype") == b"application/hwp+zip"
        for info in infos:
            if info.filename.endswith((".xml", ".hpf", ".rdf")):
                etree.fromstring(z.read(info.filename))
        assert z.testzip() is None
    return {
        "images": len(IMAGES.items), "charPr": len(R.cp), "paraPr": len(R.pp), "borderFill": len(R.bf),
        "paragraphs": section.count("<hp:p "), "tables": section.count("<hp:tbl "),
        "size": os.path.getsize(out_path),
    }


def main():
    ap = argparse.ArgumentParser(description="고천중 학생자치 개선안 HWPX 생성")
    ap.add_argument("--figs", default=os.path.join(ROOT, "figs"), help="그림 폴더 (기본 figs/)")
    ap.add_argument("--out", default=os.path.join(ROOT, "out", "고천중_학생자치_개선안.hwpx"))
    a = ap.parse_args()
    info = build(a.figs, a.out)
    print("HWPX 생성 : %s" % a.out)
    print("  그림 %(images)d  표 %(tables)d  문단 %(paragraphs)d  charPr %(charPr)d  paraPr %(paraPr)d  "
          "borderFill %(borderFill)d  크기 %(size)d bytes" % info)


if __name__ == "__main__":
    main()
