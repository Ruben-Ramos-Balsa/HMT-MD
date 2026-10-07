#!/usr/bin/env python3
"""Copia verificable del núcleo común, sin modificar fuentes anteriores."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parents[1] / 'PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = json.loads((SOURCE / 'MANIFIESTO.json').read_text())
    checks = []
    for row in manifest['files']:
        src, dst = SOURCE / row['path'], ROOT / row['path']
        if digest(src) != row['sha256']:
            raise SystemExit('Fuente común divergente: ' + str(src))
        if dst.exists() and digest(dst) != row['sha256']:
            raise SystemExit('No se sobrescribe una modificación local: ' + str(dst))
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copyfile(src, dst)
        checks.append({'path': row['path'], 'sha256': digest(dst), 'identical': True})
    result = {'status': 'PASS_IDENTIDAD_NUCLEO_COMUN',
              'scope': 'Identidad de seis archivos; no certifica autonomía ni afirmaciones matemáticas.',
              'source_manifest': str(SOURCE / 'MANIFIESTO.json'), 'files': checks}
    (ROOT / 'technical/NUCLEO_COMUN_RECIBO.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(result['status'], len(checks))

if __name__ == '__main__':
    main()
