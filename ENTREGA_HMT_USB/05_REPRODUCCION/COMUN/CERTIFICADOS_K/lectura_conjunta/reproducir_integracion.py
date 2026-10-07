#!/usr/bin/env python3
"""Compile the preserved chain with generated records and field locality."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys

sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
if '--plan' not in sys.argv:
    checked = subprocess.run([sys.executable, '-I', '-S',
                              str(root / 'comprobar_datos_incidencia.py')])
    if checked.returncode:
        raise SystemExit(checked.returncode)
spec = importlib.util.spec_from_file_location('chain_runner', root / 'reproducir_cadena.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
verifier = module.configure(root)
manifest = json.loads((root / 'MANIFIESTO.json').read_text())
for key, directory in [('vacuum_products_successor', 'deltas/productos'),
                       ('charged_locality_successor', 'deltas/localidad'),
                       ('generated_enrichment_mixed_successor', 'deltas/integracion')]:
    section = manifest[key]
    verifier.SOURCE_ROOTS += (directory,)
    verifier.MANDATORY_MODULES += tuple(section['modules'])
    verifier.PROBE_DECLARATIONS += tuple(section['axiom_queries'])
sys.argv = [sys.argv[0], '--root', str(root), *sys.argv[1:]]
raise SystemExit(verifier.main())
