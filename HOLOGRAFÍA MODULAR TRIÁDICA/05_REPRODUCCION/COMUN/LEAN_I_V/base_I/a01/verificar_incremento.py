#!/usr/bin/env python3
"""Portable, explicit replay of fifteen ordinary modules or one selected module.

--plan authenticates all preserved sources, objects, logs and public probes;
it never invokes Lean. Execution compiles only the requested cut, never the
461-module predecessor, Mathlib, or another inherited dependency.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
BASE_SHA = '822524de5672f5453dc4a63cd33d6172ed98527d576f9185647206207a01acad'
TERMINAL_SHA = 'd1911674fa5a59d25d63246ab73cc1057057c02a91439dda92d785c10d91e51d'
HELPER_SHA = '145accd5aa88f203f648f4e09d3d400122d7e047195cc18b060019c6e9c825a5'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}
SELECTED = 'SelectedOrbifoldStateFields'
SELECTED_IMPORTS = ['SelectedConformalVertex', 'LatticeOrbifoldFullStateFields', 'LatticeOrbifoldGrading']
SELECTED_SOURCE = '41eb713c7e41ecca3e0c1331bc66aa4233d3b4be3d8616494118dad331f7b146'
SELECTED_OWNER_SOURCE = '3e81a26a9fbd77540b43be1353456c836b5bb6b09a43b3fdd8799d132202e720'
SELECTED_OWNER_OBJECT = '537134f0a7b33632e87e6858e8a362e135027d25bc682eb294cc42c49b9bef7e'
ROLES = {
    'par': ('c34bc4fcbb5638ffda1021702c956d50d156b85696aa60117219d522f454fb0f',
        'PASS_UNTWISTED_EVEN_WEIGHT_PAIRING', ['GradedPairingRepresentability', 'LatticeChargePairing',
        'LatticeIntegerPairingWeights', 'LatticeUntwistedPairing', 'LatticeEvenPairingRepresentability']),
    'reconstruccion': ('9a4bf6186475376a3f6330e5fa673c3c9780abf80b027f2116852a82ec2a13f3',
        'PASS_RESTRICTED_DUAL_RECONSTRUCTION', ['LatticeEvenRestrictedDual']),
    'soporte': ('cf6aba0dff4a8e524a18abd629e7804e10efd505a6d5746efaf30e67b9b72e73',
        'PASS_CONTRAGREDIENT_HOMOGENEOUS_WEIGHT_SUPPORT', ['LatticeTwistedNormalEnergy',
        'LatticeTwistedRawEnergy', 'LatticeTwistedCorrectedEnergy', 'SkewFieldEnergy',
        'LatticeTwistedPairingEnergy', 'LatticeTwistedFullEnergy', 'LatticeContragredientWeightSupport']),
    'consumidores': ('59491b582d884ba3ba2cc2a2e240a2f61f4e97918b5cb572e79d209b6a29eb6a',
        'PASS_TWISTED_PAIR_PRODUCT', ['LatticeTwistedPairProduct', 'LatticeOrbifoldFullStateFields']),
    'selected': ('4ebc602709024225211ad2f92a5fc85f4cc8b7de665fb3e4894f51ce48d5ae88',
        'PASS_SELECTED_ORBIFOLD_SPECIALIZATION', [SELECTED]),
}


def require(test, message):
    if not test:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def axiom_reports(output):
    result = {}
    pattern = r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pattern, output):
        require(match[1] not in result, 'Repeated axiom declaration: '+match[1])
        result[match[1]] = [a.strip() for a in (match[2] or '').split(',') if a.strip()]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package-root', type=Path, required=True)
    parser.add_argument('--bundle-sha256', required=True)
    parser.add_argument('--report-dir', type=Path, required=True)
    parser.add_argument('--lean', type=Path)
    parser.add_argument('--mathlib-root', type=Path)
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('--selected', action='store_true', help='Compile only the separate inherited-axiom specialization')
    parser.add_argument('--plan', action='store_true', help='Authenticate only; do not invoke Lean')
    args = parser.parse_args()
    root, out = args.package_root.expanduser().resolve(), args.report_dir.expanduser().resolve()
    require(re.fullmatch('[0-9a-f]{64}', args.bundle_sha256), 'Explicit lowercase bundle SHA256 required')
    require(args.timeout > 0 and root.is_dir(), 'Existing package and positive timeout required')
    require(not out.exists() and not out.is_relative_to(root) and not root.is_relative_to(out),
        'Use a fresh report outside the immutable package')
    out.mkdir(parents=True, exist_ok=False)
    started, tracked = time.monotonic(), {}
    report = dict(status='RUNNING_PAIR_BUNDLE', modules=[], compiler_invoked=False,
        bundle_sha256=args.bundle_sha256, runner_sha256=sha(__file__), selected_specialization=args.selected,
        inherited_modules_recompiled=False, mathlib_rebuilt=False,
        scope='Concrete four-block state fields; no global mixed locality/Jacobi, full FLM or Monster claim.')

    def save():
        (out/'VERIFICATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')

    def local(value):
        relative = Path(value)
        require(not relative.is_absolute() and '..' not in relative.parts and str(relative) != '.',
            'Unsafe package-relative locator: '+str(value))
        path = root/relative
        require(path.resolve().is_relative_to(root), 'Locator escapes the delivered package')
        require(not any((root/Path(*relative.parts[:i])).is_symlink() for i in range(1, len(relative.parts)+1)),
            'Symlink is not a preserved package file')
        require(path.is_file(), 'Missing preserved artifact: '+str(relative))
        return path

    def track(path, digest):
        path = Path(path).resolve()
        require(re.fullmatch('[0-9a-f]{64}', digest), 'Malformed artifact SHA256')
        require(path not in tracked or tracked[path] == digest, 'Conflicting artifact digests')
        require(sha(path) == digest, 'Changed authenticated artifact: '+str(path))
        tracked[path] = digest
        return path

    def preserved(node):
        return track(local(node['path']), node['sha256'])

    def unchanged():
        require(all(sha(p) == digest for p, digest in tracked.items()), 'Authenticated input changed during replay')
        report['authenticated_inputs_unchanged'] = True

    save()
    try:
        track(__file__, report['runner_sha256'])
        bundle = read(track(local('BUNDLE_INPUTS.json'), args.bundle_sha256))
        require(bundle['schema'] == 'hmt.pair_product.bundle.v1', 'Unsupported bundle schema')
        require(preserved(bundle['replayer']) == Path(__file__).resolve(), 'Run the bound delivered replayer')
        require(bundle['old_manifest']['sha256'] == BASE_SHA
            and bundle['old_manifest']['path'] == 'antecedente/MANIFIESTO.json', 'Wrong immutable predecessor')
        manifest = read(preserved(bundle['old_manifest']))
        require(manifest['total_authenticated_modules'] == 461, 'Wrong inherited module cut')
        rows = {row['path']: row for row in manifest['files']}
        require(len(rows) == len(manifest['files']), 'Duplicate predecessor inventory')
        found = set()
        for path in (root/'antecedente').rglob('*'):
            require(not path.is_symlink(), 'Predecessor contains a symlink')
            if path.is_file():
                found.add(path.relative_to(root/'antecedente').as_posix())
        require(found == set(rows)|{'MANIFIESTO.json'}, 'Changed predecessor file inventory')
        for name, row in rows.items():
            path = track(local('antecedente/'+name), row['sha256'])
            require(path.stat().st_size == row['bytes'], 'Changed predecessor file length')
        for name, digest in bundle['artifact_files'].items():
            track(local(name), digest)
        for name, digest in bundle['copied_artifacts'].items():
            track(local(name), digest)
        require(bundle['inspector']['sha256'] == HELPER_SHA, 'Wrong pinned source inspector')
        spec = importlib.util.spec_from_file_location('delivered_public_inspector', preserved(bundle['inspector']))
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        registry, delta, selected = bundle['registry461'], bundle['delta15'], bundle['selected']
        order = [name for role, (_, _, names) in ROLES.items() if role != 'selected' for name in names]
        require(len(registry) == 461 and set(delta) == set(order) and list(selected) == [SELECTED],
            'Wrong inherited, ordinary or separate selected inventory')
        require(bundle['dependency_order15'] == order and set(bundle['ordinary_allowed_axioms']) == ORDINARY,
            'Changed dependency order or ordinary axiom policy')
        require(not (set(registry)&set(delta) or set(registry)&set(selected) or set(delta)&set(selected)),
            'Module collision between cuts')
        nodes = {**registry, **delta, **selected}
        objects = {}
        for name, node in nodes.items():
            source = track(local(node['source']), node['source_sha256'])
            objects[name] = track(local(node['object']), node['object_sha256'])
            if name in registry:
                require(node['source'].startswith('antecedente/') and node['object'].startswith('antecedente/'),
                    'Inherited artifact is not in the single predecessor copy')
                for field in ('source', 'object'):
                    require(rows[node[field].removeprefix('antecedente/')]['sha256'] == node[field+'_sha256'],
                        'Inherited module is not bound to the old manifest')
                continue
            clean = helper.without_comments(source.read_text())
            require(not re.search(r'\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by|run_elab|run_cmd)\b', clean),
                'Forbidden proof or executable escape: '+name)
            require(not re.search(r'^\s*(?:@\[[^\]\n]*\]\s*)*(?:(?:noncomputable|private|protected)\s+)*'
                r'(?:instance|structure|class|inductive|opaque|constant|mutual|elab|macro|syntax|initialize)\b', clean, re.M),
                'Unsupported declaration layout: '+name)
            namespace = ('HMT.I.' if name == SELECTED else 'HMT.IV.')+name
            if name == SELECTED:
                require(re.findall(r'^\s*namespace\s+(\S+)', clean, re.M) == [namespace], 'Changed selected namespace')
                declarations = [namespace+'.'+n for n in helper.DECL.findall(clean)]
            else:
                declarations = helper.public_declarations(name, source.read_text())
            imports = re.findall(r'^import\s+(\S+)', clean, re.M)
            theorems = [namespace+'.'+n for n in re.findall(
                r'^\s*(?:@\[[^\]\n]*\]\s*)*(?:theorem|lemma)\s+([\w\x27]+)', clean, re.M)]
            require(declarations == node['public_declarations'] and imports == node['imports']
                and theorems == node['theorem_names'], 'Source declaration inventory changed: '+name)
            require(len(declarations) == len(set(declarations)), 'Repeated public declaration')
        terminal_locator = bundle['inherited_terminal_receipt']
        require(terminal_locator['sha256'] == TERMINAL_SHA, 'Wrong inherited terminal receipt')
        terminal = read(preserved(terminal_locator))
        prior = {n: v['sha256'] for n, v in terminal['inherited_objects'].items()}
        require(terminal['status'] == 'PASS_TWISTED_TERMINAL_DELTA'
            and terminal['authenticated_inputs_unchanged'], 'Unsuccessful predecessor receipt')
        for row in terminal['modules']:
            require(row['exit_code'] == 0 and row['module'] not in prior, 'Failed/duplicate inherited module')
            prior[row['module']] = row['object_sha256']
        require(prior == {n: v['object_sha256'] for n, v in registry.items()}, 'Inherited object registry mismatch')
        policy = selected[SELECTED]['axiom_policy']
        require(selected[SELECTED]['source_sha256'] == SELECTED_SOURCE
            and selected[SELECTED]['imports'] == SELECTED_IMPORTS
            and policy['module'] == SELECTED and policy['namespace'] == 'HMT.I.'+SELECTED
            and policy['imports'] == SELECTED_IMPORTS
            and set(policy['allowed_axioms']) == ORDINARY|{'Lean.ofReduceBool'}
            and set(selected[SELECTED]['allowed_axioms']) == ORDINARY|{'Lean.ofReduceBool'}
            and policy['native_decide_in_new_source_allowed'] is False
            and policy['inherited_native_exception'] == 'Lean.ofReduceBool'
            and policy['inherited_owner'] == 'SelectedConformalVertex'
            and policy['inherited_source_sha256'] == SELECTED_OWNER_SOURCE
            and policy['inherited_object_sha256'] == SELECTED_OWNER_OBJECT,
            'Changed separate selected exception policy')
        owner = registry['SelectedConformalVertex']
        require(owner['source_sha256'] == SELECTED_OWNER_SOURCE and owner['object_sha256'] == SELECTED_OWNER_OBJECT,
            'Inherited selected owner mismatch')
        receipts = {}
        for role, (digest, status, names) in ROLES.items():
            locator = bundle['receipts'][role]
            require(locator['sha256'] == digest, 'Wrong focal receipt: '+role)
            rp = preserved(locator)
            receipt = read(rp)
            receipts[role] = receipt
            require(receipt['status'] == status and [r['module'] for r in receipt['modules']] == names,
                'Focal receipt status/inventory mismatch: '+role)
            publics = [d for name in names for d in nodes[name]['public_declarations']]
            allowed = ORDINARY|{'Lean.ofReduceBool'} if role == 'selected' else ORDINARY
            for row in receipt['modules']:
                name, node = row['module'], nodes[row['module']]
                require(node['receipt_role'] == role and row['source_sha256'] == node['source_sha256']
                    and row['olean_sha256' if role == 'soporte' else 'object_sha256'] == node['object_sha256'],
                    'Focal source/object mismatch: '+name)
                if role != 'soporte':
                    require(row['exit_code'] == 0, 'Failed focal compilation')
                    log = track(rp.parent/'build'/(name+'.log'), row['log_sha256'])
                    if 'output' in row:
                        require(log.read_text() == row['output'], 'Changed compilation transcript')
            if role == 'par':
                probe_hash, log_hash, recorded = receipt['axiom_probe_sha256'], receipt['axiom_log_sha256'], receipt['axioms']
                require(receipt['axiom_probe_exit_code'] == 0, 'Failed even-pairing probe')
            elif role == 'soporte':
                probe_hash, log_hash, recorded = None, receipt['axioms_log_sha256'], receipt['declarations']
                track(rp.parent/'compile.log', receipt['compile_log_sha256'])
            else:
                ap = receipt['axiom_probe']
                require(ap['exit_code'] == 0 and receipt['authenticated_inputs_unchanged']
                    and not receipt['inherited_modules_recompiled'], 'Failed inherited focal authentication')
                probe_hash, log_hash, recorded = ap['source_sha256'], ap['output_sha256'], ap['declarations']
            probe_path, log_path = rp.parent/'axiom_probe.lean', rp.parent/'axiom_probe.log'
            track(probe_path, probe_hash or bundle['artifact_files'][probe_path.relative_to(root).as_posix()])
            track(log_path, log_hash)
            wanted = ''.join('import '+n+'\n' for n in names)+''.join('#print axioms '+n+'\n' for n in publics)
            require(probe_path.read_text() == wanted, 'Incomplete preserved public probe: '+role)
            found_axioms = axiom_reports(log_path.read_text())
            require(set(found_axioms) == set(publics) == set(recorded), 'Incomplete public query results: '+role)
            require(all(set(found_axioms[n]) == set(recorded[n]) and set(found_axioms[n]) <= allowed for n in publics),
                'Disallowed or changed inherited axiom report: '+role)
        require(receipts['reconstruccion']['even_receipt_sha256'] == ROLES['par'][0]
            and receipts['reconstruccion']['terminal_receipt_sha256'] == TERMINAL_SHA
            and receipts['soporte']['parent_receipt_sha256'] == TERMINAL_SHA
            and receipts['consumidores']['restricted_receipt_sha256'] == ROLES['reconstruccion'][0]
            and receipts['consumidores']['support_receipt_sha256'] == ROLES['soporte'][0]
            and receipts['selected']['ordinary_receipt_sha256'] == ROLES['consumidores'][0], 'Broken focal dependency chain')
        for role, prior_roles in [('reconstruccion', ['par']),
                ('consumidores', ['par', 'reconstruccion', 'soporte']),
                ('selected', ['par', 'reconstruccion', 'soporte', 'consumidores'])]:
            expected = {**prior, **{n: v['object_sha256'] for n, v in delta.items() if v['receipt_role'] in prior_roles}}
            require(expected == {n: v['sha256'] for n, v in receipts[role]['inherited_objects'].items()},
                'Changed inherited object closure: '+role)
        external = bundle['external_objects']
        require(not set(external)&set(nodes), 'External objects must not replace project modules')
        for index, name in enumerate(order):
            imports = set(delta[name]['imports'])
            require(imports <= set(registry)|set(order[:index])|set(external), 'Unordered or unresolved import: '+name)
        require(set(SELECTED_IMPORTS) <= set(registry)|set(delta), 'Selected dependency outside authenticated cut')
        compiler = bundle['compiler']
        require(compiler == receipts['consumidores']['compiler'] == terminal['compiler'], 'Compiler identity mismatch')
        lean = track((args.lean or Path(compiler['executable'])).expanduser().resolve(), compiler['binary_sha256'])
        mathlib = args.mathlib_root
        if mathlib is None:
            candidates = {str(v['path']).split('/.lake/')[0] for v in external.values() if '/.lake/' in str(v['path'])}
            require(len(candidates) == 1, 'Specify --mathlib-root for the authenticated external runtime')
            mathlib = Path(candidates.pop())
        mathlib = mathlib.expanduser().resolve()
        require(not out.is_relative_to(mathlib) and not mathlib.is_relative_to(out)
            and not out.is_relative_to(lean.parent.parent), 'Report overlaps external runtime')
        runtime = [mathlib/'.lake/build/lib/lean', *sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean')),
            lean.parent.parent/'lib/lean']
        runtime = [p.resolve() for p in runtime if p.is_dir()]
        require(runtime, 'External runtime object roots are missing')
        for name, node in external.items():
            track(helper.resolve_object(name, runtime), node['sha256'])
        active = [SELECTED] if args.selected else order
        inherited = {**registry, **delta} if args.selected else registry
        inherited_paths = list(dict.fromkeys(objects[n].parent for n in inherited))
        paths = [*inherited_paths, *runtime]
        resolved_inherited = {}
        for name, node in inherited.items():
            actual = helper.resolve_object(name, paths)
            require(actual.is_relative_to(root), 'Inherited object escaped the relocated package: '+name)
            track(actual, node['object_sha256'])
            resolved_inherited[name] = dict(path=str(actual), sha256=node['object_sha256'])
        for name, node in external.items():
            require(sha(helper.resolve_object(name, paths)) == node['sha256'], 'External object shadowing: '+name)
        report.update(inherited_module_count=len(inherited), requested_modules=active,
            dependency_order=active, public_declarations=[d for n in active for d in nodes[n]['public_declarations']],
            theorem_names=[d for n in active for d in nodes[n]['theorem_names']],
            compiler=compiler, external_runtime_roots=[str(p) for p in runtime],
            inherited_objects={n: dict(path=str(objects[n]), sha256=v['object_sha256']) for n, v in inherited.items()},
            resolved_inherited_objects=resolved_inherited,
            internal_paths_relocated=True, axiom_policy=policy if args.selected else sorted(ORDINARY))
        report['public_declaration_count'] = len(report['public_declarations'])
        unchanged()
        if args.plan:
            report['status'] = 'PASS_PAIR_BUNDLE_SELECTED_SOURCE_PLAN_NOT_COMPILED' if args.selected else 'PASS_PAIR_BUNDLE_SOURCE_PLAN_NOT_COMPILED'
        else:
            build = out/'build'
            build.mkdir()
            env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, [build, *paths])))
            report['lean_path'] = env['LEAN_PATH']
            allowed = ORDINARY|{'Lean.ofReduceBool'} if args.selected else ORDINARY

            def run(command, log):
                report['compiler_invoked'] = True
                proc = subprocess.run(command, cwd=build, env=env, text=True, capture_output=True, timeout=args.timeout)
                log.write_text(proc.stdout+proc.stderr)
                return dict(command=command, exit_code=proc.returncode, output=log.read_text(), log_sha256=sha(log))

            for name in active:
                node = nodes[name]
                source = build/(name+'.lean')
                shutil.copy2(local(node['source']), source)
                require(sha(source) == node['source_sha256'], 'Changed source snapshot')
                obj = build/(name+'.olean')
                result = run([str(lean), '-DwarningAsError=true', '-o', str(obj), str(source)], build/(name+'.log'))
                result.update(module=name, source_sha256=sha(source))
                report['modules'].append(result)
                save()
                require(result['exit_code'] == 0 and obj.is_file(), 'Compilation failed: '+name)
                result['object_sha256'] = sha(obj)
            probe_path, probe_log = out/'axiom_probe.lean', out/'axiom_probe.log'
            probe_path.write_text(''.join('import '+n+'\n' for n in active)
                +''.join('#print axioms '+d+'\n' for d in report['public_declarations']))
            result = run([str(lean), '-DwarningAsError=true', str(probe_path)], probe_log)
            result['source_sha256'] = sha(probe_path)
            report['axiom_probe'] = result
            save()
            require(result['exit_code'] == 0, 'Public axiom probe failed')
            axioms = axiom_reports(result['output'])
            require(set(axioms) == set(report['public_declarations']) and all(set(a) <= allowed for a in axioms.values()),
                'Incomplete public query or unauthorized axiom')
            report['axioms'] = axioms
            unchanged()
            report['status'] = 'PASS_PAIR_BUNDLE_SELECTED_REPRODUCTION' if args.selected else 'PASS_PAIR_BUNDLE_ORDINARY_REPRODUCTION'
        report['authenticated_artifacts'] = {str(p): h for p, h in tracked.items()}
        report['elapsed_seconds'] = round(time.monotonic()-started, 3)
        save()
        print(json.dumps({k: report[k] for k in ('status', 'inherited_module_count', 'requested_modules',
            'public_declaration_count', 'compiler_invoked', 'authenticated_inputs_unchanged')}, indent=2))
        return 0
    except Exception as error:
        report.update(status='FAIL_PAIR_BUNDLE', error=type(error).__name__+': '+str(error),
            elapsed_seconds=round(time.monotonic()-started, 3))
        save()
        print(report['error'], file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
