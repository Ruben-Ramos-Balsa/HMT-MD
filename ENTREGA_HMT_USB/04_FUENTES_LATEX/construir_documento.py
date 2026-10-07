"""Portable source entry points. Standard library only; TeX is external.

List: python3 04_FUENTES_LATEX/construir_documento.py --list
Copy sources: python3 04_FUENTES_LATEX/construir_documento.py --id I --language ES --output /chosen/workdir
Compile a working copy: add --compile (requires TeX Live or compatible tools).
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--id')
    parser.add_argument('--language', choices=['ES', 'EN', 'FR'])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--compile', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / '06_VERIFICACION/FUENTES_DOCUMENTALES.json').read_text(encoding='utf-8'))
    if args.list:
        for document in data['documents']:
            print(document['id'], document['language'], document['entrypoint'])
        return 0
    candidates = [d for d in data['documents'] if d['id'] == args.id and d['language'] == args.language]
    if len(candidates) != 1 or args.output is None:
        parser.error('Select an existing --id and --language, with a new --output directory.')
    document = candidates[0]
    output = args.output.resolve()
    if output == root or output.is_relative_to(root):
        parser.error('The working copy must be outside the delivery.')
    if output.exists():
        parser.error('--output must be a new directory; existing files are never overwritten.')
    source = root / document['source_directory']
    shutil.copytree(source, output)
    entry = output / document['entrypoint_relative']
    print(f'Source: {entry}')
    if not args.compile:
        print('Sources copied. No compilation performed.')
        return 0
    engine = document['engine']
    executable = shutil.which(engine)
    if executable is None:
        parser.error(f'{engine} is not available. Install a TeX distribution; the source copy is preserved.')
    for _ in range(3):
        subprocess.run([executable, '-interaction=nonstopmode', '-halt-on-error', entry.name],
                       cwd=entry.parent, check=True)
    print(f'Compilation completed: {entry.with_suffix(".pdf")}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
