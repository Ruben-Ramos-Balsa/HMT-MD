#!/usr/bin/env python3
"""Read-only file-integrity check for the reorganized, portable library.

This checks distributed files, not mathematical results or scientific execution.
Python 3 standard library only. No dependencies or network access.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys

MANIFEST = '06_VERIFICACION/MANIFIESTO_DISTRIBUCION.json'
ORIGINAL = '06_VERIFICACION/MANIFIESTO.json'
ORIGINAL_SHA = '3bc8a5aad20d7de02f511d0eddd731524c2767734b93c3e4e8e853886d7fd03f'

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def relative(value):
    p = PurePosixPath(value)
    if not value or p.is_absolute() or '..' in p.parts or '\\' in value or ':' in value or p.as_posix() != value:
        raise ValueError('Unsafe manifest path: ' + value)
    return value

def verify(root):
    root = root.resolve()
    manifest = json.loads((root / MANIFEST).read_text(encoding='utf-8'))
    if manifest['schema'] != 'HMT_PORTABLE_LIBRARY_V2':
        raise ValueError('Unknown manifest schema')
    records = manifest['files']
    expected = {relative(r['path']): r for r in records}
    if len(expected) != len(records) or MANIFEST in expected:
        raise ValueError('Duplicate/self-referential manifest entry')
    failures, verified, ignored = [], 0, []
    actual = set()
    for folder, dirs, files in os.walk(root, followlinks=False):
        for name in dirs:
            p = Path(folder) / name
            if p.is_symlink():
                failures.append({'path': str(p.relative_to(root)), 'issue': 'symbolic_link'})
        for name in files:
            p = Path(folder) / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                failures.append({'path': rel, 'issue': 'symbolic_link'})
                continue
            if name == '.DS_Store':
                ignored.append(rel)
                continue
            actual.add(rel)
    for rel in sorted(actual - set(expected) - {MANIFEST}):
        failures.append({'path': rel, 'issue': 'unexpected_file'})
    for rel, row in expected.items():
        p = root / rel
        if rel not in actual or not p.is_file():
            failures.append({'path': rel, 'issue': 'missing_file'})
        elif p.stat().st_size != row['bytes'] or digest(p) != row['sha256']:
            failures.append({'path': rel, 'issue': 'content_mismatch'})
        else:
            verified += 1
    if digest(root / ORIGINAL) != ORIGINAL_SHA:
        failures.append({'path': ORIGINAL, 'issue': 'original_manifest_changed'})
    original = json.loads((root / ORIGINAL).read_text(encoding='utf-8'))
    delta = json.loads((root / '06_VERIFICACION/PROCEDENCIA/REORGANIZACION.json').read_text(encoding='utf-8'))
    preserved = 0
    for row in original['files']:
        if row['path'] == '.DS_Store':
            continue
        destination = delta['originals_preserved'].get(row['path'], row['path'])
        p = root / relative(destination)
        if not p.is_file() or p.stat().st_size != row['bytes'] or digest(p) != row['sha256']:
            failures.append({'path': row['path'], 'issue': 'original_not_preserved'})
        else:
            preserved += 1
    return {'status': 'FAIL_LIBRARY_FILES' if failures else 'PASS_LIBRARY_FILES',
            'verified_files': verified, 'original_records_preserved': preserved,
            'original_manifest_preserved': digest(root / ORIGINAL) == ORIGINAL_SHA,
            'finder_metadata_ignored': ignored, 'failure_count': len(failures),
            'failures': failures,
            'scope': 'File integrity and preservation only; not mathematical certification.'}

if __name__ == '__main__':
    try:
        root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
        result = verify(root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(0 if result['status'] == 'PASS_LIBRARY_FILES' else 1)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('FAIL_LIBRARY_FILES: ' + str(error))
        raise SystemExit(1)
