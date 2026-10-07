"""Check a relocated delivery without executing scientific programs.

Usage: python3 06_VERIFICACION/verificar_integridad.py
Uses only the Python standard library. Never modifies the delivery.
"""
from pathlib import Path
import hashlib
import json
import sys


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = root / '06_VERIFICACION/MANIFIESTO.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    failures = []
    for item in data['files']:
        relative = Path(item['path'])
        path = root / relative
        if relative.is_absolute() or '..' in relative.parts:
            failures.append([item['path'], 'UNSAFE_PATH'])
        elif not path.is_file():
            failures.append([item['path'], 'MISSING'])
        elif path.stat().st_size != item['bytes'] or digest(path) != item['sha256']:
            failures.append([item['path'], 'CHANGED'])
    expected = {f['path'] for f in data['files']}
    ignored = {'06_VERIFICACION/MANIFIESTO.json', '.DS_Store', 'Thumbs.db', 'desktop.ini'}
    unexpected = sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                        if p.is_file() and p.name not in ignored
                        and p.relative_to(root).as_posix() not in ignored
                        and p.relative_to(root).as_posix() not in expected)
    result = {'status': 'PASS_FILE_INTEGRITY' if not failures else 'FAIL_FILE_INTEGRITY',
              'checked_files': len(data['files']), 'failures': failures,
              'additional_files': unexpected,
              'scope': 'File integrity only; no scientific computation or proof is executed.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
