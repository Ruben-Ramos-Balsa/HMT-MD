#!/usr/bin/env python3
"""Genera una muestra visual de las páginas finales para inspección humana."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa/visual_finales';OUT.mkdir(parents=True,exist_ok=True)
PDF=ROOT/'metadata/visual_parte_inicial/pass11.pdf'
BIN='/Users/ruben/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm'
GROUPS={
 '01_terminal':[2601,2650,2700,2750,2800,2850,2900,2940,2970,3000,3050,3090],
 '02_conservacion':[3100,3150,3202,3240,3294,3317,3349,3380,3437,3470,3500,3550],
 '03_apendices':[3600,3650,3700,3750,3800,3850,3858,3880,3912,3939,3940,3944],
}
def render(p):
    prefix=OUT/f'p{p:04d}'
    subprocess.run([BIN,'-f',str(p),'-l',str(p),'-scale-to','1500','-singlefile','-png',str(PDF),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
pages=sorted({p for ps in GROUPS.values() for p in ps})
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,pages))
for name,ps in GROUPS.items():
    w,h=450,650;sheet=Image.new('RGB',(3*w,4*h),(220,223,226));d=ImageDraw.Draw(sheet)
    for i,p in enumerate(ps):
        im=Image.open(OUT/f'p{p:04d}.png').convert('RGB');im.thumbnail((w-16,h-30))
        sheet.paste(im,((i%3)*w+(w-im.width)//2,(i//3)*h+25))
        d.text(((i%3)*w+8,(i//3)*h+5),f'PDF {p} / pass11',fill='black')
    sheet.save(OUT/(name+'.jpg'),quality=94)
(OUT/'muestra.json').write_text(json.dumps({'pdf':str(PDF),'pages':pages,'scope':'Muestra para inspección visual; no revisión semántica total.'},indent=2)+'\n')
print('Páginas renderizadas:',len(pages))
