#!/usr/bin/env python3
"""Same common closure, followed by fields and their operator covariance."""
from pathlib import Path
import ast
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('hmt_covariance_runner', root/'verificar_lean.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
seen = set()
for node in ast.parse((root/'reproducir_voa.py').read_text()).body:
    if (isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Attribute)
            and isinstance(node.target.value, ast.Name) and node.target.value.id == 'verifier'
            and node.target.attr in ('SOURCE_ROOTS', 'MANDATORY_MODULES', 'PROBE_DECLARATIONS')):
        key = node.target.attr
        setattr(verifier, key, getattr(verifier, key)+ast.literal_eval(node.value))
        seen.add(key)
if seen != {'SOURCE_ROOTS', 'MANDATORY_MODULES', 'PROBE_DECLARATIONS'}:
    raise RuntimeError('Predecessor configuration changed')
manifest = json.loads((root/'MANIFIESTO.json').read_text())
for key, directory in [('graded_trace_successor','deltas/traza'),
                       ('charged_fields_successor','deltas/campos'),
                       ('field_covariance_successor','deltas/covariancia')]:
    section = manifest[key]
    verifier.SOURCE_ROOTS += (directory,)
    verifier.MANDATORY_MODULES += tuple(section['modules'])
    verifier.PROBE_DECLARATIONS += tuple(section['axiom_queries'])
sys.argv = [sys.argv[0], '--root', str(root), *sys.argv[1:]]
raise SystemExit(verifier.main())
