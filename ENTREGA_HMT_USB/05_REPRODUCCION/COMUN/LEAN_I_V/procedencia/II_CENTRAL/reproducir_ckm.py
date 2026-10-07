#!/usr/bin/env python3
"""Authenticate the selected I base, reuse exact sources, compile CKM consumer."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[2]
BASE = WORK / 'output/PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922'
CKM = WORK / 'output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage11_contributions/II_CKM'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')
MATHLIB = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4')
OUT = HERE / 'ckm_reproduction'
BUILD = OUT / 'build'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    base = json.loads((BASE / 'REGISTRO_REPRODUCCION.json').read_text())
    old = json.loads((CKM / 'GeneratedCKMClosure_CHECK.json').read_text())
    require(old['status'] == 'PASS_CKM_SOURCE_CLOSURE', 'Historical CKM receipt is not PASS')
    require(sha(LEAN) == 'c89073b8a577a5914ead7b740d2ad996af1ad5ad5b4bfc2825e0bce2f01b6aa4',
            'Compiler binary changed')
    require(subprocess.check_output(['git', '-C', str(MATHLIB), 'rev-parse', 'HEAD'],
                                    text=True).strip() == base['compiler']['mathlib_commit'],
            'Mathlib revision changed')
    roots = []
    for name, row in base['modules'].items():
        for field in ('source', 'object'):
            require(sha(BASE / row[field]) == row[field + '_sha256'], name + ': changed ' + field)
        folder = (BASE / row['object']).parent
        if folder not in roots:
            roots.append(folder)
    roots = [BUILD] + roots + [MATHLIB / '.lake/build/lib/lean']
    roots += sorted((MATHLIB / '.lake/packages').glob('*/.lake/build/lib/lean'))
    roots += [LEAN.parent.parent / 'lib/lean']
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, roots)))
    rows = []
    for row in old['source_closure']:
        name = row['module']
        if name in base['modules']:
            require(row['sha256'] == base['modules'][name]['source_sha256'],
                    'Incompatible historical shared source: ' + name)
            continue
        source = Path(row['source'])
        require(sha(source) == row['sha256'], 'Changed historical source: ' + name)
        rows.append((name, source))
    rows.append(('SelectedCKMPublication', HERE / 'SelectedCKMPublication.lean'))
    done = []
    for name, source in rows:
        target, obj = BUILD / (name + '.lean'), BUILD / (name + '.olean')
        cache = OUT / (name + '.json')
        prior = json.loads(cache.read_text()) if cache.exists() else {}
        if prior.get('source_sha256') == sha(source) and obj.exists() and \
                prior.get('object_sha256') == sha(obj) and prior.get('exit_code') == 0:
            print('REUSE_CHECKED', name, flush=True)
            done.append(prior)
            continue
        shutil.copy2(source, target)
        cmd = [str(LEAN), '-DwarningAsError=true', '--root=' + str(BUILD),
               '-o', str(obj), str(target)]
        print('COMPILE', name, flush=True)
        proc = subprocess.run(cmd, cwd=BUILD, env=env, capture_output=True, text=True)
        log = proc.stdout + proc.stderr
        (OUT / (name + '.log')).write_text(log)
        rec = dict(module=name, source=str(source), source_sha256=sha(source),
                   object=str(obj), object_sha256=sha(obj) if obj.exists() else None,
                   exit_code=proc.returncode, command=cmd, log=log)
        cache.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + '\n')
        if proc.returncode:
            raise RuntimeError(log)
        done.append(rec)
    log = done[-1]['log']
    decls = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", log)
    allowed = {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}
    require(len(decls) == 3 and all(set(a.strip() for a in axs.split(',')) <= allowed
                                   for _, axs in decls), 'Unexpected declarations or axioms: ' + str(decls))
    report = dict(status='PASS_SELECTED_CKM_PUBLICATION', declarations=decls,
                  modules=done, antecedent_registry_sha256=sha(BASE / 'REGISTRO_REPRODUCCION.json'),
                  historical_ckm_receipt_sha256=sha(CKM / 'GeneratedCKMClosure_CHECK.json'),
                  fabricated_ledger=False, PublishedRegister_assumed=False,
                  compiler_sha256=sha(LEAN), inherited_modules_recompiled=False,
                  scope='Selected action/sectorial CKM publication, positive quartet, spectral and commutator transport; explicit sector representation and later mass/rephasing parameters.')
    (HERE / 'CKM_VERIFICATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(report['status'])


if __name__ == '__main__':
    main()
