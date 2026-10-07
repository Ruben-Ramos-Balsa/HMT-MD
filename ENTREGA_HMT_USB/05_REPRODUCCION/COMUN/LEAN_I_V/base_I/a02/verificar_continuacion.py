#!/usr/bin/env python3
"""Compile a requested new closure on portable fields406 plus normalization407.

Reuse the frozen portable verifier for package integrity and its --plan for
antecedent source/runtime authentication. Authenticate normalization from its
pinned receipt, snapshot, object and complete axiom transcript; never rebuild it.
Compile only the explicit delta closure and query every public declaration in a
separate generated probe, whether or not sources contain their own #print lines.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FOCAL_SHA = '34bdc13bb338c8f5d873c3677ea941fb5bbe7353c97bf314ef8841e781ddb97b'
NORMALIZATION_SHA = 'b5d5227a511f9683da3fd2d4df978c50e90d824233ab96dcf815a9b0ccda6e81'
NORMALIZATION = 'LatticeTwistedChargeNormalization'
TF_SHA = 'f3363670657b5bf030edf6d193ebadb2c6e822d77fcdcffb8044090feccf9906'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path, expected, name):
    if sha(path) != expected:
        raise RuntimeError('Changed authenticated helper: '+str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authenticate_normalization(root, focal, locality, verifier):
    receipt = root/'VERIFICATION.json'
    if sha(receipt) != NORMALIZATION_SHA:
        raise RuntimeError('Changed normalization receipt')
    r = json.loads(receipt.read_text())
    if (r['status'] != 'PASS_CHARGE_NORMALIZATION_DELTA' or r['runner_sha256'] != FOCAL_SHA
            or r['base_manifest_sha256'] != focal.MANIFEST_SHA
            or r['predecessor_receipt_sha256'] != focal.RECEIPT_SHA
            or r['exit_code'] or not r['authenticated_inputs_unchanged']
            or r['predecessors_modified'] or r['predecessors_recompiled'] or r['mathlib_rebuilt']):
        raise RuntimeError('Invalid normalization predecessor')
    build = root/'build'; source = build/(NORMALIZATION+'.lean')
    if ({p.stem for p in build.glob('*.olean')} != {NORMALIZATION}
            or sha(source) != r['source_sha256'] or sha(source) != focal.SOURCE_SHA
            or sha(build/(NORMALIZATION+'.olean')) != r['object_sha256']
            or sha(root/'compile.log') != r['log_sha256']
            or (root/'compile.log').read_text() != r['output']):
        raise RuntimeError('Changed normalization snapshot, object or log')
    node = locality.inspect(verifier, source)
    for key in ('imports', 'namespace', 'public_declarations', 'theorem_names'):
        if node[key] != r['source'][key]:
            raise RuntimeError('Changed normalization public inventory: '+key)
    axioms = verifier.axiom_reports(r['output'])
    if (axioms != r['axiom_queries'] or set(axioms) != set(node['public_declarations'])
            or any(not set(a) <= ORDINARY for a in axioms.values())):
        raise RuntimeError('Incomplete normalization axiom transcript')
    return r, build


def inherited_registry(base, core, field_receipt):
    """Exact compiled module registries from receipts already checked by --plan."""
    vertex = base/'antecedente/antecedente/antecedente'
    paths = [base/'antecedente/recibos/incremento',
        base/'antecedente/antecedente/recibos/incremento', vertex/'recibos/productos',
        vertex/'recibos/conforme', vertex/'recibos/involucion',
        vertex/'antecedente/recibos/traslacion',
        vertex/'antecedente/antecedente/recibos/localidad_estados',
        vertex/'antecedente/antecedente/recibos/localidad_generadores',
        vertex/'antecedente/antecedente/antecedente/recibos/coherencia']
    pairs = [(field_receipt, base/'recibos/incremento/build')]
    pairs += [(json.loads((p/'VERIFICATION.json').read_text()), p/'build') for p in paths]
    pairs += [(json.loads((core/'recibos/covariancia_firma/LEAN_CONJUNTO.json').read_text()),
               core/'resultados/lean_unificado/build')]
    records = {}
    for receipt, build in pairs:
        for row in receipt['modules']:
            name = row['module']; obj = build/(name+'.olean')
            if name in records or row['exit_code'] or sha(obj) != row['object_sha256']:
                raise RuntimeError('Conflicting or changed inherited object: '+name)
            records[name] = dict(path=str(obj), sha256=row['object_sha256'])
    if len(records) != 406:
        raise RuntimeError('Expected the exact 406-module inherited registry')
    return records


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--normalization-report-dir', type=Path, default=HERE/'normalization_results_20260922')
    p.add_argument('--normalization-verifier', type=Path, default=HERE/'verify_charge_normalization.py')
    p.add_argument('--source-dir', type=Path, default=HERE)
    p.add_argument('--modules', nargs='+', required=True)
    p.add_argument('--report-dir', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=900)
    p.add_argument('--plan', action='store_true')
    args = p.parse_args()
    for key in ('base', 'normalization_report_dir', 'normalization_verifier', 'source_dir', 'report_dir'):
        setattr(args, key, getattr(args, key).resolve())
    base, nr, out = args.base, args.normalization_report_dir, args.report_dir
    if (out.exists() or any(out.is_relative_to(x) or x.is_relative_to(out) for x in (base,nr))
            or args.source_dir.is_relative_to(out) or args.normalization_verifier.is_relative_to(out)):
        raise RuntimeError('Use a fresh report, outside protected inputs')
    focal = load(args.normalization_verifier, FOCAL_SHA, 'continuation_normalization')
    fields = focal.authenticate(base)
    tf = load(base/'verificar_campos_torcidos.py', TF_SHA, 'continuation_fields')
    vertex_root = base/'antecedente/antecedente/antecedente'
    helper = load(vertex_root/'antecedente/antecedente/antecedente/verificar_delta.py',
        'f022db4decca339ed0873c08508b9a9a93b66a9ce711a3785526896870219939', 'continuation_helper')
    locality = load(vertex_root/'antecedente/antecedente/verificar_localidad.py',
        'c16c63bfe0f9c95f7a5e767e8f8be5b1f67524496259f1618f9fe1043ece82a3', 'continuation_inventory')
    vertex = load(vertex_root/'verificar_conforme.py',
        'a1a4d7f2a419403961cf8df6494c0d56393d7fa884a4be3a52d543a422ad396d', 'continuation_planner')
    out.mkdir(parents=True)
    report = dict(status='RUNNING', started_at_utc=datetime.now(timezone.utc).isoformat(),
        runner_sha256=sha(__file__), requested_modules=args.modules, source_dir=str(args.source_dir),
        base=str(base), base_manifest_sha256=focal.MANIFEST_SHA,
        field_receipt_sha256=focal.RECEIPT_SHA, normalization_receipt_sha256=NORMALIZATION_SHA,
        normalization_verifier_sha256=FOCAL_SHA, predecessors_modified=False,
        predecessors_recompiled=False, mathlib_rebuilt=False, compiler_invoked=False, modules=[])
    try:
        command = [sys.executable, '-I', '-S', str(base/'reproducir.py'), '--plan', '--report-dir', str(out/'antecedent_plan')]
        code, output = helper.run(command, base, args.timeout)
        (out/'antecedent_plan.log').write_text(output)
        report['antecedent_plan'] = dict(command=command, exit_code=code, output=output)
        if code:
            raise RuntimeError('Antecedent authentication plan failed')
        oldplan = json.loads((out/'antecedent_plan/PLAN.json').read_text())
        if (oldplan['status'] != 'PASS_TWISTED_FIELDS_SOURCE_PLAN_NOT_COMPILED'
                or oldplan['compiler_invoked'] or oldplan['modules'] or not oldplan['authenticated_inputs_unchanged']):
            raise RuntimeError('Antecedent plan failed or invoked compiler')
        for key in ('sources', 'dependency_order', 'public_declaration_owners', 'predecessor_receipt_sha256'):
            if fields[key] != oldplan[key]:
                raise RuntimeError('Changed inherited field source closure: '+key)
        core = Path(oldplan['base'])
        verifier = load(core/'verificar_lean.py', helper.BASE_VERIFIER_SHA, 'continuation_parser')
        vertex.check_probe(verifier, fields, fields['public_declaration_owners'])
        normalization, nb = authenticate_normalization(nr, focal, locality, verifier)
        inherited = inherited_registry(base, core, fields)
        inherited[NORMALIZATION] = dict(path=str(nb/(NORMALIZATION+'.olean')), sha256=normalization['object_sha256'])
        plan = vertex.source_plan(locality, verifier, {'continuation':args.source_dir}, args.modules, inherited)
        nodes, order, external, old_imports, owners = plan
        if not order:
            raise RuntimeError('Empty delta closure')
        report.update(sources=nodes, dependency_order=order, public_declaration_owners=owners,
            direct_inherited_imports=old_imports, inherited_module_count=len(inherited), compiler=oldplan['compiler'])
        build = out/'build'
        paths = [build, nb, base/'recibos/incremento/build', *map(Path, oldplan['lean_path'].split(os.pathsep))]
        lean_path = os.pathsep.join(map(str, paths)); report['lean_path'] = lean_path
        tracked = {Path(v['path']):v['sha256'] for v in inherited.values()}
        report['external_objects'] = dict(oldplan['external_objects'])
        for name in external:
            obj = helper.object_for(name, paths)
            if name in report['external_objects'] and sha(obj) != report['external_objects'][name]['sha256']:
                raise RuntimeError('Inherited external object changed: '+name)
            report['external_objects'][name] = dict(path=str(obj), sha256=sha(obj))
        for name, witness in {**inherited, **report['external_objects']}.items():
            obj = helper.object_for(name, paths)
            if sha(obj) != witness['sha256']:
                raise RuntimeError('An object shadows authenticated import: '+name)
            tracked[obj] = witness['sha256']
        lean = Path(oldplan['compiler']['executable']); tracked[lean] = oldplan['compiler']['binary_sha256']
        if args.plan:
            report['status'] = 'PASS_TWISTED_CONTINUATION_SOURCE_PLAN_NOT_COMPILED'
        else:
            build.mkdir()
            for name in order:
                node = nodes[name]; source = args.source_dir/node['path']
                if sha(source) != node['sha256']:
                    raise RuntimeError('Source changed before compilation: '+name)
                snapshot, obj = build/(name+'.lean'), build/(name+'.olean')
                snapshot.write_bytes(source.read_bytes())
                command = [str(lean), '-DwarningAsError=true', '--root='+str(build), '-o', str(obj), str(snapshot)]
                print(name+': compiling new continuation only', flush=True)
                report['compiler_invoked'] = True
                code, output = helper.run(command, base, args.timeout, env=dict(os.environ, LEAN_PATH=lean_path))
                (build/(name+'.log')).write_text(output)
                row = dict(module=name, source_sha256=node['sha256'], command=command,
                    exit_code=code, output=output, log_sha256=sha(build/(name+'.log')))
                report['modules'].append(row)
                if code or sha(source) != node['sha256'] or sha(snapshot) != node['sha256']:
                    raise RuntimeError('Compilation failed or source changed: '+name)
                row['object_sha256'] = sha(obj)
                tracked.update({source:node['sha256'], snapshot:node['sha256'], obj:row['object_sha256'],
                    build/(name+'.log'):row['log_sha256']})
            queries = [q for name in order for q in nodes[name]['public_declarations']]
            probe = ''.join('import '+name+'\n' for name in order)+''.join('#print axioms '+q+'\n' for q in queries)
            (out/'axiom_probe.lean').write_text(probe)
            code, output = helper.run([str(lean), '--stdin'], base, args.timeout,
                env=dict(os.environ, LEAN_PATH=lean_path), stdin=probe)
            (out/'axiom_probe.log').write_text(output); axioms = verifier.axiom_reports(output)
            report['axiom_probe'] = dict(exit_code=code, output=output, declarations=axioms,
                source_sha256=sha(out/'axiom_probe.lean'), output_sha256=sha(out/'axiom_probe.log'))
            if code or set(axioms) != set(queries) or any(not set(a) <= ORDINARY for a in axioms.values()):
                raise RuntimeError('Incomplete public query or disallowed new axiom')
            report.update(status='PASS_TWISTED_CONTINUATION_DELTA', public_declaration_count=len(queries),
                theorem_names=[q for name in order for q in nodes[name]['theorem_names']],
                axioms=sorted({a for values in axioms.values() for a in values}))
        focal.authenticate(base); authenticate_normalization(nr, focal, locality, verifier)
        if any(sha(f) != h for f,h in tracked.items()):
            raise RuntimeError('Authenticated input changed during continuation')
        if vertex.source_plan(locality, verifier, {'continuation':args.source_dir}, args.modules, inherited) != plan:
            raise RuntimeError('Selected delta closure changed')
        report['authenticated_inputs_unchanged'] = True
    except Exception as error:
        report.update(status='FAIL_TWISTED_CONTINUATION_DELTA', error=str(error))
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    path = out/('PLAN.json' if args.plan else 'VERIFICATION.json')
    helper.write_json(path, report)
    print(json.dumps(dict(status=report['status'], receipt=str(path),
        compiled_modules=[m['module'] for m in report['modules']], error=report.get('error'))))
    return 0 if report['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
