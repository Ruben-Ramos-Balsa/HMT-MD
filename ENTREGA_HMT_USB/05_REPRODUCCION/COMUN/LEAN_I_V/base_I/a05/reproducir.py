#!/usr/bin/env python3
"""Replay only the delivered increment after authenticating its predecessors."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
old = root/'antecedente'
path = root/'verificar_orbifold.py'
spec = importlib.util.spec_from_file_location('hmt_orbifold_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules', *['LatticeEvenProducts', 'LatticeEvenGrading', 'LatticeHalfIntegerField', 'LatticeParityNondegenerate', 'LatticeHalfVirasoroRelations']]
for flag, value in [
    ('--orbifold-root', root/'lean/orbifold'),
    ('--twisted-root', root/'lean/twisted'),
    ('--products-helper', old/'verificar_productos.py'),
    ('--vertex-helper', old/'verificar_conforme.py'),
    ('--vertex-root', old/'lean/vertex'),
    ('--conformal-root', old/'lean/conformal'),
    ('--involution-root', old/'lean/involution'),
    ('--products-report-dir', old/'recibos/productos'),
    ('--conformal-report-dir', old/'recibos/conforme'),
    ('--involution-report-dir', old/'recibos/involucion'),
    ('--translation-root', old/'antecedente/lean'),
    ('--translation-report-dir', old/'antecedente/recibos/traslacion'),
    ('--locality-root', old/'antecedente/antecedente/lean'),
    ('--locality-report-dir', old/'antecedente/antecedente/recibos/localidad_estados'),
    ('--generator-locality-report-dir', old/'antecedente/antecedente/recibos/localidad_generadores'),
    ('--coherence-root', old/'antecedente/antecedente/antecedente/lean'),
    ('--coherence-report-dir', old/'antecedente/antecedente/antecedente/recibos/coherencia'),
    ('--helper', old/'antecedente/antecedente/antecedente/verificar_delta.py'),
    ('--locality-helper', old/'antecedente/antecedente/verificar_localidad.py'),
    ('--translation-helper', old/'antecedente/verificar_traslacion.py'),
    ('--base', old/'antecedente/antecedente/antecedente/antecedente/antecedente'),
    ('--report-dir', root/'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag, str(value)]
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
