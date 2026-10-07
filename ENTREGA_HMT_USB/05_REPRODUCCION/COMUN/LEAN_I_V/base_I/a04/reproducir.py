#!/usr/bin/env python3
"""Replay only the delivered finite-module delta; never auto-run from USB."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
old = root/'antecedente'
vertex = old/'antecedente'
path = root/'verificar_modulo_finito.py'
spec = importlib.util.spec_from_file_location('hmt_finite_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules', *['LatticeOrbifoldGrading', 'LatticeTwistedWeightTwo']]
for flag, value in [
    ('--finite-root', root/'lean/finite'),
    ('--orbifold-root', old/'lean/orbifold'),
    ('--twisted-root', old/'lean/twisted'),
    ('--orbifold-helper', old/'verificar_orbifold.py'),
    ('--orbifold-report-dir', old/'recibos/incremento'),
    ('--products-helper', vertex/'verificar_productos.py'),
    ('--vertex-helper', vertex/'verificar_conforme.py'),
    ('--vertex-root', vertex/'lean/vertex'),
    ('--conformal-root', vertex/'lean/conformal'),
    ('--involution-root', vertex/'lean/involution'),
    ('--products-report-dir', vertex/'recibos/productos'),
    ('--conformal-report-dir', vertex/'recibos/conforme'),
    ('--involution-report-dir', vertex/'recibos/involucion'),
    ('--translation-root', vertex/'antecedente/lean'),
    ('--translation-report-dir', vertex/'antecedente/recibos/traslacion'),
    ('--locality-root', vertex/'antecedente/antecedente/lean'),
    ('--locality-report-dir', vertex/'antecedente/antecedente/recibos/localidad_estados'),
    ('--generator-locality-report-dir', vertex/'antecedente/antecedente/recibos/localidad_generadores'),
    ('--coherence-root', vertex/'antecedente/antecedente/antecedente/lean'),
    ('--coherence-report-dir', vertex/'antecedente/antecedente/antecedente/recibos/coherencia'),
    ('--helper', vertex/'antecedente/antecedente/antecedente/verificar_delta.py'),
    ('--locality-helper', vertex/'antecedente/antecedente/verificar_localidad.py'),
    ('--translation-helper', vertex/'antecedente/verificar_traslacion.py'),
    ('--base', vertex/'antecedente/antecedente/antecedente/antecedente/antecedente'),
    ('--report-dir', root/'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag, str(value)]
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
