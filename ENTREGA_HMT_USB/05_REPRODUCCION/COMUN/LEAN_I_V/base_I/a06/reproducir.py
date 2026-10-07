#!/usr/bin/env python3
"""Replay only the new vertex/conformal closure on authenticated predecessors."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root/'verificar_productos.py'
spec = importlib.util.spec_from_file_location('hmt_vertex_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules', *['SelectedConformalVertex', 'LatticeEvenLocality', 'LatticeEvenConformal']]
for flag, value in [
    ('--vertex-root', root/'lean/vertex'),
    ('--conformal-root', root/'lean/conformal'),
    ('--involution-root', root/'lean/involution'),
    ('--translation-root', root/'antecedente/lean'),
    ('--translation-report-dir', root/'antecedente/recibos/traslacion'),
    ('--locality-root', root/'antecedente/antecedente/lean'),
    ('--locality-report-dir', root/'antecedente/antecedente/recibos/localidad_estados'),
    ('--generator-locality-report-dir', root/'antecedente/antecedente/recibos/localidad_generadores'),
    ('--coherence-root', root/'antecedente/antecedente/antecedente/lean'),
    ('--coherence-report-dir', root/'antecedente/antecedente/antecedente/recibos/coherencia'),
    ('--helper', root/'antecedente/antecedente/antecedente/verificar_delta.py'),
    ('--locality-helper', root/'antecedente/antecedente/verificar_localidad.py'),
    ('--translation-helper', root/'antecedente/verificar_traslacion.py'),
    ('--vertex-helper', root/'verificar_conforme.py'),
    ('--involution-report-dir', root/'recibos/involucion'),
    ('--conformal-report-dir', root/'recibos/conforme'),
    ('--base', root/'antecedente/antecedente/antecedente/antecedente/antecedente'),
    ('--report-dir', root/'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag, str(value)]
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
