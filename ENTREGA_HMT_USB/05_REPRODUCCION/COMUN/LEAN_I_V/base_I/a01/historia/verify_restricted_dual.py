#!/usr/bin/env python3
"""Authenticate frozen even-pairing/461 objects and compile only the restricted dual.

No inherited module or Mathlib is rebuilt. Every public declaration is queried.
Use a fresh report directory. --relocate OLD=NEW remaps recorded absolute roots.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
DEFAULT_EVEN = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_ARTICULO_I_20260917/even_pairing')
DEFAULT_TERMINAL = PROJECT/'output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage18_article_I/exceptional/twisted_fields/terminal_contragredient_results_20260922'
EVEN_SHA = 'c34bc4fcbb5638ffda1021702c956d50d156b85696aa60117219d522f454fb0f'
HELPER_SHA = '145accd5aa88f203f648f4e09d3d400122d7e047195cc18b060019c6e9c825a5'
TERMINAL_SHA = 'd1911674fa5a59d25d63246ab73cc1057057c02a91439dda92d785c10d91e51d'
SOURCE_SHA = 'c1256e5a8116ced874cbda0153f963438c0c44c5c4540e5155fbee894841a31b'
NAME = 'LatticeEvenRestrictedDual'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(test, message):
    if not test:
        raise RuntimeError(message)


def axiom_reports(output):
    found = {}
    pattern = r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pattern, output):
        name = match.group(1)
        require(name not in found, 'Repeated axiom report: '+name)
        found[name] = [a.strip() for a in (match.group(2) or '').split(',') if a.strip()]
    return found


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--even-root', type=Path, default=DEFAULT_EVEN)
    p.add_argument('--terminal-report-dir', type=Path, default=DEFAULT_TERMINAL)
    p.add_argument('--helper', type=Path)
    p.add_argument('--source-dir', type=Path, default=HERE)
    p.add_argument('--report-dir', type=Path, default=HERE/'resultados')
    p.add_argument('--lean', type=Path)
    p.add_argument('--relocate', action='append', default=[], metavar='OLD=NEW')
    p.add_argument('--timeout', type=int, default=300)
    p.add_argument('--plan', action='store_true')
    args = p.parse_args()
    for key, value in vars(args).items():
        if isinstance(value, Path):
            setattr(args, key, value.expanduser().resolve())
    args.helper = args.helper or args.even_root/'verify_even_pairing.py'
    require(args.timeout > 0, 'Positive timeout required')
    roots = [(DEFAULT_EVEN, args.even_root), (DEFAULT_TERMINAL, args.terminal_report_dir)]
    for item in args.relocate:
        old, sep, new = item.partition('=')
        require(sep and old and new, 'Use --relocate OLD=NEW')
        roots.append((Path(old).expanduser().resolve(), Path(new).expanduser().resolve()))
    roots.sort(key=lambda pair: len(str(pair[0])), reverse=True)

    def relocate(value):
        path = Path(value)
        for old, new in roots:
            if path == old or path.is_relative_to(old):
                return new/path.relative_to(old)
        return path

    out = args.report_dir
    protected = (args.even_root, args.terminal_report_dir)
    require(not out.exists() and out != args.source_dir and not args.source_dir.is_relative_to(out)
        and not args.helper.is_relative_to(out)
        and all(not out.is_relative_to(x) and not x.is_relative_to(out) for x in protected),
        'Use a fresh report outside protected predecessor roots')
    out.mkdir(parents=True, exist_ok=False)
    started, tracked = time.monotonic(), {}
    report = dict(status='RUNNING_RESTRICTED_DUAL_RECONSTRUCTION', modules=[],
        compiler_invoked=False, inherited_modules_recompiled=False,
        mathlib_rebuilt=False, pdfs_changed=False, sealed_461_modified=False,
        runner_sha256=sha(__file__), source_sha256=SOURCE_SHA,
        even_receipt_sha256=EVEN_SHA, terminal_receipt_sha256=TERMINAL_SHA,
        helper_sha256=HELPER_SHA, scope='Linear equivalence of the actual even '
        'carrier and its dual functionals with bounded weight support. Consumers '
        'must prove that support condition; no TT field or Jacobi claim.')

    def save():
        (out/'VERIFICATION.json').write_text(json.dumps(report, indent=2)+'\n')

    def track(path, expected):
        path = Path(path).resolve()
        require(path not in tracked or tracked[path] == expected, 'Conflicting hashes: '+str(path))
        require(sha(path) == expected, 'Changed authenticated artifact: '+str(path))
        tracked[path] = expected
        return path

    def ordinary_probe(names, output, expected=None):
        found = axiom_reports(output)
        require(len(names) == len(set(names)) and set(found) == set(names), 'Incomplete public axiom probe')
        require(all(set(a) <= ORDINARY for a in found.values()), 'Nonordinary axiom')
        if expected is not None:
            require(set(found) == set(expected) and all(set(found[n]) == set(expected[n])
                for n in found), 'Axiom transcript differs from receipt')
        return found

    def check_probe(root, names, imports, source_hash, log_hash, recorded):
        probe = track(root/'axiom_probe.lean', source_hash)
        log = track(root/'axiom_probe.log', log_hash)
        wanted = ''.join('import '+n+'\n' for n in imports)
        wanted += ''.join('#print axioms '+n+'\n' for n in names)
        require(probe.read_text() == wanted, 'Changed probe inventory')
        return ordinary_probe(names, log.read_text(), recorded)

    save()
    try:
        track(__file__, report['runner_sha256'])
        track(args.helper, HELPER_SHA)
        spec = importlib.util.spec_from_file_location('restricted_dual_even_helper', args.helper)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        er = track(args.even_root/'resultados/VERIFICATION.json', EVEN_SHA)
        tr = track(args.terminal_report_dir/'VERIFICATION.json', TERMINAL_SHA)
        even, terminal = json.loads(er.read_text()), json.loads(tr.read_text())
        require(even['status'] == 'PASS_UNTWISTED_EVEN_WEIGHT_PAIRING'
            and even['runner_sha256'] == HELPER_SHA and not even['inherited_modules_recompiled'],
            'Invalid even-pairing predecessor')
        require(terminal['status'] == 'PASS_TWISTED_TERMINAL_DELTA'
            and terminal['authenticated_inputs_unchanged']
            and not any(terminal[k] for k in ('predecessors_modified','predecessors_recompiled','mathlib_rebuilt')),
            'Invalid terminal predecessor')
        require(even['compiler'] == terminal['compiler'], 'Predecessor compiler mismatch')
        compiler = dict(terminal['compiler'])
        lean = args.lean or relocate(compiler['executable'])
        track(lean, compiler['binary_sha256'])
        compiler['executable'] = str(lean)
        report['compiler'] = compiler
        registry = {}

        def register(name, path, digest):
            track(path, digest)
            require(name not in registry or registry[name]['sha256'] == digest,
                'Inherited module hash collision: '+name)
            registry[name] = dict(path=str(path), sha256=digest)

        for name, item in terminal['inherited_objects'].items():
            register(name, relocate(item['path']), item['sha256'])
        require(len(registry) == terminal['inherited_module_count'], 'Incomplete terminal inherited registry')
        rows = terminal['modules']
        require([r['module'] for r in rows] == terminal['dependency_order']
            and set(terminal['sources']) == set(terminal['dependency_order']), 'Terminal inventory mismatch')
        publics = []
        for row in rows:
            name, build = row['module'], args.terminal_report_dir/'build'
            node = terminal['sources'][name]
            require(row['exit_code'] == 0 and row['source_sha256'] == node['sha256'], 'Terminal compile failed')
            track(build/(name+'.lean'), node['sha256'])
            log = track(build/(name+'.log'), row['log_sha256'])
            require(log.read_text() == row['output'], 'Terminal compile transcript mismatch')
            register(name, build/(name+'.olean'), row['object_sha256'])
            publics.extend(node['public_declarations'])
        tp = terminal['axiom_probe']
        require(tp['exit_code'] == 0 and len(publics) == terminal['public_declaration_count'], 'Terminal probe failed')
        check_probe(args.terminal_report_dir, publics, terminal['dependency_order'],
            tp['source_sha256'], tp['output_sha256'], tp['declarations'])
        require(len(registry) == 461, 'Expected the sealed 461-module cut')
        external = {}
        for name, item in terminal['external_objects'].items():
            obj = track(relocate(item['path']), item['sha256'])
            external[name] = dict(path=str(obj), sha256=item['sha256'])
        for oldpath, digest in even['authenticated_and_unchanged_artifacts'].items():
            track(args.helper if Path(oldpath).name == 'verify_even_pairing.py' else relocate(oldpath), digest)
        names, publics = [], []
        for row in even['modules']:
            name = row['module']
            require(name not in names and row['exit_code'] == 0, 'Even module inventory mismatch')
            names.append(name)
            source = track(args.even_root/(name+'.lean'), row['source_sha256'])
            track(args.even_root/'resultados'/(name+'.log'), row['log_sha256'])
            publics.extend(helper.public_declarations(name, source.read_text()))
            register(name, args.even_root/(name+'.olean'), row['object_sha256'])
            for dep in row['dependencies']:
                obj = track(relocate(dep['object']), dep['object_sha256'])
                old = registry.get(dep['module']) or external.get(dep['module'])
                require(old is None or old['sha256'] == dep['object_sha256'], 'Dependency hash mismatch')
                if dep['module'] not in registry:
                    external[dep['module']] = dict(path=str(obj), sha256=dep['object_sha256'])
        require(names == helper.NAMES and publics == even['public_declarations']
            and len(publics) == even['public_declaration_count'] and even['axiom_probe_exit_code'] == 0,
            'Even public inventory mismatch')
        check_probe(args.even_root/'resultados', publics, names,
            even['axiom_probe_sha256'], even['axiom_log_sha256'], even['axioms'])
        build = out/'build'
        paths = list(dict.fromkeys([build, args.terminal_report_dir/'build', args.even_root,
            *(relocate(p) for p in terminal['lean_path'].split(os.pathsep))]))
        resolved = {}
        for name, item in {**registry, **external}.items():
            obj = helper.resolve_object(name, paths)
            track(obj, item['sha256'])
            resolved[name] = dict(path=str(obj), sha256=item['sha256'])
        source = track(args.source_dir/(NAME+'.lean'), SOURCE_SHA)
        content, clean = source.read_text(), helper.without_comments(source.read_text())
        forbidden = r'\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by|run_elab|run_cmd|elab|macro|syntax|initialize|instance|structure|class|inductive|opaque|mutual|constant)\b'
        require(not re.search(forbidden, clean), 'Unsupported or forbidden source command')
        declarations = helper.public_declarations(NAME, content)
        imports = re.findall(r'^import\s+(\S+)', clean, re.M)
        require(imports and all(n in registry or n in external for n in imports), 'Unregistered new import')
        theorems = re.findall(r'^\s*(?:@\[[^\]\n]*\]\s*)*(?:theorem|lemma)\s+([\w\x27]+)', clean, re.M)
        report.update(public_declarations=declarations, public_declaration_count=len(declarations),
            theorem_names=['HMT.IV.'+NAME+'.'+n for n in theorems], imports=imports,
            inherited_module_count=len(registry), inherited_objects=registry,
            resolved_objects=resolved, lean_path=os.pathsep.join(map(str, paths)))
        env = dict(os.environ, LEAN_PATH=report['lean_path'])
        if not args.plan:
            build.mkdir()
            snapshot = build/(NAME+'.lean')
            snapshot.write_text(content)
            obj = build/(NAME+'.olean')
            command = [str(lean), '-DwarningAsError=true', '--root='+str(build), '-o', str(obj), str(snapshot)]
            report['compiler_invoked'] = True
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=args.timeout)
            log = build/(NAME+'.log')
            log.write_text(result.stdout+result.stderr)
            row = dict(module=NAME, source_sha256=SOURCE_SHA, command=command,
                exit_code=result.returncode, log_sha256=sha(log), output=log.read_text())
            report['modules'].append(row)
            save()
            require(result.returncode == 0, 'Focal compilation failed: '+log.read_text())
            row['object_sha256'] = sha(obj)
            track(snapshot, SOURCE_SHA)
            track(obj, row['object_sha256'])
            probe = out/'axiom_probe.lean'
            probe.write_text('import '+NAME+'\n'+''.join('#print axioms '+d+'\n' for d in declarations))
            command = [str(lean), '-DwarningAsError=true', str(probe)]
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=args.timeout)
            log = out/'axiom_probe.log'
            log.write_text(result.stdout+result.stderr)
            report['axiom_probe'] = dict(command=command, exit_code=result.returncode,
                source_sha256=sha(probe), output_sha256=sha(log), output=log.read_text())
            save()
            require(result.returncode == 0, 'Axiom probe failed')
            report['axioms'] = ordinary_probe(declarations, log.read_text())
            report['axiom_probe']['declarations'] = report['axioms']
        helper.unchanged({str(p): h for p,h in tracked.items()})
        report.update(status=('PASS_RESTRICTED_DUAL_SOURCE_PLAN_NOT_COMPILED' if args.plan else
            'PASS_RESTRICTED_DUAL_RECONSTRUCTION'), authenticated_inputs_unchanged=True,
            authenticated_artifacts={str(p):h for p,h in tracked.items()},
            elapsed_seconds=round(time.monotonic()-started,3))
        save()
        print(report['status'], len(declarations), 'public declarations;',len(theorems),'theorems',flush=True)
    except Exception as error:
        report.update(status='FAIL_RESTRICTED_DUAL_RECONSTRUCTION', error=str(error),
            elapsed_seconds=round(time.monotonic()-started,3))
        save()
        raise


if __name__ == '__main__':
    main()
