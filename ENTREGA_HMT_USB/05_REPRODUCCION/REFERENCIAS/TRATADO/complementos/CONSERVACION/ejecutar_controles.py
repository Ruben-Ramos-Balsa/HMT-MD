#!/usr/bin/env python3
"""Ejecuta los controles suplementarios; no certifica el corpus completo."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    scripts = sorted((here / 'antecedentes').glob('verificar*.py'))
    scripts += sorted(here.glob('verificar*.py'))
    runs = []
    for script in scripts:
        for optimized in (False, True):
            command = [sys.executable, '-I', '-S']
            if optimized: command.append('-O')
            command.append(str(script))
            proc = subprocess.run(command, cwd=script.parent, capture_output=True, text=True)
            runs.append(dict(script=str(script.relative_to(here)),
                             sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                             optimized=optimized, returncode=proc.returncode,
                             stdout=proc.stdout, stderr=proc.stderr))
            print(script.name, 'optimized='+str(optimized), 'exit='+str(proc.returncode), flush=True)
            if proc.returncode != 0:
                print(proc.stdout, proc.stderr)
    report = dict(scope='finite exact supplementary controls; analytical proofs are in the manuscript',
                  runs=runs, passed=all(r['returncode']==0 for r in runs))
    if args.report:
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if not report['passed']: raise SystemExit(1)
    print('PASS_CONTROLES_SUPLEMENTARIOS', len(runs))

if __name__ == '__main__': main()
