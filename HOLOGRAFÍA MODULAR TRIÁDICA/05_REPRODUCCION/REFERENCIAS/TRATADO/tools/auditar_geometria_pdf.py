#!/usr/bin/env python3
"""Examina todas las páginas mediante la extracción geométrica de Poppler.

Los indicadores localizan páginas para inspección visual. No sustituyen esa
inspección ni verifican el significado de ecuaciones o demostraciones.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import shutil
import xml.etree.ElementTree as ET
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--pdf',type=Path,default=ROOT/'build/main.pdf')
    parser.add_argument('--prefix',default='CONTROL_GEOMETRICO')
    args=parser.parse_args()
    rotations=[int(p.rotation or 0)%360 for p in PdfReader(args.pdf).pages]
    out=ROOT/'qa';out.mkdir(exist_ok=True)
    xml=out/(args.prefix+'.html')
    executable=shutil.which('pdftotext') or '/Users/ruben/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/pdftotext'
    subprocess.run([executable,'-bbox-layout',str(args.pdf),str(xml)],check=True)
    # Algunas fuentes matemáticas producen controles C0 en la capa de
    # extracción. Se excluyen sólo de la copia XML analítica, no del PDF.
    clean=out/(args.prefix+'.xml')
    forbidden=bytes([*range(0,9),11,12,*range(14,32)])
    removed=0
    with xml.open('rb') as source,clean.open('wb') as target:
        for block in iter(lambda:source.read(1024*1024),b''):
            filtered=block.translate(None,forbidden)
            removed+=len(block)-len(filtered);target.write(filtered)
    rows=[]
    for event,node in ET.iterparse(clean,events=('end',)):
        if node.tag.rsplit('}',1)[-1]!='page': continue
        page=len(rows)+1; media_width=float(node.attrib['width']);media_height=float(node.attrib['height'])
        rotation=rotations[page-1]
        width,height=(media_height,media_width) if rotation in (90,270) else (media_width,media_height)
        words=[];lines=[]
        for child in node.iter():
            kind=child.tag.rsplit('}',1)[-1]
            if kind=='word':
                words.append({'text':''.join(child.itertext()),**{k:float(child.attrib[k]) for k in ('xMin','yMin','xMax','yMax')}})
            elif kind=='line': lines.append(child.attrib)
        body=[w for w in words if 65<w['yMin']<height-65]
        escaped=[w for w in words if w['xMin']<18 or w['xMax']>width-18 or w['yMin']<12 or w['yMax']>height-12]
        suspect=[w for w in words if '??' in w['text'] or '\ufffd' in w['text']]
        rows.append({'page':page,'width':width,'height':height,'media_width':media_width,'media_height':media_height,'rotation':rotation,'words':len(words),'body_words':len(body),'lines':len(lines),
                     'body_first_y':min((w['yMin'] for w in body),default=None),
                     'body_last_y':max((w['yMax'] for w in body),default=None),
                     'short_body':len(body)<75,'extreme_words':escaped,'suspect_tokens':suspect,
                     'opening':' '.join(w['text'] for w in words[:35])})
        node.clear()
    report={'scope':'Control geométrico de todas las páginas; candidatos para inspección visual.',
            'pdf':str(args.pdf),'sha256':hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
            'pages':len(rows),'extraction_c0_controls_removed':removed,'non_a4':[r['page'] for r in rows if abs(r['media_width']-595.276)>2 or abs(r['media_height']-841.89)>2],
            'short_pages':[r['page'] for r in rows if r['short_body']],
            'extreme_pages':[r['page'] for r in rows if r['extreme_words']],
            'suspect_pages':[r['page'] for r in rows if r['suspect_tokens']],
            'records':rows}
    (ROOT/'metadata'/(args.prefix+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'},ensure_ascii=False))

if __name__=='__main__': main()
