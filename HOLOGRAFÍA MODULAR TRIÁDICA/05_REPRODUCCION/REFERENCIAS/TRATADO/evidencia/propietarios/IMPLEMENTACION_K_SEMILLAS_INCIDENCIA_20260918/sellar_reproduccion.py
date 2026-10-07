#!/usr/bin/env python3
"""Attach successful relocation receipts without changing any proved source."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reproduction-root',type=Path,required=True)
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    target=here.parent/'PAQUETE_CONTINUIDAD_K_UNIDAD_20260918'
    source=args.reproduction_root.resolve()
    manifest_path=target/'MANIFIESTO.json'
    manifest=json.loads(manifest_path.read_text())
    base_hash=sha(manifest_path)
    if sha(source/'MANIFIESTO.json') != base_hash:
        raise RuntimeError('Reproduced snapshot differs from delivery snapshot')
    reports=[
        ('resultados/CONSERVACION_DOCUMENTAL.json','CONSERVACION_REUBICADA.json','PASS_CONSERVACION_FUENTES_Y_CLAUSURA_LOCAL'),
        ('resultados/REPRODUCCION_REGIONAL.json','FIRMAS_REUBICADAS.json','PASS_REPRODUCCION_REGIONAL_LOCAL'),
        ('resultados/lean_unificado/VERIFICATION.json','LEAN_REUBICADO.json','PASS_PORTABLE_LEAN_SOURCE_CLOSURE')]
    for old,name,status in reports:
        report=json.loads((source/old).read_text())
        if report['status']!=status:
            raise RuntimeError('Unsuccessful receipt: '+old)
        if name=='LEAN_REUBICADO.json':
            for item in report['sources']:
                if sha(target/item['path'])!=item['sha256']:
                    raise RuntimeError('Proved source changed: '+item['path'])
            if report['manifest_sha256']!=base_hash:
                raise RuntimeError('Lean receipt snapshot mismatch')
        dest=target/'recibos/reproduccion'/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes((source/old).read_bytes())
        manifest['files'].append(dict(path=str(dest.relative_to(target)),source=str(source/old),
            sha256=sha(dest),bytes=dest.stat().st_size,role='SUCCESSFUL_RELOCATION_RECEIPT'))
    manifest['verified_base_manifest_sha256']=base_hash
    manifest['relocation_verification']={
        'status':'PASS_SOURCE_PRESERVATION_REGIONAL_REPRODUCTION_AND_LEAN_CLOSURE',
        'source_files_changed_after_verification':False,
        'scope':'The reproduced source snapshot is unchanged; only these proof receipts extend the manifest.'}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    archive=target.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for relative in sorted({item['path'] for item in manifest['files']}|{'MANIFIESTO.json'}):
            z.write(target/relative,Path(target.name)/relative)
        bad=z.testzip()
        if bad:
            raise RuntimeError('Invalid ZIP member: '+bad)
    print(json.dumps(dict(status='PASS_SEALED_REPRODUCTION',files=len(manifest['files']),
        zip=str(archive),zip_sha256=sha(archive),manifest_sha256=sha(manifest_path)),ensure_ascii=False))

if __name__=='__main__':
    main()
