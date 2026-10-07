#!/usr/bin/env python3
"""Check the raw triple annihilations from the two original localities."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
LOCALITY = HERE.parent
STATE_FIELD = LOCALITY.parent / 'state_field'
SOURCE = HERE / 'LatticeTripleLocality.lean'
BUILD = HERE / 'triple_build'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text())

def main():
    inputs = []
    receipt_hashes = {}
    kernel = read(HERE / 'kernel_build/VERIFICATION.json')
    binomial = read(HERE / 'binomial_build/VERIFICATION.json')
    assert kernel['status'] == 'PASS_DONG_RESIDUE_KERNEL'
    assert binomial['status'] == 'PASS_DONG_BINOMIAL_RESIDUE'
    assert sha(HERE/'kernel_build/VERIFICATION.json') == binomial['predecessor_kernel_receipt_sha256']
    for folder, data in [('kernel_build', kernel), ('binomial_build', binomial)]:
        receipt_hashes[folder] = sha(HERE/folder/'VERIFICATION.json')
        source = Path(data['source'])
        inputs.extend([(source,data['source_sha256']),
            (HERE/folder/(source.stem+'.olean'),data['object_sha256'])])
    state_path = STATE_FIELD/'normal_coherence_results/VERIFICATION.json'
    assert sha(state_path) == kernel['predecessor_receipt_sha256']
    state = read(state_path)
    for owner, folder in [(STATE_FIELD, 'normal_coherence_results'), (LOCALITY, 'resultados')]:
        path = owner/folder/'VERIFICATION.json'
        data = read(path)
        assert data['status'] == 'PASS_STATE_FIELD_DELTA'
        receipt_hashes[str(path)] = sha(path)
        for row in data['modules']:
            inputs.extend([(owner/(row['module']+'.lean'),row['source_sha256']),
                (owner/folder/'build'/(row['module']+'.olean'),row['object_sha256'])])
    base = Path(state['base'])
    base_path = base/'resultados/lean_unificado/VERIFICATION.json'
    assert sha(base_path) == kernel['base_receipt_sha256']
    receipt_hashes[str(base_path)] = sha(base_path)
    for row in read(base_path)['modules']:
        inputs.extend([(base/row['source'],row['source_sha256']),
            (base/'resultados/lean_unificado/build'/(row['module'].replace('.','/')+'.olean'),
             row['object_sha256'])])
    for p,h in inputs:
        assert sha(p) == h, p
    lean = Path(kernel['compiler']['executable'])
    assert sha(lean) == kernel['compiler']['binary_sha256']
    BUILD.mkdir(exist_ok=True)
    obj = BUILD/(SOURCE.stem+'.olean')
    before = sha(SOURCE)
    command = [str(lean), '-DwarningAsError=true', '--root='+str(HERE), '-o', str(obj), str(SOURCE)]
    env = dict(os.environ)
    env['LEAN_PATH'] = ':'.join([str(BUILD),str(HERE/'binomial_build'),
        str(LOCALITY/'resultados/build'),kernel['lean_path']])
    start = time.time()
    proc = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (BUILD/'compile.log').write_text(proc.stdout)
    axioms = {name: sorted(re.findall(r'[\w.]+', deps)) for name,deps in
              re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", proc.stdout)}
    unchanged = before == sha(SOURCE) and all(sha(p) == h for p,h in inputs)
    allowed = {'propext','Classical.choice','Quot.sound'}
    ok = proc.returncode == 0 and unchanged and len(axioms) == 16 and all(
        set(a) <= allowed for a in axioms.values())
    receipt = dict(status='PASS_RAW_TRIPLE_LOCALITY' if ok else 'FAIL_RAW_TRIPLE_LOCALITY',
        source=str(SOURCE),source_sha256=before,object_sha256=sha(obj) if proc.returncode == 0 else None,
        inherited_receipts=receipt_hashes,inherited_modules_authenticated=len(inputs)//2,
        sources_and_objects_unchanged=unchanged,command=command,lean_path=env['LEAN_PATH'],
        compiler=kernel['compiler'],elapsed_seconds=time.time()-start,exit_code=proc.returncode,
        declarations=axioms,output=proc.stdout,
        scope='Raw ABC-CAB and BAC-CBA annihilations from A-C/B-C locality; their difference annihilated from A-B locality; all three crossing powers under pointwise vector evaluation. No locality of composites is assumed.')
    (BUILD/'VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(proc.stdout)
    print(receipt['status'])
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
