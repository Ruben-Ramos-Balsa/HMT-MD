#!/usr/bin/env python3
"""Replay the existing exceptional interface, then the principal consumer."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
DECL = 'HMT.I.ArticleIPrincipalPublication.article_I_principal_publication'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report-dir', type=Path, required=True)
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--mathlib-root', type=Path, required=True)
    args = ap.parse_args()
    out = args.report_dir.resolve()
    if out.exists() or out.is_relative_to(HERE):
        raise RuntimeError('Choose a fresh result directory outside the delivery')
    out.mkdir(parents=True)
    first = [sys.executable, '-I', '-S', str(HERE/'reproducir.py'),
             '--report-dir', str(out/'exceptional'), '--lean', str(args.lean.resolve()),
             '--mathlib-root', str(args.mathlib_root.resolve())]
    subprocess.run(first, check=True)
    receipt = json.loads((out/'exceptional/VERIFICATION.json').read_text())
    if receipt['status'] != 'PASS_ARTICLE_I_HMT_EXCEPTIONAL_INTERFACE':
        raise RuntimeError('Exceptional antecedent did not compile')
    build = out/'exceptional/build'
    source = HERE/'lean/ArticleIPrincipalPublication.lean'
    shutil.copy2(source, build/source.name)
    mathlib, lean = args.mathlib_root.resolve(), args.lean.resolve()
    roots = [build, mathlib/'.lake/build/lib/lean']
    roots += sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))
    roots += [lean.parent.parent/'lib/lean']
    obj = build/'ArticleIPrincipalPublication.olean'
    cmd = [str(lean), '-DwarningAsError=true', '--root='+str(build),
           '-o', str(obj), str(build/source.name)]
    result = subprocess.run(cmd, cwd=build,
        env=dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, roots))),
        capture_output=True, text=True, timeout=180)
    log = result.stdout+result.stderr
    (out/'compilation.log').write_text(log)
    ax = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", log)
    axioms = [s.strip() for s in ax[0][1].split(',')] if len(ax) == 1 else []
    ok = (result.returncode == 0 and len(ax) == 1 and ax[0][0] == DECL and
          set(axioms) <= {'propext','Classical.choice','Quot.sound','Lean.ofReduceBool'})
    report = dict(status='PASS_ARTICLE_I_PRINCIPAL_PUBLICATION' if ok else 'FAIL_ARTICLE_I_PRINCIPAL_PUBLICATION',
        command=cmd, exit_code=result.returncode, declaration=DECL, axioms=axioms,
        source_sha256=sha(source), log_sha256=sha(out/'compilation.log'),
        object_sha256=sha(obj) if obj.exists() else None,
        compiler=receipt['compiler'], inherited_modules=477,
        newly_compiled_modules=['ArticleIExceptionalInterface','ArticleIPrincipalPublication'],
        inherited_modules_recompiled=False, full_FLM_formalization_claimed=False,
        exceptional_receipt_sha256=sha(out/'exceptional/VERIFICATION.json'),
        scope='Exact principal conjunction of regional, alpha, action/electron, APP-plane, spin/helicity and exceptional proofs; classical application by bibliography.')
    (out/'VERIFICATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    if not ok:
        raise RuntimeError(log)
    print(report['status'])


if __name__ == '__main__':
    main()
