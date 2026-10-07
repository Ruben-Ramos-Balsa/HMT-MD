#!/usr/bin/env python3
"""Comprueba preservación estricta frente al antecesor117.

El comprobador heredado de114→117 presupone un traslado H5 ya realizado.
Este control no repite ese traslado: exige identidad de los archivos H5 y
del electrón, y preservación literal de todo el cuerpo salvo tres adiciones
y la corrección bibliográfica explícita de la edición activa.
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import json
import re
import runpy

p=argparse.ArgumentParser()
p.add_argument('--base',type=Path,required=True)
p.add_argument('--root',type=Path,required=True)
p.add_argument('--receipt',type=Path,required=True)
args=p.parse_args()
base,root=args.base.resolve(),args.root.resolve()
allowed={'sections/excepcional.tex','sections/conclusiones.tex','sections/bibliografia.tex','sections/resumen.tex'}
changed=[]
same=[]
for old in [base/'main.tex',*sorted((base/'sections').glob('*.tex')),*sorted((base/'figures').glob('*'))]:
    if not old.is_file():
        continue
    rel=old.relative_to(base).as_posix()
    new=root/rel
    if not new.is_file():
        raise RuntimeError('Archivo omitido '+rel)
    if old.read_bytes()==new.read_bytes():
        same.append(rel)
    elif rel not in allowed:
        raise RuntimeError('Cambio fuera del alcance '+rel)
    else:
        before,after=old.read_text(),new.read_text()
        if rel.endswith('excepcional.tex'):
            for name in ('k_direccion_dimensional','moonshine_comparacion','pantallas_dualidad'):
                after=after.replace('\\input{sections/'+name+'.tex}\n\n','')
            if before!=after:
                raise RuntimeError('La prolongación original ha cambiado')
        elif rel.endswith('conclusiones.tex'):
            start=after.index('La dirección \\(u_K=P_3P_{11}K\\)')
            end=after.index('\\input{sections/revision_conclusion.tex}',start)
            if after[:start]+after[end:]!=before:
                raise RuntimeError('Conclusiones previas alteradas')
        elif rel.endswith('resumen.tex'):
            start=after.index('El registro \\(K\\) selecciona además')
            end=after.index('\\vspace{7pt}',start)
            if after[:start]+after[end:]!=before.replace('\n\n\\vspace{7pt}','\n\\vspace{7pt}'):
                raise RuntimeError('Resumen previo alterado')
        else:
            def items(t):
                return {m[1]:m[0] for m in re.finditer(r'\\bibitem\{([^}]+)\}.*?(?=\\bibitem|\\end\{thebibliography\})',t,re.S)}
            olditems,newitems=items(before),items(after)
            for key,value in olditems.items():
                if key not in ('hmtintegral','hmtsintesis') and newitems.get(key)!=value:
                    raise RuntimeError('Referencia previa alterada '+key)
            if '2\\,249' not in newitems['hmtintegral'] or '2\\,084' not in newitems['hmtintegral']:
                raise RuntimeError('Falta edición actual o antecedente')
            if '399 páginas' not in newitems['hmtsintesis'] or '141 páginas' not in newitems['hmtsintesis']:
                raise RuntimeError('Falta síntesis actual o antecedente')
        changed.append(rel)
V=runpy.run_path(str(root/'technical/verificar_delta_editorial.py'),run_name='biblioteca_delta')
B,R=V['Document'](base),V['Document'](root)
norm=V['normalize_math']
bc=Counter(norm(e['body'],e['path'],e['labels']) for e in B.equations)
rc=Counter(norm(e['body'],e['path'],e['labels']) for e in R.equations)
if bc-rc:
    raise RuntimeError('Expresiones previas eliminadas o alteradas')
if set(B.labels)-set(R.labels):
    raise RuntimeError('Etiquetas previas eliminadas')
if B.errors or R.errors:
    raise RuntimeError(str(B.errors+R.errors))
report={'status':'PASS_AMPLIACION_ADITIVA_I_117','unchanged_files':same,
 'changed_files':changed,'original_equations_preserved':len(B.equations),
 'new_total_equations':len(R.equations),'original_labels_preserved':len(B.labels),
 'new_total_labels':len(R.labels),'original_figure_inclusions':len(B.figures),
 'new_figure_inclusions':len(R.figures),'H5_and_electron_byte_identical':True,
 'scope':'Preservación documental exacta; no certifica verdad global ni prioridad histórica.'}
args.receipt.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['status'],len(same),'archivos idénticos;',len(B.equations),'ecuaciones previas conservadas')
