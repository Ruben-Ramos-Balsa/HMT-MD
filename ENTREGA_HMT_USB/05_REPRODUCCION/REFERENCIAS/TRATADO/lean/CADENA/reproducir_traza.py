#!/usr/bin/env python3
"""One entry for the preserved base and its all-weight reflected trace."""
from pathlib import Path
import ast
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('hmt_trace_runner', root / 'verificar_lean.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
# Reuse the predecessor's declared closure without executing its main routine.
config = ast.parse((root / 'reproducir_voa.py').read_text())
seen = set()
for node in config.body:
    if (isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Attribute)
            and isinstance(node.target.value, ast.Name)
            and node.target.value.id == 'verifier'
            and node.target.attr in ('SOURCE_ROOTS', 'MANDATORY_MODULES', 'PROBE_DECLARATIONS')):
        key = node.target.attr
        setattr(verifier, key, getattr(verifier, key) + ast.literal_eval(node.value))
        seen.add(key)
if seen != {'SOURCE_ROOTS', 'MANDATORY_MODULES', 'PROBE_DECLARATIONS'}:
    raise RuntimeError('Predecessor closure configuration changed')
manifest = json.loads((root / 'MANIFIESTO.json').read_text())
trace = manifest['graded_trace_successor']
verifier.SOURCE_ROOTS += ('deltas/traza',)
verifier.MANDATORY_MODULES += tuple(trace['modules'])
verifier.PROBE_DECLARATIONS += tuple(trace['axiom_queries'])
sys.argv = [sys.argv[0], '--root', str(root), *sys.argv[1:]]
raise SystemExit(verifier.main())
