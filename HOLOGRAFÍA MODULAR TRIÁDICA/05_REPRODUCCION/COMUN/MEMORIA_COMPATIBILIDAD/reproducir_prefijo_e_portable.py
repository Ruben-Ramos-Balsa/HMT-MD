#!/usr/bin/env python3
"""Run the unchanged finite-prefix witness with its owner resolved locally.

Only the OWNER path assignment is adapted in memory. The original file, seed,
lift matrices, calendar and output checks are unchanged. The owner generator
is parsed by the original witness, not executed as a full generation campaign.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / 'fuentes_ley9' / 'reproducir_prefijo_e_1828.py'
OWNER = ROOT / 'fuentes_ley9' / 'propietarios' / 'generar_desde_estructura.py'

def main():
    if not ORIGINAL.is_file() or not OWNER.is_file():
        raise SystemExit('DEPENDENCY_MISSING: finite-prefix original or local owner')
    tree = ast.parse(ORIGINAL.read_text(), filename=str(ORIGINAL))
    changed = 0
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'OWNER' for t in node.targets):
            if len(node.targets) != 1:
                raise SystemExit('Unexpected OWNER assignment; refusing broader adaptation')
            node.value = ast.Call(func=ast.Name(id='Path', ctx=ast.Load()),
                                  args=[ast.Constant(value=str(OWNER))], keywords=[])
            changed += 1
    if changed != 1:
        raise SystemExit('Expected exactly one OWNER path assignment')
    code = compile(ast.fix_missing_locations(tree), str(ORIGINAL), 'exec')
    exec(code, {'__name__': '__main__', '__file__': str(ORIGINAL)})

if __name__ == '__main__':
    main()
