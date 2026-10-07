#!/usr/bin/env python3
"""Copia preservadora de fuentes y ampliaciones. No declara completitud."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path('/Users/ruben/Documents/New project')
ORIGIN = PROJECT/'output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree'
TREE = ROOT/'source/tree'
REL = Path('New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito')
MAN = TREE/REL
OLD = ROOT.parent/'REV02/source'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def prepare():
    if TREE.exists():
        raise SystemExit('La base ya existe; no se sobreescribe la edición en curso.')
    shutil.copytree(ORIGIN, TREE)
    (ROOT/'metadata').mkdir(exist_ok=True)
    rows=[]
    for p in sorted(ORIGIN.rglob('*')):
        if p.is_file():
            q=TREE/p.relative_to(ORIGIN)
            assert digest(p)==digest(q)
            rows.append({'source':str(p),'destination':str(q.relative_to(ROOT)),
                         'sha256':digest(p),'disposition':'CONSERVAR'})
    (ROOT/'metadata/PRESERVACION_BASE_INTEGRAL.json').write_text(json.dumps({
        'scope':'Identidad material de la copia inicial; no cobertura de la nueva exposición',
        'files':rows},ensure_ascii=False,indent=2)+'\n')
    ext=MAN/'ampliacion_20260919'
    ext.mkdir()
    for p in (OLD/'chapters').glob('*.tex'):
        if not re.match(r'0[1-6]_',p.name):
            continue
        s=p.read_text()
        # Encabezados subordinados dentro de su residencia causal.
        levels={'chapter':'section','section':'subsection',
                'subsection':'subsubsection','subsubsection':'paragraph'}
        s=re.sub(r'\\(chapter|section|subsection|subsubsection)(?=[*\[{])',
                 lambda m:'\\'+levels[m[1]],s)
        s=s.replace('\\input{generated/','\\input{ampliacion_20260919/generated/')
        (ext/p.name).write_text(s)
    shutil.copytree(OLD/'generated',ext/'generated')
    src=MAN/'main_paquete_union_demostrativa_20260904.tex'
    s=src.read_text()
    s=s.replace('pdftitle={El cierre holográfico del infinito}',
                'pdftitle={Holografía Modular Triádica}')
    s=s.replace('pdfsubject={La estructura discreta del continuo y el origen de las constantes fundamentales}',
                'pdfsubject={Exposición sistemática del núcleo formal, sus extensiones y derivaciones}')
    s=s.replace('\\begin{document}',
                '\\input{ampliacion_20260919/compatibilidad.tex}\n\\begin{document}',1)
    start=s.index('\\hypersetup{pageanchor=false}',s.index('\\frontmatter'))
    end=s.index('\\pagenumbering{arabic}',start)
    s=s[:start]+'\\input{ampliacion_20260919/portada.tex}\n'+s[end:]
    s=s.replace('\\input{frontmatter/00_prefacio_autoral_20260826}',
                '\\input{ampliacion_20260919/presentacion.tex}\n\\input{frontmatter/00_prefacio_autoral_20260826}')
    # Se conserva toda la arquitectura integral. Las ampliaciones preceden
    # o siguen a los propietarios indicados y no alteran la numeración de capítulos.
    wrapper=MAN/'sucesor_102/parte_i_ii_1_26_editor_unico.tex'
    w=wrapper.read_text()
    replacements={
        '\\label{chap:sucesor-102-01}':
            '\\label{chap:sucesor-102-01}\n'+''.join(
                '\\input{ampliacion_20260919/'+n+'}\n' for n in
                ['01_app.tex','03_trit_euler.tex','04_tpk_emisor.tex','05_calendario_memoria.tex']),
        '\\label{chap:sucesor-102-03}':
            '\\label{chap:sucesor-102-03}\n\\input{ampliacion_20260919/02_geometria_app.tex}',
        '\\label{chap:sucesor-102-12}':
            '\\label{chap:sucesor-102-12}\n\\input{ampliacion_20260919/06_euler_conservacion.tex}'
    }
    for key,val in replacements.items():
        assert w.count(key)==1,key
        w=w.replace(key,val)
    wrapper.write_text(w)
    (MAN/'main.tex').write_text(s)
    bbl=PROJECT/'output/REVISION_EDITORIAL_HMT_MD_20260905/02_PDF/INTEGRAL/main_paquete_union_demostrativa_20260904.bbl'
    (ROOT/'build').mkdir(exist_ok=True)
    if bbl.exists():
        shutil.copy2(bbl,ROOT/'build/main.bbl')
    (ROOT/'metadata/ENTRADA_MAESTRA.json').write_text(json.dumps({
        'main':str((MAN/'main.tex').relative_to(ROOT)),
        'working_directory':str(MAN.relative_to(ROOT)),
        'origin_main':str(src),
        'source_copy_count':len(rows),
        'delivery_ready':False},ensure_ascii=False,indent=2)+'\n')
    print('BASE_COPIADA',len(rows),'archivos; maestro',MAN/'main.tex')

if __name__=='__main__':
    prepare()
