#!/usr/bin/env python3
"""Replay the all-state locality proof on the unchanged selected HMT carrier."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root / 'verificar_localidad.py'
spec = importlib.util.spec_from_file_location('hmt_locality_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
for flag, value in [
    ('--modules', 'SelectedDescendantLocality'),
    ('--source-root', root / 'lean'),
    ('--dong-root', root / 'lean/dong'),
    ('--coherence-root', root / 'antecedente/lean'),
    ('--coherence-report-dir', root / 'antecedente/recibos/coherencia'),
    ('--locality-report-dir', root / 'recibos/localidad_generadores'),
    ('--helper', root / 'antecedente/verificar_delta.py'),
    ('--base', root / 'antecedente/antecedente/antecedente'),
    ('--report-dir', root / 'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag + '=') for a in args):
        defaults.extend([flag, str(value)])
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
