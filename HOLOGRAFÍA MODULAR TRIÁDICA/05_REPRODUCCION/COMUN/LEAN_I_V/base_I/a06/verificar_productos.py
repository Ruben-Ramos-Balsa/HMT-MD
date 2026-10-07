#!/usr/bin/env python3
"""Verify only new requested modules after the frozen 340-module conformal cut.

The previous vertex-extension verifier is imported by pinned hash, not changed.
All 323 older modules and all 17 modules in conformal_closed_results are reused
after authenticating source, snapshot, object, receipt, queries and external
objects. No predecessor or Mathlib rebuild occurs. Every public declaration of
the selected new closure is queried. Only SelectedConformalVertex in its exact
namespace may inherit Lean.ofReduceBool from the sealed selected origin; no new
native proof is permitted. All other declarations use ordinary axioms only.
--plan does not compile. Roots, receipts, helpers and runtime locations move.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
HELPER_SHA = 'f022db4decca339ed0873c08508b9a9a93b66a9ce711a3785526896870219939'
LOCALITY_HELPER_SHA = 'c16c63bfe0f9c95f7a5e767e8f8be5b1f67524496259f1618f9fe1043ece82a3'
TRANSLATION_HELPER_SHA = '8ab2f716cc15d892795aac3ae7ba5a53d6bfcf293f8545f34e0c1918dc06c4fb'
TRANSLATION_SHA = '58db187960f39204c9a885f8a70f593d132d17b6ea6460103647738811eef0aa'
INVOLUTION_SHA = 'ba709864f60103749e18864ff1c2261d0e718a21e4cbdfbeda1990e344d55318'
PREDECESSOR_RUNNER_SHA = 'a1a4d7f2a419403961cf8df6494c0d56393d7fa884a4be3a52d543a422ad396d'
CONFORMAL_SHA = 'd77a961bb9fed30a971654096d311de8f94d3058ad017a8e8397a3b091bcac43'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}
SELECTED_MODULE = 'SelectedConformalVertex'
SELECTED_NAMESPACE = 'HMT.I.SelectedConformalVertex'


def sha(path):
    import hashlib
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def load(path, expected, name):
    if sha(path) != expected:
        raise RuntimeError('Authenticated helper changed: ' + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authenticate_conformal(previous, helper, locality, verifier, receipt_path,
                           roots, inherited, tracked):
    if sha(receipt_path) != CONFORMAL_SHA:
        raise RuntimeError('Changed seventeen-module conformal receipt')
    r = json.loads(receipt_path.read_text())
    if (r['status'] != 'PASS_VERTEX_EXTENSION_DELTA'
            or r['runner_sha256'] != PREDECESSOR_RUNNER_SHA
            or r['inherited_module_count'] != 323
            or r['compiler']['binary_sha256'] != helper.LEAN_SHA
            or r['compiler']['mathlib_commit'] != helper.MATHLIB_COMMIT
            or not r['authenticated_inputs_unchanged']
            or r['predecessors_modified'] or r['predecessors_recompiled']
            or r['mathlib_rebuilt']):
        raise RuntimeError('Incompatible conformal predecessor')
    expected_receipts = dict(base=helper.BASE_RECEIPT_SHA,
        coherence=locality.COHERENCE_SHA, generator_locality=locality.LOCALITY_SHA,
        locality='867e422b5b95948f1ec34de21f73f61bb213f059c0ea521e9b9f7f133d60d05d',
        translation=TRANSLATION_SHA, involution=INVOLUTION_SHA)
    if r['predecessor_receipt_sha256'] != expected_receipts:
        raise RuntimeError('Wrong conformal ancestry')
    plan = previous.source_plan(locality, verifier, roots, r['requested_modules'], inherited)
    nodes, order, _, _, owners = plan
    if nodes != r['sources'] or order != r['dependency_order'] or owners != r['public_declaration_owners']:
        raise RuntimeError('Changed conformal source closure or public inventory')
    records = {row['module']:row for row in r['modules']}
    if len(records) != 17 or len(r['modules']) != 17 or records.keys() != nodes.keys():
        raise RuntimeError('Expected exactly seventeen conformal modules')
    build = receipt_path.parent/'build'
    tracked[receipt_path] = CONFORMAL_SHA
    for name, node in nodes.items():
        source = helper.relative_file(roots[node['root']], node['path'])
        snapshot, obj = build/(name+'.lean'), build/(name+'.olean')
        row = records[name]
        if (row['exit_code'] or row['source_sha256'] != node['sha256']
                or sha(snapshot) != node['sha256'] or sha(obj) != row['object_sha256']):
            raise RuntimeError('Changed conformal snapshot/object: ' + name)
        tracked.update({source:node['sha256'], snapshot:node['sha256'], obj:row['object_sha256']})
    previous.check_probe(verifier, r, owners)
    return r, nodes, build


def main():
    here = Path(__file__).resolve().parent
    parent = here.parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--modules', nargs='+', required=True)
    p.add_argument('--vertex-root', type=Path, default=here)
    p.add_argument('--conformal-root', type=Path, default=parent/'conformal_structure')
    p.add_argument('--involution-root', type=Path, default=parent/'involution_coherence')
    p.add_argument('--translation-root', type=Path, default=parent/'translation_coherence')
    p.add_argument('--locality-root', type=Path, default=parent/'descendant_locality')
    p.add_argument('--coherence-root', type=Path, default=parent/'state_field')
    for key in ('coherence-report-dir', 'generator-locality-report-dir', 'locality-report-dir',
                'translation-report-dir', 'involution-report-dir', 'helper', 'locality-helper',
                'translation-helper', 'vertex-helper', 'conformal-report-dir', 'base'):
        p.add_argument('--'+key, type=Path)
    p.add_argument('--report-dir', type=Path, default=here/'products_incremental_results')
    p.add_argument('--lean', type=Path, default=Path.home()/'.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')
    p.add_argument('--mathlib', type=Path, default=Path('/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4'))
    p.add_argument('--timeout', type=int, default=900)
    p.add_argument('--plan', action='store_true')
    args = p.parse_args()
    defaults = dict(coherence_report_dir=args.coherence_root/'normal_coherence_results',
        generator_locality_report_dir=args.locality_root/'resultados',
        locality_report_dir=args.locality_root/'locality_closed_results',
        translation_report_dir=args.translation_root/'translation_closed_results',
        involution_report_dir=args.involution_root/'involution_closed_results',
        helper=args.coherence_root/'verify_state_field.py',
        locality_helper=args.locality_root/'verify_descendant_locality.py',
        translation_helper=args.translation_root/'verify_translation_coherence.py',
        vertex_helper=here/'verify_vertex_extension.py',
        conformal_report_dir=here/'conformal_closed_results')
    for key, value in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, value)
    for key, value in vars(args).items():
        if isinstance(value, Path):
            setattr(args, key, value.expanduser().resolve())
    requested = list(dict.fromkeys(x.removesuffix('.lean') for x in args.modules))
    if args.timeout <= 0 or any(not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', x) for x in requested):
        p.error('Use positive timeout and simple module names')
    roots = dict(vertex=args.vertex_root, conformal=args.conformal_root, involution=args.involution_root)
    report = dict(schema='hmt.lean.vertex.products.incremental.v1', status='RUNNING',
        started_at_utc=datetime.now(timezone.utc).isoformat(), invocation=sys.argv,
        runner_sha256=sha(__file__), requested_modules=requested, modules=[],
        predecessors_modified=False, predecessors_recompiled=False, mathlib_rebuilt=False,
        compiler_invoked=False, allowed_delta_axioms=sorted(ORDINARY),
        inherited_axiom_exception=dict(module=SELECTED_MODULE,
            namespace=SELECTED_NAMESPACE, extra_axioms=['Lean.ofReduceBool'],
            reason='Inherited selected origin only; no new native proof in any source.'),
        scope='Exactly the listed declarations; no implicit VOA, twisted-orbifold or FLM promotion.')
    writable = False
    try:
        previous = load(args.vertex_helper, PREDECESSOR_RUNNER_SHA, 'frozen_vertex_extension')
        authenticate_successor = previous.authenticate_successor
        source_plan = previous.source_plan
        helper = load(args.helper, HELPER_SHA, 'vertex_base_helper')
        locality = load(args.locality_helper, LOCALITY_HELPER_SHA, 'vertex_locality_helper')
        translation = load(args.translation_helper, TRANSLATION_HELPER_SHA, 'vertex_translation_helper')
        outputs = next((x for x in here.parents if x.name == 'output'), None)
        base = args.base or (outputs/helper.BASE_NAME if outputs else None)
        if base is None:
            raise RuntimeError('Use --base to locate the relocated base279')
        protected = [base, args.coherence_report_dir, args.generator_locality_report_dir,
            args.locality_report_dir, args.translation_report_dir, args.involution_report_dir,
            args.conformal_report_dir]
        if any(args.report_dir.is_relative_to(x) or x.is_relative_to(args.report_dir) for x in protected):
            raise RuntimeError('Output overlaps an authenticated predecessor')
        if any(x.is_relative_to(args.report_dir) for x in
               [*roots.values(), args.helper, args.locality_helper, args.translation_helper, args.vertex_helper, Path(__file__).resolve()]):
            raise RuntimeError('Output overlaps sources or helper files')
        if args.report_dir.exists():
            raise RuntimeError('Report directory must not exist; prior receipts are preserved')
        verifier, old, b_sources, _, b_build = helper.authenticate_base(base)
        # Validate every query recorded by the sealed base, including its
        # explicitly inherited native selector axioms. No new native is allowed.
        bp = old['axiom_probe']
        base_queries = re.findall(r'^#print axioms\s+(\S+)', bp['source'], re.M)
        if (bp['exit_code'] or set(base_queries) != set(bp['declarations'])
                or verifier.axiom_reports(bp['output']) != bp['declarations']
                or any(not set(v) <= ORDINARY | {'Lean.ofReduceBool'} for v in bp['declarations'].values())):
            raise RuntimeError('Invalid base axiom-probe transcript')
        tracked = {args.helper: HELPER_SHA, args.locality_helper: LOCALITY_HELPER_SHA,
            args.translation_helper: TRANSLATION_HELPER_SHA, args.vertex_helper: PREDECESSOR_RUNNER_SHA,
            Path(__file__).resolve(): report['runner_sha256']}
        c, cs, _, cb = locality.authenticate_delta(helper, verifier,
            args.coherence_report_dir/'VERIFICATION.json', locality.COHERENCE_SHA,
            args.coherence_root, 17, b_sources, tracked)
        inherited = {**b_sources, **cs}
        g, gs, _, gb = locality.authenticate_delta(helper, verifier,
            args.generator_locality_report_dir/'VERIFICATION.json', locality.LOCALITY_SHA,
            args.locality_root, 2, inherited, tracked)
        inherited.update(gs)
        l, ls, lb = translation.authenticate_locality(helper, locality, verifier,
            args.locality_report_dir/'VERIFICATION.json', args.locality_root, inherited, tracked)
        inherited.update(ls)
        t, ts, tb = authenticate_successor(helper, locality, verifier,
            args.translation_report_dir/'VERIFICATION.json', TRANSLATION_SHA, args.translation_root,
            'PASS_TRANSLATION_COHERENCE_DELTA', 12, inherited, tracked, 'HMT.I.SelectedTranslationCoherence')
        inherited.update(ts)
        inv, ins, ib = authenticate_successor(helper, locality, verifier,
            args.involution_report_dir/'VERIFICATION.json', INVOLUTION_SHA, args.involution_root,
            'PASS_INVOLUTION_COHERENCE_DELTA', 2, inherited, tracked)
        inherited.update(ins)
        if len(inherited) != 323:
            raise RuntimeError('Expected the exact 323-module predecessor cut')
        conformal, conf_sources, conf_build = authenticate_conformal(
            previous, helper, locality, verifier,
            args.conformal_report_dir/'VERIFICATION.json', roots, inherited, tracked)
        inherited.update(conf_sources)
        if len(inherited) != 340:
            raise RuntimeError('Expected 323 + 17 authenticated predecessor modules')
        # The older helper checks complete public inventories; additionally
        # authenticate that the recorded transcripts reproduce those inventories.
        for receipt in (c, g, l):
            probe = receipt['axiom_probe']
            if verifier.axiom_reports(probe['output']) != probe['declarations']:
                raise RuntimeError('Changed inherited probe transcript')
        plan = source_plan(locality, verifier, roots, requested, inherited)
        nodes, order, external, old_imports, owners = plan
        for name, node in nodes.items():
            if name == SELECTED_MODULE or node['namespace'] == SELECTED_NAMESPACE:
                if name != SELECTED_MODULE or node['namespace'] != SELECTED_NAMESPACE:
                    raise RuntimeError('Selected exception requires exact owner module and namespace')
        report.update(base=str(base), source_roots={k:str(v) for k,v in roots.items()},
            inherited_module_count=len(inherited), sources=nodes, dependency_order=order,
            direct_inherited_imports=old_imports, public_declaration_owners=owners,
            predecessor_receipt_sha256=dict(base=helper.BASE_RECEIPT_SHA,
                coherence=locality.COHERENCE_SHA, generator_locality=locality.LOCALITY_SHA,
                locality=translation.LOCALITY_SHA, translation=TRANSLATION_SHA, involution=INVOLUTION_SHA,
                conformal=CONFORMAL_SHA))
        # Resolve and hash ALL inherited external objects even for a plan.
        lean, mathlib, paths, compiler = helper.external_paths(args, old)
        report['compiler'] = compiler
        receipts = (old, c, g, l, t, inv, conformal)
        external_names = set(external)
        for receipt in receipts:
            external_names.update(receipt['external_objects'])
        report['external_objects'] = {}
        for name in sorted(external_names):
            path = helper.object_for(name, paths)
            digest = sha(path)
            for receipt in receipts:
                witness = receipt['external_objects'].get(name)
                if witness and digest != witness.get('sha256', witness.get('object_sha256')):
                    raise RuntimeError('Changed inherited external object: ' + name)
            tracked[path] = digest
            report['external_objects'][name] = dict(path=str(path), sha256=digest)
        args.report_dir.mkdir(parents=True)
        writable = True
        build = args.report_dir/'build'
        resolution = [build, conf_build, ib, tb, lb, gb, cb, b_build, *paths]
        for receipt in receipts:
            for row in receipt['modules']:
                if sha(helper.object_for(row['module'], resolution)) != row['object_sha256']:
                    raise RuntimeError('An unauthenticated object shadows a predecessor: ' + row['module'])
        for name, witness in report['external_objects'].items():
            if sha(helper.object_for(name, resolution)) != witness['sha256']:
                raise RuntimeError('An unauthenticated object shadows an external import: ' + name)
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, resolution)))
        report['lean_path'] = env['LEAN_PATH']
        if args.plan:
            report['status'] = 'PASS_VERTEX_PRODUCTS_SOURCE_PLAN_NOT_COMPILED'
        else:
            build.mkdir()
            for name in order:
                node = nodes[name]
                source = helper.relative_file(roots[node['root']], node['path'])
                if sha(source) != node['sha256']:
                    raise RuntimeError('Source changed before compilation: ' + name)
                snapshot, obj = build/(name+'.lean'), build/(name+'.olean')
                snapshot.write_bytes(source.read_bytes())
                command = [str(lean), '-DwarningAsError=true', '--root='+str(build), '-o', str(obj), str(snapshot)]
                print(name+': compiling new delta only', flush=True)
                report['compiler_invoked'] = True
                code, output = helper.run(command, mathlib, args.timeout, env=env)
                (build/(name+'.log')).write_text(output)
                row = dict(module=name, source_sha256=node['sha256'], command=command,
                           exit_code=code, output=output, mode='COMPILED_NEW_DELTA')
                report['modules'].append(row)
                if code:
                    raise RuntimeError(f'Compilation failed for {name} ({code})\n{output}')
                if sha(snapshot) != node['sha256'] or sha(source) != node['sha256']:
                    raise RuntimeError('Source changed while compiling: ' + name)
                row['object_sha256'] = sha(obj)
            queries = [q for name in order for q in nodes[name]['public_declarations']]
            probe = ''.join('import '+name+'\n' for name in order)+''.join('#print axioms '+q+'\n' for q in queries)
            (args.report_dir/'axiom_probe.lean').write_text(probe)
            code, output = helper.run([str(lean),'--stdin'], mathlib, args.timeout, env=env, stdin=probe)
            axioms = verifier.axiom_reports(output)
            report['axiom_probe'] = dict(exit_code=code, output=output, declarations=axioms)
            if code or set(axioms) != set(queries):
                raise RuntimeError('Incomplete delta public-declaration axiom probe')
            for query, values in axioms.items():
                allowed = ORDINARY | ({'Lean.ofReduceBool'}
                    if owners[query] == SELECTED_MODULE
                    and query.startswith(SELECTED_NAMESPACE + '.') else set())
                if not set(values) <= allowed:
                    raise RuntimeError('Disallowed new delta axiom: ' + query)
            for row in report['modules']:
                if sha(build/(row['module']+'.olean')) != row['object_sha256']:
                    raise RuntimeError('New compiled object changed')
            report.update(status='PASS_VERTEX_PRODUCTS_DELTA',
                public_declaration_count=len(queries),
                theorem_names=[q for name in order for q in nodes[name]['theorem_names']],
                declarations_using_inherited_native_axiom=[q for q in queries
                    if 'Lean.ofReduceBool' in axioms[q]],
                axioms=sorted({a for values in axioms.values() for a in values}))
        helper.authenticate_base(base)
        if any(sha(path) != digest for path,digest in tracked.items()) or sha(lean) != helper.LEAN_SHA:
            raise RuntimeError('Authenticated input or compiler changed during verification')
        if source_plan(locality, verifier, roots, requested, inherited) != plan:
            raise RuntimeError('The selected source closure changed during verification')
        report['authenticated_inputs_unchanged'] = True
        exit_code = 0
    except Exception as error:
        report.update(status='FAIL_VERTEX_PRODUCTS_DELTA', error_type=type(error).__name__, error=str(error))
        exit_code = 1
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    path = args.report_dir/('PLAN.json' if args.plan else 'VERIFICATION.json')
    if writable:
        helper.write_json(path, report)
    print(json.dumps(dict(status=report['status'], receipt=str(path) if writable else None,
        compiled_modules=[r['module'] for r in report['modules']],
        public_declarations=report.get('public_declaration_count'), error=report.get('error')), indent=2))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
