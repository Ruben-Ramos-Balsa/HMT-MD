#!/usr/bin/env python3
"""Authenticate the preserved package and replay only its terminal Lean proof."""
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


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def read(p):
    return json.loads(Path(p).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir', required=True, type=Path)
    parser.add_argument('--lean', type=Path)
    parser.add_argument('--mathlib-root', type=Path)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out = args.report_dir.expanduser().resolve()
    require(not out.exists() and not out.is_relative_to(root),
            'Use a fresh report directory outside the delivered package')
    out.mkdir(parents=True)
    report = dict(status='RUNNING', compiler_invoked=False,
                  inherited_modules_recompiled=False, full_FLM_formalization_claimed=False)

    def save():
        (out/'VERIFICATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')

    def local(name):
        p = root/name
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,
                'Unsafe locator')
        require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),
                'Missing or unsafe delivered file: '+name)
        return p

    try:
        manifest = read(root/'MANIFIESTO.json')
        found = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        expected = set(manifest['files']) | {'MANIFIESTO.json'}
        require(found == expected, 'Delivered file inventory differs from manifest')
        for name, digest in manifest['files'].items():
            require(sha(local(name)) == digest, 'Changed file: '+name)
        registry = read(root/'REGISTRO_REPRODUCCION.json')
        report.update(manifest_sha256=sha(root/'MANIFIESTO.json'),
                      authenticated_files=len(expected), inherited_modules=len(registry['modules']),
                      terminal_declarations=registry['declarations'])
        if args.verify_only:
            report['status'] = 'PASS_INTERFACE_PACKAGE_INTEGRITY'
            save()
            print(report['status'])
            return
        require(args.lean and args.mathlib_root, 'Specify --lean and --mathlib-root')
        lean, mathlib = args.lean.resolve(), args.mathlib_root.resolve()
        require(sha(lean) == registry['compiler']['binary_sha256'], 'Unmatched Lean compiler')
        commit = subprocess.check_output(['git','-C',str(mathlib),'rev-parse','HEAD'], text=True).strip()
        require(commit == registry['compiler']['mathlib_commit'], 'Unmatched Mathlib commit')
        roots = [mathlib/'.lake/build/lib/lean']
        roots += sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))
        roots += [lean.parent.parent/'lib/lean']
        for name, item in registry['external_objects'].items():
            rel = Path(*name.split('.')).with_suffix('.olean')
            candidates = [d/rel for d in roots if (d/rel).is_file()]
            require(candidates and sha(candidates[0]) == item['sha256'],
                    'Unmatched external dependency: '+name)
        build = out/'build'
        build.mkdir()
        for name, item in registry['modules'].items():
            for kind in ('source','object'):
                p = local(item[kind])
                require(sha(p) == item[kind+'_sha256'], 'Changed module: '+name)
            dest = build/Path(*name.split('.')).with_suffix('.olean')
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(local(item['object']), dest)
        source = local('lean/ArticleIExceptionalInterface.lean')
        shutil.copy2(source, build/source.name)
        command = [str(lean), '-DwarningAsError=true', '--root='+str(build),
                   '-o', str(build/'ArticleIExceptionalInterface.olean'), str(build/source.name)]
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str,[build]+roots)))
        result = subprocess.run(command, cwd=build, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        (out/'compilation.log').write_text(result.stdout)
        report.update(command=command, exit_code=result.returncode, compiler_invoked=True,
                      source_sha256=sha(source), compiler=registry['compiler'])
        require(result.returncode == 0, 'Terminal Lean compilation failed')
        pattern = r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
        axioms = {m[1]:[a.strip() for a in (m[2] or '').split(',') if a.strip()]
                  for m in re.finditer(pattern,result.stdout)}
        require(set(axioms) == set(registry['declarations']), 'Incomplete public axiom report')
        allowed = {'propext','Classical.choice','Quot.sound','Lean.ofReduceBool'}
        require(all(set(xs) <= allowed for xs in axioms.values()), 'Unexpected axiom')
        require(not re.search(r'\b(?:sorryAx|sorry|admit|unsafe|native_decide)\b', result.stdout),
                'Unexpected proof bypass in compilation output')
        report.update(status='PASS_ARTICLE_I_HMT_EXCEPTIONAL_INTERFACE', axioms=axioms,
                      inherited_computational_dependency='Lean.ofReduceBool',
                      object_sha256=sha(build/'ArticleIExceptionalInterface.olean'),
                      log_sha256=sha(out/'compilation.log'),
                      statement='HMT exceptional interface and classical lattice hypotheses; FLM applied by bibliography, not a Lean axiom')
        save()
        print(report['status'])
    except Exception as exc:
        report.update(status='FAIL_ARTICLE_I_HMT_EXCEPTIONAL_INTERFACE', error=str(exc))
        save()
        raise


if __name__ == '__main__':
    main()
