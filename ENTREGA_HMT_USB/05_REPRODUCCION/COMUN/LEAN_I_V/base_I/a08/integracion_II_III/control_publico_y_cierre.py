#!/usr/bin/env python3
"""Bounded public-declaration check of an already compiled delta; never compiles its 25 sources."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('focal_helpers', ROOT/'integrar_delta.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
sha, need, save = helpers.sha, helpers.need, helpers.save

def source_names(path):
    code = helpers.mask(path.read_text())
    namespace = ''; stack = []; found = []
    for lineno, raw in enumerate(code.splitlines(),1):
        line = raw.strip()
        ns = re.fullmatch(r'namespace\s+([\w.]+)',line)
        if ns:
            stack.append(('namespace',namespace,ns[1]))
            namespace = '.'.join(x for x in [namespace,ns[1]] if x)
            continue
        if re.fullmatch(r'(?:noncomputable\s+)?section(?:\s+[\w.]+)?',line):
            stack.append(('section',namespace,'')); continue
        end = re.fullmatch(r'end(?:\s+([\w.]+))?',line)
        if end:
            need(bool(stack), 'Unmatched end in '+str(path))
            kind,previous,label = stack.pop()
            if end[1] and kind == 'namespace':
                need(end[1] == label, 'Namespace end mismatch in '+str(path))
            namespace = previous; continue
        match = re.match(r'^(?:@\[[^\n]*?\]\s*)*(?:(?:noncomputable|protected|partial)\s+)?(theorem|lemma|def|abbrev|structure|inductive|instance)\s+([\w\u0370-\u03ff][\w\u0370-\u03ff\'.]*)',line)
        if match:
            found.append({'name': '.'.join(x for x in [namespace,match[2]] if x),
                          'kind':match[1],'line':lineno})
    # Lean closes unnamed sections at end of file; namespaces must still match.
    need(not namespace and all(k=='section' for k,_,_ in stack) and bool(found),
         'Unclosed namespace or empty inventory: '+str(path))
    need(len(found)==len({r['name'] for r in found}), 'Duplicate source name: '+str(path))
    return found

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--compiled',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args(); compiled=args.compiled.resolve(); out=args.output.resolve()
    need(compiled.is_relative_to(ROOT) and out.is_relative_to(ROOT),'Capsule-local directories required')
    need(not out.exists(),'Refusing overwrite of prior control')
    out.mkdir(parents=True)
    rec={'status':'RUNNING_PUBLIC_CONTROL', 'started_at':datetime.now(timezone.utc).isoformat(),
         'command':[sys.executable,'-I','-S','-B',str(Path(__file__).resolve()),*sys.argv[1:]],
         'runner_sha256':sha(__file__), 'delta_sources_recompiled':0,
         'base_modules_recompiled':0,'mathlib_rebuilt':False,'timeout_seconds':300}
    start=time.monotonic()
    try:
        previous_path=compiled/'VERIFICATION.json'; previous=json.loads(previous_path.read_text())
        need(len(previous['modules'])==25 and all(x['exit_code']==0 for x in previous['modules']), 'Previous 25 compilations are not all successful')
        need(previous.get('originals_unchanged_after') is True,'Previous originals check failed')
        need(previous['runner_sha256']==sha(ROOT/'integrar_delta.py'),'Original runner changed')
        rec['preserved_initial_execution']={'path':str(previous_path),'sha256':sha(previous_path),
            'status':previous['status'],'explanation':'25 source compilations succeeded; the unbounded all-environment-declarations probe was interrupted by scope decision, not by a mathematical failure.',
            'error':previous.get('error')}
        mf=ROOT/'MANIFIESTO_ENTRADAS.json'; manifest=json.loads(mf.read_text())
        need(sha(mf)==previous['input_manifest_sha256'],'Input manifest changed')
        sources={s['module']:s for s in manifest['sources']}
        native=set(previous['native_axiom_modules_from_preserved_receipts'])
        names={}; inherited={}; inventory={}
        for module,row in sources.items():
            path=ROOT/row['path'];need(sha(path)==row['sha256'],'Delta source changed')
            inventory[module]=source_names(path)
            for decl in inventory[module]:
                need(decl['name'] not in names,'Duplicate declaration across sources')
                names[decl['name']]=module
        for row in previous['modules']:
            for name in row['source_axiom_queries']:
                inherited[name]=row['module']
        union=dict(names);union.update(inherited)
        rec.update(public_source_count=len(names), inherited_query_count=len(inherited),
                   union_query_count=len(union), source_inventory=inventory,
                   native_modules_from_preserved_receipts=sorted(native))
        save(out/'PUBLIC_INVENTORY.json',{'source_inventory':inventory,'inherited_queries':inherited,'query_union':union})
        # Before the probe authenticate every actual object/import/source to be reused.
        tracked=dict(previous['authenticated_originals_before'])
        for row in previous['modules']:
            tracked[str(compiled/'build'/(row['module']+'.olean'))]=row['object_sha256']
            tracked[str(compiled/(row['module']+'.log'))]=row['log_sha256']
            for dep in row['dependencies'].values():
                tracked[dep['path']]=dep['sha256']
        need(all(Path(p).is_file() and sha(p)==h for p,h in tracked.items()),'Pre-probe object/import/source identity changed')
        probe=''.join('import '+m+'\n' for m in manifest['possible_incremental_compile_order'])
        probe+=''.join('#print axioms '+n+'\n' for n in sorted(union))
        source=out/'ProbePublic.lean';source.write_text(probe)
        command=[previous['compiler']['executable'],'-DwarningAsError=true',str(source)]
        env=dict(os.environ,LEAN_PATH=previous['lean_path'])
        rec['probe_command']=command;save(out/'VERIFICATION.json',rec)
        p=subprocess.run(command,cwd=out,env=env,text=True,capture_output=True,timeout=300)
        log=p.stdout+p.stderr;lp=out/'public_queries.log';lp.write_text(log)
        rec.update(exit_code=p.returncode, probe_source_sha256=sha(source),probe_log_sha256=sha(lp))
        if p.returncode: print(log,flush=True)
        need(p.returncode==0,'Public declaration probe failed')
        checked=helpers.reports(log)
        missing=sorted(set(union)-set(checked));unexpected=[]
        for name,module in union.items():
            allowed=helpers.STANDARD|({'Lean.ofReduceBool'} if module in native else set())
            if name in checked and not set(checked[name]) <= allowed:
                unexpected.append({'name':name,'module':module,'axioms':checked[name]})
        rec.update(missing_queries=missing,unexpected_axioms=unexpected,axiom_queries=checked)
        need(not missing and not unexpected,'Public coverage or axiom-boundary failure')
        # Independent final closure: every recorded delta object, resolved import,
        # original source, base object and external object is rehashed after the probe.
        changed=[p for p,h in tracked.items() if not Path(p).is_file() or sha(p)!=h]
        dependency_objects={v['path']:v['sha256'] for r in previous['modules'] for v in r['dependencies'].values()}
        closure={'status':'PASS_CIERRE_HUELLAS_DELTA_II_III' if not changed else 'FAIL_CIERRE_HUELLAS_DELTA_II_III',
                 'initial_receipt':str(previous_path),'initial_receipt_sha256':sha(previous_path),
                 'delta_object_count':25,'resolved_dependency_occurrences':sum(len(r['dependencies']) for r in previous['modules']),
                 'unique_resolved_dependency_objects':len(dependency_objects),
                 'all_authenticated_paths_count':len(tracked),'changed_files':changed,
                 'delta_objects':[{'module':r['module'],'path':str(compiled/'build'/(r['module']+'.olean')),'sha256':r['object_sha256']} for r in previous['modules']],
                 'resolved_dependency_objects':dependency_objects,
                 'all_authenticated_paths':tracked,'scientific_sources_modified':False,
                 'sources_or_base_recompiled':False,'checked_at':datetime.now(timezone.utc).isoformat()}
        save(out/'CIERRE_HUELLAS.json',closure)
        need(not changed,'Final source/object/import identity changed')
        rec.update(status='PASS_25_COMPILACIONES_COBERTURA_PUBLICA_Y_HUELLAS_II_III',
                   final_closure_sha256=sha(out/'CIERRE_HUELLAS.json'),
                   final_scope='25 unchanged delta compilations over authenticated base279, complete public-source declaration and inherited-query coverage, and final object/import identity. Generated/private auxiliary census is not claimed; original global probe remains interrupted.')
    except subprocess.TimeoutExpired as e:
        (out/'public_queries_partial.log').write_bytes((e.stdout or b'')+(e.stderr or b''))
        rec.update(status='FAIL_PUBLIC_CONTROL_TIMEOUT',error='Public probe exceeded the explicit 300s bound')
    except BaseException as e:
        rec.update(status='FAIL_PUBLIC_CONTROL',error={'type':type(e).__name__,'message':str(e)})
    rec.update(finished_at=datetime.now(timezone.utc).isoformat(),seconds=round(time.monotonic()-start,3))
    save(out/'VERIFICATION.json',rec)
    print(json.dumps({k:rec.get(k) for k in ['status','public_source_count','inherited_query_count','union_query_count','seconds','error']},ensure_ascii=False),flush=True)
    return 0 if rec['status'].startswith('PASS_25_') else 1

if __name__=='__main__':raise SystemExit(main())
