#!/usr/bin/env python3
"""Reproduce the selected Article IV increment over the authenticated Article I delivery."""
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
SOURCES = [
    ('OrthogonalKScreen', 'OrthogonalKScreen.lean'),
    ('SelectedKDirection', 'k_direction/SelectedKDirection.lean'),
    ('P3ChartProjection', 'k_direction/P3ChartProjection.lean'),
    ('SelectedLorentzScreen', 'lorentz_screen/SelectedLorentzScreen.lean'),
    ('ArticleIVSelectedScreens', 'ArticleIVSelectedScreens.lean'),
]
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    return json.loads(Path(p).read_text())


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--parent', type=Path, required=True,
                    help='Unpacked PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922')
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--mathlib-root', type=Path, required=True)
    ap.add_argument('--report-dir', type=Path, required=True)
    args = ap.parse_args()
    parent, lean, mathlib, out = [p.resolve() for p in
                                (args.parent, args.lean, args.mathlib_root, args.report_dir)]
    require(not out.exists() and not out.is_relative_to(HERE) and
            not out.is_relative_to(parent), 'Choose a fresh external result directory')
    out.mkdir(parents=True)
    report = dict(status='RUNNING', inherited_modules_recompiled=False, pdfs_changed=False)
    tracked = {}

    def save():
        (out / 'VERIFICATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')

    def authenticate(p, digest):
        require(p.is_file() and sha(p) == digest, 'Changed input: ' + str(p))
        tracked[str(p)] = digest

    try:
        for name, digest in read(HERE / 'MANIFEST.json')['files'].items():
            p = HERE / name
            require(p.resolve().is_relative_to(HERE), 'Unsafe increment locator')
            authenticate(p, digest)
        parent_manifest = read(parent / 'MANIFIESTO.json')
        require(sha(parent / 'MANIFIESTO.json') ==
                '1c0b6133b4a17367294542ee21c750d9d824f9ca741473e32add034261c1ac28',
                'Unexpected Article I edition')
        for name, digest in parent_manifest['files'].items():
            p = parent / name
            require(p.resolve().is_relative_to(parent), 'Unsafe parent locator')
            authenticate(p, digest)
        registry = read(parent / 'REGISTRO_REPRODUCCION.json')
        compiler = registry['compiler']
        authenticate(lean, compiler['binary_sha256'])
        commit = subprocess.check_output(['git', '-C', str(mathlib), 'rev-parse', 'HEAD'],
                                         text=True).strip()
        require(commit == compiler['mathlib_commit'], 'Unexpected Mathlib revision')
        roots = [mathlib / '.lake/build/lib/lean']
        roots += sorted((mathlib / '.lake/packages').glob('*/.lake/build/lib/lean'))
        roots += [lean.parent.parent / 'lib/lean']
        external_objects = dict(registry['external_objects'])
        external_objects.update(read(HERE / 'external-objects.json'))
        for name, item in external_objects.items():
            rel = Path(*name.split('.')).with_suffix('.olean')
            p = next((root / rel for root in roots if (root / rel).is_file()), None)
            require(p is not None, 'Missing external module: ' + name)
            authenticate(p, item['sha256'])
        build = out / 'build'
        build.mkdir()
        for name, item in registry['modules'].items():
            for kind in ('source', 'object'):
                authenticate(parent / item[kind], item[kind + '_sha256'])
            dest = build / Path(*name.split('.')).with_suffix('.olean')
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(parent / item['object'], dest)
        shutil.copy2(parent / 'verificacion/ArticleIExceptionalInterface.olean',
                     build / 'ArticleIExceptionalInterface.olean')
        certificate = subprocess.run(
            [sys.executable, '-I', '-S', str(HERE / 'k_direction/verify_p3_table.py'),
             '--owner', str(HERE / 'evidence/variacional.py')],
            cwd=HERE, capture_output=True, text=True, timeout=60)
        (out / 'P3_character_check.log').write_text(certificate.stdout + certificate.stderr)
        require(certificate.returncode == 0, certificate.stdout + certificate.stderr)
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, [build] + roots)))
        modules = {}
        for name, locator in SOURCES:
            source = HERE / locator
            shutil.copy2(source, build / source.name)
            obj = build / (name + '.olean')
            cmd = [str(lean), '-DwarningAsError=true', '--root=' + str(build),
                   '-o', str(obj), str(build / source.name)]
            result = subprocess.run(cmd, cwd=build, env=env,
                                    capture_output=True, text=True, timeout=300)
            log = result.stdout + result.stderr
            logpath = out / (name + '.log')
            logpath.write_text(log)
            require(result.returncode == 0, name + ':\n' + log)
            pattern = r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
            axioms = {m[1]: [x.strip() for x in (m[2] or '').split(',') if x.strip()]
                      for m in re.finditer(pattern, log)}
            require(axioms and all(set(xs) <= ALLOWED for xs in axioms.values()),
                    'Unexpected or missing axiom report: ' + name)
            require('sorryAx' not in log, 'Incomplete proof: ' + name)
            modules[name] = dict(source=locator, source_sha256=sha(source),
                                 object=str(obj), object_sha256=sha(obj),
                                 command=cmd, log_sha256=sha(logpath), axioms=axioms)
            report['modules'] = modules
            save()
        for p, digest in tracked.items():
            require(sha(p) == digest, 'Input changed during reproduction: ' + p)
        report.update(status='PASS_ARTICLE_IV_SELECTED_SCREENS', compiler=compiler,
                      modules=modules, parent_manifest_sha256=sha(parent / 'MANIFIESTO.json'),
                      manifest_sha256=sha(HERE / 'MANIFEST.json'),
                      authenticated_artifacts=len(tracked),
                      external_objects_authenticated=len(external_objects),
                      inherited_modules=478,
                      P3_character_sum_checked_in='Python exact Q(sqrt(5))',
                      P3_matrix_identities_checked_in='Lean kernel',
                      new_axioms=[], inherited_computational_axiom='Lean.ofReduceBool',
                      scope='Selected K direction, orthogonal rank-ten projection, graph quotient, '
                            'selected Lorentz quotient and coordinated elliptic duality; '
                            'classical FLM application inherited, not reproved.')
        save()
        print(report['status'])
    except Exception as exc:
        report.update(status='FAIL_ARTICLE_IV_SELECTED_SCREENS', error=str(exc))
        save()
        raise


if __name__ == '__main__':
    main()
