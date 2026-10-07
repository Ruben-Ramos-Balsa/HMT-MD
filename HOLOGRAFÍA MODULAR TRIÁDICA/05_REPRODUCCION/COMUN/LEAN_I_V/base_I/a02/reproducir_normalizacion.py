#!/usr/bin/env python3
"""Explicit replay: connecting a USB does not execute code."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root/'verificar_normalizacion.py'
spec = importlib.util.spec_from_file_location('hmt_continuation_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args, defaults = sys.argv[1:], []
for flag, value in [
    ('--base', root/'antecedente'),
    ('--source', root/'lean/normalization/LatticeTwistedChargeNormalization.lean'),
    ('--report-dir', root/'resultados_normalizacion_nuevos'),
]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag, str(value)]
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
