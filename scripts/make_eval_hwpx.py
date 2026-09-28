"""검정(인정)도서 선정 평가표 3장을 무작위 점수로 채워 HWPX로 만든다

세 평가표 점수 합계 순위가 동아출판 1위, 미래엔 2위, 비상교육 3위가 되도록 뽑는다
"""
import random
import sys
import zipfile
from xml.sax.saxutils import escape

PUBLISHERS = ["㈜교학사", "동아출판㈜", "㈜엔이능률", "㈜와이비엠", "㈜지학사",
              "㈜천재교과서(김화경)", "㈜천재교과서(김동재)", "㈜비상교육", "㈜미래엔"]
DONGA, BISANG, MIRAE = 1, 7, 8

ITEMS = [
    ("교육과정", "학습 분량의 적절성", 20),
    ("학습내용선정", "내용 수준의 적정성", 20),
    ("학습내용 선정", "정확성", 10),
    ("학습내용 조직", "단원, 학년 간 연계 및 계열성", 10),
    ("교수학습활동", "교수학습 활동의 유용성", 10),
    ("학습평가", "종합적 사고력 평가", 10),
    ("표현표기 및 외형체제", "표현, 표기의 정확성 및 가독성", 10),
    ("재정적 부분", "교과용 도서의 가격", 10),
]

N_SHEETS = 3
MIN_TOTAL = 76

# 위원마다 1~3위 순서를 다르게 하되 세 명 합산은 동아출판, 미래엔, 비상교육 순
SHEET_TOP3 = [
    (DONGA, MIRAE, BISANG),
    (MIRAE, DONGA, BISANG),
    (DONGA, BISANG, MIRAE),
]


def gen_sheet(rng, bias):
    """위원 한 명의 평가표 [출판사][항목] 점수"""
    sheet = []
    for p in range(len(PUBLISHERS)):
        row = []
        for _, _, mx in ITEMS:
            ratio = min(1.0, max(0.7, bias[p] + rng.uniform(-0.08, 0.08)))
            row.append(round(mx * ratio))
        sheet.append(row)
    return sheet


def gen_ranked_sheet(rng, top3):
    while True:
        bias = [rng.uniform(0.78, 0.86) for _ in PUBLISHERS]
        for bonus, p in zip((0.12, 0.09, 0.06), top3):
            bias[p] = 0.8 + bonus + rng.uniform(-0.01, 0.01)
        sheet = gen_sheet(rng, bias)
        t = [sum(r) for r in sheet]
        if min(t) >= MIN_TOTAL and ordered(t, top3):
            return sheet


def generate(seed):
    rng = random.Random(seed)
    while True:
        sheets = [gen_ranked_sheet(rng, top3) for top3 in SHEET_TOP3]
        totals = [sum(sum(s[p]) for s in sheets) for p in range(len(PUBLISHERS))]
        if ordered(totals, (DONGA, MIRAE, BISANG)):
            return sheets, totals


def ordered(t, top3):
    a, b, c = top3
    others = max(v for p, v in enumerate(t) if p not in top3)
    return t[a] > t[b] > t[c] > others


RECOMMEND = [
    ("동아출판", "교육과정 성취기준을 충실히 반영하고 학습 분량과 내용 수준이 학생들의 학력 수준에 적합함. "
     "실생활 맥락의 도입 활동과 단계적 탐구 활동으로 개념을 자연스럽게 형성할 수 있으며 기본과 심화 문제의 난이도 배치가 균형적임. "
     "이전 학년과의 계열성을 고려한 단원 구성과 정확한 용어 및 기호 표기, 깔끔한 편집으로 가독성이 뛰어나 "
     "세 위원 합산 최고점을 받아 1순위로 추천함."),
    ("미래엔", "단원 간 연계가 매끄럽고 수학적 오개념을 바로잡는 코너와 자기 평가 활동이 잘 갖추어져 있음. "
     "서술형 평가 문항과 교수학습 자료, 디지털 연계 자료가 풍부하여 다양한 수업 방법에 활용하기 좋으나 "
     "일부 단원의 학습 분량이 다소 많은 점을 고려하여 2순위로 추천함."),
    ("비상교육", "개념 정리와 예제 구성이 명확하고 편집이 깔끔하여 학생들이 스스로 학습하기에 용이함. "
     "종합적 사고력을 요구하는 프로젝트 과제가 우수하나 "
     "학생 참여형 활동의 안내가 상대적으로 간략한 점을 고려하여 3순위로 추천함."),
]

OPINIONS = [
    "동아출판㈜ 교과서는 교육과정 성취기준을 충실히 반영하면서도 학습 분량이 적절하여 한 학기 수업 운영에 무리가 없다. "
    "개념 도입 단계에서 실생활 소재를 활용하고 탐구 활동과 문제 해결 과정이 단계적으로 제시되어 학생 스스로 사고를 확장하기에 좋다. "
    "㈜미래엔 교과서는 단원 간 연계가 매끄럽고 서술형 평가 문항이 풍부하며 ㈜비상교육 교과서는 편집이 깔끔하고 가독성이 높다. "
    "종합적으로 1순위 동아출판㈜, 2순위 ㈜미래엔, 3순위 ㈜비상교육을 추천함.",

    "㈜미래엔 교과서는 수학적 오개념을 짚어 주는 코너와 자기 평가 활동이 돋보이고 교수학습 자료와 디지털 연계 자료가 풍부하여 수업 활용도가 높다. "
    "동아출판㈜ 교과서는 내용 수준이 학생들의 학력 분포에 잘 맞고 기본 문제와 심화 문제의 난이도 배치가 균형적이다. "
    "㈜비상교육 교과서는 개념 정리와 예제 구성이 명확하여 자기주도 학습에 도움이 된다. "
    "따라서 1순위 ㈜미래엔, 2순위 동아출판㈜, 3순위 ㈜비상교육으로 추천함.",

    "동아출판㈜ 교과서는 이전 학년과의 계열성을 고려한 복습 코너와 다음 단원 예고가 잘 구성되어 학습의 흐름이 자연스럽고 가격 면에서도 부담이 적다. "
    "㈜비상교육 교과서는 종합적 사고력을 요구하는 프로젝트 과제가 우수하고 삽화와 도표가 내용 이해를 돕도록 배치되어 있다. "
    "㈜미래엔 교과서는 서술형 평가 문항이 풍부하나 일부 단원의 학습 분량이 다소 많다. "
    "이에 1순위 동아출판㈜, 2순위 ㈜비상교육, 3순위 ㈜미래엔을 추천함.",
]


# ---------------------------------------------------------------- HWPX 조립

NS = ('xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" '
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
      'xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"')

XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
LANGS = ["HANGUL", "LATIN", "HANJA", "JAPANESE", "OTHER", "SYMBOL", "USER"]


def lang_attrs(v):
    return " ".join(f'{l.lower()}="{v}"' for l in LANGS)


def border_fill(bid, line, fill=None):
    sides = "".join(f'<hh:{s}Border type="{line}" width="0.12 mm" color="#000000"/>'
                    for s in ("left", "right", "top", "bottom"))
    brush = (f'<hc:fillBrush><hc:winBrush faceColor="{fill}" hatchColor="#000000" alpha="0"/></hc:fillBrush>'
             if fill else "")
    return (f'<hh:borderFill id="{bid}" threeD="0" shadow="0" centerLine="NONE" breakCellSeparateLine="0">'
            '<hh:slash type="NONE" Crooked="0" isCounter="0"/>'
            '<hh:backSlash type="NONE" Crooked="0" isCounter="0"/>'
            f'{sides}<hh:diagonal type="SOLID" width="0.1 mm" color="#000000"/>{brush}</hh:borderFill>')


def char_pr(cid, height, bold=False):
    return (f'<hh:charPr id="{cid}" height="{height}" textColor="#000000" shadeColor="none" '
            'useFontSpace="0" useKerning="0" symMark="NONE" borderFillIDRef="2">'
            f'<hh:fontRef {lang_attrs(0)}/><hh:ratio {lang_attrs(100)}/>'
            f'<hh:spacing {lang_attrs(0)}/><hh:relSz {lang_attrs(100)}/><hh:offset {lang_attrs(0)}/>'
            + ('<hh:bold/>' if bold else '') +
            '<hh:underline type="NONE" shape="SOLID" color="#000000"/>'
            '<hh:strikeout shape="NONE" color="#000000"/><hh:outline type="NONE"/>'
            '<hh:shadow type="NONE" color="#B2B2B2" offsetX="10" offsetY="10"/></hh:charPr>')


def para_pr(pid, align, line=160):
    m = "".join(f'<hc:{k} value="0" unit="HWPUNIT"/>' for k in ("intent", "left", "right", "prev", "next"))
    return (f'<hh:paraPr id="{pid}" tabPrIDRef="0" condense="0" fontLineHeight="0" snapToGrid="1" '
            'suppressLineNumbers="0" checked="0">'
            f'<hh:align horizontal="{align}" vertical="BASELINE"/>'
            '<hh:heading type="NONE" idRef="0" level="0"/>'
            '<hh:breakSetting breakLatinWord="KEEP_WORD" breakNonLatinWord="KEEP_WORD" widowOrphan="0" '
            'keepWithNext="0" keepLines="0" pageBreakBefore="0" lineWrap="BREAK"/>'
            '<hh:autoSpacing eAsianEng="0" eAsianNum="0"/>'
            f'<hh:margin>{m}</hh:margin>'
            f'<hh:lineSpacing type="PERCENT" value="{line}" unit="HWPUNIT"/>'
            '<hh:border borderFillIDRef="2" offsetLeft="0" offsetRight="0" offsetTop="0" '
            'offsetBottom="0" connect="0" ignoreMargin="0"/></hh:paraPr>')


# charPr: 0 본문 10pt, 1 제목 16pt 굵게, 2 표 9pt, 3 표 9pt 굵게, 4 소제목 12pt 굵게
# paraPr: 0 양쪽, 1 가운데, 2 오른쪽, 3 가운데(표 안 줄간격 좁게)
# borderFill: 1 없음, 2 없음+빈 채우기, 3 실선, 4 실선+회색
def header_xml():
    fonts = "".join(
        f'<hh:fontface lang="{l}" fontCnt="1"><hh:font id="0" face="맑은 고딕" type="TTF" isEmbedded="0">'
        '<hh:typeInfo familyType="FCAT_GOTHIC" weight="6" proportion="4" contrast="0" strokeVariation="1" '
        'armStyle="1" letterform="1" midline="1" xHeight="1"/></hh:font></hh:fontface>' for l in LANGS)
    bfs = (border_fill(1, "NONE") + border_fill(2, "NONE", "none")
           + border_fill(3, "SOLID") + border_fill(4, "SOLID", "#E7E6E6"))
    chars = (char_pr(0, 1000) + char_pr(1, 1600, True) + char_pr(2, 900)
             + char_pr(3, 900, True) + char_pr(4, 1200, True))
    paras = (para_pr(0, "JUSTIFY") + para_pr(1, "CENTER") + para_pr(2, "RIGHT")
             + para_pr(3, "CENTER", 130))
    return (XML_DECL + f'<hh:head {NS} version="1.4" secCnt="1">'
            '<hh:beginNum page="1" footnote="1" endnote="1" pic="1" tbl="1" equation="1"/>'
            '<hh:refList>'
            f'<hh:fontfaces itemCnt="7">{fonts}</hh:fontfaces>'
            f'<hh:borderFills itemCnt="4">{bfs}</hh:borderFills>'
            f'<hh:charProperties itemCnt="5">{chars}</hh:charProperties>'
            '<hh:tabProperties itemCnt="1"><hh:tabPr id="0" autoTabLeft="0" autoTabRight="0"/></hh:tabProperties>'
            f'<hh:paraProperties itemCnt="4">{paras}</hh:paraProperties>'
            '<hh:styles itemCnt="1"><hh:style id="0" type="PARA" name="바탕글" engName="Normal" '
            'paraPrIDRef="0" charPrIDRef="0" nextStyleIDRef="0" langID="1042" lockForm="0"/></hh:styles>'
            '</hh:refList>'
            '<hh:compatibleDocument targetProgram="HWP201X"><hh:layoutCompatibility/></hh:compatibleDocument>'
            '<hh:docOption><hh:linkinfo path="" pageInherit="0" footnoteInherit="0"/></hh:docOption>'
            '<hh:trackchageConfig flags="56"/>'
            '</hh:head>')


SEC_PR = (
    '<hp:secPr id="" textDirection="HORIZONTAL" spaceColumns="1134" tabStop="8000" tabStopVal="4000" '
    'tabStopUnit="HWPUNIT" outlineShapeIDRef="0" memoShapeIDRef="0" textVerticalWidthHead="0" masterPageCnt="0">'
    '<hp:grid lineGrid="0" charGrid="0" wonggojiFormat="0"/>'
    '<hp:startNum pageStartsOn="BOTH" page="0" pic="0" tbl="0" equation="0"/>'
    '<hp:visibility hideFirstHeader="0" hideFirstFooter="0" hideFirstMasterPage="0" border="SHOW_ALL" '
    'fill="SHOW_ALL" hideFirstPageNum="0" hideFirstEmptyLine="0" showLineNumber="0"/>'
    '<hp:lineNumberShape restartType="0" countBy="0" distance="0" startNumber="0"/>'
    '<hp:pagePr landscape="WIDELY" width="59528" height="84186" gutterType="LEFT_ONLY">'
    '<hp:margin header="2835" footer="2835" gutter="0" left="4252" right="4252" top="4252" bottom="4252"/>'
    '</hp:pagePr>'
    '<hp:footNotePr><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" suffixChar=")" supscript="0"/>'
    '<hp:noteLine length="-1" type="SOLID" width="0.12 mm" color="#000000"/>'
    '<hp:noteSpacing betweenNotes="283" belowLine="567" aboveLine="850"/>'
    '<hp:numbering type="CONTINUOUS" newNum="1"/><hp:placement place="EACH_COLUMN" beneathText="0"/>'
    '</hp:footNotePr>'
    '<hp:endNotePr><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" suffixChar=")" supscript="0"/>'
    '<hp:noteLine length="14692344" type="SOLID" width="0.12 mm" color="#000000"/>'
    '<hp:noteSpacing betweenNotes="0" belowLine="567" aboveLine="850"/>'
    '<hp:numbering type="CONTINUOUS" newNum="1"/><hp:placement place="END_OF_DOCUMENT" beneathText="0"/>'
    '</hp:endNotePr>'
    + "".join(f'<hp:pageBorderFill type="{t}" borderFillIDRef="1" textBorder="PAPER" headerInside="0" '
              'footerInside="0" fillArea="PAPER"><hp:offset left="1417" right="1417" top="1417" bottom="1417"/>'
              '</hp:pageBorderFill>' for t in ("BOTH", "EVEN", "ODD"))
    + '</hp:secPr>'
    '<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="1" sameSz="1" sameGap="0"/></hp:ctrl>'
)

_pid = [0]
_tid = [1000]


def para(text, para_pr=0, char_pr=0, page_break=False, prefix=""):
    _pid[0] += 1
    t = f'<hp:t>{escape(text)}</hp:t>' if text else ''
    return (f'<hp:p id="{_pid[0]}" paraPrIDRef="{para_pr}" styleIDRef="0" pageBreak="{int(page_break)}" '
            f'columnBreak="0" merged="0"><hp:run charPrIDRef="{char_pr}">{prefix}{t}</hp:run></hp:p>')


def cell(r, c, w, h, text, bold=False, shaded=False):
    bf = 4 if shaded else 3
    return (f'<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="{bf}">'
            '<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" '
            'linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
            + para(str(text), 0 if len(str(text)) > 40 else 3, 3 if bold else 2) +
            '</hp:subList>'
            f'<hp:cellAddr colAddr="{c}" rowAddr="{r}"/><hp:cellSpan colSpan="1" rowSpan="1"/>'
            f'<hp:cellSz width="{w}" height="{h}"/>'
            '<hp:cellMargin left="141" right="141" top="141" bottom="141"/></hp:tc>')


def table(rows, widths, heights, bold_rows=(), bold_cols=(), shaded_rows=(), shaded_cols=()):
    _tid[0] += 1
    body = ""
    for r, row in enumerate(rows):
        body += "<hp:tr>"
        for c, text in enumerate(row):
            body += cell(r, c, widths[c], heights[r], text,
                         bold=r in bold_rows or c in bold_cols,
                         shaded=r in shaded_rows or c in shaded_cols)
        body += "</hp:tr>"
    tbl = (f'<hp:tbl id="{_tid[0]}" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" '
           'textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" '
           f'rowCnt="{len(rows)}" colCnt="{len(widths)}" cellSpacing="0" borderFillIDRef="3" noAdjust="0">'
           f'<hp:sz width="{sum(widths)}" widthRelTo="ABSOLUTE" height="{sum(heights)}" heightRelTo="ABSOLUTE" protect="0"/>'
           '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" '
           'vertRelTo="PARA" horzRelTo="COLUMN" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
           '<hp:outMargin left="0" right="0" top="0" bottom="0"/>'
           '<hp:inMargin left="141" right="141" top="141" bottom="141"/>'
           f'{body}</hp:tbl>')
    return para("", 1, 0, prefix=tbl)


SCORE_WIDTHS = [5400, 7600, 3000] + [4000] * len(PUBLISHERS)


def score_table(sheet):
    head = ["평가영역", "평가기준", "항목별 점수"] + PUBLISHERS
    rows = [head]
    for i, (area, crit, mx) in enumerate(ITEMS):
        rows.append([area, crit, mx] + [sheet[p][i] for p in range(len(PUBLISHERS))])
    rows.append(["합계", "", 100] + [sum(sheet[p]) for p in range(len(PUBLISHERS))])
    widths = SCORE_WIDTHS
    heights = [3200] + [2400] * len(ITEMS) + [2400]
    return table(rows, widths, heights, bold_rows=(0, len(rows) - 1),
                 shaded_rows=(0, len(rows) - 1), shaded_cols=(0, 1, 2))


# 총괄표 양식의 출판사 순서와 표기
SUMMARY_ORDER = [(MIRAE, "미래엔"), (3, "와이비엠"), (DONGA, "동아출판"), (2, "NE능률"),
                 (6, "천재교과서-김동재"), (5, "천재교과서-김화경"), (BISANG, "비상교육"),
                 (0, "교학사"), (4, "지학사")]


def summary_table(sheets, totals):
    rank = {p: i + 1 for i, p in enumerate(sorted(range(len(totals)), key=lambda p: -totals[p]))}
    head = ["출판사명"] + [f"위원 {k + 1}" for k in range(len(sheets))] + ["총점", "평균", "비고"]
    rows = [head]
    for p, name in SUMMARY_ORDER:
        note = f"{rank[p]}순위 추천" if rank[p] <= 3 else ""
        rows.append([name] + [sum(s[p]) for s in sheets]
                    + [totals[p], f"{totals[p] / len(sheets):.1f}", note])
    widths = [11000] + [6000] * len(sheets) + [6000, 6000, 8000]
    heights = [2400] * len(rows)
    return table(rows, widths, heights, bold_rows=(0,), bold_cols=(0,),
                 shaded_rows=(0,), shaded_cols=(0,))


def section_xml(sheets, totals):
    body = ""
    for k, sheet in enumerate(sheets):
        first = k == 0
        body += para("검정(인정)도서 선정 평가표", 1, 1, page_break=not first,
                     prefix=SEC_PR if first else "")
        body += para(f"과 목 : 수학과      위 원 : 평가표 {k + 1}      (인)", 2, 0)
        body += score_table(sheet)
        body += table([["<종합의견 및 추천의견>"], [OPINIONS[k]]], [sum(SCORE_WIDTHS)], [2400, 9000],
                      bold_rows=(0,), shaded_rows=(0,))
    body += para("검인정도서 선정기준 평가 총괄표", 1, 1, page_break=True)
    body += para("과 목 : 수학", 0, 0)
    body += summary_table(sheets, totals)
    body += para("추천 검인정도서 및 추천 의견서", 1, 1, page_break=True)
    body += para("과 목 : 수학", 0, 0)
    rows = [["순위", "출판사명", "추 천 의 견"]] + [[i + 1, n, t] for i, (n, t) in enumerate(RECOMMEND)]
    body += table(rows, [3000, 7000, 40000], [2400, 12000, 12000, 12000],
                  bold_rows=(0,), shaded_rows=(0,))
    return XML_DECL + f'<hs:sec {NS}>{body}</hs:sec>'


VERSION = (XML_DECL + '<hv:HCFVersion xmlns:hv="http://www.hancom.co.kr/hwpml/2011/version" '
           'tagetApplication="WORDPROCESSOR" major="5" minor="1" micro="0" buildNumber="1" os="1" '
           'xmlVersion="1.4" application="Hancom Office Hangul" appVersion="11, 0, 0, 0"/>')
CONTAINER = (XML_DECL + '<ocf:container xmlns:ocf="urn:oasis:names:tc:opendocument:xmlns:container" '
             'xmlns:hpf="http://www.hancom.co.kr/schema/2011/hpf"><ocf:rootfiles>'
             '<ocf:rootfile full-path="Contents/content.hpf" media-type="application/hwpml-package+xml"/>'
             '</ocf:rootfiles></ocf:container>')
MANIFEST = XML_DECL + '<odf:manifest xmlns:odf="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"/>'
CONTENT = (XML_DECL + f'<opf:package {NS} version="" unique-identifier="" id="">'
           '<opf:metadata><opf:title>검정(인정)도서 선정 평가표</opf:title><opf:language>ko</opf:language>'
           '</opf:metadata><opf:manifest>'
           '<opf:item id="header" href="Contents/header.xml" media-type="application/xml"/>'
           '<opf:item id="section0" href="Contents/section0.xml" media-type="application/xml"/>'
           '<opf:item id="settings" href="settings.xml" media-type="application/xml"/>'
           '</opf:manifest><opf:spine><opf:itemref idref="header" linear="yes"/>'
           '<opf:itemref idref="section0" linear="yes"/></opf:spine></opf:package>')
SETTINGS = (XML_DECL + '<ha:HWPApplicationSetting xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" '
            'xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0">'
            '<ha:CaretPosition listIDRef="0" paraIDRef="0" pos="0"/></ha:HWPApplicationSetting>')


def write_hwpx(path, sheets, totals):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/hwp+zip", compress_type=zipfile.ZIP_STORED)
        files = {
            "version.xml": VERSION,
            "Contents/header.xml": header_xml(),
            "Contents/section0.xml": section_xml(sheets, totals),
            "Contents/content.hpf": CONTENT,
            "settings.xml": SETTINGS,
            "META-INF/container.xml": CONTAINER,
            "META-INF/manifest.xml": MANIFEST,
        }
        for name, data in files.items():
            z.writestr(name, data.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "검정도서_선정_평가표_3종.hwpx"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    sheets, totals = generate(seed)
    write_hwpx(out, sheets, totals)
    for k, s in enumerate(sheets):
        print(f"평가표 {k + 1}:", [sum(r) for r in s])
    for name, t in sorted(zip(PUBLISHERS, totals), key=lambda x: -x[1]):
        print(f"{name:<16}{t}")
