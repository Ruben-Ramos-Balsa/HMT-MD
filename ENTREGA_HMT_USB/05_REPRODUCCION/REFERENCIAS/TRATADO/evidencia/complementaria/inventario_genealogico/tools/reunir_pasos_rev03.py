#!/usr/bin/env python3
"""Conserva REV02 literalmente y añade el desarrollo elemental REV03."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path('/Users/ruben/Documents/New project')
NEW = ROOT/'REV03_PASOS_Y_CONTRATOS'
PARTS = [
    '24_CONCORDANCIA_Y_SIGUIENTE_PRECISION.md',
    '20_TRIT_OPERACIONES_Y_PRUEBAS.md',
    '21_EMISOR_TRAZA_COMPLETA.md',
    '22_REFINAMIENTO_CAMBIO_CARTA_PASOS.md',
    '23_CONTRATOS_FORMALIZACION_Y_CONSTRUCCION.md',
]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def preserve_write(path, text):
    raw = text.encode('utf-8')
    if path.exists():
        assert path.read_bytes() == raw, f'Revisión ya escrita distinta: {path}'
    else:
        path.write_bytes(raw)

def record(path):
    raw = path.read_bytes()
    return {'path':str(path),'sha256':sha(raw),'bytes':len(raw)}

def main():
    for version in ('01','02'):
        m = json.loads((ROOT/f'MANIFIESTO_REV{version}.json').read_text())
        assert sha(Path(m['artifact']).read_bytes()) == m['artifact_sha256']
        for item in m['parts']:
            assert sha(Path(item['path']).read_bytes()) == item['sha256']
    previous = ROOT/'INVENTARIO_ACUMULATIVO_REV02.md'
    records=[]
    pieces=[]
    for path in [previous]+[NEW/name for name in PARTS]:
        raw=path.read_bytes()
        body=raw.decode('utf-8')
        assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',body), path
        item=record(path);item['lines']=len(body.splitlines());records.append(item)
        pieces.append(f'\n<!-- BEGIN INTEGRAL {path.name}; SHA256={item["sha256"]} -->\n\n'+body+f'\n<!-- END INTEGRAL {path.name} -->\n')
    artifact=ROOT/'INVENTARIO_ACUMULATIVO_REV03.md'
    text=(
        '# Inventario genealógico HMT — revisión acumulativa 03\n\n'
        '19 de septiembre de 2026. Contiene REV02 íntegra —y, dentro de ella, REV01 íntegra— '
        'más las operaciones, pruebas descompuestas, trazas y contratos de REV03. '
        'Esta ampliación no declara completo el inventario global ni compilado el futuro tratado.\n\n'
        f'Acceso a lo añadido: [concordancia y siguiente precisión](<{NEW/PARTS[0]}>).\n'
    )+'\n'.join(pieces)
    assert previous.read_text() in text
    assert (ROOT/'INVENTARIO_ACUMULATIVO_REV01.md').read_text() in text
    links=re.findall(r'\]\(<(/[^>]+)>\)',text)
    missing=[]
    for ref in links:
        path=Path(re.sub(r':\d+(?:-\d+)?$','',ref))
        if not path.exists() and path!=artifact:
            missing.append(ref)
    assert not missing,missing
    preserve_write(artifact,text)
    support=[record(p) for p in sorted(NEW.iterdir()) if p.is_file() and p.suffix in ('.md','.json','.tsv','.py')]
    manifest={
        'artifact':str(artifact),'artifact_sha256':sha(text.encode()),'parts':records,
        'support_files':support,
        'rev02_preserved_verbatim':True,'rev01_preserved_verbatim':True,
        'prior_part_hashes_unchanged':True,'local_links_checked':len(links),'missing_local_links':[],
        'global_corpus_scope_preserved':True,'global_source_roots':56,
        'all_dependencies_validated':False,'mathematical_completeness_certified':False,
        'new_pdf_compilation':False,'new_lean_compilation':False,
        'source_files_modified':[],'pdfs_modified':[],
        'documentary_scope':'DESARROLLO_ELEMENTAL_Y_CONTRATOS_PARA_REDACCION_POSTERIOR',
    }
    preserve_write(ROOT/'MANIFIESTO_REV03.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    old_receipt=ROOT/'RECIBO_CAUSAL_REV02.json'
    receipt=json.loads(old_receipt.read_text())
    receipt.update({
        'artifact':str(artifact),'artifact_sha256':manifest['artifact_sha256'],
        'result_id':'INVENTARIO_DOCUMENTAL_GENERATIVO_HMT_20260919_REV03',
        'scope_note':'Conservación literal de REV02 y REV01. Desarrollo elemental TRIT, emisor, refinamiento y contratos. No certifica exhaustividad global, CH, un PDF ni una compilación Lean nueva.',
        'current_source_map':str(NEW/PARTS[0]),
        'inherited_receipt':{'path':str(old_receipt),'sha256':sha(old_receipt.read_bytes())},
    })
    receipt['genealogy']['source_locators']=[
        f'{r["path"]}:1-{r["lines"]} sha256={r["sha256"]}' for r in records
    ]
    receipt['result_boundary']['work_performed']=[
        'Preservación literal de REV01 y REV02 y control de sus partes',
        'Descomposición de pruebas de aritmética trítica y realizaciones cuadráticas',
        'Traza completa reproducible del emisor de 54 operaciones con fibras',
        'Desarrollo de recurrencias, inversas y publicación de cilindros',
        'Localización de contratos materiales y herramientas LaTeX/Lean/Python',
    ]
    preserve_write(ROOT/'RECIBO_CAUSAL_REV03.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    refs=subprocess.check_output(
        ['python3','-I','-S',str(PROJECT/'PUBLICACION_HMT/SERIE_ARTICULOS_HMT/herramientas/render_referencias_serie.py')],
        text=True,cwd=PROJECT)
    preserve_write(ROOT/'REFERENCIAS_SERIE_REV03.md',refs)
    print(json.dumps({k:manifest[k] for k in ('artifact','artifact_sha256','rev02_preserved_verbatim','rev01_preserved_verbatim','local_links_checked','new_pdf_compilation','new_lean_compilation')},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
