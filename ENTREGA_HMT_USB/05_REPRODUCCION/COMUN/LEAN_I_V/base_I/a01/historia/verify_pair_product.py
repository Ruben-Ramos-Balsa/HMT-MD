#!/usr/bin/env python3
"""Authenticate restricted-dual and weight-support receipts; compile only two consumers.

The frozen reconstruction runner is called only with --plan. All predecessor
objects and probes are authenticated and reused. A fresh output is mandatory.
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
RESTRICTED_ROOT = PROJECT/'output/ARTICLE_I_RESTRICTED_DUAL_RECONSTRUCTION_20260922'
SUPPORT_ROOT = PROJECT/'output/ARTICLE_I_CONTRAGREDIENT_WEIGHT_SUPPORT_20260922'
RESTRICTED_SHA = '9a4bf6186475376a3f6330e5fa673c3c9780abf80b027f2116852a82ec2a13f3'
RESTRICTED_RUNNER_SHA = '371c854ed5b2f077f5f9325f0fdbb34b041a74c60444aba4187f7af8e32850bb'
SUPPORT_SHA = 'cf6aba0dff4a8e524a18abd629e7804e10efd505a6d5746efaf30e67b9b72e73'
SUPPORT_RUNNER_SHA = 'ab3a4bf64a0dfbae841dc64b15514e760893c60944c9328b54dd60699887b9ec'
SOURCES = {
    'LatticeTwistedPairProduct': 'bfa1ab60591cad5b4701899b0b619ba6526482ddcc57dd163741501f8a0fb57c',
    'LatticeOrbifoldFullStateFields': '58e63dc8a0104011a01aeae63d7be4ff5ce1fc68371f9e7d140d594fa65ce23c',
}
SUPPORT_NAMES = ['LatticeTwistedNormalEnergy', 'LatticeTwistedRawEnergy',
    'LatticeTwistedCorrectedEnergy', 'SkewFieldEnergy', 'LatticeTwistedPairingEnergy',
    'LatticeTwistedFullEnergy', 'LatticeContragredientWeightSupport']
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--restricted-root', type=Path, default=RESTRICTED_ROOT)
    p.add_argument('--restricted-report-dir', type=Path)
    p.add_argument('--support-root', type=Path, default=SUPPORT_ROOT)
    p.add_argument('--source-dir', type=Path, default=HERE)
    p.add_argument('--report-dir', type=Path, default=HERE/'resultados')
    for flag in ('even-root', 'terminal-report-dir', 'helper', 'lean'):
        p.add_argument('--'+flag, type=Path)
    p.add_argument('--relocate', action='append', default=[], metavar='OLD=NEW')
    p.add_argument('--timeout', type=int, default=300)
    p.add_argument('--plan', action='store_true')
    args = p.parse_args()
    for key,value in vars(args).items():
        if isinstance(value,Path): setattr(args,key,value.expanduser().resolve())
    args.restricted_report_dir = args.restricted_report_dir or args.restricted_root/'resultados_02'
    require(args.timeout > 0, 'Positive timeout required')
    roots = [(RESTRICTED_ROOT,args.restricted_root),(SUPPORT_ROOT,args.support_root)]
    for mapping in args.relocate:
        old,sep,new = mapping.partition('=')
        require(sep and old and new, 'Use --relocate OLD=NEW')
        roots.append((Path(old).expanduser().resolve(),Path(new).expanduser().resolve()))
    roots.sort(key=lambda pair:len(str(pair[0])),reverse=True)

    def relocate(value):
        path = Path(value)
        for old,new in roots:
            if path == old or path.is_relative_to(old): return new/path.relative_to(old)
        return path

    out = args.report_dir
    protected = [args.restricted_root,args.restricted_report_dir,args.support_root,
        PROJECT/'output/PAQUETE_ARTICULO_I_DUALIDAD_DE_ESTADOS_20260922']
    protected += [v for v in (args.even_root,args.terminal_report_dir) if v is not None]
    require(not out.exists() and out != args.source_dir and not args.source_dir.is_relative_to(out)
        and all(not out.is_relative_to(r) and not r.is_relative_to(out) for r in protected),
        'Use a fresh report outside every protected input')
    out.mkdir(parents=True,exist_ok=False)
    started,tracked = time.monotonic(),{}
    report = dict(status='RUNNING_TWISTED_PAIR_PRODUCT', modules=[], compiler_invoked=False,
        runner_sha256=sha(__file__), restricted_receipt_sha256=RESTRICTED_SHA,
        support_receipt_sha256=SUPPORT_SHA, inherited_modules_recompiled=False,
        mathlib_rebuilt=False, sealed_461_modified=False, pdfs_changed=False,
        scope='Concrete TT Laurent field and complete four-block state-field assignment. '
        'Vacuum, creation, injectivity and inherited conformal Virasoro c=24 are proved; '
        'no claim of global mixed Jacobi/locality, full FLM or Monster automorphisms.')

    def save():
        (out/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')

    def track(path,digest):
        path = Path(path).resolve()
        require(path not in tracked or tracked[path] == digest, 'Conflicting pinned artifact')
        require(sha(path) == digest, 'Changed authenticated artifact: '+str(path))
        tracked[path] = digest
        return path

    def load(path,digest,name):
        track(path,digest)
        spec = importlib.util.spec_from_file_location(name,path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    save()
    try:
        track(__file__,report['runner_sha256'])
        old_runner = args.restricted_root/'verify_restricted_dual.py'
        old = load(old_runner,RESTRICTED_RUNNER_SHA,'pair_product_reconstruction')
        old_receipt = track(args.restricted_report_dir/'VERIFICATION.json',RESTRICTED_SHA)
        rr = json.loads(old_receipt.read_text())
        require(rr['status'] == 'PASS_RESTRICTED_DUAL_RECONSTRUCTION'
            and rr['authenticated_inputs_unchanged'] and not rr['inherited_modules_recompiled']
            and not rr['mathlib_rebuilt'] and rr['runner_sha256'] == RESTRICTED_RUNNER_SHA,
            'Invalid restricted-dual receipt')
        command = [sys.executable,'-I','-S',str(old_runner),'--plan',
            '--source-dir',str(args.restricted_root),'--report-dir',str(out/'restricted_plan'),
            '--timeout',str(args.timeout)]
        for flag in ('even_root','terminal_report_dir','helper','lean'):
            if getattr(args,flag) is not None:
                command += ['--'+flag.replace('_','-'),str(getattr(args,flag))]
        for item in args.relocate: command += ['--relocate',item]
        proc = subprocess.run(command,capture_output=True,text=True,timeout=args.timeout)
        planlog = out/'restricted_plan.log'
        planlog.write_text(proc.stdout+proc.stderr)
        report['restricted_plan'] = dict(command=command,exit_code=proc.returncode,
            output=planlog.read_text(),log_sha256=sha(planlog))
        save()
        require(proc.returncode == 0,'Restricted authentication plan failed')
        plan = json.loads((out/'restricted_plan/VERIFICATION.json').read_text())
        require(plan['status'] == 'PASS_RESTRICTED_DUAL_SOURCE_PLAN_NOT_COMPILED'
            and not plan['compiler_invoked'] and not plan['modules']
            and plan['authenticated_inputs_unchanged'],'Parent plan compiled or failed')
        for key in ('source_sha256','public_declarations','public_declaration_count',
                    'theorem_names','imports','inherited_module_count'):
            require(plan[key] == rr[key],'Changed reconstruction inventory: '+key)
        require({n:v['sha256'] for n,v in plan['inherited_objects'].items()} ==
            {n:v['sha256'] for n,v in rr['inherited_objects'].items()}, 'Changed predecessor registry')
        for path,digest in plan['authenticated_artifacts'].items(): track(path,digest)
        helper_path = args.helper or (args.even_root or old.DEFAULT_EVEN)/'verify_even_pairing.py'
        helper = load(helper_path,old.HELPER_SHA,'pair_product_inspector')

        def probe(names,output,expected=None):
            found = old.axiom_reports(output)
            require(len(names) == len(set(names)) and set(found) == set(names), 'Incomplete public probe')
            require(all(set(a) <= ORDINARY for a in found.values()),'Unexpected axiom')
            if expected is not None:
                require(set(found) == set(expected) and all(set(found[n]) == set(expected[n]) for n in found),
                    'Axiom log disagrees with receipt')
            return found

        registry = dict(plan['inherited_objects'])
        resolved = dict(plan['resolved_objects'])
        require(len(rr['modules']) == 1,'Unexpected reconstruction module count')
        row = rr['modules'][0]
        name,build = row['module'],args.restricted_report_dir/'build'
        require(name == old.NAME and row['exit_code'] == 0,'Reconstruction compile failed')
        track(build/(name+'.lean'),row['source_sha256'])
        log = track(build/(name+'.log'),row['log_sha256'])
        require(log.read_text() == row['output'],'Changed reconstruction log')
        obj = track(build/(name+'.olean'),row['object_sha256'])
        registry[name] = dict(path=str(obj),sha256=row['object_sha256'])
        ap = rr['axiom_probe']
        require(ap['exit_code'] == 0,'Reconstruction probe failed')
        pp = track(args.restricted_report_dir/'axiom_probe.lean',ap['source_sha256'])
        pl = track(args.restricted_report_dir/'axiom_probe.log',ap['output_sha256'])
        require(pp.read_text() == 'import '+name+'\n'+''.join('#print axioms '+d+'\n' for d in rr['public_declarations'])
            and pl.read_text() == ap['output'],'Changed reconstruction public probe')
        probe(rr['public_declarations'],pl.read_text(),rr['axioms'])
        support_receipt = track(args.support_root/'VERIFICATION.json',SUPPORT_SHA)
        support = json.loads(support_receipt.read_text())
        track(args.support_root/'verify_weight_support.py',SUPPORT_RUNNER_SHA)
        require(support['status'] == 'PASS_CONTRAGREDIENT_HOMOGENEOUS_WEIGHT_SUPPORT'
            and support['verifier_sha256'] == SUPPORT_RUNNER_SHA
            and support['parent_receipt_sha256'] == rr['terminal_receipt_sha256']
            and support['compiler_sha256'] == plan['compiler']['binary_sha256'], 'Invalid weight-support receipt')
        track(args.support_root/'compile.log',support['compile_log_sha256'])
        slog = track(args.support_root/'axioms.log',support['axioms_log_sha256'])
        require([r['module'] for r in support['modules']] == SUPPORT_NAMES,'Support module inventory mismatch')
        support_publics = []
        for row in support['modules']:
            name = row['module']
            require(name not in registry,'Support module collides with predecessor')
            src = track(args.support_root/(name+'.lean'),row['source_sha256'])
            obj = track(args.support_root/(name+'.olean'),row['olean_sha256'])
            support_publics += helper.public_declarations(name,src.read_text())
            registry[name] = dict(path=str(obj),sha256=row['olean_sha256'])
        sp = args.support_root/'WeightSupportAxioms.lean'
        wanted = ''.join('import '+n+'\n' for n in SUPPORT_NAMES)+''.join('#print axioms '+d+'\n' for d in support_publics)
        require(sp.read_text() == wanted,'Incomplete support probe source')
        track(sp,sha(sp))
        probe(support_publics,slog.read_text(),support['declarations'])
        require(len(registry) == 474,'Expected 461+5+1+7 inherited modules')
        build = out/'build'
        paths = list(dict.fromkeys([build,args.restricted_report_dir/'build',args.support_root,
            *map(Path,plan['lean_path'].split(os.pathsep))]))
        for name,witness in {**resolved,**registry}.items():
            obj = helper.resolve_object(name,paths)
            track(obj,witness['sha256'])
            resolved[name] = dict(path=str(obj),sha256=witness['sha256'])
        lean = Path(plan['compiler']['executable'])
        track(lean,plan['compiler']['binary_sha256'])
        contents,owners,theorems,imports = {},{},[],{}
        for name,digest in SOURCES.items():
            src = track(args.source_dir/(name+'.lean'),digest)
            contents[name] = src.read_text()
            clean = helper.without_comments(contents[name])
            forbidden = r'\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by|run_elab|run_cmd|elab|macro|syntax|initialize|instance|structure|class|inductive|opaque|mutual|constant)\b'
            require(not re.search(forbidden,clean),'Unsupported new source command')
            ds = helper.public_declarations(name,contents[name])
            for d in ds:
                require(d not in owners,'Duplicate public declaration')
                owners[d] = name
            imports[name] = re.findall(r'^import\s+(\S+)',clean,re.M)
            require(all(n in registry or n in resolved or n in list(SOURCES)[:list(SOURCES).index(name)]
                for n in imports[name]),'Unregistered new import')
            theorems += ['HMT.IV.'+name+'.'+n for n in re.findall(r'^\s*(?:@\[[^\]\n]*\]\s*)*(?:theorem|lemma)\s+([\w\x27]+)',clean,re.M)]
        report.update(inherited_module_count=len(registry),inherited_objects=registry,
            resolved_objects=resolved,compiler=plan['compiler'],public_declaration_owners=owners,
            public_declaration_count=len(owners),theorem_names=theorems,imports=imports,
            source_hashes=SOURCES,dependency_order=list(SOURCES),lean_path=os.pathsep.join(map(str,paths)))
        env = dict(os.environ,LEAN_PATH=report['lean_path'])
        if not args.plan:
            build.mkdir()
            for name,digest in SOURCES.items():
                src,obj,log = build/(name+'.lean'),build/(name+'.olean'),build/(name+'.log')
                src.write_text(contents[name])
                command = [str(lean),'-DwarningAsError=true','--root='+str(build),'-o',str(obj),str(src)]
                report['compiler_invoked'] = True
                proc = subprocess.run(command,env=env,capture_output=True,text=True,timeout=args.timeout)
                log.write_text(proc.stdout+proc.stderr)
                row = dict(module=name,source_sha256=digest,command=command,exit_code=proc.returncode,
                    log_sha256=sha(log),output=log.read_text())
                report['modules'].append(row)
                save()
                require(proc.returncode == 0,'New consumer compile failed: '+name)
                row['object_sha256'] = sha(obj)
                track(src,digest); track(obj,row['object_sha256'])
                print('COMPILED',name,flush=True)
            ps,pl = out/'axiom_probe.lean',out/'axiom_probe.log'
            ps.write_text(''.join('import '+n+'\n' for n in SOURCES)+''.join('#print axioms '+d+'\n' for d in owners))
            command = [str(lean),'-DwarningAsError=true',str(ps)]
            proc = subprocess.run(command,env=env,capture_output=True,text=True,timeout=args.timeout)
            pl.write_text(proc.stdout+proc.stderr)
            report['axiom_probe'] = dict(command=command,exit_code=proc.returncode,
                source_sha256=sha(ps),output_sha256=sha(pl),output=pl.read_text())
            save()
            require(proc.returncode == 0,'New public probe failed')
            report['axioms'] = probe(list(owners),pl.read_text())
            report['axiom_probe']['declarations'] = report['axioms']
        helper.unchanged({str(p):h for p,h in tracked.items()})
        report.update(status='PASS_TWISTED_PAIR_SOURCE_PLAN_NOT_COMPILED' if args.plan else
            'PASS_TWISTED_PAIR_PRODUCT',authenticated_inputs_unchanged=True,
            authenticated_artifacts={str(p):h for p,h in tracked.items()},
            elapsed_seconds=round(time.monotonic()-started,3))
        save()
        print(report['status'],len(owners),'public declarations;',len(theorems),'theorems',flush=True)
    except Exception as error:
        report.update(status='FAIL_TWISTED_PAIR_PRODUCT',error=str(error),
            elapsed_seconds=round(time.monotonic()-started,3))
        save()
        raise


if __name__ == '__main__':
    main()
