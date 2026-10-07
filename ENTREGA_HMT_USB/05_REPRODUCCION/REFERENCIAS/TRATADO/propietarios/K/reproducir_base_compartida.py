#!/usr/bin/env python3
"""Compile the complete declared local closure, including its shared entry point."""
from pathlib import Path
import importlib.util
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('hmt_shared_runner', root / 'verificar_lean.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
verifier.SOURCE_ROOTS += ('deltas/witt', 'deltas/accion_electron', 'deltas/base_compartida')
verifier.MANDATORY_MODULES += ('WittReaderCompatibility', 'SelectedActionDomain',
    'ElectronOrientationBridge', 'SelectedElectronPublication',
    'SelectedArticleIComposition', 'SharedArticleIBase')
verifier.PROBE_DECLARATIONS += ('HMT.I.WittReaderCompatibility.charge_eq',
    'HMT.I.SelectedArticleI.principal_action_electron_composition',
    'HMT.Shared.ArticleI.shared_action_electron_incidence')
sys.argv = [sys.argv[0], '--root', str(root), *sys.argv[1:]]
raise SystemExit(verifier.main())
