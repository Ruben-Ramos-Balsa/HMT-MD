#!/usr/bin/env python3
"""Preserve the sealed exceptional delivery and append one principal consumer."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OLD = BASE/'PAQUETE_ARTICULO_I_ENGANCHE_HMT_FLM_20260922'
DEST = BASE/'PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922'
AUTHOR = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_ARTICULO_I_20260917/principal_electron')
OLD_SHA = '16107f09ddb59b569335d5fcb6aeb3f48da277c94d88c6ffc990751082b3f8d0'
SOURCE_SHA = 'abcdec5a3f44672f546070eb69a6945e4d4348523ba35292dd1f103e9357cf9f'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n')


def seal():
    write(DEST/'MANIFIESTO.json', dict(schema='hmt.article-I.principal-publication.v1',
        predecessor_sha256=OLD_SHA, registered_modules=479,
        full_FLM_formalization_claimed=False,
        files={p.relative_to(DEST).as_posix():sha(p) for p in sorted(DEST.rglob('*'))
               if p.is_file() and p != DEST/'MANIFIESTO.json'}))


def prepare():
    if DEST.exists() or sha(OLD/'MANIFIESTO.json') != OLD_SHA:
        raise RuntimeError('Require an unchanged predecessor and a new delivery')
    source = AUTHOR/'ArticleIPrincipalPublication.lean'
    if sha(source) != SOURCE_SHA:
        raise RuntimeError('Changed compiled principal source')
    old_manifest = json.loads((OLD/'MANIFIESTO.json').read_text())
    for name, digest in old_manifest['files'].items():
        if sha(OLD/name) != digest:
            raise RuntimeError('Changed predecessor file: '+name)
    shutil.copytree(OLD, DEST)
    history = DEST/'historia_entrega'
    history.mkdir()
    for name in ['README.md','MANIFIESTO.json','prepare_delivery.py']:
        shutil.copy2(DEST/name, history/name)
    for name in ['README.md','reproducir_principal.py','prepare_delivery.py']:
        shutil.copy2(HERE/name, DEST/name)
    shutil.copy2(source, DEST/'lean'/source.name)
    shutil.copy2(source, HERE/source.name)
    proof = DEST/'verificacion_principal_autor'
    proof.mkdir()
    for name in ['VERIFICATION.json','compilation.log','ArticleIPrincipalPublication.olean']:
        shutil.copy2(AUTHOR/'resultados'/name, proof/name)
    shutil.copy2(AUTHOR/'verify_principal.py', proof/'verify_principal.py')
    shutil.copy2(AUTHOR/'README.md', proof/'README.md')
    seal()
    print(DEST)


def finish(report):
    receipt = json.loads((report/'VERIFICATION.json').read_text())
    if receipt['status'] != 'PASS_ARTICLE_I_PRINCIPAL_PUBLICATION':
        raise RuntimeError('Need successful relocated replay')
    v = DEST/'verificacion_principal'
    if v.exists():
        raise RuntimeError('Already finalized')
    v.mkdir()
    for name in ['VERIFICATION.json','compilation.log']:
        shutil.copy2(report/name, v/name)
    shutil.copy2(DEST/'MANIFIESTO.json', v/'MANIFIESTO_ENTRADA_COMPILACION.json')
    shutil.copy2(report/'exceptional/VERIFICATION.json', v/'VERIFICATION_EXCEPCIONAL.json')
    shutil.copy2(report/'exceptional/build/ArticleIPrincipalPublication.olean',v/'ArticleIPrincipalPublication.olean')
    if (HERE/'metadata').is_dir():
        shutil.copytree(HERE/'metadata', DEST/'metadatos_principal')
    seal()
    archive = DEST.with_suffix('.zip')
    if archive.exists():
        raise RuntimeError('Archive exists')
    files = {p.relative_to(DEST).as_posix():sha(p) for p in DEST.rglob('*') if p.is_file()}
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for name in sorted(files):
            z.write(DEST/name, DEST.name+'/'+name)
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None or set(z.namelist()) != {DEST.name+'/'+n for n in files}:
            raise RuntimeError('ZIP integrity error')
        for n,digest in files.items():
            if hashlib.sha256(z.read(DEST.name+'/'+n)).hexdigest() != digest:
                raise RuntimeError('ZIP hash error: '+n)
    info = dict(status='PASS_ARTICLE_I_PRINCIPAL_DELIVERY', package=str(DEST), zip=str(archive),
        zip_sha256=sha(archive), manifest_sha256=sha(DEST/'MANIFIESTO.json'),
        terminal_receipt_sha256=sha(v/'VERIFICATION.json'), files=len(files),
        registered_modules=479, full_FLM_formalization_claimed=False, PDFs_modified=False)
    write(HERE/'ENTREGA.json',info)
    print(json.dumps(info,ensure_ascii=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--finish', type=Path)
    args = ap.parse_args()
    finish(args.finish.resolve()) if args.finish else prepare()
