#!/usr/bin/env python3
"""Reproduce the conserved exceptional chain and the vacuum product step."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parent
if '--plan' not in sys.argv:
    checked=subprocess.run([sys.executable,'-I','-S',str(root/'comprobar_datos_incidencia.py')])
    if checked.returncode:
        raise SystemExit(checked.returncode)
spec=importlib.util.spec_from_file_location('chain_runner',root/'reproducir_cadena.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
v=m.configure(root)
section=json.loads((root/'MANIFIESTO.json').read_text())['vacuum_products_successor']
v.SOURCE_ROOTS+=('deltas/productos',)
v.MANDATORY_MODULES+=tuple(section['modules'])
v.PROBE_DECLARATIONS+=tuple(section['axiom_queries'])
sys.argv=[sys.argv[0],'--root',str(root),*sys.argv[1:]]
raise SystemExit(v.main())
