#!/usr/bin/env python3
"""Prepare the reviewed REV04 successor through the unchanged canonical gates.

The registered assertion remains documentary. No scientific status is promoted.
Every changed source is compared with the preserved REV03 before materialization.
"""
import argparse
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parents[1] / 'APERTURAS_PAPER_RESTAURADAS_20260911_REV03' / ROOT.name
HERE = ROOT / 'technical/preflight_20260911'
spec = importlib.util.spec_from_file_location('iv_editorial_rev04', HERE / 'preparar_editorial.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
engine.OLD = OLD
engine.REVIEW = OLD / 'technical'

JUSTIFICATIONS = {
 'sections/extension.tex': 'Etiqueta interna de la construcción de curvatura mixta ya incluida; texto y fórmulas intactos.',
 'sections/registro_k.tex': 'Inclusión contigua de la caracterización integral ya demostrada en II.',
 'sections/registro_imagen_integral.tex': 'Recuperación íntegra de II: relaciones, inversa, Hadamard, covarianza, contribuciones y falsadores.',
 'sections/continuo_conjunto.tex': 'Mapa tipado de las cinco operaciones conjuntas, numeración automática y contextualización del terminal.',
 'sections/01_hilbert_nonadico.tex': 'Recuperación del cociclo polarizado y de la extensión central orientada, con sus pruebas.',
 'sections/iv_mapa_operaciones.tex': 'Mapa de dominios y operaciones del mismo estado genealógico.',
 'sections/iv_weyl_orientado.tex': 'Forma alternante, cociclo, extensión y representación, conservando la convención X^a Z^b.',
}

def prepare():
    def files(root):
        return {str(p.relative_to(root)):p for p in {root/'main.tex', *root.joinpath('sections').rglob('*.tex'), *root.joinpath('figures').rglob('*')} if p.is_file()}
    before, after = files(OLD), files(ROOT)
    engine.ensure(set(before) <= set(after), 'Se ha retirado una fuente previa.')
    changes=[]
    for name,path in sorted(after.items()):
        oldhash=engine.digest(before[name]) if name in before else None
        if oldhash == engine.digest(path):
            continue
        engine.ensure(name in JUSTIFICATIONS, 'Cambio sin revisión declarada: '+name)
        changes.append({'path':name,'before_sha256':oldhash,'after_sha256':engine.digest(path),
            'disposition':'AMPLIAR' if oldhash is None else 'SUSTITUIR_POR_CORRECCION_TRAZADA',
            'justification':JUSTIFICATIONS[name],
            'content_preserved':'Original conservado en REV03; las pruebas anteriores se cotejan separadamente en QA_REV04.json.',
            'residences':[{'path':name}]})
    delta={'technical_review_by':'root','technical_review_complete':True,
        'author_review_of_exact_matrix_or_hashes':False,'source_root':str(ROOT),
        'predecessor_root':str(OLD),'common_kernel':engine.spec(engine.COMMON),'changes':changes,
        'scope':'Recuperaciones matemáticas y edición focal autorizadas; no nueva validación global de física ni de problemas terminales.'}
    path=HERE/'DELTA_EDITORIAL_REVISADO_REV04.json'
    engine.write(path,delta)
    engine.prepare(path)

def run_preflight():
    run=engine.current_run()
    engine.contract(run)
    path=run/'CONTRATO_PRECOMPILACION.json'
    value=engine.read(path)
    value['artifact']['output_pdf']=str(ROOT/'output/pdf/MOONSHINE_DUALIDAD_T_Y_TEORIA_M.pdf')
    engine.write(path,value)
    import subprocess,sys
    return subprocess.run([sys.executable,'-I','-S',str(engine.SCRIPTS/'precompile_hmt_md.py'),
        '--contract',str(path),'--receipt',str(run/'RECIBO_PRECOMPILACION.json')],check=False).returncode

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['prepare','registration-patch','run'])
    args=parser.parse_args()
    if args.mode=='prepare': prepare()
    elif args.mode=='registration-patch': engine.registration_patch(engine.current_run())
    else: raise SystemExit(run_preflight())
