#!/usr/bin/env python3
"""Extrae navegación y prepara imágenes para inspección humana; no la suplanta."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT/'output/pdf/ARITMETICA_GENEALOGICA_PRIMOS_Y_ESTRUCTURA_ESPECTRAL_ZETA.pdf'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--pdftoppm', default='/Users/ruben/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm')
    a=ap.parse_args()
    out=ROOT/'technical/revision_visual'
    out.mkdir(parents=True,exist_ok=True)
    reader=PdfReader(PDF)
    rows=[]
    def walk(items,depth=0):
        for item in items:
            if isinstance(item,list):
                walk(item,depth+1)
            else:
                rows.append({'title':item.title,'depth':depth,'physical_page':reader.get_destination_page_number(item)+1})
    walk(reader.outline)
    pages=[]
    for n,page in enumerate(reader.pages,1):
        text=page.extract_text()
        pages.append({'physical_page':n,'characters':len(text),'text':text})
    (out/'PAGINAS.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
    wanted=('Centro, frontera','Transporte nonádico','Lectores de frontera','Eliminación coerciva','Conclusiones','Procedencia de los resultados')
    top=[x for x in rows if x['depth']==0]
    selected=set(range(1,min(11,len(pages))+1))
    spans=[]
    for i,row in enumerate(top):
        if row['title'].startswith(wanted):
            following=[x['physical_page'] for x in top[i+1:] if x['physical_page']>row['physical_page']]
            stop=following[0]-1 if following else len(pages)
            spans.append({'title':row['title'],'first':row['physical_page'],'last':stop})
            selected.update(range(row['physical_page'],stop+1))
    report={'pdf':str(PDF),'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),
            'pages':len(pages),'outline':rows,'selected_spans':spans,
            'selected_physical_pages':sorted(selected),
            'blank_text_pages':[p['physical_page'] for p in pages if not p['text'].strip()],
            'inspection_status':'PREPARADO_PARA_INSPECCION_VISUAL; no implica inspección realizada'}
    (out/'NAVEGACION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if a.render:
        subprocess.run([a.pdftoppm,'-r','80','-png',str(PDF),str(out/'pagina')],check=True,capture_output=True)
        files={int(p.stem.split('-')[-1]):p for p in out.glob('pagina-*.png')}
        ordered=sorted(selected)
        for offset in range(0,len(ordered),12):
            sheet=Image.new('RGB',(930,1392),'#e5e5e5')
            draw=ImageDraw.Draw(sheet)
            for j,n in enumerate(ordered[offset:offset+12]):
                im=Image.open(files[n]).convert('RGB')
                im.thumbnail((292,320))
                x=(j%3)*310+(310-im.width)//2
                y=(j//3)*348+22
                sheet.paste(im,(x,y))
                draw.text(((j%3)*310+10,(j//3)*348+5),f'Página física {n}',fill='black')
            sheet.save(out/f'contacto-{offset//12+1:02d}.png')
    print(json.dumps({k:report[k] for k in ('pages','selected_spans','selected_physical_pages','blank_text_pages')},ensure_ascii=False))

if __name__=='__main__':
    main()
