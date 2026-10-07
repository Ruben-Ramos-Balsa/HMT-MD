#!/usr/bin/env python3
"""Recompile the weight-support delta only; inspect all public declarations."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/ruben/Documents/New project')
PARENT = ROOT / 'output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage18_article_I/exceptional/twisted_fields/terminal_contragredient_results_20260922/VERIFICATION.json'
PARENT_SHA = 'd1911674fa5a59d25d63246ab73cc1057057c02a91439dda92d785c10d91e51d'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')
LEAN_SHA = 'c89073b8a577a5914ead7b740d2ad996af1ad5ad5b4bfc2825e0bce2f01b6aa4'
MODULES = [
    'LatticeTwistedNormalEnergy', 'LatticeTwistedRawEnergy',
    'LatticeTwistedCorrectedEnergy', 'SkewFieldEnergy',
    'LatticeTwistedPairingEnergy', 'LatticeTwistedFullEnergy',
    'LatticeContragredientWeightSupport',
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert sha(PARENT) == PARENT_SHA and sha(LEAN) == LEAN_SHA
    parent = json.loads(PARENT.read_text())
    assert parent['status'] == 'PASS_TWISTED_TERMINAL_DELTA'
    env = os.environ.copy()
    env['LEAN_PATH'] = str(HERE)+':'+parent['lean_path']
    declarations, records, log = [], [], []
    for module in MODULES:
        source = HERE/(module+'.lean')
        body = source.read_text()
        stripped = re.sub(r'/\-.*?\-/', '', body, flags=re.S)
        assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', stripped)
        namespace = re.search(r'^namespace\s+(\S+)', body, flags=re.M).group(1)
        names = re.findall(r'^(?:@\[[^\n]*?\]\s*)?(?:def|theorem|lemma|abbrev)\s+(\w+)', body, flags=re.M)
        declarations.extend(namespace+'.'+name for name in names)
        cmd = [str(LEAN), '-DwarningAsError=true', '-o', str(source.with_suffix('.olean')), str(source)]
        proc = subprocess.run(cmd, cwd=HERE, env=env, text=True, capture_output=True)
        log.append(module+'\n'+proc.stdout+proc.stderr)
        (HERE/'compile.log').write_text('\n'.join(log))
        if proc.returncode:
            raise RuntimeError(module+'\n'+proc.stdout+proc.stderr)
        records.append({'module':module, 'source_sha256':sha(source),
                        'olean_sha256':sha(source.with_suffix('.olean')), 'command':cmd})
        print('PASS '+module, flush=True)
    probe = HERE/'WeightSupportAxioms.lean'
    probe.write_text('\n'.join('import '+module for module in MODULES)+'\n'+
                     '\n'.join('#print axioms '+name for name in declarations)+'\n')
    proc = subprocess.run([str(LEAN), str(probe)], cwd=HERE, env=env, text=True, capture_output=True)
    (HERE/'axioms.log').write_text(proc.stdout+proc.stderr)
    assert proc.returncode == 0, proc.stdout+proc.stderr
    found = re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", proc.stdout, flags=re.S)
    ax = {name:[a.strip() for a in items.split(',') if a.strip()] for name,items in found}
    independent = re.findall(r"'([^']+)' does not depend on any axioms", proc.stdout)
    ax.update({name:[] for name in independent})
    assert set(ax) == set(declarations), set(declarations)-set(ax)
    assert not any(set(xs)-{'propext','Classical.choice','Quot.sound'} for xs in ax.values())
    result = {
        'status':'PASS_CONTRAGREDIENT_HOMOGENEOUS_WEIGHT_SUPPORT',
        'modules':records, 'declarations':ax,
        'compiler':str(LEAN), 'compiler_sha256':sha(LEAN),
        'parent_receipt':str(PARENT), 'parent_receipt_sha256':sha(PARENT),
        'lean_path':env['LEAN_PATH'], 'verifier_sha256':sha(Path(__file__)),
        'compile_log_sha256':sha(HERE/'compile.log'), 'axioms_log_sha256':sha(HERE/'axioms.log'),
        'scope':'Actual raw/corrected/descended/TE energy covariance and one-weight support of the actual contragredient coefficient. No additional covariance hypothesis in the terminal theorem; no assertion of mixed Jacobi.',
    }
    (HERE/'VERIFICATION.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':result['status'],'modules':len(records),'declarations':len(ax)}))

if __name__ == '__main__':
    main()
