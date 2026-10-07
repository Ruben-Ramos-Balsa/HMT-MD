#!/usr/bin/env python3
"""Compile only the 25 authenticated II/III additions over the unchanged base279.

Adapted from CIERRE_II_III_DESDE_BASE_20260918/reproduce.py: source/object
authentication, isolated output, import resolution and recorded axiom queries.
No mathematical source, original receipt, central object or Mathlib is written.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PIN = '8bea2ab748f0b9d81496ed0b9a36c6949a55aca6bcdf7b2f081d2dd79eec6ea0'
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def mask(text):
    # Preserve line positions while masking nested Lean comments and strings.
    out = list(text)
    i, depth, line, string = 0, 0, False, False
    while i < len(text):
        pair, ch = text[i:i+2], text[i]
        if line:
            if ch == '\n': line = False
            else: out[i] = ' '
        elif depth:
            if pair == '/-': out[i:i+2] = '  '; depth += 1; i += 1
            elif pair == '-/': out[i:i+2] = '  '; depth -= 1; i += 1
            elif ch != '\n': out[i] = ' '
        elif string:
            if ch == '\\' and i+1 < len(text): out[i:i+2] = '  '; i += 1
            elif ch == '"': out[i] = ' '; string = False
            elif ch != '\n': out[i] = ' '
        elif pair == '--': out[i:i+2] = '  '; line = True; i += 1
        elif pair == '/-': out[i:i+2] = '  '; depth = 1; i += 1
        elif ch == '"': out[i] = ' '; string = True
        i += 1
    need(not depth and not string, 'Unterminated comment/string')
    return ''.join(out)

def reports(log):
    result = {n: sorted(a.strip() for a in block.split(',') if a.strip())
              for n, block in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", log, re.S)}
    result.update({n: [] for n in re.findall(r"'([^']+)' does not depend on any axioms", log)})
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--resume', action='store_true', help='Reuse only exact outputs of this focal execution')
    args = parser.parse_args()
    out = args.output.resolve()
    need(out.is_relative_to(ROOT) and out != ROOT, 'Output must be a new subdirectory of the capsule')
    need(not out.exists() or args.resume, 'Output exists; refuse overwrite without authenticated resume')
    out.mkdir(parents=True, exist_ok=args.resume)
    build = out / 'build'; build.mkdir(exist_ok=True)
    rec = {'status': 'RUNNING_II_III_279_PLUS_25', 'started_at': datetime.now(timezone.utc).isoformat(),
           'command': [sys.executable, '-I', '-S', '-B', str(Path(__file__).resolve()), *sys.argv[1:]],
           'runner_sha256': sha(__file__), 'base_modules_recompiled': 0, 'mathlib_rebuilt': False,
           'scope': 'Only the 25 unchanged integration sources and all their elaborated declarations; no whole-article certification',
           'modules': []}
    tracked = {}
    try:
        mf = ROOT / 'MANIFIESTO_ENTRADAS.json'
        need(sha(mf) == PIN, 'Input capsule manifest changed')
        manifest = json.loads(mf.read_text())
        base = Path(manifest['base']['path'])
        brp = base / manifest['base']['receipt']
        need(sha(brp) == manifest['base']['receipt_sha256'], 'Central receipt changed')
        br = json.loads(brp.read_text()); need(br['status'] == 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE', 'Base not PASS')
        central = {r['module']: r for r in br['sources']}
        objects = {r['module']: r for r in br['modules']}
        need(len(central) == 279, 'Wrong base cardinality')
        bb = base / 'resultados/lean_unificado/build'
        lean = Path(br['compiler']['executable'])
        need(sha(lean) == br['compiler']['binary_sha256'], 'Compiler changed')
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=br['mathlib'], text=True).strip()
        need(commit == manifest['base']['mathlib_commit'], 'Mathlib commit changed')
        tracked[str(mf)] = PIN; tracked[str(brp)] = sha(brp); tracked[str(lean)] = sha(lean)
        for name, row in central.items():
            src = base / row['path']; obj = bb / (name.replace('.', '/') + '.olean')
            need(sha(src) == row['sha256'] == objects[name]['source_sha256'], 'Base source changed: '+name)
            need(sha(obj) == objects[name]['object_sha256'], 'Base object changed: '+name)
            tracked[str(src)] = row['sha256']; tracked[str(obj)] = objects[name]['object_sha256']
        for name, row in br['external_objects'].items():
            p = Path(row['path']); expected = row.get('object_sha256', row.get('sha256'))
            need(sha(p) == expected, 'External object changed: '+name)
            tracked[str(p)] = expected
        sources = {r['module']: r for r in manifest['sources']}
        native_modules = set(); known_queries = {}
        for rr in manifest['receipts']:
            p = ROOT / rr['path']; need(sha(p) == rr['sha256'], 'Preserved receipt changed')
            tracked[str(p)] = rr['sha256']; r = json.loads(p.read_text())
            rows = r.get('results', r.get('compiled_modules', []))
            if 'source_sha256' in r and 'source' in r:
                rows = list(rows) + [{'module': Path(r['source']).stem, 'axioms': r.get('axioms', {})}]
            for row in rows:
                n = row['module']; qs = row.get('axiom_queries', row.get('axioms', {}))
                if n not in sources: continue
                known_queries.setdefault(n, {}).update(qs)
                if any('Lean.ofReduceBool' in ax for ax in qs.values()): native_modules.add(n)
        for name, row in sources.items():
            p = ROOT / row['path']; need(sha(p) == row['sha256'], 'Delta source changed: '+name)
            tracked[str(p)] = row['sha256']; code = mask(p.read_text())
            need(not re.search(r'\b(?:axiom|sorry|admit|sorryAx|unsafe|run_elab|run_cmd|initialize)\b|#eval|\b(?:IO|System)\.', code),
                 'Review required for executable or unproved Lean content: '+name)
        need(len(sources) == 25, 'Wrong delta cardinality')
        rec.update(base=str(base), base_receipt_sha256=sha(brp), base_modules=279,
                   input_manifest_sha256=PIN, compiler=br['compiler'], mathlib_commit=commit,
                   native_axiom_modules_from_preserved_receipts=sorted(native_modules),
                   authenticated_originals_before=tracked)
        deps = [bb] + [Path(p) for p in br['lean_path'].split(os.pathsep)[1:]]
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, [build]+deps)))
        rec['lean_path'] = env['LEAN_PATH']
        need(not any(p.stem not in sources for p in build.glob('*.olean')), 'Unexpected local object shadows base')
        for name in manifest['possible_incremental_compile_order']:
            row = sources[name]; src = ROOT / row['path']; local = build / (name+'.lean')
            obj = build / (name+'.olean'); prior = out / (name+'.json'); logp = out / (name+'.log')
            shutil.copyfile(src, local)
            direct = {}
            for imp in row['imports']:
                n = imp['module']; rel = Path(*n.split('.')).with_suffix('.olean')
                found = next((p/rel for p in [build]+deps if (p/rel).is_file()), None)
                need(found is not None, 'Unresolved imported object: '+n)
                if n in central:
                    need(found == bb/rel and sha(found) == objects[n]['object_sha256'], 'Central object shadowed: '+n)
                direct[n] = {'path': str(found), 'sha256': sha(found)}
            fp = hashlib.sha256(json.dumps([row['sha256'], direct, br['compiler']['binary_sha256']], sort_keys=True).encode()).hexdigest()
            if args.resume and prior.exists() and obj.exists() and logp.exists():
                old = json.loads(prior.read_text())
                if old.get('fingerprint') == fp and old.get('exit_code') == 0 and old.get('object_sha256') == sha(obj) and old.get('log_sha256') == sha(logp):
                    old['reused_focal_execution'] = True; rec['modules'].append(old)
                    print('REUSE_FOCAL '+name, flush=True); continue
            command = [str(lean), '-DwarningAsError=true', '--root='+str(build), '-o', str(obj), str(local)]
            t = time.monotonic(); proc = subprocess.run(command, cwd=build, env=env, text=True, capture_output=True)
            log = proc.stdout+proc.stderr; logp.write_text(log); qs = reports(log)
            r = {'module': name, 'source': str(src), 'source_sha256': sha(src), 'dependencies': direct,
                 'fingerprint': fp, 'command': command, 'exit_code': proc.returncode,
                 'seconds': round(time.monotonic()-t,3), 'log_sha256': sha(logp),
                 'object_sha256': sha(obj) if obj.exists() and proc.returncode == 0 else None,
                 'source_axiom_queries': qs, 'reused_focal_execution': False}
            save(prior,r); rec['modules'].append(r); save(out/'VERIFICATION.json',rec)
            print(('PASS ' if not proc.returncode else 'FAIL ')+name, flush=True)
            if proc.returncode: print(log, flush=True)
            need(proc.returncode == 0, 'Lean compilation failed: '+name)
            need(set(known_queries.get(name,{})) <= set(qs), 'Prior axiom queries missing: '+name)
            allow = STANDARD | ({'Lean.ofReduceBool'} if name in native_modules else set())
            need(all(set(ax) <= allow for ax in qs.values()), 'Unexpected source-query axiom: '+name)
        # Enumerate kernel-environment declarations owned by the 25 modules,
        # including private/generated helpers, then query their transitive axioms.
        order = manifest['possible_incremental_compile_order']
        probe = ''.join('import '+n+'\n' for n in order)
        probe += 'import Lean.Util.CollectAxioms\nopen Lean Elab Command\n'
        probe += 'run_elab do\n  let env ← getEnv\n  let selected : List String := '+json.dumps(order)+'\n'
        probe += '''  for (name, _) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let owner := env.header.moduleNames[idx.toNat]!
      if selected.contains owner.toString then
        let axioms ← Lean.collectAxioms name
        let names := String.intercalate "," (axioms.toList.map Name.toString)
        logInfo m!"CAPSULE_AXIOMS|{owner}|{name}|{names}"
'''
        pp = build/'ProbeAllDelta.lean'; pp.write_text(probe)
        cmd = [str(lean), '-DwarningAsError=true', '--root='+str(build), str(pp)]
        p = subprocess.run(cmd, cwd=build, env=env, text=True, capture_output=True)
        log = p.stdout+p.stderr; lp = out/'all_declarations.log'; lp.write_text(log)
        rec['all_declarations_probe'] = {'command': cmd, 'exit_code': p.returncode,
                                        'source_sha256': sha(pp), 'log_sha256': sha(lp)}
        if p.returncode: print(log, flush=True)
        need(p.returncode == 0, 'All-declaration probe failed')
        declarations = {}
        for module, name, ax in re.findall(r'CAPSULE_AXIOMS\|([^|\r\n]+)\|([^|\r\n]+)\|([^\r\n]*)', log):
            vals = sorted(a for a in ax.split(',') if a)
            allow = STANDARD | ({'Lean.ofReduceBool'} if module in native_modules else set())
            need(set(vals) <= allow, 'Unexpected axiom for '+module+': '+name+': '+str(vals))
            declarations[name] = {'module': module, 'axioms': vals}
        need({x['module'] for x in declarations.values()} == set(sources), 'Declaration inventory omits modules')
        rec['all_declarations_probe']['declarations'] = declarations
        rec['all_declarations_probe']['count'] = len(declarations)
        save(out/'ALL_DECLARATIONS.json', declarations)
        rec['status'] = 'PASS_II_III_INCREMENTAL_279_PLUS_25'
    except BaseException as error:
        rec['status'] = 'FAIL_II_III_INCREMENTAL_279_PLUS_25'
        rec['error'] = {'type': type(error).__name__, 'message': str(error)}
        print(str(error), file=sys.stderr, flush=True)
    finally:
        changed = [p for p,h in tracked.items() if not Path(p).is_file() or sha(p) != h]
        rec['originals_unchanged_after'] = not changed
        rec['changed_originals'] = changed
        if changed: rec['status'] = 'FAIL_ORIGINAL_IDENTITY_CHANGED'
        rec['finished_at'] = datetime.now(timezone.utc).isoformat()
        save(out/'VERIFICATION.json',rec)
    print(json.dumps({'status':rec['status'],'receipt':str(out/'VERIFICATION.json'),
                      'compiled_delta':len(rec['modules']),
                      'declarations':rec.get('all_declarations_probe',{}).get('count'),
                      'originals_unchanged':rec.get('originals_unchanged_after')}),flush=True)
    return 0 if rec['status'] == 'PASS_II_III_INCREMENTAL_279_PLUS_25' else 1

if __name__ == '__main__':
    raise SystemExit(main())
