#!/usr/bin/env python3
"""Extend the unchanged verifier configuration to the later manifested deltas.

The verifier's compilation and cache checks are unchanged. Previously proved
modules can be reused only under its source/dependency/compiler/object checks.
The source manifest and receipt report the enlarged target set explicitly.
"""
from pathlib import Path
import importlib.util
import sys

sys.dont_write_bytecode=True
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('hmt_full_delta_runner',root/'verificar_lean.py')
verifier=importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
verifier.SOURCE_ROOTS += ('deltas/witt','deltas/accion_electron')
verifier.MANDATORY_MODULES += ('WittReaderCompatibility','SelectedActionDomain',
    'ElectronOrientationBridge','SelectedElectronPublication','SelectedArticleIComposition')
verifier.PROBE_DECLARATIONS += ('HMT.I.WittReaderCompatibility.charge_eq',
    'HMT.I.SelectedArticleI.principal_action_electron_composition')
sys.argv=[sys.argv[0],'--root',str(root),*sys.argv[1:]]
raise SystemExit(verifier.main())
