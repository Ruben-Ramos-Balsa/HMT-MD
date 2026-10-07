#!/usr/bin/env python3
"""Sucesora III: conservación literal del cuerpo y una inserción nueva."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('ARTICULO_III_VACIO_ELECTROMAGNETICO_20260909_REV02')
if (ROOT/'antecedentes/articulo_III_rev02').is_dir():
    BASE=ROOT/'antecedentes/articulo_III_rev02'
marker='\\input{manuscrito/sections/04b_reconstruccion_forma_lc.tex}\n'
files=[BASE/'main.tex']
for d in ('manuscrito','base_articulo_I','base_articulo_II'):
    files.extend(p for p in (BASE/d).rglob('*') if p.is_file() and p.suffix in ('.tex','.bib','.png','.jpg','.pdf'))
rows=[]
for old in sorted(set(files)):
    rel=old.relative_to(BASE); new=ROOT/rel
    before=old.read_bytes();after=new.read_bytes()
    if str(rel)=='main.tex':
        t=after.decode();assert t.count(marker)==1
        assert t.replace(marker,'').encode()==before
        state='identical_after_removing_single_input'
    else:
        assert before==after,str(rel);state='byte_identical'
    rows.append({'path':str(rel),'sha256_predecessor':hashlib.sha256(before).hexdigest(),'check':state})
r={'status':'PASS_PRESERVACION_III_REV03','files':rows,'predecessor':str(BASE),
   'scope':'Una inserción focal, sin sustitución del cuerpo; no certifica cierre científico global.'}
(ROOT/'technical/PRESERVACION_REV03.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(r['status'],len(rows),'archivos previos conservados')
