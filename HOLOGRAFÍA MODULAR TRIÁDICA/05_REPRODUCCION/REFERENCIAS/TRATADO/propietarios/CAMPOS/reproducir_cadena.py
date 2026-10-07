#!/usr/bin/env python3
"""Check the single source closure; compile only changed or uncached sources."""
from pathlib import Path
import ast
import importlib.util
import json
import sys

sys.dont_write_bytecode = True

def configure(root):
    spec = importlib.util.spec_from_file_location('hmt_exceptional_verifier', root/'verificar_lean.py')
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)
    found = set()
    for node in ast.parse((root/'reproducir_voa.py').read_text()).body:
        if (isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Attribute)
                and isinstance(node.target.value, ast.Name) and node.target.value.id == 'verifier'
                and node.target.attr in ('SOURCE_ROOTS','MANDATORY_MODULES','PROBE_DECLARATIONS')):
            key = node.target.attr
            setattr(v,key,getattr(v,key)+ast.literal_eval(node.value))
            found.add(key)
    if found != {'SOURCE_ROOTS','MANDATORY_MODULES','PROBE_DECLARATIONS'}:
        raise RuntimeError('Predecessor runner configuration changed')
    manifest = json.loads((root/'MANIFIESTO.json').read_text())
    for key, directory in [('graded_trace_successor','deltas/traza'),
            ('charged_fields_successor','deltas/campos'),
            ('field_covariance_successor','deltas/covariancia'),
            ('field_generation_successor','deltas/generacion'),
            ('exceptional_union_successor','deltas/union')]:
        v.SOURCE_ROOTS += (directory,)
        v.MANDATORY_MODULES += tuple(manifest[key]['modules'])
    # Every source's own #print axioms is checked on compilation or verified
    # cache reuse. The previous 534 and peer 160 queries retain their receipts.
    # This fresh final import probe checks the joint entry, not those counts again.
    v.PROBE_DECLARATIONS = tuple(manifest['exceptional_union_successor']['axiom_queries'])
    return v

if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    verifier = configure(root)
    sys.argv = [sys.argv[0], '--root', str(root), *sys.argv[1:]]
    raise SystemExit(verifier.main())
