#!/usr/bin/env python3
"""Verify a requested new closure after the frozen 354-module vertex cut.

All 354 predecessor sources, snapshots, objects, receipts, public axiom-query
transcripts and external objects are authenticated and reused. No predecessor
or Mathlib is rebuilt. Only the requested dependency closure from the explicit
orbifold/twisted roots is compiled, into a fresh report directory. Every public
declaration is queried, and all new declarations must use ordinary axioms only.
The inherited selected-origin native axiom is checked solely in its already
sealed declarations; no new native proof or new native-dependent theorem is
accepted. --plan authenticates and inventories without invoking Lean.
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
PRODUCTS_RUNNER_SHA = 'b802974d566d3e0f9021dbc77e6b8c0ee6f50483ae7a212bc4e09942f2f91ac8'
PRODUCTS_SHA = '0bea29292112ad21de3c261e8ada14e39642f9e6dcc0d0e85e0deb91f4f98dd0'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}


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


def authenticate_products(products, vertex, helper, locality, verifier,
                          receipt_path, roots, inherited, tracked):
    if sha(receipt_path) != PRODUCTS_SHA:
        raise RuntimeError('Changed fourteen-module vertex-products receipt')
    r = json.loads(receipt_path.read_text())
    expected_receipts = dict(base=helper.BASE_RECEIPT_SHA,
        coherence=locality.COHERENCE_SHA, generator_locality=locality.LOCALITY_SHA,
        locality='867e422b5b95948f1ec34de21f73f61bb213f059c0ea521e9b9f7f133d60d05d',
        translation=products.TRANSLATION_SHA, involution=products.INVOLUTION_SHA,
        conformal=products.CONFORMAL_SHA)
    if (r['status'] != 'PASS_VERTEX_PRODUCTS_DELTA'
            or r['runner_sha256'] != PRODUCTS_RUNNER_SHA
            or r['inherited_module_count'] != 340
            or r['predecessor_receipt_sha256'] != expected_receipts
            or r['compiler']['binary_sha256'] != helper.LEAN_SHA
            or r['compiler']['mathlib_commit'] != helper.MATHLIB_COMMIT
            or not r['authenticated_inputs_unchanged']
            or r['predecessors_modified'] or r['predecessors_recompiled']
            or r['mathlib_rebuilt']):
        raise RuntimeError('Incompatible vertex-products predecessor')
    nodes, order, _, _, owners = vertex.source_plan(
        locality, verifier, roots, r['requested_modules'], inherited)
    if (nodes != r['sources'] or order != r['dependency_order']
            or owners != r['public_declaration_owners']):
        raise RuntimeError('Changed vertex-products source closure or public inventory')
    records = {row['module']: row for row in r['modules']}
    if len(records) != 14 or len(r['modules']) != 14 or records.keys() != nodes.keys():
        raise RuntimeError('Expected exactly fourteen vertex-products modules')
    build = receipt_path.parent/'build'
    tracked[receipt_path] = PRODUCTS_SHA
    for name, node in nodes.items():
        source = helper.relative_file(roots[node['root']], node['path'])
        snapshot, obj = build/(name+'.lean'), build/(name+'.olean')
        row = records[name]
        if (row['exit_code'] or row['source_sha256'] != node['sha256']
                or sha(snapshot) != node['sha256'] or sha(obj) != row['object_sha256']):
            raise RuntimeError('Changed vertex-products snapshot/object: ' + name)
        tracked.update({source:node['sha256'], snapshot:node['sha256'], obj:row['object_sha256']})
    vertex.check_probe(verifier, r, owners, products.SELECTED_NAMESPACE)
    declarations = r['axiom_probe']['declarations']
    actual_native = sorted(q for q, axioms in declarations.items() if 'Lean.ofReduceBool' in axioms)
    if actual_native != sorted(r['declarations_using_inherited_native_axiom']):
        raise RuntimeError('Changed inherited native-axiom declaration list')
    for q in actual_native:
        if (owners[q] != products.SELECTED_MODULE
                or not q.startswith(products.SELECTED_NAMESPACE + '.')):
            raise RuntimeError('Inherited native axiom escaped its sealed owner: ' + q)
    return r, nodes, build


def main():
    here = Path(__file__).resolve().parent
    parent = here.parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--modules', nargs='+', required=True)
    for name, default in dict(orbifold=here, twisted=parent/'twisted_sector',
            vertex=parent/'vertex_extension', conformal=parent/'conformal_structure',
            involution=parent/'involution_coherence', translation=parent/'translation_coherence',
            locality=parent/'descendant_locality', coherence=parent/'state_field').items():
        p.add_argument('--'+name+'-root', type=Path, default=default)
    for key in ('coherence-report-dir', 'generator-locality-report-dir', 'locality-report-dir',
                'translation-report-dir', 'involution-report-dir', 'conformal-report-dir',
                'products-report-dir', 'helper', 'locality-helper', 'translation-helper',
                'vertex-helper', 'products-helper', 'base'):
        p.add_argument('--'+key, type=Path)
    p.add_argument('--report-dir', type=Path, default=here/'orbifold_incremental_results')
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
        conformal_report_dir=args.vertex_root/'conformal_closed_results',
        products_report_dir=args.vertex_root/'products_closed_results',
        helper=args.coherence_root/'verify_state_field.py',
        locality_helper=args.locality_root/'verify_descendant_locality.py',
        translation_helper=args.translation_root/'verify_translation_coherence.py',
        vertex_helper=args.vertex_root/'verify_vertex_extension.py',
        products_helper=args.vertex_root/'verify_vertex_products.py')
    for key, value in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, value)
    for key, value in vars(args).items():
        if isinstance(value, Path):
            setattr(args, key, value.expanduser().resolve())
    requested = list(dict.fromkeys(x.removesuffix('.lean') for x in args.modules))
    if args.timeout <= 0 or any(not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', x) for x in requested):
        p.error('Use positive timeout and simple module names')
    old_roots = dict(vertex=args.vertex_root, conformal=args.conformal_root,
        involution=args.involution_root)
    roots = dict(orbifold=args.orbifold_root, twisted=args.twisted_root)
    report = dict(schema='hmt.lean.orbifold.input.incremental.v1', status='RUNNING',
        started_at_utc=datetime.now(timezone.utc).isoformat(), invocation=sys.argv,
        runner_sha256=sha(__file__), requested_modules=requested, modules=[],
        predecessors_modified=False, predecessors_recompiled=False, mathlib_rebuilt=False,
        compiler_invoked=False, allowed_delta_axioms=sorted(ORDINARY),
        scope='Exactly the listed declarations; no implicit twisted-module, orbifold or FLM promotion.')
    writable = False
    try:
        products = load(args.products_helper, PRODUCTS_RUNNER_SHA, 'frozen_vertex_products')
        vertex = load(args.vertex_helper, products.PREDECESSOR_RUNNER_SHA, 'frozen_vertex_extension')
        helper = load(args.helper, products.HELPER_SHA, 'orbifold_base_helper')
        locality = load(args.locality_helper, products.LOCALITY_HELPER_SHA, 'orbifold_locality_helper')
        translation = load(args.translation_helper, products.TRANSLATION_HELPER_SHA, 'orbifold_translation_helper')
        outputs = next((x for x in here.parents if x.name == 'output'), None)
        base = args.base or (outputs/helper.BASE_NAME if outputs else None)
        if base is None:
            raise RuntimeError('Use --base to locate the relocated base279')
        protected = [base, args.coherence_report_dir, args.generator_locality_report_dir,
            args.locality_report_dir, args.translation_report_dir, args.involution_report_dir,
            args.conformal_report_dir, args.products_report_dir]
        if any(args.report_dir.is_relative_to(x) or x.is_relative_to(args.report_dir) for x in protected):
            raise RuntimeError('Output overlaps an authenticated predecessor')
        helpers = [args.helper, args.locality_helper, args.translation_helper,
            args.vertex_helper, args.products_helper, Path(__file__).resolve()]
        if any(x.is_relative_to(args.report_dir) for x in [*roots.values(), *old_roots.values(), *helpers]):
            raise RuntimeError('Output overlaps sources or helper files')
        if args.report_dir.exists():
            raise RuntimeError('Report directory must not exist; prior receipts are preserved')
        verifier, old, b_sources, _, b_build = helper.authenticate_base(base)
        bp = old['axiom_probe']
        base_queries = re.findall(r'^#print axioms\s+(\S+)', bp['source'], re.M)
        if (bp['exit_code'] or set(base_queries) != set(bp['declarations'])
                or verifier.axiom_reports(bp['output']) != bp['declarations']
                or any(not set(v) <= ORDINARY | {'Lean.ofReduceBool'} for v in bp['declarations'].values())):
            raise RuntimeError('Invalid base axiom-probe transcript')
        tracked = {args.helper:products.HELPER_SHA,
            args.locality_helper:products.LOCALITY_HELPER_SHA,
            args.translation_helper:products.TRANSLATION_HELPER_SHA,
            args.vertex_helper:products.PREDECESSOR_RUNNER_SHA,
            args.products_helper:PRODUCTS_RUNNER_SHA,
            Path(__file__).resolve():report['runner_sha256']}
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
        t, ts, tb = vertex.authenticate_successor(helper, locality, verifier,
            args.translation_report_dir/'VERIFICATION.json', products.TRANSLATION_SHA,
            args.translation_root, 'PASS_TRANSLATION_COHERENCE_DELTA', 12, inherited,
            tracked, 'HMT.I.SelectedTranslationCoherence')
        inherited.update(ts)
        inv, ins, ib = vertex.authenticate_successor(helper, locality, verifier,
            args.involution_report_dir/'VERIFICATION.json', products.INVOLUTION_SHA,
            args.involution_root, 'PASS_INVOLUTION_COHERENCE_DELTA', 2, inherited, tracked)
        inherited.update(ins)
        if len(inherited) != 323:
            raise RuntimeError('Expected exactly 323 modules before conformal cut')
        conf, conf_sources, conf_build = products.authenticate_conformal(vertex, helper,
            locality, verifier, args.conformal_report_dir/'VERIFICATION.json',
            old_roots, inherited, tracked)
        inherited.update(conf_sources)
        if len(inherited) != 340:
            raise RuntimeError('Expected exactly 340 modules before products cut')
        prod, prod_sources, prod_build = authenticate_products(products, vertex, helper,
            locality, verifier, args.products_report_dir/'VERIFICATION.json',
            old_roots, inherited, tracked)
        inherited.update(prod_sources)
        if len(inherited) != 354:
            raise RuntimeError('Expected exactly 354 authenticated predecessor modules')
        for receipt in (c, g, l):
            probe = receipt['axiom_probe']
            if verifier.axiom_reports(probe['output']) != probe['declarations']:
                raise RuntimeError('Changed inherited probe transcript')
        plan = vertex.source_plan(locality, verifier, roots, requested, inherited)
        nodes, order, external, old_imports, owners = plan
        report.update(base=str(base), source_roots={k:str(v) for k,v in roots.items()},
            inherited_module_count=len(inherited), sources=nodes, dependency_order=order,
            direct_inherited_imports=old_imports, public_declaration_owners=owners,
            predecessor_receipt_sha256=dict(base=helper.BASE_RECEIPT_SHA,
                coherence=locality.COHERENCE_SHA, generator_locality=locality.LOCALITY_SHA,
                locality=translation.LOCALITY_SHA, translation=products.TRANSLATION_SHA,
                involution=products.INVOLUTION_SHA, conformal=products.CONFORMAL_SHA,
                products=PRODUCTS_SHA))
        lean, mathlib, paths, compiler = helper.external_paths(args, old)
        report['compiler'] = compiler
        receipts = (old, c, g, l, t, inv, conf, prod)
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
        resolution = [build, prod_build, conf_build, ib, tb, lb, gb, cb, b_build, *paths]
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
            report['status'] = 'PASS_ORBIFOLD_INPUT_SOURCE_PLAN_NOT_COMPILED'
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
            code, output = helper.run([str(lean), '--stdin'], mathlib, args.timeout, env=env, stdin=probe)
            axioms = verifier.axiom_reports(output)
            report['axiom_probe'] = dict(exit_code=code, output=output, declarations=axioms)
            if code or set(axioms) != set(queries):
                raise RuntimeError('Incomplete delta public-declaration axiom probe')
            for query, values in axioms.items():
                if not set(values) <= ORDINARY:
                    raise RuntimeError('Disallowed new delta axiom: ' + query)
            for row in report['modules']:
                if sha(build/(row['module']+'.olean')) != row['object_sha256']:
                    raise RuntimeError('New compiled object changed')
            report.update(status='PASS_ORBIFOLD_INPUT_DELTA', public_declaration_count=len(queries),
                theorem_names=[q for name in order for q in nodes[name]['theorem_names']],
                axioms=sorted({a for values in axioms.values() for a in values}))
        helper.authenticate_base(base)
        if any(sha(path) != digest for path,digest in tracked.items()) or sha(lean) != helper.LEAN_SHA:
            raise RuntimeError('Authenticated input or compiler changed during verification')
        if vertex.source_plan(locality, verifier, roots, requested, inherited) != plan:
            raise RuntimeError('The selected source closure changed during verification')
        report['authenticated_inputs_unchanged'] = True
        exit_code = 0
    except Exception as error:
        report.update(status='FAIL_ORBIFOLD_INPUT_DELTA', error_type=type(error).__name__, error=str(error))
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
