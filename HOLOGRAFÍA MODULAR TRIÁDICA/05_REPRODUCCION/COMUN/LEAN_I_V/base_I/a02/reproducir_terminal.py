#!/usr/bin/env python3
"""Replay only the terminal consumers of the authenticated state fields."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root/'verificar_terminal.py'
spec = importlib.util.spec_from_file_location('hmt_terminal_replay',path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args,defaults = sys.argv[1:],[]
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules',*['LatticeTwistedPositiveConformal', 'LatticeTwistedContragredientCoefficients', 'LatticeTwistedCoordinateConjugation', 'LatticeIntegerFockPairing']]
for flag,value in [
    ('--base',root/'antecedente'),
    ('--parent-report-dir',root/'recibos/descendientes'),
    ('--parent-receipt-sha256','b42c80807a0fc92bd4ee316158d0492d51dfa8b9f6772a38b5996a96c32f0662'),
    ('--parent-verifier',root/'verificar_descendientes.py'),
    ('--parent-source-dir',root/'lean/descendants'),
    ('--normalization-report-dir',root/'recibos/normalizacion'),
    ('--normalization-verifier',root/'verificar_normalizacion.py'),
    ('--continuation-report-dir',root/'recibos/continuacion'),
    ('--continuation-verifier',root/'verificar_continuacion.py'),
    ('--continuation-source-dir',root/'lean/continuation'),
    ('--source-dir',root/'lean/terminal'),
    ('--report-dir',root/'resultados_terminales_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag,str(value)]
sys.argv = [str(path),*defaults,*args]
raise SystemExit(runner.main())
