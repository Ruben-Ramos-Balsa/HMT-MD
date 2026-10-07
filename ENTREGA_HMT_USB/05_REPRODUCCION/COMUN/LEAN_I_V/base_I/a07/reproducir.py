#!/usr/bin/env python3
"""Replay the checked state-field translation delta on its unchanged origin."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root / 'verificar_traslacion.py'
spec = importlib.util.spec_from_file_location('hmt_translation_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
for flag, value in [
    ('--modules', 'SelectedTranslationCoherence'),
    ('--source-root', root / 'lean'),
    ('--base', root / 'antecedente/antecedente/antecedente/antecedente'),
    ('--locality-root', root / 'antecedente/lean'),
    ('--locality-report-dir', root / 'antecedente/recibos/localidad_estados'),
    ('--generator-locality-report-dir', root / 'antecedente/recibos/localidad_generadores'),
    ('--coherence-root', root / 'antecedente/antecedente/lean'),
    ('--coherence-report-dir', root / 'antecedente/antecedente/recibos/coherencia'),
    ('--helper', root / 'antecedente/antecedente/verificar_delta.py'),
    ('--locality-helper', root / 'antecedente/verificar_localidad.py'),
    ('--report-dir', root / 'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag + '=') for a in args):
        defaults.extend([flag, str(value)])
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
