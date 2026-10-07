#!/usr/bin/env python3
"""Verify an explicit descendant-locality delta without rebuilding its ancestors.

The authenticated cut is the frozen 279-module base, 17 state-field coherence
modules and two coefficient-locality modules. Only the requested local modules
and their unsatisfied local imports are compiled, in dependency order. The
three historical Dong objects may be reused only against pinned receipts and
unchanged sources; all public declarations of the selected delta are queried,
including declarations not listed in those historical focal receipts.

No Lean source, prior receipt, prior object or Mathlib file is written. Results
go to a fresh --report-dir. --plan authenticates sources without invoking Lean.
This receipt describes exact declarations; it does not promote them to an
unlisted locality, VOA, FLM or Moonshine theorem.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True

HELPER_SHA = 'f022db4decca339ed0873c08508b9a9a93b66a9ce711a3785526896870219939'
COHERENCE_SHA = '620583b804d93d031a8abcdf94606ab20c3d7bf1c213cac5c3e7890c571098b8'
LOCALITY_SHA = '48865bb1efd903a9c4ba6f3105f441953fe69dcbf2a7d84799b0d1fb66f083bd'
ORDINARY_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
SELECTED_NAMESPACE = 'HMT.I.SelectedDescendantLocality'
SELECTED_MODULE = 'SelectedDescendantLocality'
SELECTED_IMPORTS = {'SelectedStateField', 'LatticeDescendantLocality'}
DONG_CACHES = {
    'LatticeDongKernel': ('kernel_build', 'PASS_DONG_RESIDUE_KERNEL',
        '6aefa5af0e3790a27f6f0368ffff6a9b96a87151dda73471eb523384fdea6d21'),
    'LatticeDongBinomial': ('binomial_build', 'PASS_DONG_BINOMIAL_RESIDUE',
        'bb8868b02e2f69e79565af53f700234d5016ebba05616ba23d9251d3e00460e1'),
    'LatticeTripleLocality': ('triple_build', 'PASS_RAW_TRIPLE_LOCALITY',
        '99d9e2d1f7dc130067eafc0363fe4a30f68fe6f0d1b1cece490f1004870d3967'),
}


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def load_helper(path):
    if sha(path) != HELPER_SHA:
        raise RuntimeError('The inherited verifier changed; use its sealed copy')
    spec = importlib.util.spec_from_file_location('authenticated_state_field_delta', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inspect(verifier, path):
    raw = path.read_bytes()
    imports, _ = verifier.inspect_source(raw, str(path))
    code = verifier.mask_comments_strings(raw.decode('utf-8'))
    if re.search(r'\b(?:native_decide|ofReduceBool|ofReduceNat|unsafe)\b', code):
        raise RuntimeError('Unsafe or new native proof in delta: ' + str(path))
    namespaces = re.findall(r'^\s*namespace\s+([\w.]+)', code, re.M)
    if len(namespaces) != 1:
        raise RuntimeError('Expected one explicit namespace: ' + str(path))
    if path.stem == SELECTED_MODULE or namespaces[0] == SELECTED_NAMESPACE:
        if (path.stem != SELECTED_MODULE or namespaces[0] != SELECTED_NAMESPACE
                or set(imports) != SELECTED_IMPORTS):
            raise RuntimeError('Selected-origin exception requires its exact module, namespace and imports')
    # Anchor at command indentation. Private helpers are deliberately omitted;
    # anonymous instances are rejected rather than silently missed.
    pattern = re.compile(
        r'^\s*(?:@\[[^\]]*\]\s*)*'
        r'(?P<mods>(?:(?:private|protected|noncomputable|scoped)\s+)*)'
        r'(?P<kind>theorem|lemma|def|abbrev|structure|inductive|instance|opaque)\s+'
        r'(?P<name>[A-Za-z_][\w\']*)', re.M)
    public, theorems, private = [], [], []
    for match in pattern.finditer(code):
        name = namespaces[0] + '.' + match['name']
        if 'private' in match['mods'].split():
            private.append(name)
            continue
        public.append(name)
        if match['kind'] in ('theorem', 'lemma'):
            theorems.append(name)
    if re.search(r'^\s*(?:@\[[^\]]*\]\s*)*(?:noncomputable\s+)?instance\s*[:(\[{]',
                 code, re.M):
        raise RuntimeError('Name public instances explicitly for inventory: ' + str(path))
    if not public or len(public) != len(set(public)):
        raise RuntimeError('Empty or conflicting public declarations: ' + str(path))
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(),
                bytes=len(raw), imports=imports, namespace=namespaces[0],
                public_declarations=public, theorem_names=theorems,
                private_helpers_omitted=private)


def authenticate_delta(helper, verifier, receipt_path, expected, source_root,
                       count, inherited, tracked):
    if sha(receipt_path) != expected:
        raise RuntimeError('The sealed predecessor receipt changed: ' + str(receipt_path))
    tracked[receipt_path] = expected
    receipt = json.loads(receipt_path.read_text())
    if (receipt['status'] != 'PASS_STATE_FIELD_DELTA'
            or receipt['runner_sha256'] != HELPER_SHA
            or receipt['base_manifest_sha256'] != helper.BASE_MANIFEST_SHA
            or receipt['base_receipt_sha256'] != helper.BASE_RECEIPT_SHA
            or receipt['compiler']['binary_sha256'] != helper.LEAN_SHA
            or receipt['compiler']['mathlib_commit'] != helper.MATHLIB_COMMIT):
        raise RuntimeError('Unsuccessful or incompatible predecessor: ' + str(receipt_path))
    records = {r['module']: r for r in receipt['modules']}
    sources = receipt['sources']
    if len(records) != count or records.keys() != sources.keys():
        raise RuntimeError('Wrong predecessor module set: ' + str(receipt_path))
    probe = receipt['axiom_probe']
    queries = {q for node in sources.values() for q in node['public_declarations']}
    if probe['exit_code'] or set(probe['declarations']) != queries:
        raise RuntimeError('Incomplete predecessor public axiom probe')
    for q, axioms in probe['declarations'].items():
        allowed = ORDINARY_AXIOMS | ({'Lean.ofReduceBool'}
                    if q.startswith('HMT.I.SelectedStateField.') else set())
        if not set(axioms) <= allowed:
            raise RuntimeError('Unexpected predecessor axiom: ' + q)
    build = receipt_path.parent / 'build'
    for name, node in sources.items():
        source = helper.relative_file(source_root, node['path'])
        snapshot = build / (name + '.lean')
        obj = build / (name + '.olean')
        row = records[name]
        imports, _ = verifier.inspect_source(source.read_bytes(), str(source))
        if (sha(source) != node['sha256'] or sha(snapshot) != node['sha256']
                or row['source_sha256'] != node['sha256'] or row['exit_code']
                or sha(obj) != row['object_sha256'] or imports != node['imports']):
            raise RuntimeError('Predecessor source/object graph mismatch: ' + name)
        if name in inherited:
            raise RuntimeError('Predecessor shadows a module: ' + name)
        for dep in imports:
            if (dep not in sources and dep not in inherited
                    and dep.split('.')[0] not in verifier.EXTERNAL_PREFIXES):
                raise RuntimeError('Unresolved predecessor dependency: ' + dep)
        tracked.update({source: node['sha256'], snapshot: node['sha256'],
                        obj: row['object_sha256']})
    return receipt, sources, records, build


def source_plan(verifier, roots, requested, inherited):
    paths = {}
    for root in roots:
        for path in sorted(root.glob('*.lean')):
            name = path.stem
            if name in paths:
                raise RuntimeError('Duplicate local module name: ' + name)
            paths[name] = path
    nodes, order, visiting, visited, external, old_imports = {}, [], set(), set(), set(), set()

    def visit(name):
        if name in inherited:
            old_imports.add(name)
            return
        if name in visited:
            return
        if name in visiting:
            raise RuntimeError('Cyclic local import: ' + name)
        if name not in paths:
            raise RuntimeError('Unresolved requested/imported module: ' + name)
        visiting.add(name)
        node = inspect(verifier, paths[name])
        nodes[name] = node
        for dep in node['imports']:
            if dep in inherited or dep in paths:
                visit(dep)
            elif dep.split('.')[0] in verifier.EXTERNAL_PREFIXES:
                external.add(dep)
            else:
                raise RuntimeError(f'Unresolved import {dep} in {name}')
        visiting.remove(name)
        visited.add(name)
        order.append(name)

    for name in requested:
        if name in inherited:
            raise RuntimeError('Requested module is already sealed; do not rebuild: ' + name)
        visit(name)
    return nodes, order, sorted(external), sorted(old_imports)


def dong_cache(name, node, dong_root, tracked):
    """Return only a byte-authenticated historical object, never a loose .olean."""
    if name not in DONG_CACHES:
        return None
    folder, status, expected = DONG_CACHES[name]
    receipt_path = dong_root / folder / 'VERIFICATION.json'
    obj = dong_root / folder / (name + '.olean')
    if not receipt_path.is_file() or sha(receipt_path) != expected:
        return None
    receipt = json.loads(receipt_path.read_text())
    if (receipt['status'] != status or receipt['exit_code'] != 0
            or not receipt['sources_and_objects_unchanged']
            or receipt['source_sha256'] != node['sha256'] or not obj.is_file()
            or sha(obj) != receipt['object_sha256']):
        return None
    if any(not set(ax) <= ORDINARY_AXIOMS for ax in receipt['declarations'].values()):
        raise RuntimeError('Unexpected axiom in historical Dong receipt')
    tracked.update({receipt_path: expected, obj: receipt['object_sha256']})
    return dict(receipt=str(receipt_path), receipt_sha256=expected,
                object_path=str(obj), object_sha256=receipt['object_sha256'],
                compiler=receipt['compiler'])


def main():
    here = Path(__file__).resolve().parent
    previous = here.parent / 'state_field'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--modules', nargs='+', required=True,
                        help='Explicit module names; new local dependencies are included automatically')
    parser.add_argument('--source-root', type=Path, default=here)
    parser.add_argument('--dong-root', type=Path, default=here / 'dong')
    parser.add_argument('--coherence-root', type=Path, default=previous)
    parser.add_argument('--coherence-report-dir', type=Path,
                        default=previous / 'normal_coherence_results')
    parser.add_argument('--locality-report-dir', type=Path, default=here / 'resultados')
    parser.add_argument('--helper', type=Path, default=previous / 'verify_state_field.py')
    parser.add_argument('--base', type=Path)
    parser.add_argument('--report-dir', type=Path, default=here / 'incremental_results')
    parser.add_argument('--lean', type=Path, default=Path.home() /
                        '.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')
    parser.add_argument('--mathlib', type=Path, default=Path('/Users/ruben/Documents/'
                        'ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4'))
    parser.add_argument('--timeout', type=int, default=900)
    parser.add_argument('--no-dong-cache', action='store_true',
                        help='Recompile selected Dong modules in the new results only')
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    for key in ('source_root', 'dong_root', 'coherence_root', 'coherence_report_dir',
                'locality_report_dir', 'helper', 'report_dir'):
        setattr(args, key, getattr(args, key).expanduser().resolve())
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    requested = list(dict.fromkeys(name.removesuffix('.lean') for name in args.modules))
    report_dir = args.report_dir
    report = dict(schema='hmt.lean.descendant.locality.incremental.v1', status='RUNNING',
                  started_at_utc=datetime.now(timezone.utc).isoformat(), invocation=sys.argv,
                  runner_sha256=sha(Path(__file__)), requested_modules=requested, modules=[],
                  predecessors_modified=False, predecessors_recompiled=False,
                  mathlib_rebuilt=False, compiler_invoked=False,
                  scope='Exact public source declarations recorded below; no implicit promotion.',
                  allowed_delta_axioms=sorted(ORDINARY_AXIOMS),
                  inherited_axiom_exception=dict(module=SELECTED_MODULE,
                      namespace=SELECTED_NAMESPACE, imports=sorted(SELECTED_IMPORTS),
                      extra_axioms=['Lean.ofReduceBool'],
                      reason='Inherited selectedOrigin only; no new native proof in any source.'))
    writable = False
    try:
        helper = load_helper(args.helper)
        coherence_path = args.coherence_report_dir / 'VERIFICATION.json'
        if sha(coherence_path) != COHERENCE_SHA:
            raise RuntimeError('Coherence receipt is not the frozen successful cut')
        coherence_hint = json.loads(coherence_path.read_text())
        base = (args.base or Path(coherence_hint['base'])).expanduser().resolve()
        protected = [base, args.coherence_report_dir, args.locality_report_dir,
                     *(args.dong_root / row[0] for row in DONG_CACHES.values())]
        if any(report_dir.is_relative_to(p) or p.is_relative_to(report_dir) for p in protected):
            raise RuntimeError('Report directory overlaps a protected predecessor')
        if report_dir.exists() and any(report_dir.iterdir()):
            raise RuntimeError('Use a fresh report directory; existing results are preserved')
        report_dir.mkdir(parents=True, exist_ok=True)
        writable = True
        verifier, old, base_sources, base_records, base_build = helper.authenticate_base(base)
        tracked = {args.helper: HELPER_SHA, Path(__file__).resolve(): report['runner_sha256']}
        coherence, c_sources, c_records, c_build = authenticate_delta(
            helper, verifier, coherence_path, COHERENCE_SHA, args.coherence_root,
            17, base_sources, tracked)
        inherited = {**base_sources, **c_sources}
        locality_path = args.locality_report_dir / 'VERIFICATION.json'
        locality, l_sources, l_records, l_build = authenticate_delta(
            helper, verifier, locality_path, LOCALITY_SHA, args.source_root,
            2, inherited, tracked)
        inherited.update(l_sources)
        roots = list(dict.fromkeys([args.source_root, args.dong_root]))
        nodes, order, external, old_imports = source_plan(verifier, roots, requested, inherited)
        caches = {}
        for name in order:
            if not args.no_dong_cache:
                cache = dong_cache(name, nodes[name], args.dong_root, tracked)
                if cache:
                    if (cache['compiler']['binary_sha256'] != helper.LEAN_SHA
                            or cache['compiler']['mathlib_commit'] != helper.MATHLIB_COMMIT):
                        raise RuntimeError('Incompatible historical Dong compiler')
                    caches[name] = cache
        report.update(base=str(base), base_receipt_sha256=helper.BASE_RECEIPT_SHA,
                      coherence_receipt_sha256=COHERENCE_SHA, locality_receipt_sha256=LOCALITY_SHA,
                      inherited_module_count=len(inherited), sources=nodes,
                      dependency_order=order, compile_order=[n for n in order if n not in caches],
                      reused_dong_objects=caches, direct_inherited_imports=old_imports)
        if args.plan:
            report['status'] = 'PASS_DESCENDANT_LOCALITY_SOURCE_PLAN_NOT_COMPILED'
        else:
            lean, mathlib, paths, compiler = helper.external_paths(args, old)
            report['compiler'] = compiler
            report['external_objects'] = {}
            external_names = set(external)
            for receipt in (old, coherence, locality):
                external_names.update(receipt['external_objects'])
            for name in sorted(external_names):
                path = helper.object_for(name, paths)
                digest = sha(path)
                for receipt in (old, coherence, locality):
                    witness = receipt['external_objects'].get(name)
                    if witness and digest != witness.get('sha256', witness.get('object_sha256')):
                        raise RuntimeError('Inherited external object changed: ' + name)
                tracked[path] = digest
                report['external_objects'][name] = dict(path=str(path), sha256=digest)
            build = report_dir / 'build'
            build.mkdir()
            # Only copied/authenticated local objects enter this fresh build path.
            env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str,
                       [build, l_build, c_build, base_build, *paths])))
            report['lean_path'] = env['LEAN_PATH']
            for name in order:
                node = nodes[name]
                source = Path(node['path'])
                if sha(source) != node['sha256']:
                    raise RuntimeError('Source changed before use: ' + name)
                snapshot, target = build / (name + '.lean'), build / (name + '.olean')
                snapshot.write_bytes(source.read_bytes())
                row = dict(module=name, source_sha256=node['sha256'])
                report['modules'].append(row)
                if name in caches:
                    target.write_bytes(Path(caches[name]['object_path']).read_bytes())
                    row.update(mode='REUSED_AUTHENTICATED_DONG_OBJECT', exit_code=0,
                               predecessor_receipt_sha256=caches[name]['receipt_sha256'])
                else:
                    command = [str(lean), '-DwarningAsError=true', '--root=' + str(build),
                               '-o', str(target), str(snapshot)]
                    print(name + ': compiling delta', flush=True)
                    code, output = helper.run(command, mathlib, args.timeout, env=env)
                    report['compiler_invoked'] = True
                    (build / (name + '.log')).write_text(output, encoding='utf-8')
                    row.update(mode='COMPILED_NEW_DELTA', command=command,
                               exit_code=code, output=output)
                    if code:
                        raise RuntimeError(f'Compilation failed for {name} ({code})\n{output}')
                if sha(snapshot) != node['sha256'] or sha(source) != node['sha256']:
                    raise RuntimeError('Source changed during use: ' + name)
                row['object_sha256'] = sha(target)
            queries = [q for n in order for q in nodes[n]['public_declarations']]
            if not queries or len(queries) != len(set(queries)):
                raise RuntimeError('Empty or conflicting public inventory')
            probe = ''.join('import ' + name + '\n' for name in order)
            probe += ''.join('#print axioms ' + q + '\n' for q in queries)
            (report_dir / 'axiom_probe.lean').write_text(probe, encoding='utf-8')
            code, output = helper.run([str(lean), '--stdin'], mathlib, args.timeout,
                                      env=env, stdin=probe)
            report['compiler_invoked'] = True
            axioms = verifier.axiom_reports(output)
            report['axiom_probe'] = dict(exit_code=code, output=output, declarations=axioms)
            if code or set(axioms) != set(queries):
                raise RuntimeError('The public-declaration axiom probe was incomplete')
            if any(not set(values) <= (ORDINARY_AXIOMS | {'Lean.ofReduceBool'}
                       if q.startswith(SELECTED_NAMESPACE + '.') else ORDINARY_AXIOMS)
                   for q, values in axioms.items()):
                raise RuntimeError('A new declaration depends on nonordinary axioms')
            helper.authenticate_base(base)
            if any(sha(path) != digest for path, digest in tracked.items()):
                raise RuntimeError('An inherited receipt/source/object changed during verification')
            after, after_order, _, _ = source_plan(verifier, roots, requested, inherited)
            if after != nodes or after_order != order:
                raise RuntimeError('The selected source closure changed during verification')
            for row in report['modules']:
                if sha(build / (row['module'] + '.olean')) != row['object_sha256']:
                    raise RuntimeError('A compiled or reused delta object changed')
            if sha(lean) != helper.LEAN_SHA:
                raise RuntimeError('The compiler changed during verification')
            report.update(status='PASS_DESCENDANT_LOCALITY_DELTA',
                          public_declaration_count=len(queries),
                          theorem_names=[q for n in order for q in nodes[n]['theorem_names']],
                          declarations_using_inherited_native_axiom=[q for q, values in axioms.items()
                              if 'Lean.ofReduceBool' in values],
                          axioms=sorted({a for values in axioms.values() for a in values}))
        exit_code = 0
    except Exception as error:
        report.update(status='FAIL_DESCENDANT_LOCALITY_DELTA',
                      error_type=type(error).__name__, error=str(error))
        exit_code = 1
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    receipt_path = report_dir / ('PLAN.json' if args.plan else 'VERIFICATION.json')
    if writable:
        helper.write_json(receipt_path, report)
    print(json.dumps(dict(status=report['status'], receipt=str(receipt_path) if writable else None,
                         compiled_modules=[r['module'] for r in report['modules']
                                           if r.get('mode') == 'COMPILED_NEW_DELTA'],
                         reused_modules=[r['module'] for r in report['modules']
                                         if r.get('mode') == 'REUSED_AUTHENTICATED_DONG_OBJECT'],
                         public_declarations=report.get('public_declaration_count'),
                         error=report.get('error')), indent=2, ensure_ascii=False))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
