#!/usr/bin/env python3
"""Build a successor without altering the 477-module predecessor."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OLD = BASE/'PAQUETE_ARTICULO_I_CAMPOS_ORBIFOLD_CONSTRUIDOS_20260922'
DEST = BASE/'PAQUETE_ARTICULO_I_ENGANCHE_HMT_FLM_20260922'
OLD_SHA = 'cc66cba53f0737d196513197bf796f64d7ed4d5b23c8296cde9df23d18b989ab'
NAMES = ['ClassicalLeechHypotheses','selected_classical_hypotheses',
         'same_generated_mark_and_lattice','selected_radial_norm_is_54',
         'sum_product_defect_matches_selected_norm','full_sum_product_defect_retained',
         'selected_neighbor_no_roots','article_I_exceptional_interface']


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def seal():
    write(DEST/'MANIFIESTO.json', dict(schema='hmt.exceptional.interface.v1',
        scope='Cierre del enganche excepcional HMT; aplicación bibliográfica de FLM',
        predecessor_sha256=OLD_SHA, registered_modules=478,
        files={p.relative_to(DEST).as_posix():sha(p) for p in sorted(DEST.rglob('*'))
               if p.is_file() and p != DEST/'MANIFIESTO.json'}))


def prepare():
    if DEST.exists():
        raise RuntimeError('Refuse to overwrite a delivery')
    if sha(OLD/'MANIFIESTO.json') != OLD_SHA:
        raise RuntimeError('Changed predecessor')
    DEST.mkdir()
    shutil.copytree(OLD,DEST/'antecedente')
    (DEST/'lean').mkdir()
    shutil.copy2(HERE/'ArticleIExceptionalInterface.lean',DEST/'lean/ArticleIExceptionalInterface.lean')
    for name in ['README.md','APLICACION_CLASICA.md','reproducir.py','prepare_delivery.py']:
        shutil.copy2(HERE/name,DEST/name)
    src = BASE/'ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/01/ES/source/sections'
    (DEST/'fuentes_cotejadas').mkdir()
    for name in ['excepcional.tex','bibliografia.tex','incidencia_reticulo.tex']:
        shutil.copy2(src/name,DEST/'fuentes_cotejadas'/name)
    data = json.loads((OLD/'BUNDLE_INPUTS.json').read_text())
    modules = {**data['registry461'],**data['delta15'],**data['selected']}
    if len(modules) != 477:
        raise RuntimeError('Wrong predecessor module count')
    registry = {}
    for name,row in modules.items():
        registry[name] = {k:('antecedente/'+row[k] if k in ('source','object') else row[k])
                         for k in ('source','source_sha256','object','object_sha256')}
    write(DEST/'REGISTRO_REPRODUCCION.json',dict(modules=registry,
        compiler=data['compiler'], external_objects=data['external_objects'],
        declarations=['HMT.I.ArticleIExceptionalInterface.'+n for n in NAMES]))
    seal()
    print(DEST)


def finish(report):
    receipt = json.loads((report/'VERIFICATION.json').read_text())
    if receipt['status'] != 'PASS_ARTICLE_I_HMT_EXCEPTIONAL_INTERFACE':
        raise RuntimeError('Need actual successful replay')
    if sha(DEST/'MANIFIESTO.json') != receipt['manifest_sha256']:
        raise RuntimeError('Input manifest differs from the compiled receipt')
    verification = DEST/'verificacion'
    if verification.exists():
        raise RuntimeError('Already finalized')
    verification.mkdir()
    shutil.copy2(DEST/'MANIFIESTO.json', verification/'MANIFIESTO_ENTRADA_COMPILACION.json')
    for name in ['VERIFICATION.json','compilation.log']:
        shutil.copy2(report/name,verification/name)
    shutil.copy2(report/'build/ArticleIExceptionalInterface.olean',verification/'ArticleIExceptionalInterface.olean')
    shutil.copy2(HERE/'prepare_delivery.py', DEST/'prepare_delivery.py')
    metadata = HERE/'metadata'
    if metadata.is_dir():
        shutil.copytree(metadata, DEST/'metadatos')
    seal()
    zipped = DEST.with_suffix('.zip')
    if zipped.exists():
        raise RuntimeError('Refuse to overwrite ZIP')
    with zipfile.ZipFile(zipped,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(DEST.rglob('*')):
            if p.is_file():
                z.write(p,DEST.name+'/'+p.relative_to(DEST).as_posix())
    with zipfile.ZipFile(zipped) as z:
        if z.testzip() is not None:
            raise RuntimeError('ZIP CRC error')
        files = {p.relative_to(DEST).as_posix():sha(p) for p in DEST.rglob('*') if p.is_file()}
        if set(z.namelist()) != {DEST.name+'/'+p for p in files}:
            raise RuntimeError('ZIP inventory mismatch')
        for name,digest in files.items():
            if hashlib.sha256(z.read(DEST.name+'/'+name)).hexdigest() != digest:
                raise RuntimeError('ZIP content mismatch')
    info = dict(status='PASS_INTERFACE_DELIVERY', package=str(DEST), zip=str(zipped),
                zip_sha256=sha(zipped), manifest_sha256=sha(DEST/'MANIFIESTO.json'),
                files=len(files), registered_modules=478,
                terminal_receipt_sha256=sha(verification/'VERIFICATION.json'),
                full_FLM_formalization_claimed=False, PDFs_modified=False)
    write(HERE/'ENTREGA.json',info)
    print(json.dumps(info,ensure_ascii=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--finish',type=Path)
    args = ap.parse_args()
    finish(args.finish.resolve()) if args.finish else prepare()
