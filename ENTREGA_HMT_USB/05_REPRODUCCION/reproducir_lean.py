"""Portable entry to the existing I–V Lean package. No execution by default.

--check-package checks files/imports only. --run explicitly invokes Lean.
Lean 4.21.0 and a built Mathlib tree are required for --run.
"""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check-package',action='store_true')
    group.add_argument('--run',action='store_true')
    parser.add_argument('--article',choices=['all','I','II','III','IV','V'],default='all')
    parser.add_argument('--lean',type=Path)
    parser.add_argument('--mathlib',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    package = root / '05_REPRODUCCION/COMUN/LEAN_I_V'
    output = args.output.resolve()
    if output.exists() or output.is_relative_to(root):
        parser.error('Choose a new output directory outside the delivery.')
    command = [sys.executable,'-I','-S',str(package/'reproducir.py'),'--report-dir',str(output)]
    if args.check_package:
        command.append('--verify-only')
    else:
        lean = args.lean or shutil.which('lean')
        mathlib = args.mathlib or root / '05_REPRODUCCION/DEPENDENCIAS/mathlib4'
        if not lean or not Path(lean).is_file():
            parser.error('Supply the installed Lean 4.21.0 executable using --lean.')
        if not (mathlib/'.lake/build/lib/lean/Mathlib.olean').is_file():
            parser.error('Build the bundled Mathlib sources first, or supply the same built revision using --mathlib.')
        command += ['--article',args.article,'--from-sources','--portable-toolchain','--lean',str(lean),'--mathlib-root',str(mathlib)]
    return subprocess.run(command,check=False).returncode


if __name__ == '__main__':
    sys.exit(main())
