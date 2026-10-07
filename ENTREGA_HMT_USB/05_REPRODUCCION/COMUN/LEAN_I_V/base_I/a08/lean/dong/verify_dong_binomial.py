#!/usr/bin/env python3
"""Authenticate and compile only the triple-crossing/binomial delta."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent.parent / 'state_field'
SOURCE = HERE / 'LatticeDongBinomial.lean'
BUILD = HERE / 'binomial_build'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    kernel_path = HERE / 'kernel_build/VERIFICATION.json'
    kernel = json.loads(kernel_path.read_text())
    assert kernel['status'] == 'PASS_DONG_RESIDUE_KERNEL'
    authenticated = [(Path(kernel['source']), kernel['source_sha256']),
        (HERE / 'kernel_build/LatticeDongKernel.olean', kernel['object_sha256'])]
    prior_path = PREVIOUS / 'normal_coherence_results/VERIFICATION.json'
    assert sha(prior_path) == kernel['predecessor_receipt_sha256']
    prior = json.loads(prior_path.read_text())
    for row in prior['modules']:
        authenticated.extend([
            (PREVIOUS / (row['module']+'.lean'), row['source_sha256']),
            (PREVIOUS / 'normal_coherence_results/build' / (row['module']+'.olean'),
             row['object_sha256'])])
    base = Path(prior['base'])
    base_path = base / 'resultados/lean_unificado/VERIFICATION.json'
    assert sha(base_path) == kernel['base_receipt_sha256']
    base_receipt = json.loads(base_path.read_text())
    for row in base_receipt['modules']:
        authenticated.extend([
            (base / row['source'], row['source_sha256']),
            (base / 'resultados/lean_unificado/build' /
             (row['module'].replace('.','/')+'.olean'), row['object_sha256'])])
    for path, expected in authenticated:
        assert sha(path) == expected, path
    lean = Path(kernel['compiler']['executable'])
    assert sha(lean) == kernel['compiler']['binary_sha256']
    BUILD.mkdir(exist_ok=True)
    target = BUILD / (SOURCE.stem+'.olean')
    before = sha(SOURCE)
    command = [str(lean), '-DwarningAsError=true', '--root='+str(HERE),
               '-o', str(target), str(SOURCE)]
    env = dict(os.environ)
    env['LEAN_PATH'] = str(BUILD)+':'+kernel['lean_path']
    start = time.time()
    proc = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    (BUILD / 'compile.log').write_text(proc.stdout)
    axioms = {name: sorted(re.findall(r'[\w.]+', deps)) for name, deps in
              re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", proc.stdout)}
    unchanged = sha(SOURCE) == before and all(sha(p) == h for p,h in authenticated)
    allowed = {'propext','Classical.choice','Quot.sound'}
    ok = proc.returncode == 0 and unchanged and len(axioms) == 10 and all(
        set(a) <= allowed for a in axioms.values())
    receipt = dict(status='PASS_DONG_BINOMIAL_RESIDUE' if ok else 'FAIL_DONG_BINOMIAL_RESIDUE',
        source=str(SOURCE), source_sha256=before,
        object_sha256=sha(target) if proc.returncode == 0 else None,
        predecessor_kernel_receipt_sha256=sha(kernel_path),
        inherited_modules_authenticated=len(authenticated)//2,
        sources_and_objects_unchanged=unchanged, command=command,
        lean_path=env['LEAN_PATH'], compiler=kernel['compiler'],
        elapsed_seconds=time.time()-start, exit_code=proc.returncode,
        declarations=axioms, output=proc.stdout,
        scope='Exact binomial bound on a vector and concrete triple-crossing/residue identities; actual field integrand annihilations are not assumed to have been discharged.')
    (BUILD / 'VERIFICATION.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(proc.stdout)
    print(receipt['status'])
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
