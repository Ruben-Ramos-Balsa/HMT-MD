#!/usr/bin/env python3
"""Sella el contenido documental y prepara un único paquete de entrega.

El manifiesto acredita integridad material. No decide la validez de los
enunciados ni sustituye los controles de cobertura o de maquetación.
"""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'HOLOGRAFIA_MODULAR_TRIADICA_20260919'

def sha(path):
    value = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()

def included(path):
    rel = path.relative_to(ROOT)
    if '__pycache__' in rel.parts or path.name == '.DS_Store':
        return False
    if rel.parts[0] in {'source', 'incoming', 'datos', 'evidencia', 'tools'}:
        return True
    if rel.parts[0] == 'output':
        return rel == Path('output/pdf') / (NAME + '.pdf')
    if rel.parts[0] == 'lean':
        return 'build' not in rel.parts and path.suffix not in {'.olean', '.ilean'}
    if rel.parts[0] == 'verificaciones':
        return 'build' not in rel.parts and path.suffix not in {'.olean', '.ilean', '.o', '.so', '.trace'}
    if rel.parts[0] == 'metadata':
        if path.name in {'MANIFIESTO_ENTREGA.json', 'RECIBO_PAQUETE_ENTREGA.json'}:
            return False
        if path.name.startswith('qa_') or path.suffix in {'.png', '.jpg', '.jpeg', '.pdf', '.aux', '.log', '.out'}:
            return False
        if path.name.startswith('texto_'):
            return False
        return True
    return len(rel.parts) == 1 and path.suffix in {'.md', '.sh'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    manifest_path = ROOT / 'metadata/MANIFIESTO_ENTREGA.json'
    archive_path = ROOT.parent / (NAME + '_FUENTES_Y_CERTIFICADOS.zip')
    if args.verify_only:
        manifest = json.loads(manifest_path.read_text())
        errors = [row['path'] for row in manifest['files']
                  if not (ROOT / row['path']).is_file()
                  or sha(ROOT / row['path']) != row['sha256']]
        print(json.dumps({'files': len(manifest['files']), 'errors': errors,
                          'status': 'PASS_INTEGRIDAD_ENTREGA' if not errors else 'FAIL_INTEGRIDAD_ENTREGA'}))
        raise SystemExit(bool(errors))
    pdf = ROOT / 'output/pdf' / (NAME + '.pdf')
    if not pdf.is_file():
        raise SystemExit('No existe el PDF final; no se prepara una entrega parcial.')
    editorial = json.loads((ROOT / 'metadata/VERIFICACION_EDITORIAL_FINAL.json').read_text())
    if editorial['status'] != 'PASS_COMPOSICION_DOCUMENTAL_FINAL' or editorial['sha256'] != sha(pdf):
        raise SystemExit('El PDF requiere su control editorial final actualizado antes de empaquetar.')
    paths = sorted(p for p in ROOT.rglob('*') if p.is_file() and included(p))
    rows = [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in paths]
    manifest = {
        'schema': 'hmt-entrega-documental-v1',
        'title': 'Holografía Modular Triádica',
        'subtitle': 'Exposición sistemática del núcleo formal, sus extensiones y derivaciones.',
        'scope': 'Integridad de PDF, fuentes y evidencia; no certificación matemática global.',
        'excluded_work_products': ['build/', 'qa/', 'imágenes y PDF intermedios de metadata/', 'caché compilada de verificaciones/'],
        'preservation': 'Los productos excluidos permanecen en la carpeta de trabajo. Los paquetes de evidencia se incluyen íntegros.',
        'file_count': len(rows), 'total_bytes': sum(r['bytes'] for r in rows), 'files': rows,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in paths + [manifest_path]:
            archive.write(path, str(Path(NAME) / path.relative_to(ROOT)))
    with zipfile.ZipFile(archive_path) as archive:
        damaged = archive.testzip()
        entries = len(archive.infolist())
    receipt = {
        'scope': 'Integridad del paquete ZIP y de su manifiesto.',
        'status': 'PASS_PAQUETE_DOCUMENTAL' if damaged is None else 'FAIL_PAQUETE_DOCUMENTAL',
        'archive': str(archive_path), 'archive_sha256': sha(archive_path),
        'archive_bytes': archive_path.stat().st_size, 'archive_entries': entries,
        'manifest': str(manifest_path), 'manifest_sha256': sha(manifest_path),
        'pdf': str(pdf), 'pdf_sha256': sha(pdf), 'damaged_entry': damaged,
    }
    (ROOT / 'metadata/RECIBO_PAQUETE_ENTREGA.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(receipt, ensure_ascii=False))

if __name__ == '__main__':
    main()
