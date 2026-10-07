#!/usr/bin/env python3
"""Reuse the full preserved closure; add the jointly produced frame reader."""
from pathlib import Path
import contextlib
import importlib.util
import json
import subprocess
import sys

sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
if '--plan' not in sys.argv:
    check = subprocess.run([sys.executable, '-I', '-S', str(root / 'comprobar_datos_incidencia.py')])
    if check.returncode:
        raise SystemExit(check.returncode)
spec = importlib.util.spec_from_file_location('chain_runner', root / 'reproducir_cadena.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
verifier = module.configure(root)
manifest = json.loads((root / 'MANIFIESTO.json').read_text())
for key, directory in [
    ('vacuum_products_successor', 'deltas/productos'),
    ('charged_locality_successor', 'deltas/localidad'),
    ('generated_enrichment_mixed_successor', 'deltas/integracion'),
    ('survival_register_successor', 'deltas/supervivencia'),
    ('iterated_selector_signature_successor', 'deltas/selector'),
    ('joint_reading_transport_successor', 'deltas/lectura_conjunta'),
]:
    section = manifest[key]
    verifier.SOURCE_ROOTS += (directory,)
    verifier.MANDATORY_MODULES += tuple(section['modules'])
    verifier.PROBE_DECLARATIONS += tuple(section['axiom_queries'])
# Every predecessor's query is preserved in its source/cache receipt. Repeating
# hundreds of them in a single final process wastes time without changing any
# theorem. Probe the explicit cross-module interfaces of this delta here.
verifier.PROBE_DECLARATIONS = tuple(manifest['joint_reading_transport_successor']['integration_queries'])
sys.argv = [sys.argv[0], '--root', str(root), *sys.argv[1:]]
log = root / 'resultados/lectura_conjunta.log'
log.parent.mkdir(exist_ok=True)
with log.open('w') as stream, contextlib.redirect_stdout(stream):
    code = verifier.main()
receipt = root / 'resultados/lean_unificado' / ('PLAN.json' if '--plan' in sys.argv else 'VERIFICATION.json')
data = json.loads(receipt.read_text())
print(json.dumps({'status': data['status'], 'returncode': code,
                  'modules': data.get('local_module_count'),
                  'compiled': len(data.get('compiled_modules', [])),
                  'cached': len(data.get('cached_modules', [])),
                  'error': data.get('error'), 'receipt': str(receipt), 'log': str(log)}, indent=2))
raise SystemExit(code)
