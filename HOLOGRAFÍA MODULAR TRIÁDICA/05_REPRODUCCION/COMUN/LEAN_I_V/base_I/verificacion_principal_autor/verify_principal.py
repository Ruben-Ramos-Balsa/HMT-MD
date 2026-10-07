#!/usr/bin/env python3
"""Authenticate preserved inputs and compile only the Article I consumer."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKAGE = Path('/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_ENGANCHE_HMT_FLM_20260922')
PREVIOUS = HERE.parent / 'COMPROBACION_INTERFAZ_FINAL_20260922'
MATHLIB = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4')
SOURCE_SHA = 'abcdec5a3f44672f546070eb69a6945e4d4348523ba35292dd1f103e9357cf9f'
REGISTRY_SHA = 'a8b3cb25ef5dd3fec120c85dbfa3f9e3b7f948a431890c593355ecbf0ac3ad8d'
MANIFEST_SHA = '16107f09ddb59b569335d5fcb6aeb3f48da277c94d88c6ffc990751082b3f8d0'
RECEIPT_SHA = '266d9b8913747b36cac0db5188b7ee835ee779033c30a07fab6d06726ddee3af'
DECLARATION = 'HMT.I.ArticleIPrincipalPublication.article_I_principal_publication'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    source = HERE / 'ArticleIPrincipalPublication.lean'
    tracked = {
        str(source): SOURCE_SHA,
        str(PACKAGE / 'REGISTRO_REPRODUCCION.json'): REGISTRY_SHA,
        str(PACKAGE / 'MANIFIESTO.json'): MANIFEST_SHA,
        str(PREVIOUS / 'VERIFICATION.json'): RECEIPT_SHA,
        str(Path(__file__).resolve()): sha(__file__),
    }
    for name, digest in tracked.items():
        require(sha(name) == digest, 'Changed input: ' + name)
    registry = read(PACKAGE / 'REGISTRO_REPRODUCCION.json')
    prior = read(PREVIOUS / 'VERIFICATION.json')
    require(prior['status'] == 'PASS_ARTICLE_I_HMT_EXCEPTIONAL_INTERFACE', 'Unverified antecedent')
    for name, digest in read(PACKAGE / 'MANIFIESTO.json')['files'].items():
        require(sha(PACKAGE / name) == digest, 'Changed delivery: ' + name)
    compiler = registry['compiler']
    lean = Path(compiler['executable'])
    tracked[str(lean)] = compiler['binary_sha256']
    commit = subprocess.check_output(['git', '-C', str(MATHLIB), 'rev-parse', 'HEAD'], text=True).strip()
    require(commit == compiler['mathlib_commit'], 'Unmatched Mathlib revision')
    roots = [MATHLIB / '.lake/build/lib/lean']
    roots += sorted((MATHLIB / '.lake/packages').glob('*/.lake/build/lib/lean'))
    roots += [lean.parent.parent / 'lib/lean']
    for name, item in registry['external_objects'].items():
        rel = Path(*name.split('.')).with_suffix('.olean')
        obj = next((root / rel for root in roots if (root / rel).is_file()), None)
        require(obj is not None, 'Missing external object: ' + name)
        tracked[str(obj)] = item['sha256']
    build = PREVIOUS / 'build'
    for name, item in registry['modules'].items():
        tracked[str(build / Path(*name.split('.')).with_suffix('.olean'))] = item['object_sha256']
    tracked[str(build / 'ArticleIExceptionalInterface.olean')] = prior['object_sha256']
    for name, digest in tracked.items():
        require(sha(name) == digest, 'Changed compiled dependency: ' + name)
    out = HERE / 'resultados'
    require(not out.exists(), 'Result directory already exists; preserve it')
    out.mkdir()
    obj = out / 'ArticleIPrincipalPublication.olean'
    command = [str(lean), '-DwarningAsError=true', '--root=' + str(HERE), '-o', str(obj), str(source)]
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, [build] + roots)))
    result = subprocess.run(command, cwd=HERE, env=env, text=True, capture_output=True, timeout=180)
    output = result.stdout + result.stderr
    (out / 'compilation.log').write_text(output)
    report = dict(status='FAIL_ARTICLE_I_PRINCIPAL_PUBLICATION', command=command,
                  exit_code=result.returncode, compiler=compiler,
                  source=str(source), source_sha256=sha(source),
                  imports=['ArticleIExceptionalInterface', 'SelectedCylinderSignature',
                           'APPSpinBridge', 'ElectronSpinRotation'],
                  inherited_modules_recompiled=False, pdfs_changed=False,
                  full_FLM_formalization_claimed=False,
                  declaration=DECLARATION, log_sha256=sha(out / 'compilation.log'))

    def save():
        (out / 'VERIFICATION.json').write_text(json.dumps(report, indent=2) + '\n')

    save()
    require(result.returncode == 0, output)
    matches = list(re.finditer(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output))
    require(len(matches) == 1 and matches[0][1] == DECLARATION, 'Unexpected axiom report')
    axioms = [x.strip() for x in matches[0][2].split(',') if x.strip()]
    require(set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'},
            'Unexpected axiom')
    for name, digest in tracked.items():
        require(sha(name) == digest, 'Input changed during compilation: ' + name)
    report.update(status='PASS_ARTICLE_I_PRINCIPAL_PUBLICATION', axioms=axioms,
                  object=str(obj), object_sha256=sha(obj),
                  authenticated_and_unchanged_artifacts=tracked,
                  scope='Composition of existing regional, alpha, action/electron, APP-plane, '
                        'spin/helicity and exceptional-interface proofs; explicit dimensional '
                        'units, refinement and unit direction; classical FLM remains bibliographic.')
    save()
    print(report['status'])


if __name__ == '__main__':
    main()
