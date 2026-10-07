#!/usr/bin/env python3
"""Check the residue-kernel delta; no claim of complete Dong locality."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent.parent / 'state_field'
SOURCE = HERE / 'LatticeDongKernel.lean'
BUILD = HERE / 'kernel_build'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    prior_path = PREVIOUS / 'normal_coherence_results/VERIFICATION.json'
    prior = json.loads(prior_path.read_text())
    assert prior['status'] == 'PASS_STATE_FIELD_DELTA'
    assert len(prior['modules']) == 17
    authenticated = []
    for row in prior['modules']:
        src = PREVIOUS / (row['module']+'.lean')
        obj = PREVIOUS / 'normal_coherence_results/build' / (row['module']+'.olean')
        assert sha(src) == row['source_sha256'], src
        assert sha(obj) == row['object_sha256'], obj
        authenticated.extend([(src,row['source_sha256']),(obj,row['object_sha256'])])
    base = Path(prior['base'])
    base_path = base / 'resultados/lean_unificado/VERIFICATION.json'
    base_receipt = json.loads(base_path.read_text())
    assert base_receipt['status'] == 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE'
    assert len(base_receipt['modules']) == 279
    for row in base_receipt['modules']:
        src = base / row['source']
        obj = base / 'resultados/lean_unificado/build' / (row['module'].replace('.','/')+'.olean')
        assert sha(src) == row['source_sha256'], src
        assert sha(obj) == row['object_sha256'], obj
        authenticated.extend([(src,row['source_sha256']),(obj,row['object_sha256'])])
    BUILD.mkdir(exist_ok=True)
    lean = Path(prior['compiler']['executable'])
    assert sha(lean) == prior['compiler']['binary_sha256']
    before = sha(SOURCE)
    target = BUILD / (SOURCE.stem+'.olean')
    command = [str(lean), '-DwarningAsError=true', '--root='+str(HERE), '-o', str(target), str(SOURCE)]
    env = dict(os.environ)
    env['LEAN_PATH'] = str(BUILD)+':'+prior['lean_path']
    start = time.time()
    proc = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (BUILD / 'compile.log').write_text(proc.stdout)
    axioms = {name: sorted(re.findall(r'[\w.]+', deps)) for name,deps in
              re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", proc.stdout)}
    unchanged = sha(SOURCE) == before and all(sha(p) == h for p,h in authenticated)
    allowed = {'propext','Classical.choice','Quot.sound'}
    ok = proc.returncode == 0 and unchanged and len(axioms) == 7 and all(set(a) <= allowed for a in axioms.values())
    receipt = dict(status='PASS_DONG_RESIDUE_KERNEL' if ok else 'FAIL_DONG_RESIDUE_KERNEL',
        source=str(SOURCE), source_sha256=before, object_sha256=sha(target) if proc.returncode == 0 else None,
        predecessor_receipt_sha256=sha(prior_path), base_receipt_sha256=sha(base_path),
        inherited_modules_authenticated=296, sources_and_objects_unchanged=unchanged,
        command=command, lean_path=env['LEAN_PATH'], compiler=prior['compiler'],
        elapsed_seconds=time.time()-start, exit_code=proc.returncode, declarations=axioms, output=proc.stdout,
        scope='All-degree residue-kernel coefficients, signs, polynomial clearing and order split; not the full Dong locality proof.')
    (BUILD / 'VERIFICATION.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(proc.stdout)
    print(receipt['status'])
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
