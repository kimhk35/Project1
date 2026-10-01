#!/usr/bin/env python3
"""render.js 가 만든 PDF 를 다시 압축한다 (pikepdf)"""
import os
import pikepdf

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'PRAXIS_Vol01_창간특집호.pdf')
tmp = p + '.tmp'
with pikepdf.open(p) as pdf:
    pdf.docinfo['/Title'] = 'PRAXIS 창간특집호 · 2026년 9월'
    pdf.docinfo['/Author'] = 'PRAXIS 편집부 · 편집장 McKay'
    pdf.docinfo['/Subject'] = '교육 AI · 에듀테크 · 학습과학'
    pdf.save(tmp, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate, recompress_flate=True)
os.replace(tmp, p)
print('pdf optimized', os.path.getsize(p) // 1024, 'KB')
