#!/usr/bin/env python3
"""Delta exacto I125→sucesora: una inserción, ningún párrafo sustituido."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('ARTICULO_K_MOONSHINE_DUALIDAD_20260909')
if (ROOT/'antecedentes/articulo_I_125').is_dir():
    BASE=ROOT/'antecedentes/articulo_I_125'
marker='\\input{sections/helicidad_electron.tex}\n\n'
rows=[]
for old in [BASE/'main.tex',*sorted((BASE/'sections').rglob('*.tex')),*sorted((BASE/'figures').rglob('*'))]:
    if not old.is_file(): continue
    rel=old.relative_to(BASE); new=ROOT/rel
    before=old.read_bytes(); after=new.read_bytes()
    if str(rel)=='sections/electron.tex':
        text=after.decode()
        assert text.count(marker)==1
        assert text.replace(marker,'').encode()==before
        status='identical_after_removing_single_input'
    else:
        assert before==after,str(rel)
        status='byte_identical'
    rows.append({'path':str(rel),'sha256_predecessor':hashlib.sha256(before).hexdigest(),'check':status})
report={'status':'PASS_PRESERVACION_I125_HELICIDAD','files':rows,'predecessor':str(BASE),
 'new_source':'sections/helicidad_electron.tex','scope':'Conservación literal de fuentes; no prueba semántica global.'}
(ROOT/'technical/PRESERVACION_HELICIDAD.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['status'],len(rows),'archivos previos conservados')
