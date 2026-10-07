#!/usr/bin/env python3
"""Verify only descendants after fields406 + normalization407 + continuation418.

The pinned continuation verifier authenticates its antecedents with --plan.
Its eleven compiled modules, snapshots, logs and complete public axiom probe
are then reused. Only the requested new source closure is compiled and queried.
No predecessor verifier, source, receipt or object is modified or rebuilt.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CONTINUATION_SHA = 'ad69d93c9775446c6528d0eb531f91983b783c0d5a91750eb02f5a5299a9145d'
RUNNER_SHA = '288b259509c86ef7f89c120ae4daaabef38598fa220be4dfca0fc07c3198d98d'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path, expected, name):
    if sha(path) != expected:
        raise RuntimeError('Changed authenticated helper: '+str(path))
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def authenticate_continuation(root, source_root, previous, vertex, locality, verifier):
    receipt = root/'VERIFICATION.json'
    if sha(receipt) != CONTINUATION_SHA:
        raise RuntimeError('Changed sealed continuation receipt')
    r = json.loads(receipt.read_text())
    if (r['status'] != 'PASS_TWISTED_CONTINUATION_DELTA' or r['runner_sha256'] != RUNNER_SHA
            or r['normalization_receipt_sha256'] != previous.NORMALIZATION_SHA
            or r['inherited_module_count'] != 407 or not r['authenticated_inputs_unchanged']
            or r['predecessors_modified'] or r['predecessors_recompiled'] or r['mathlib_rebuilt']):
        raise RuntimeError('Incompatible continuation predecessor')
    rows = {row['module']:row for row in r['modules']}
    build = root/'build'
    if (len(rows) != 11 or len(rows) != len(r['modules']) or set(rows) != set(r['sources'])
            or {p.stem for p in build.glob('*.olean')} != set(rows)):
        raise RuntimeError('Expected exact eleven-module compiled continuation')
    for name,node in r['sources'].items():
        row = rows[name]; source = source_root/node['path']
        if node['path'] != name+'.lean' or node['root'] != 'continuation':
            raise RuntimeError('Unexpected continuation source locator')
        inspected = locality.inspect(verifier,source)
        if (row['exit_code'] or row['source_sha256'] != node['sha256']
                or sha(source) != node['sha256'] or sha(build/(name+'.lean')) != node['sha256']
                or sha(build/(name+'.olean')) != row['object_sha256']
                or sha(build/(name+'.log')) != row['log_sha256']
                or (build/(name+'.log')).read_text() != row['output']
                or any(inspected[k] != node[k] for k in ('imports','namespace','public_declarations','theorem_names'))):
            raise RuntimeError('Changed continuation source, object, log or inventory: '+name)
    vertex.check_probe(verifier,r,r['public_declaration_owners'])
    queries = [q for m in r['dependency_order'] for q in r['sources'][m]['public_declarations']]
    expected = ''.join('import '+m+'\n' for m in r['dependency_order'])+''.join('#print axioms '+q+'\n' for q in queries)
    if (r['public_declaration_count'] != len(queries) or (root/'axiom_probe.lean').read_text() != expected
            or sha(root/'axiom_probe.lean') != r['axiom_probe']['source_sha256']
            or sha(root/'axiom_probe.log') != r['axiom_probe']['output_sha256']
            or (root/'axiom_probe.log').read_text() != r['axiom_probe']['output']):
        raise RuntimeError('Changed continuation public axiom probe')
    return r,build


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base',type=Path,required=True)
    p.add_argument('--normalization-report-dir',type=Path,default=HERE/'normalization_results_20260922')
    p.add_argument('--normalization-verifier',type=Path,default=HERE/'verify_charge_normalization.py')
    p.add_argument('--continuation-report-dir',type=Path,default=HERE/'continuation_results_20260922')
    p.add_argument('--continuation-verifier',type=Path,default=HERE/'verify_twisted_continuation.py')
    p.add_argument('--continuation-source-dir',type=Path,default=HERE)
    p.add_argument('--source-dir',type=Path,default=HERE)
    p.add_argument('--modules',nargs='+',required=True)
    p.add_argument('--report-dir',type=Path,required=True)
    p.add_argument('--timeout',type=int,default=900)
    p.add_argument('--plan',action='store_true')
    args = p.parse_args()
    for key,value in vars(args).items():
        if isinstance(value,Path):
            setattr(args,key,value.resolve())
    base,nr,cr,out = args.base,args.normalization_report_dir,args.continuation_report_dir,args.report_dir
    if (out.exists() or any(out.is_relative_to(x) or x.is_relative_to(out) for x in (base,nr,cr))
            or any(x.is_relative_to(out) for x in (args.source_dir,args.continuation_source_dir,
                args.normalization_verifier,args.continuation_verifier))):
        raise RuntimeError('Use a fresh report outside protected inputs')
    previous = load(args.continuation_verifier,RUNNER_SHA,'descendants_previous')
    focal = previous.load(args.normalization_verifier,previous.FOCAL_SHA,'descendants_focal')
    fields = focal.authenticate(base)
    if sha(cr/'VERIFICATION.json') != CONTINUATION_SHA:
        raise RuntimeError('Changed continuation receipt')
    old = json.loads((cr/'VERIFICATION.json').read_text())
    vertex_root = base/'antecedente/antecedente/antecedente'
    helper = previous.load(vertex_root/'antecedente/antecedente/antecedente/verificar_delta.py',
        'f022db4decca339ed0873c08508b9a9a93b66a9ce711a3785526896870219939','descendants_helper')
    locality = previous.load(vertex_root/'antecedente/antecedente/verificar_localidad.py',
        'c16c63bfe0f9c95f7a5e767e8f8be5b1f67524496259f1618f9fe1043ece82a3','descendants_inventory')
    vertex = previous.load(vertex_root/'verificar_conforme.py',
        'a1a4d7f2a419403961cf8df6494c0d56393d7fa884a4be3a52d543a422ad396d','descendants_planner')
    core = vertex_root/'antecedente/antecedente/antecedente/antecedente/antecedente'
    verifier = previous.load(core/'verificar_lean.py',helper.BASE_VERIFIER_SHA,'descendants_parser')
    out.mkdir(parents=True)
    report = dict(status='RUNNING',started_at_utc=datetime.now(timezone.utc).isoformat(),runner_sha256=sha(__file__),
        base=str(base),base_manifest_sha256=focal.MANIFEST_SHA,field_receipt_sha256=focal.RECEIPT_SHA,
        normalization_receipt_sha256=previous.NORMALIZATION_SHA,continuation_receipt_sha256=CONTINUATION_SHA,
        requested_modules=args.modules,source_dir=str(args.source_dir),predecessors_modified=False,
        predecessors_recompiled=False,mathlib_rebuilt=False,compiler_invoked=False,modules=[])
    try:
        command = [sys.executable,'-I','-S',str(args.continuation_verifier),'--base',str(base),
            '--normalization-report-dir',str(nr),'--normalization-verifier',str(args.normalization_verifier),
            '--source-dir',str(args.continuation_source_dir),'--modules',*old['requested_modules'],
            '--plan','--report-dir',str(out/'antecedent_plan')]
        code,output = helper.run(command,base,args.timeout)
        (out/'antecedent_plan.log').write_text(output)
        report['antecedent_plan'] = dict(command=command,exit_code=code,output=output)
        if code:
            raise RuntimeError('Antecedent continuation plan failed')
        prior_plan = json.loads((out/'antecedent_plan/PLAN.json').read_text())
        if (prior_plan['status'] != 'PASS_TWISTED_CONTINUATION_SOURCE_PLAN_NOT_COMPILED'
                or prior_plan['compiler_invoked'] or prior_plan['modules'] or not prior_plan['authenticated_inputs_unchanged']):
            raise RuntimeError('Antecedent plan failed or recompiled a module')
        for key in ('sources','dependency_order','public_declaration_owners','direct_inherited_imports'):
            if prior_plan[key] != old[key]:
                raise RuntimeError('Changed continuation closure: '+key)
        old,cb = authenticate_continuation(cr,args.continuation_source_dir,previous,vertex,locality,verifier)
        normalization,nb = previous.authenticate_normalization(nr,focal,locality,verifier)
        inherited = previous.inherited_registry(base,core,fields)
        inherited[previous.NORMALIZATION] = dict(path=str(nb/(previous.NORMALIZATION+'.olean')),sha256=normalization['object_sha256'])
        inherited.update({r['module']:dict(path=str(cb/(r['module']+'.olean')),sha256=r['object_sha256']) for r in old['modules']})
        if len(inherited) != 418:
            raise RuntimeError('Expected exactly 418 authenticated predecessors')
        plan = vertex.source_plan(locality,verifier,{'descendants':args.source_dir},args.modules,inherited)
        nodes,order,external,imports,owners = plan
        if not order:
            raise RuntimeError('Empty new descendant closure')
        report.update(sources=nodes,dependency_order=order,public_declaration_owners=owners,
            direct_inherited_imports=imports,inherited_module_count=len(inherited),compiler=prior_plan['compiler'])
        build = out/'build'; paths = [build,cb,*map(Path,prior_plan['lean_path'].split(os.pathsep))]
        lean_path = os.pathsep.join(map(str,paths)); report['lean_path'] = lean_path
        tracked = {Path(v['path']):v['sha256'] for v in inherited.values()}
        report['external_objects'] = dict(prior_plan['external_objects'])
        for name in external:
            obj = helper.object_for(name,paths)
            if name in report['external_objects'] and sha(obj) != report['external_objects'][name]['sha256']:
                raise RuntimeError('Changed inherited external object: '+name)
            report['external_objects'][name] = dict(path=str(obj),sha256=sha(obj))
        for name,witness in {**inherited,**report['external_objects']}.items():
            obj = helper.object_for(name,paths)
            if sha(obj) != witness['sha256']:
                raise RuntimeError('Object shadows verified import: '+name)
            tracked[obj] = witness['sha256']
        lean = Path(prior_plan['compiler']['executable']); tracked[lean] = prior_plan['compiler']['binary_sha256']
        if args.plan:
            report['status'] = 'PASS_TWISTED_DESCENDANTS_SOURCE_PLAN_NOT_COMPILED'
        else:
            build.mkdir()
            for name in order:
                node = nodes[name]; source = args.source_dir/node['path']
                if sha(source) != node['sha256']:
                    raise RuntimeError('Source changed before compilation: '+name)
                snapshot,obj = build/(name+'.lean'),build/(name+'.olean'); snapshot.write_bytes(source.read_bytes())
                command = [str(lean),'-DwarningAsError=true','--root='+str(build),'-o',str(obj),str(snapshot)]
                print(name+': compiling new descendants only',flush=True); report['compiler_invoked'] = True
                code,output = helper.run(command,base,args.timeout,env=dict(os.environ,LEAN_PATH=lean_path))
                (build/(name+'.log')).write_text(output)
                row = dict(module=name,source_sha256=node['sha256'],command=command,exit_code=code,
                    output=output,log_sha256=sha(build/(name+'.log'))); report['modules'].append(row)
                if code or sha(source) != node['sha256'] or sha(snapshot) != node['sha256']:
                    raise RuntimeError('Compilation failed or source changed: '+name)
                row['object_sha256'] = sha(obj)
                tracked.update({source:node['sha256'],snapshot:node['sha256'],obj:row['object_sha256'],build/(name+'.log'):row['log_sha256']})
            queries = [q for name in order for q in nodes[name]['public_declarations']]
            probe = ''.join('import '+name+'\n' for name in order)+''.join('#print axioms '+q+'\n' for q in queries)
            (out/'axiom_probe.lean').write_text(probe)
            code,output = helper.run([str(lean),'--stdin'],base,args.timeout,env=dict(os.environ,LEAN_PATH=lean_path),stdin=probe)
            (out/'axiom_probe.log').write_text(output); axioms = verifier.axiom_reports(output)
            report['axiom_probe'] = dict(exit_code=code,output=output,declarations=axioms,
                source_sha256=sha(out/'axiom_probe.lean'),output_sha256=sha(out/'axiom_probe.log'))
            if code or set(axioms) != set(queries) or any(not set(a) <= ORDINARY for a in axioms.values()):
                raise RuntimeError('Incomplete descendant query or disallowed new axiom')
            report.update(status='PASS_TWISTED_DESCENDANTS_DELTA',public_declaration_count=len(queries),
                theorem_names=[q for name in order for q in nodes[name]['theorem_names']],
                axioms=sorted({a for values in axioms.values() for a in values}))
        focal.authenticate(base); previous.authenticate_normalization(nr,focal,locality,verifier)
        authenticate_continuation(cr,args.continuation_source_dir,previous,vertex,locality,verifier)
        if any(sha(f) != h for f,h in tracked.items()):
            raise RuntimeError('Authenticated input changed during descendant verification')
        if vertex.source_plan(locality,verifier,{'descendants':args.source_dir},args.modules,inherited) != plan:
            raise RuntimeError('Requested descendant closure changed')
        report['authenticated_inputs_unchanged'] = True
    except Exception as error:
        report.update(status='FAIL_TWISTED_DESCENDANTS_DELTA',error=str(error))
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    path = out/('PLAN.json' if args.plan else 'VERIFICATION.json'); helper.write_json(path,report)
    print(json.dumps(dict(status=report['status'],receipt=str(path),compiled_modules=[r['module'] for r in report['modules']],error=report.get('error'))))
    return 0 if report['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
