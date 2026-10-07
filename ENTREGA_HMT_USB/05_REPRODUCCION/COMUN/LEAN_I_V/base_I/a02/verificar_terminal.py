#!/usr/bin/env python3
"""Authenticate descendants418+N and compile only an explicitly requested terminal delta.

The pinned parent runner is executed only with --plan. Its compiled receipt is
selected by an explicit SHA256, and its complete source/object/log/probe record
is checked separately. Existing modules and Mathlib are never rebuilt. All
public declarations of the new closure receive ordinary-only axiom queries.
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
HERE = Path(__file__).resolve().parent
PARENT_RUNNER_SHA = 'f106854e5e5c47e39058447c2b18e0b70c3527758086d50304aa6ca444a9f5a8'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path, expected, name):
    if sha(path) != expected:
        raise RuntimeError('Changed authenticated helper: '+str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authenticate_parent(root, expected, source_root, parent, vertex, locality, verifier):
    receipt = root/'VERIFICATION.json'
    if sha(receipt) != expected:
        raise RuntimeError('Changed explicitly selected parent receipt')
    r = json.loads(receipt.read_text())
    if (r['status'] != 'PASS_TWISTED_DESCENDANTS_DELTA'
            or r['runner_sha256'] != PARENT_RUNNER_SHA
            or r['continuation_receipt_sha256'] != parent.CONTINUATION_SHA
            or r['inherited_module_count'] != 418 or not r['authenticated_inputs_unchanged']
            or not r['compiler_invoked'] or r['predecessors_modified']
            or r['predecessors_recompiled'] or r['mathlib_rebuilt']):
        raise RuntimeError('Invalid compiled descendants predecessor')
    rows = {row['module']: row for row in r['modules']}
    build = root/'build'
    if (not rows or len(rows) != len(r['modules']) or set(rows) != set(r['sources'])
            or [row['module'] for row in r['modules']] != r['dependency_order']
            or {p.stem for p in build.glob('*.olean')} != set(rows)
            or {p.stem for p in build.glob('*.lean')} != set(rows)
            or {p.stem for p in build.glob('*.log')} != set(rows)):
        raise RuntimeError('Parent compiled closure is incomplete or contains extra modules')
    for name, node in r['sources'].items():
        if node['path'] != name+'.lean' or node['root'] != 'descendants':
            raise RuntimeError('Unexpected parent source locator: '+name)
        row = rows[name]
        source = source_root/node['path']
        inspected = locality.inspect(verifier, source)
        if (row['exit_code'] or row['source_sha256'] != node['sha256']
                or sha(source) != node['sha256'] or sha(build/(name+'.lean')) != node['sha256']
                or sha(build/(name+'.olean')) != row['object_sha256']
                or sha(build/(name+'.log')) != row['log_sha256']
                or (build/(name+'.log')).read_text() != row['output']
                or any(inspected[k] != node[k] for k in
                       ('imports', 'namespace', 'public_declarations', 'theorem_names'))):
            raise RuntimeError('Changed parent source, object, log or inventory: '+name)
    vertex.check_probe(verifier, r, r['public_declaration_owners'])
    queries = [q for m in r['dependency_order'] for q in r['sources'][m]['public_declarations']]
    theorems = [q for m in r['dependency_order'] for q in r['sources'][m]['theorem_names']]
    probe = ''.join('import '+m+'\n' for m in r['dependency_order'])
    probe += ''.join('#print axioms '+q+'\n' for q in queries)
    axioms = verifier.axiom_reports((root/'axiom_probe.log').read_text())
    if (len(queries) != len(set(queries)) or r['public_declaration_count'] != len(queries)
            or r['theorem_names'] != theorems or r['axiom_probe']['exit_code']
            or (root/'axiom_probe.lean').read_text() != probe
            or sha(root/'axiom_probe.lean') != r['axiom_probe']['source_sha256']
            or sha(root/'axiom_probe.log') != r['axiom_probe']['output_sha256']
            or (root/'axiom_probe.log').read_text() != r['axiom_probe']['output']
            or axioms != r['axiom_probe']['declarations'] or set(axioms) != set(queries)
            or any(not set(a) <= ORDINARY for a in axioms.values())):
        raise RuntimeError('Parent public axiom probe is changed, incomplete or disallowed')
    return r, build


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--parent-report-dir', type=Path, required=True)
    p.add_argument('--parent-receipt-sha256', required=True)
    p.add_argument('--parent-verifier', type=Path, default=HERE/'verify_twisted_descendants.py')
    p.add_argument('--parent-source-dir', type=Path, default=HERE)
    p.add_argument('--normalization-report-dir', type=Path, default=HERE/'normalization_results_20260922')
    p.add_argument('--normalization-verifier', type=Path, default=HERE/'verify_charge_normalization.py')
    p.add_argument('--continuation-report-dir', type=Path, default=HERE/'continuation_results_20260922')
    p.add_argument('--continuation-verifier', type=Path, default=HERE/'verify_twisted_continuation.py')
    p.add_argument('--continuation-source-dir', type=Path, default=HERE)
    p.add_argument('--source-dir', type=Path, default=HERE)
    p.add_argument('--modules', nargs='+', required=True)
    p.add_argument('--report-dir', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=900)
    p.add_argument('--plan', action='store_true')
    args = p.parse_args()
    if not re.fullmatch('[0-9a-f]{64}', args.parent_receipt_sha256):
        p.error('--parent-receipt-sha256 must be an explicit lowercase SHA256')
    if args.timeout <= 0 or any(not re.fullmatch('[A-Za-z_][A-Za-z_0-9]*', m) for m in args.modules):
        p.error('Use a positive timeout and simple module names without extensions')
    args.modules = list(dict.fromkeys(args.modules))
    for key, value in vars(args).items():
        if isinstance(value, Path):
            setattr(args, key, value.resolve())
    base, nr, cr, pr, out = (args.base, args.normalization_report_dir,
        args.continuation_report_dir, args.parent_report_dir, args.report_dir)
    if (out.exists() or any(out.is_relative_to(x) or x.is_relative_to(out)
            for x in (base, nr, cr, pr)) or any(x.is_relative_to(out) for x in
            (args.source_dir, args.parent_source_dir, args.continuation_source_dir,
             args.normalization_verifier, args.continuation_verifier, args.parent_verifier))):
        raise RuntimeError('Use a fresh report outside all protected inputs')
    parent = load(args.parent_verifier, PARENT_RUNNER_SHA, 'terminal_parent')
    previous = load(args.continuation_verifier, parent.RUNNER_SHA, 'terminal_continuation')
    focal = load(args.normalization_verifier, previous.FOCAL_SHA, 'terminal_normalization')
    fields = focal.authenticate(base)
    vertex_root = base/'antecedente/antecedente/antecedente'
    helper = load(vertex_root/'antecedente/antecedente/antecedente/verificar_delta.py',
        'f022db4decca339ed0873c08508b9a9a93b66a9ce711a3785526896870219939', 'terminal_helper')
    locality = load(vertex_root/'antecedente/antecedente/verificar_localidad.py',
        'c16c63bfe0f9c95f7a5e767e8f8be5b1f67524496259f1618f9fe1043ece82a3', 'terminal_inventory')
    vertex = load(vertex_root/'verificar_conforme.py',
        'a1a4d7f2a419403961cf8df6494c0d56393d7fa884a4be3a52d543a422ad396d', 'terminal_planner')
    core = vertex_root/'antecedente/antecedente/antecedente/antecedente/antecedente'
    verifier = load(core/'verificar_lean.py', helper.BASE_VERIFIER_SHA, 'terminal_parser')
    old, pb = authenticate_parent(pr, args.parent_receipt_sha256,
        args.parent_source_dir, parent, vertex, locality, verifier)
    out.mkdir(parents=True)
    report = dict(status='RUNNING', started_at_utc=datetime.now(timezone.utc).isoformat(),
        runner_sha256=sha(__file__), parent_runner_sha256=PARENT_RUNNER_SHA,
        parent_receipt_sha256=args.parent_receipt_sha256, parent_report_dir=str(pr),
        parent_source_dir=str(args.parent_source_dir), base=str(base),
        base_manifest_sha256=focal.MANIFEST_SHA, field_receipt_sha256=focal.RECEIPT_SHA,
        normalization_receipt_sha256=previous.NORMALIZATION_SHA,
        continuation_receipt_sha256=parent.CONTINUATION_SHA,
        requested_modules=args.modules, source_dir=str(args.source_dir),
        predecessors_modified=False, predecessors_recompiled=False,
        mathlib_rebuilt=False, compiler_invoked=False, modules=[])
    try:
        command = [sys.executable, '-I', '-S', str(args.parent_verifier), '--base', str(base),
            '--normalization-report-dir', str(nr), '--normalization-verifier', str(args.normalization_verifier),
            '--continuation-report-dir', str(cr), '--continuation-verifier', str(args.continuation_verifier),
            '--continuation-source-dir', str(args.continuation_source_dir),
            '--source-dir', str(args.parent_source_dir), '--modules', *old['requested_modules'],
            '--timeout', str(args.timeout), '--plan', '--report-dir', str(out/'parent_plan')]
        code, output = helper.run(command, base, args.timeout)
        (out/'parent_plan.log').write_text(output)
        report['parent_plan'] = dict(command=command, exit_code=code, output=output,
            log_sha256=sha(out/'parent_plan.log'))
        if code:
            raise RuntimeError('Parent descendants authentication plan failed')
        prior_plan = json.loads((out/'parent_plan/PLAN.json').read_text())
        if (prior_plan['status'] != 'PASS_TWISTED_DESCENDANTS_SOURCE_PLAN_NOT_COMPILED'
                or prior_plan['compiler_invoked'] or prior_plan['modules']
                or prior_plan['inherited_module_count'] != 418
                or not prior_plan['authenticated_inputs_unchanged']):
            raise RuntimeError('Parent plan is invalid or invoked compilation')
        for key in ('sources', 'dependency_order', 'public_declaration_owners',
                    'direct_inherited_imports', 'base_manifest_sha256', 'field_receipt_sha256',
                    'normalization_receipt_sha256', 'continuation_receipt_sha256', 'runner_sha256'):
            if prior_plan[key] != old[key]:
                raise RuntimeError('Changed authenticated parent closure: '+key)
        if (prior_plan['compiler']['binary_sha256'] != old['compiler']['binary_sha256']
                or {k:v['sha256'] for k,v in prior_plan['external_objects'].items()} !=
                   {k:v['sha256'] for k,v in old['external_objects'].items()}):
            raise RuntimeError('Changed parent compiler or external-object inventory')
        continuation, cb = parent.authenticate_continuation(cr, args.continuation_source_dir,
            previous, vertex, locality, verifier)
        normalization, nb = previous.authenticate_normalization(nr, focal, locality, verifier)
        inherited = previous.inherited_registry(base, core, fields)
        inherited[previous.NORMALIZATION] = dict(path=str(nb/(previous.NORMALIZATION+'.olean')),
            sha256=normalization['object_sha256'])
        for receipt, build_root in ((continuation, cb), (old, pb)):
            for row in receipt['modules']:
                name = row['module']
                if name in inherited:
                    raise RuntimeError('Parent module collides with an inherited module: '+name)
                inherited[name] = dict(path=str(build_root/(name+'.olean')), sha256=row['object_sha256'])
        if len(inherited) != 418+len(old['modules']):
            raise RuntimeError('Incomplete inherited418+parent compiled registry')
        plan = vertex.source_plan(locality, verifier, {'terminal':args.source_dir}, args.modules, inherited)
        nodes, order, external, imports, owners = plan
        if not order:
            raise RuntimeError('Empty new terminal closure')
        report.update(sources=nodes, dependency_order=order, public_declaration_owners=owners,
            direct_inherited_imports=imports, inherited_module_count=len(inherited),
            parent_module_count=len(old['modules']), inherited_objects=inherited,
            compiler=prior_plan['compiler'])
        build = out/'build'
        paths = [build, pb, *map(Path, prior_plan['lean_path'].split(os.pathsep))]
        lean_path = os.pathsep.join(map(str, paths))
        report['lean_path'] = lean_path
        tracked = {Path(v['path']):v['sha256'] for v in inherited.values()}
        tracked.update({pr/'VERIFICATION.json':args.parent_receipt_sha256,
            args.parent_verifier:PARENT_RUNNER_SHA, args.continuation_verifier:parent.RUNNER_SHA,
            args.normalization_verifier:previous.FOCAL_SHA, Path(__file__).resolve():report['runner_sha256']})
        report['external_objects'] = dict(prior_plan['external_objects'])
        for name in external:
            obj = helper.object_for(name, paths)
            if name in report['external_objects'] and sha(obj) != report['external_objects'][name]['sha256']:
                raise RuntimeError('Changed inherited external object: '+name)
            report['external_objects'][name] = dict(path=str(obj), sha256=sha(obj))
        for name, witness in {**inherited, **report['external_objects']}.items():
            obj = helper.object_for(name, paths)
            if sha(obj) != witness['sha256']:
                raise RuntimeError('Object shadows an authenticated import: '+name)
            tracked[obj] = witness['sha256']
        lean = Path(prior_plan['compiler']['executable'])
        tracked[lean] = prior_plan['compiler']['binary_sha256']
        if sha(lean) != tracked[lean]:
            raise RuntimeError('Compiler changed after the authentication plan')
        if args.plan:
            report['status'] = 'PASS_TWISTED_TERMINAL_SOURCE_PLAN_NOT_COMPILED'
        else:
            build.mkdir()
            for name in order:
                node = nodes[name]
                source = args.source_dir/node['path']
                if sha(source) != node['sha256']:
                    raise RuntimeError('Source changed before compilation: '+name)
                snapshot, obj = build/(name+'.lean'), build/(name+'.olean')
                snapshot.write_bytes(source.read_bytes())
                command = [str(lean), '-DwarningAsError=true', '--root='+str(build), '-o', str(obj), str(snapshot)]
                print(name+': compiling new terminal delta only', flush=True)
                report['compiler_invoked'] = True
                code, output = helper.run(command, base, args.timeout, env=dict(os.environ, LEAN_PATH=lean_path))
                (build/(name+'.log')).write_text(output)
                row = dict(module=name, source_sha256=node['sha256'], command=command, exit_code=code,
                    output=output, log_sha256=sha(build/(name+'.log')))
                report['modules'].append(row)
                if code or sha(source) != node['sha256'] or sha(snapshot) != node['sha256']:
                    raise RuntimeError('Compilation failed or source changed: '+name)
                row['object_sha256'] = sha(obj)
                tracked.update({source:node['sha256'], snapshot:node['sha256'],
                    obj:row['object_sha256'], build/(name+'.log'):row['log_sha256']})
            queries = [q for name in order for q in nodes[name]['public_declarations']]
            probe = ''.join('import '+name+'\n' for name in order)
            probe += ''.join('#print axioms '+q+'\n' for q in queries)
            (out/'axiom_probe.lean').write_text(probe)
            code, output = helper.run([str(lean), '--stdin'], base, args.timeout,
                env=dict(os.environ, LEAN_PATH=lean_path), stdin=probe)
            (out/'axiom_probe.log').write_text(output)
            axioms = verifier.axiom_reports(output)
            report['axiom_probe'] = dict(exit_code=code, output=output, declarations=axioms,
                source_sha256=sha(out/'axiom_probe.lean'), output_sha256=sha(out/'axiom_probe.log'))
            tracked.update({out/'axiom_probe.lean':report['axiom_probe']['source_sha256'],
                out/'axiom_probe.log':report['axiom_probe']['output_sha256']})
            if (code or len(queries) != len(set(queries)) or set(axioms) != set(queries)
                    or any(not set(a) <= ORDINARY for a in axioms.values())):
                raise RuntimeError('Incomplete terminal query or disallowed new axiom')
            report.update(status='PASS_TWISTED_TERMINAL_DELTA', public_declaration_count=len(queries),
                theorem_names=[q for name in order for q in nodes[name]['theorem_names']],
                axioms=sorted({a for values in axioms.values() for a in values}))
        focal.authenticate(base)
        previous.authenticate_normalization(nr, focal, locality, verifier)
        parent.authenticate_continuation(cr, args.continuation_source_dir, previous, vertex, locality, verifier)
        authenticate_parent(pr, args.parent_receipt_sha256, args.parent_source_dir,
            parent, vertex, locality, verifier)
        if any(sha(f) != h for f,h in tracked.items()):
            raise RuntimeError('Authenticated input changed during terminal verification')
        if vertex.source_plan(locality, verifier, {'terminal':args.source_dir}, args.modules, inherited) != plan:
            raise RuntimeError('Requested terminal closure changed')
        report['authenticated_inputs_unchanged'] = True
    except Exception as error:
        report.update(status='FAIL_TWISTED_TERMINAL_DELTA', error=str(error))
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    path = out/('PLAN.json' if args.plan else 'VERIFICATION.json')
    helper.write_json(path, report)
    print(json.dumps(dict(status=report['status'], receipt=str(path),
        compiled_modules=[r['module'] for r in report['modules']], error=report.get('error'))))
    return 0 if report['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
