#!/usr/bin/env python3
"""Explicit replay of the delivered descendant delta, not USB autoexecution."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root/'verificar_descendientes.py'
spec = importlib.util.spec_from_file_location('hmt_descendants_replay',path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args,defaults = sys.argv[1:],[]
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules',*['LatticeTwistedPositiveStateDescent', 'LatticeTwistedStateConformal', 'LatticeTwistedCorrectionInverse']]
for flag,value in [
    ('--base',root/'antecedente'),
    ('--normalization-report-dir',root/'recibos/normalizacion'),
    ('--normalization-verifier',root/'verificar_normalizacion.py'),
    ('--continuation-report-dir',root/'recibos/continuacion'),
    ('--continuation-verifier',root/'verificar_continuacion.py'),
    ('--continuation-source-dir',root/'lean/continuation'),
    ('--source-dir',root/'lean/descendants'),
    ('--report-dir',root/'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag,str(value)]
sys.argv = [str(path),*defaults,*args]
raise SystemExit(runner.main())
