#!/usr/bin/env python3
"""Verify only an explicit translation/coherence delta and its local imports.

Reuse the authenticated 279 + 17 + 2 + 11 predecessor objects without
rebuilding them or Mathlib. Every public source declaration in the requested
closure is queried with #print axioms. Reports require a fresh directory.
--plan authenticates the source/object cut without invoking Lean; it is not a
compilation receipt. All source, receipt, helper and runtime roots can move.
No result beyond the exact recorded declarations is implicitly certified.
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
LOCALITY_HELPER_SHA = 'c16c63bfe0f9c95f7a5e767e8f8be5b1f67524496259f1618f9fe1043ece82a3'
LOCALITY_SHA = '867e422b5b95948f1ec34de21f73f61bb213f059c0ea521e9b9f7f133d60d05d'
ORDINARY_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
SELECTED_MODULE = 'SelectedTranslationCoherence'
SELECTED_NAMESPACE = 'HMT.I.SelectedTranslationCoherence'
SELECTED_IMPORTS = {'SelectedDescendantLocality', 'LatticeStateFieldTranslation'}


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def load_helper(path, expected, name):
    if sha(path) != expected:
        raise RuntimeError('Changed authenticated helper: ' + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authenticate_locality(helper, locality, verifier, receipt_path, root,
                          inherited, tracked):
    """Relocate absolute historical source paths, never trust loose objects."""
    if sha(receipt_path) != LOCALITY_SHA:
        raise RuntimeError('Full-state locality receipt is not the sealed cut')
    receipt = json.loads(receipt_path.read_text())
    if (receipt['status'] != 'PASS_DESCENDANT_LOCALITY_DELTA'
            or receipt['runner_sha256'] != LOCALITY_HELPER_SHA
            or receipt['base_receipt_sha256'] != helper.BASE_RECEIPT_SHA
            or receipt['coherence_receipt_sha256'] != locality.COHERENCE_SHA
            or receipt['locality_receipt_sha256'] != locality.LOCALITY_SHA
            or receipt['compiler']['binary_sha256'] != helper.LEAN_SHA
            or receipt['compiler']['mathlib_commit'] != helper.MATHLIB_COMMIT
            or receipt['inherited_module_count'] != 298):
        raise RuntimeError('Incompatible full-state locality predecessor')
    sources = receipt['sources']
    records = {row['module']: row for row in receipt['modules']}
    if len(records) != 11 or len(receipt['modules']) != 11 or records.keys() != sources.keys():
        raise RuntimeError('Expected exactly eleven full-state locality modules')
    historical_root = Path(sources['SelectedDescendantLocality']['path']).parent
    build = receipt_path.parent / 'build'
    owners = {}
    tracked[receipt_path] = LOCALITY_SHA
    for name, node in sources.items():
        old_path = Path(node['path'])
        relative = old_path.relative_to(historical_root) if old_path.is_absolute() else old_path
        source = helper.relative_file(root, str(relative))
        snapshot, obj = build / (name + '.lean'), build / (name + '.olean')
        row = records[name]
        inspected = locality.inspect(verifier, source)
        if (name in inherited or inspected['sha256'] != node['sha256']
                or sha(snapshot) != node['sha256'] or row['exit_code']
                or row['source_sha256'] != node['sha256']
                or sha(obj) != row['object_sha256']
                or any(inspected[key] != node[key] for key in
                       ('imports', 'namespace', 'public_declarations', 'theorem_names'))):
            raise RuntimeError('Locality source/object/inventory mismatch: ' + name)
        for dep in inspected['imports']:
            if (dep not in sources and dep not in inherited
                    and dep.split('.')[0] not in verifier.EXTERNAL_PREFIXES):
                raise RuntimeError('Unresolved sealed locality import: ' + dep)
        for declaration in node['public_declarations']:
            if declaration in owners:
                raise RuntimeError('Conflicting sealed public declaration: ' + declaration)
            owners[declaration] = name
        tracked.update({source: node['sha256'], snapshot: node['sha256'],
                        obj: row['object_sha256']})
    probe = receipt['axiom_probe']
    if probe['exit_code'] or set(probe['declarations']) != set(owners):
        raise RuntimeError('Incomplete sealed locality public-declaration probe')
    selected = sources['SelectedDescendantLocality']
    if (selected['namespace'] != locality.SELECTED_NAMESPACE
            or set(selected['imports']) != locality.SELECTED_IMPORTS):
        raise RuntimeError('Wrong inherited selected-origin module')
    for declaration, axioms in probe['declarations'].items():
        allowed = ORDINARY_AXIOMS | ({'Lean.ofReduceBool'}
                    if owners[declaration] == 'SelectedDescendantLocality' else set())
        if not set(axioms) <= allowed:
            raise RuntimeError('Unexpected inherited axiom: ' + declaration)
    return receipt, sources, build


def source_plan(locality, verifier, root, requested, inherited):
    nodes, order, external, old_imports = locality.source_plan(
        verifier, [root], requested, inherited)
    owners = {}
    # The inherited inspector inventories ordinary named declarations. Reject
    # unsupported declaration-producing syntax rather than silently omitting it.
    declaration = re.compile(
        r'^\s*(?:@\[[^\]]*\]\s*)*'
        r'(?P<mods>(?:(?:private|protected|noncomputable|scoped|public|partial)\s+)*)'
        r'(?P<kind>theorem|lemma|def|abbrev|structure|inductive|instance|opaque|class|constant)'
        r'\b\s+(?P<name>[^\s:({\[]+)', re.M)
    for name, node in nodes.items():
        source = Path(node['path'])
        if not source.resolve().is_relative_to(root):
            raise RuntimeError('Selected source escapes its root: ' + name)
        code = verifier.mask_comments_strings(source.read_text(encoding='utf-8'))
        if re.search(r'^\s*(?:elab|macro|syntax|run_cmd|initialize|builtin_initialize|export)\b',
                     code, re.M):
            raise RuntimeError('Unsupported declaration-producing command: ' + name)
        found = []
        for match in declaration.finditer(code):
            if (match['kind'] in {'class', 'constant'}
                    or {'public', 'partial'} & set(match['mods'].split())
                    or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9']*", match['name'])):
                raise RuntimeError('Use supported explicitly named declarations: ' + name)
            if 'private' not in match['mods'].split():
                found.append(node['namespace'] + '.' + match['name'])
        if found != node['public_declarations']:
            raise RuntimeError('Incomplete public source inventory: ' + name)
        if name == SELECTED_MODULE or node['namespace'] == SELECTED_NAMESPACE:
            if (name != SELECTED_MODULE or node['namespace'] != SELECTED_NAMESPACE
                    or set(node['imports']) != SELECTED_IMPORTS):
                raise RuntimeError('Selected exception needs exact module, namespace and imports')
        for query in node['public_declarations']:
            if query in owners:
                raise RuntimeError('Conflicting delta public declaration: ' + query)
            owners[query] = name
        node['path'] = str(source.relative_to(root))
    return nodes, order, external, old_imports, owners


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--modules', nargs='+', required=True,
                        help='Explicit new modules; include their unsatisfied local imports')
    parser.add_argument('--source-root', type=Path, default=here)
    parser.add_argument('--locality-root', type=Path, default=here.parent / 'descendant_locality')
    parser.add_argument('--locality-report-dir', type=Path,
                        help='Frozen eleven-module report; defaults to locality-root/locality_closed_results')
    parser.add_argument('--generator-locality-report-dir', type=Path,
                        help='Frozen two-module report; defaults to locality-root/resultados')
    parser.add_argument('--coherence-root', type=Path, default=here.parent / 'state_field')
    parser.add_argument('--coherence-report-dir', type=Path,
                        help='Frozen seventeen-module report; defaults to coherence-root/normal_coherence_results')
    parser.add_argument('--helper', type=Path, help='Pinned state-field verifier')
    parser.add_argument('--locality-helper', type=Path, help='Pinned descendant-locality verifier')
    parser.add_argument('--base', type=Path, help='Frozen 279-module package root')
    parser.add_argument('--report-dir', type=Path, default=here / 'incremental_results')
    parser.add_argument('--lean', type=Path, default=Path.home() /
                        '.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')
    parser.add_argument('--mathlib', type=Path, default=Path('/Users/ruben/Documents/'
                        'ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4'))
    parser.add_argument('--timeout', type=int, default=900)
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    defaults = dict(locality_report_dir=args.locality_root / 'locality_closed_results',
                    generator_locality_report_dir=args.locality_root / 'resultados',
                    coherence_report_dir=args.coherence_root / 'normal_coherence_results',
                    helper=args.coherence_root / 'verify_state_field.py',
                    locality_helper=args.locality_root / 'verify_descendant_locality.py')
    for key, default in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, default)
    for key, value in vars(args).items():
        if isinstance(value, Path):
            setattr(args, key, value.expanduser().resolve())
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    requested = list(dict.fromkeys(name.removesuffix('.lean') for name in args.modules))
    if any(not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', name) for name in requested):
        parser.error('--modules accepts simple module names, not paths')
    report_dir = args.report_dir
    report = dict(schema='hmt.lean.translation.coherence.incremental.v1', status='RUNNING',
                  started_at_utc=datetime.now(timezone.utc).isoformat(), invocation=sys.argv,
                  runner_sha256=sha(Path(__file__)), requested_modules=requested, modules=[],
                  predecessors_modified=False, predecessors_recompiled=False,
                  mathlib_rebuilt=False, compiler_invoked=False,
                  scope='Exact public source declarations recorded below; no implicit promotion.',
                  allowed_delta_axioms=sorted(ORDINARY_AXIOMS),
                  inherited_axiom_exception=dict(module=SELECTED_MODULE,
                      namespace=SELECTED_NAMESPACE, imports=sorted(SELECTED_IMPORTS),
                      extra_axioms=['Lean.ofReduceBool'],
                      reason='Inherited selected origin only; no new native proof.'))
    writable = False
    try:
        helper = load_helper(args.helper, HELPER_SHA, 'translation_state_field_helper')
        locality = load_helper(args.locality_helper, LOCALITY_HELPER_SHA,
                               'translation_descendant_locality_helper')
        outputs = next((path for path in here.parents if path.name == 'output'), None)
        base = args.base or (outputs / helper.BASE_NAME if outputs else None)
        if base is None:
            raise RuntimeError('Use --base to locate the relocated frozen package')
        base = base.resolve()
        protected = [base, args.coherence_report_dir, args.generator_locality_report_dir,
                     args.locality_report_dir]
        if any(report_dir.is_relative_to(path) or path.is_relative_to(report_dir)
               for path in protected):
            raise RuntimeError('Report directory overlaps a protected predecessor')
        if any(path.is_relative_to(report_dir) for path in
               (args.source_root, args.locality_root, args.coherence_root,
                args.helper, args.locality_helper, Path(__file__).resolve())):
            raise RuntimeError('Report directory overlaps protected sources or helpers')
        if report_dir.exists():
            raise RuntimeError('Use a new report directory; existing directories are never overwritten')
        verifier, old, base_sources, _, base_build = helper.authenticate_base(base)
        tracked = {args.helper: HELPER_SHA, args.locality_helper: LOCALITY_HELPER_SHA,
                   Path(__file__).resolve(): report['runner_sha256']}
        coherence, c_sources, _, c_build = locality.authenticate_delta(
            helper, verifier, args.coherence_report_dir / 'VERIFICATION.json',
            locality.COHERENCE_SHA, args.coherence_root, 17, base_sources, tracked)
        inherited = {**base_sources, **c_sources}
        generators, g_sources, _, g_build = locality.authenticate_delta(
            helper, verifier, args.generator_locality_report_dir / 'VERIFICATION.json',
            locality.LOCALITY_SHA, args.locality_root, 2, inherited, tracked)
        inherited.update(g_sources)
        full_locality, l_sources, l_build = authenticate_locality(
            helper, locality, verifier, args.locality_report_dir / 'VERIFICATION.json',
            args.locality_root, inherited, tracked)
        inherited.update(l_sources)
        if len(inherited) != 309:
            raise RuntimeError('Expected the exact 279 + 17 + 2 + 11 predecessor cut')
        nodes, order, external, old_imports, owners = source_plan(
            locality, verifier, args.source_root, requested, inherited)
        report.update(base=str(base), source_root=str(args.source_root),
                      coherence_root=str(args.coherence_root), locality_root=str(args.locality_root),
                      base_manifest_sha256=helper.BASE_MANIFEST_SHA,
                      base_receipt_sha256=helper.BASE_RECEIPT_SHA,
                      coherence_receipt_sha256=locality.COHERENCE_SHA,
                      generator_locality_receipt_sha256=locality.LOCALITY_SHA,
                      locality_receipt_sha256=LOCALITY_SHA,
                      helper_sha256=HELPER_SHA, locality_helper_sha256=LOCALITY_HELPER_SHA,
                      inherited_module_count=len(inherited), sources=nodes,
                      dependency_order=order, compile_order=order,
                      direct_inherited_imports=old_imports,
                      public_declaration_owners=owners)
        report_dir.mkdir(parents=True)
        writable = True
        if args.plan:
            report['status'] = 'PASS_TRANSLATION_COHERENCE_SOURCE_PLAN_NOT_COMPILED'
        else:
            lean, mathlib, paths, compiler = helper.external_paths(args, old)
            report['compiler'] = compiler
            report['external_objects'] = {}
            receipts = (old, coherence, generators, full_locality)
            external_names = set(external)
            for receipt in receipts:
                external_names.update(receipt['external_objects'])
            for name in sorted(external_names):
                path = helper.object_for(name, paths)
                digest = sha(path)
                for receipt in receipts:
                    witness = receipt['external_objects'].get(name)
                    if witness and digest != witness.get('sha256', witness.get('object_sha256')):
                        raise RuntimeError('Changed inherited external object: ' + name)
                tracked[path] = digest
                report['external_objects'][name] = dict(path=str(path), sha256=digest)
            build = report_dir / 'build'
            build.mkdir()
            resolution_paths = [build, l_build, g_build, c_build, base_build, *paths]
            # A stray predecessor object must not shadow an authenticated one.
            for receipt in receipts:
                for row in receipt['modules']:
                    resolved = helper.object_for(row['module'], resolution_paths)
                    if sha(resolved) != row['object_sha256']:
                        raise RuntimeError('Shadowed inherited object: ' + row['module'])
            for name, witness in report['external_objects'].items():
                if sha(helper.object_for(name, resolution_paths)) != witness['sha256']:
                    raise RuntimeError('Shadowed external object: ' + name)
            env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, resolution_paths)))
            report['lean_path'] = env['LEAN_PATH']
            for name in order:
                node = nodes[name]
                source = helper.relative_file(args.source_root, node['path'])
                if sha(source) != node['sha256']:
                    raise RuntimeError('Source changed before compilation: ' + name)
                snapshot, obj = build / (name + '.lean'), build / (name + '.olean')
                snapshot.write_bytes(source.read_bytes())
                command = [str(lean), '-DwarningAsError=true', '--root=' + str(build),
                           '-o', str(obj), str(snapshot)]
                print(name + ': compiling new delta only', flush=True)
                report['compiler_invoked'] = True
                code, output = helper.run(command, mathlib, args.timeout, env=env)
                (build / (name + '.log')).write_text(output, encoding='utf-8')
                row = dict(module=name, mode='COMPILED_NEW_DELTA', source_sha256=node['sha256'],
                           command=command, exit_code=code, output=output)
                report['modules'].append(row)
                if code:
                    raise RuntimeError(f'Compilation failed for {name} ({code})\n{output}')
                if sha(snapshot) != node['sha256'] or sha(source) != node['sha256']:
                    raise RuntimeError('Source changed during compilation: ' + name)
                row['object_sha256'] = sha(obj)
            queries = [query for name in order for query in nodes[name]['public_declarations']]
            probe = ''.join('import ' + name + '\n' for name in order)
            probe += ''.join('#print axioms ' + query + '\n' for query in queries)
            (report_dir / 'axiom_probe.lean').write_text(probe, encoding='utf-8')
            code, output = helper.run([str(lean), '--stdin'], mathlib, args.timeout,
                                      env=env, stdin=probe)
            axioms = verifier.axiom_reports(output)
            report['axiom_probe'] = dict(exit_code=code, output=output, declarations=axioms)
            if code or set(axioms) != set(queries):
                raise RuntimeError('Incomplete public-declaration axiom probe')
            for query, values in axioms.items():
                allowed = ORDINARY_AXIOMS | ({'Lean.ofReduceBool'}
                            if owners[query] == SELECTED_MODULE else set())
                if not set(values) <= allowed:
                    raise RuntimeError('Disallowed delta axiom: ' + query)
            report.update(status='PASS_TRANSLATION_COHERENCE_DELTA',
                          public_declaration_count=len(queries),
                          theorem_names=[query for name in order for query in nodes[name]['theorem_names']],
                          declarations_using_inherited_native_axiom=[query for query, values in axioms.items()
                              if 'Lean.ofReduceBool' in values],
                          axioms=sorted({axiom for values in axioms.values() for axiom in values}))
            for row in report['modules']:
                if sha(build / (row['module'] + '.olean')) != row['object_sha256']:
                    raise RuntimeError('A newly compiled object changed')
            if sha(lean) != helper.LEAN_SHA:
                raise RuntimeError('Compiler changed during verification')
        helper.authenticate_base(base)
        if any(sha(path) != digest for path, digest in tracked.items()):
            raise RuntimeError('An authenticated receipt/source/object/helper changed')
        after = source_plan(locality, verifier, args.source_root, requested, inherited)
        if after != (nodes, order, external, old_imports, owners):
            raise RuntimeError('The requested source closure changed during verification')
        report['authenticated_inputs_unchanged'] = True
        exit_code = 0
    except Exception as error:
        report.update(status='FAIL_TRANSLATION_COHERENCE_DELTA',
                      error_type=type(error).__name__, error=str(error))
        exit_code = 1
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    receipt_path = report_dir / ('PLAN.json' if args.plan else 'VERIFICATION.json')
    if writable:
        helper.write_json(receipt_path, report)
    print(json.dumps(dict(status=report['status'], receipt=str(receipt_path) if writable else None,
                         compiled_modules=[row['module'] for row in report['modules']],
                         public_declarations=report.get('public_declaration_count'),
                         error=report.get('error')), indent=2, ensure_ascii=False))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
