#!/usr/bin/env python3
"""Check the negation-lift delta over the verified selected-algebra build."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
BUILD = HERE / 'algebra_build'
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

previous_path = HERE / 'SELECTED_ALGEBRA_VERIFICATION.json'
previous = json.loads(previous_path.read_text())
assert previous['status'] == 'PASS_SELECTED_LATTICE_ALGEBRA_INCREMENTAL'
for row in previous['compiled']:
    assert sha(row['source']) == row['source_sha256']
    assert sha(BUILD / (row['module'] + '.olean')) == row['object_sha256']
source = HERE / 'WittNegationLift.lean'
shutil.copy2(source, BUILD / source.name)
cmd = ['/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean',
    '-DwarningAsError=true', '--root=' + str(BUILD),
    '-o', str(BUILD / 'WittNegationLift.olean'), str(BUILD / source.name)]
start = time.monotonic()
proc = subprocess.run(cmd, capture_output=True, text=True,
    env=dict(os.environ, LEAN_PATH=previous['lean_path']), timeout=180)
output = proc.stdout + proc.stderr
(BUILD / 'WittNegationLift.log').write_text(output)
axioms = {a.strip() for group in re.findall(r'depends on axioms:\s*\[([^]]*)\]', output)
    for a in group.split(',') if a.strip()}
ok = proc.returncode == 0 and axioms <= {'propext','Classical.choice','Quot.sound'} and 'sorryAx' not in output
result = {'status': 'PASS_WITT_NEGATION_LIFT' if ok else 'FAIL_WITT_NEGATION_LIFT',
    'source': str(source), 'source_sha256': sha(source), 'command': cmd,
    'antecedent_receipt': str(previous_path), 'antecedent_receipt_sha256': sha(previous_path),
    'antecedents_recompiled': False, 'elapsed_seconds': round(time.monotonic()-start, 3),
    'axioms': sorted(axioms), 'output': output, 'exit_code': proc.returncode}
if ok:
    result['object_sha256'] = sha(BUILD / 'WittNegationLift.olean')
(HERE / 'WITT_NEGATION_VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n')
print(output)
print(result['status'])
raise SystemExit(0 if ok else 1)
