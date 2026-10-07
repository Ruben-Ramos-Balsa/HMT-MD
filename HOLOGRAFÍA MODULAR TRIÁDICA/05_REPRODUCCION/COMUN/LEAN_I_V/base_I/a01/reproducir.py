#!/usr/bin/env python3
"""Explicit ordinary replay; --plan only authenticates the delivered closure."""
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parent
args = sys.argv[1:]
if any(a == '--package-root' or a.startswith('--package-root=') or
       a == '--bundle-sha256' or a.startswith('--bundle-sha256=') for a in args):
    raise SystemExit('The wrapper binds its own package root and bundle SHA256.')
defaults = []
if not any(a == '--report-dir' or a.startswith('--report-dir=') for a in args):
    defaults = ['--report-dir', str(root.parent/(root.name+'_resultados_nuevos'))]
raise SystemExit(subprocess.call([sys.executable, '-I', '-S',
    str(root/'verificar_incremento.py'), '--package-root', str(root),
    '--bundle-sha256', 'b61cf786919e529a3982ee67f225d9a43c13316a10508e64056ef6a5215640b6', *defaults, *args]))
