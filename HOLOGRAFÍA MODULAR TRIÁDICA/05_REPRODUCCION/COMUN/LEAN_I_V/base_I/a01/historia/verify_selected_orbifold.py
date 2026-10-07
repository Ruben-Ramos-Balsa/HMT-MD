#!/usr/bin/env python3
"""Separate selected specialization with one explicitly inherited native axiom.

The ordinary two-module receipt and its complete authenticated inputs are reused.
Only SelectedOrbifoldStateFields, in its exact namespace/import scope, permits
Lean.ofReduceBool inherited from the pinned SelectedConformalVertex object.
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
ORDINARY_RECEIPT_SHA = '59491b582d884ba3ba2cc2a2e240a2f61f4e97918b5cb572e79d209b6a29eb6a'
ORDINARY_RUNNER_SHA = '43b01708c930c356a6a008ecefdb69cd050509d47739c2035e5cfa6c87224034'
SOURCE_SHA = '41eb713c7e41ecca3e0c1331bc66aa4233d3b4be3d8616494118dad331f7b146'
SELECTED_SOURCE_SHA = '3e81a26a9fbd77540b43be1353456c836b5bb6b09a43b3fdd8799d132202e720'
SELECTED_OBJECT_SHA = '537134f0a7b33632e87e6858e8a362e135027d25bc682eb294cc42c49b9bef7e'
HELPER_SHA = '145accd5aa88f203f648f4e09d3d400122d7e047195cc18b060019c6e9c825a5'
DEFAULT_HELPER = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_ARTICULO_I_20260917/even_pairing/verify_even_pairing.py')
NAME = 'SelectedOrbifoldStateFields'
NAMESPACE = 'HMT.I.'+NAME
IMPORTS = ['SelectedConformalVertex','LatticeOrbifoldFullStateFields','LatticeOrbifoldGrading']
ORDINARY = {'propext','Classical.choice','Quot.sound'}
ALLOWED = ORDINARY | {'Lean.ofReduceBool'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(test,message):
    if not test: raise RuntimeError(message)


def axioms(output):
    found = {}
    for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",output):
        require(m.group(1) not in found,'Repeated axiom query')
        found[m.group(1)] = [a.strip() for a in (m.group(2) or '').split(',') if a.strip()]
    return found


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ordinary-report-dir',type=Path,default=HERE/'resultados')
    p.add_argument('--ordinary-runner',type=Path,default=HERE/'verify_pair_product.py')
    p.add_argument('--source-dir',type=Path,default=HERE)
    p.add_argument('--helper',type=Path,default=DEFAULT_HELPER)
    p.add_argument('--report-dir',type=Path,default=HERE/'selected_results')
    p.add_argument('--relocate',action='append',default=[],metavar='OLD=NEW')
    p.add_argument('--timeout',type=int,default=300)
    p.add_argument('--plan',action='store_true')
    args = p.parse_args()
    for k,v in vars(args).items():
        if isinstance(v,Path): setattr(args,k,v.expanduser().resolve())
    mappings=[]
    for item in args.relocate:
        old,sep,new=item.partition('=')
        require(sep and old and new,'Use --relocate OLD=NEW')
        mappings.append((Path(old).resolve(),Path(new).resolve()))
    mappings.sort(key=lambda x:len(str(x[0])),reverse=True)

    def relocate(value):
        path=Path(value)
        for old,new in mappings:
            if path==old or path.is_relative_to(old): return new/path.relative_to(old)
        return path

    out=args.report_dir
    require(args.timeout>0 and not out.exists() and not args.ordinary_report_dir.is_relative_to(out)
        and not out.is_relative_to(args.ordinary_report_dir) and not args.source_dir.is_relative_to(out),
        'Use a fresh specialization report outside protected inputs')
    out.mkdir(parents=True,exist_ok=False)
    started,tracked=time.monotonic(),{}
    report=dict(status='RUNNING_SELECTED_ORBIFOLD_SPECIALIZATION',ordinary_receipt_sha256=ORDINARY_RECEIPT_SHA,
        runner_sha256=sha(__file__),source_sha256=SOURCE_SHA,modules=[],compiler_invoked=False,
        inherited_modules_recompiled=False,mathlib_rebuilt=False,sealed_461_modified=False,
        axiom_policy=dict(module=NAME,namespace=NAMESPACE,imports=IMPORTS,allowed_axioms=sorted(ALLOWED),
            inherited_native_exception='Lean.ofReduceBool',native_decide_in_new_source_allowed=False,
            inherited_owner='SelectedConformalVertex',inherited_source_sha256=SELECTED_SOURCE_SHA,
            inherited_object_sha256=SELECTED_OBJECT_SHA),
        scope='Specialization of the four concrete products to the unchanged selectedOrigin; '
            'separate from the ordinary-only generic receipt. No global Jacobi/locality or Monster claim.')

    def save(): (out/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')

    def track(path,digest):
        path=Path(path).resolve()
        require(path not in tracked or tracked[path]==digest,'Conflicting expected hash')
        require(sha(path)==digest,'Changed input: '+str(path))
        tracked[path]=digest
        return path

    save()
    try:
        track(__file__,report['runner_sha256'])
        track(args.ordinary_runner,ORDINARY_RUNNER_SHA)
        receipt=track(args.ordinary_report_dir/'VERIFICATION.json',ORDINARY_RECEIPT_SHA)
        prior=json.loads(receipt.read_text())
        require(prior['status']=='PASS_TWISTED_PAIR_PRODUCT' and prior['authenticated_inputs_unchanged']
            and not prior['inherited_modules_recompiled'] and not prior['mathlib_rebuilt']
            and prior['runner_sha256']==ORDINARY_RUNNER_SHA,'Invalid ordinary receipt')
        for path,digest in prior['authenticated_artifacts'].items(): track(relocate(path),digest)
        track(args.helper,HELPER_SHA)
        spec=importlib.util.spec_from_file_location('selected_orbifold_inspector',args.helper)
        helper=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        registry={n:dict(path=str(relocate(v['path'])),sha256=v['sha256']) for n,v in prior['inherited_objects'].items()}
        for row in prior['modules']:
            name=row['module']; build=args.ordinary_report_dir/'build'
            require(row['exit_code']==0 and name not in registry,'Invalid ordinary module')
            track(build/(name+'.lean'),row['source_sha256'])
            log=track(build/(name+'.log'),row['log_sha256'])
            require(log.read_text()==row['output'],'Ordinary compile transcript changed')
            obj=track(build/(name+'.olean'),row['object_sha256'])
            registry[name]=dict(path=str(obj),sha256=row['object_sha256'])
        require(len(registry)==476,'Expected 476 ordinary modules before selection')
        ap=prior['axiom_probe']; names=list(prior['public_declaration_owners'])
        require(ap['exit_code']==0,'Ordinary axiom probe failed')
        ps=track(args.ordinary_report_dir/'axiom_probe.lean',ap['source_sha256'])
        pl=track(args.ordinary_report_dir/'axiom_probe.log',ap['output_sha256'])
        require(ps.read_text()==''.join('import '+n+'\n' for n in prior['dependency_order'])+
            ''.join('#print axioms '+n+'\n' for n in names) and pl.read_text()==ap['output'],
            'Ordinary public probe changed')
        ordinary_found=axioms(pl.read_text())
        require(set(ordinary_found)==set(names) and ordinary_found==prior['axioms']
            and all(set(v)<=ORDINARY for v in ordinary_found.values()),'Ordinary axiom policy changed')
        witness=registry['SelectedConformalVertex']
        require(witness['sha256']==SELECTED_OBJECT_SHA,'Selected owner object changed')
        owner_source=Path(witness['path']).with_suffix('.lean')
        track(owner_source,SELECTED_SOURCE_SHA)
        report['inherited_selected_owner']=dict(source=str(owner_source),source_sha256=SELECTED_SOURCE_SHA,**witness)
        build=out/'build'
        paths=list(dict.fromkeys([build,args.ordinary_report_dir/'build',
            *(relocate(v) for v in prior['lean_path'].split(os.pathsep))]))
        resolved={n:dict(path=str(relocate(v['path'])),sha256=v['sha256']) for n,v in prior['resolved_objects'].items()}
        for n,w in {**resolved,**registry}.items():
            obj=helper.resolve_object(n,paths)
            track(obj,w['sha256'])
            resolved[n]=dict(path=str(obj),sha256=w['sha256'])
        source=track(args.source_dir/(NAME+'.lean'),SOURCE_SHA)
        body=source.read_text(); clean=helper.without_comments(body)
        require(re.findall(r'^\s*namespace\s+(\S+)',clean,re.M)==[NAMESPACE]
            and re.findall(r'^import\s+(\S+)',clean,re.M)==IMPORTS,'Selected namespace/import boundary changed')
        require(not re.search(r'\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by|run_elab|run_cmd|elab|macro|syntax|initialize|instance|structure|class|inductive|opaque|mutual|constant)\b',clean),
            'Forbidden command in selected consumer')
        publics=[NAMESPACE+'.'+n for n in helper.DECL.findall(clean)]
        require(len(publics)==6 and len(set(publics))==6,'Expected exactly six selected public declarations')
        theorems=[NAMESPACE+'.'+n for n in re.findall(r'^\s*(?:theorem|lemma)\s+([\w\x27]+)',clean,re.M)]
        compiler=dict(prior['compiler']); lean=relocate(compiler['executable'])
        track(lean,compiler['binary_sha256']); compiler['executable']=str(lean)
        report.update(compiler=compiler,inherited_module_count=len(registry),inherited_objects=registry,
            resolved_objects=resolved,public_declarations=publics,public_declaration_count=len(publics),
            theorem_names=theorems,lean_path=os.pathsep.join(map(str,paths)))
        env=dict(os.environ,LEAN_PATH=report['lean_path'])
        if not args.plan:
            build.mkdir()
            snapshot,obj,log=build/(NAME+'.lean'),build/(NAME+'.olean'),build/(NAME+'.log')
            snapshot.write_text(body)
            cmd=[str(lean),'-DwarningAsError=true','--root='+str(build),'-o',str(obj),str(snapshot)]
            report['compiler_invoked']=True
            proc=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=args.timeout)
            log.write_text(proc.stdout+proc.stderr)
            row=dict(module=NAME,source_sha256=SOURCE_SHA,command=cmd,exit_code=proc.returncode,
                log_sha256=sha(log),output=log.read_text())
            report['modules'].append(row); save()
            require(proc.returncode==0,'Selected consumer compilation failed')
            row['object_sha256']=sha(obj); track(obj,row['object_sha256']); track(snapshot,SOURCE_SHA)
            ps,pl=out/'axiom_probe.lean',out/'axiom_probe.log'
            ps.write_text('import '+NAME+'\n'+''.join('#print axioms '+d+'\n' for d in publics))
            cmd=[str(lean),'-DwarningAsError=true',str(ps)]
            proc=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=args.timeout)
            pl.write_text(proc.stdout+proc.stderr)
            report['axiom_probe']=dict(command=cmd,exit_code=proc.returncode,source_sha256=sha(ps),
                output_sha256=sha(pl),output=pl.read_text()); save()
            require(proc.returncode==0,'Selected public probe failed')
            found=axioms(pl.read_text())
            require(set(found)==set(publics) and all(set(a)<=ALLOWED for a in found.values()),
                'Selected axiom inventory exceeds the explicit inherited exception')
            report['axioms']=found; report['axiom_probe']['declarations']=found
        helper.unchanged({str(p):h for p,h in tracked.items()})
        report.update(status='PASS_SELECTED_ORBIFOLD_SOURCE_PLAN_NOT_COMPILED' if args.plan else
            'PASS_SELECTED_ORBIFOLD_SPECIALIZATION',authenticated_inputs_unchanged=True,
            authenticated_artifacts={str(p):h for p,h in tracked.items()},elapsed_seconds=round(time.monotonic()-started,3))
        save(); print(report['status'],len(publics),'public declarations;',len(theorems),'theorems',flush=True)
    except Exception as error:
        report.update(status='FAIL_SELECTED_ORBIFOLD_SPECIALIZATION',error=str(error),
            elapsed_seconds=round(time.monotonic()-started,3)); save(); raise


if __name__=='__main__': main()
