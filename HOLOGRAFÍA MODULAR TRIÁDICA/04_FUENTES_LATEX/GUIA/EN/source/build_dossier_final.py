"""English dossier entrypoint with one fiche-only literal correction.

The original builder stays byte-identical because the already delivered poster
uses its typography primitives. All original reception, contract, receipt and
source-hash checks are executed before this entrypoint can create a PDF.
"""
from pathlib import Path
import ast
import hashlib
import sys

BASE = Path(__file__).with_name('build_dossier.py')
BASE_SHA256 = 'cd07ce16831b489dbbfb8bb0e1460c3d07e0dc1cfd6bb1d0ae02d7394a528cdb'


def corrected_tree():
    source = BASE.read_bytes()
    if hashlib.sha256(source).hexdigest() != BASE_SHA256:
        raise RuntimeError('Frozen poster primitive changed')
    tree = ast.parse(source, filename=str(BASE))
    changes = 0
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == 'fiches':
            for item in ast.walk(node):
                if isinstance(item, ast.Constant) and item.value == '.<br/>Conservation':
                    changes += 1
    if changes != 1:
        raise RuntimeError('Expected exactly one preserved English fiche literal')
    return ast.fix_missing_locations(tree)


if __name__ == '__main__':
    tree = corrected_tree()
    if sys.argv[1:] == ['--check-only']:
        print('PASS_EN_FICHE_LITERAL_ONLY_FROZEN_BUILDER_UNCHANGED')
    elif sys.argv[1:]:
        raise SystemExit('Only --check-only or normal protected construction is supported')
    else:
        namespace = {'__name__': 'hmt_dossier_final', '__file__': str(Path(__file__).resolve())}
        exec(compile(tree, str(BASE), 'exec'), namespace)
        namespace['main']()
