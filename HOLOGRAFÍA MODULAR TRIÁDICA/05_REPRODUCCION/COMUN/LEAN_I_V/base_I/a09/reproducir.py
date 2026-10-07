#!/usr/bin/env python3
"""Replay the normal-coherence source closure with the preserved HMT base."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root / 'verificar_delta.py'
spec = importlib.util.spec_from_file_location('hmt_normal_coherence_verifier', path)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
arguments = sys.argv[1:]
defaults = []
for flag, value in [('--base', root / 'antecedente/antecedente'),
                    ('--source-root', root / 'lean'),
                    ('--report-dir', root / 'resultados')]:
    if not any(arg == flag or arg.startswith(flag + '=') for arg in arguments):
        defaults.extend([flag, str(value)])
sys.argv = [str(path), *defaults, *arguments]
raise SystemExit(verifier.main())
