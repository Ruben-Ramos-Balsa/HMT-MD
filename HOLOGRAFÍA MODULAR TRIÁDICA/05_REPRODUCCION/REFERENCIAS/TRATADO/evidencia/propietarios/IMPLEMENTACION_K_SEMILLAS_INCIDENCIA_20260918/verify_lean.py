#!/usr/bin/env python3
"""Build the exact source closure without modifying the concurrent delivery.

Reuse an inherited olean only when its receipt names the same source hash and
the dependency source hashes also match. Store the actual object hash used.
The two new modules are always compiled and their reported axioms inspected.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
SERIES = PROJECT / 'output/AMPLIACION_FORMAL_LEAN_SERIE_20260916'
SOURCE = SERIES / 'stage18_article_I/delivery/HMT_ARTICULO_I_FUENTES_Y_PRUEBAS_ES_EN_REV04B/lean'
CACHE = SERIES / 'stage18_article_I/exceptional/verified_build'
MATHLIB = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4')
BIN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin')
LOCAL = ['WeightedIncidenceRecovery', 'GeneratedMarkedIncidence']
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def source_of(name):
    return (ROOT if name in LOCAL else SOURCE) / (name + '.lean')

def imports(path):
    return [name for line in path.read_text().splitlines()
            if line.startswith('import ') for name in line[7:].split()
            if (SOURCE / (name + '.lean')).exists() or name in LOCAL]

def main():
    build, logs = ROOT/'build', ROOT/'logs'
    build.mkdir(exist_ok=True)
    logs.mkdir(exist_ok=True)
    raw = subprocess.check_output([str(BIN/'lake'), 'env', 'printenv', 'LEAN_PATH'], cwd=MATHLIB, text=True).strip()
    dependency_paths = os.pathsep.join(str((MATHLIB/p).resolve()) if not Path(p).is_absolute() else p for p in raw.split(os.pathsep))
    env = dict(os.environ, LEAN_PATH=str(build)+os.pathsep+dependency_paths)
    compiler = subprocess.check_output([str(BIN/'lean'), '--version'], text=True).strip()
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=MATHLIB, text=True).strip()
    oldfile = ROOT/'VERIFICATION_LEAN.json'
    old = {x['module']: x for x in json.loads(oldfile.read_text()).get('modules', [])} if oldfile.exists() else {}
    ordered, seen = [], set()
    def visit(name):
        if name in seen:
            return
        seen.add(name)
        for dep in imports(source_of(name)):
            visit(dep)
        ordered.append(name)
    for target in LOCAL:
        visit(target)
    records = []
    for name in ordered:
        src = source_of(name)
        deps = {dep: sha(source_of(dep)) for dep in imports(src)}
        obj, log = build/(name+'.olean'), logs/(name+'.txt')
        local = name in LOCAL
        fingerprint = hashlib.sha256((compiler+commit+sha(src)+json.dumps(deps, sort_keys=True)).encode()).hexdigest()
        cached = False
        if not local and name in old and old[name]['fingerprint'] == fingerprint and obj.exists() and log.exists() and sha(obj) == old[name]['object_sha256']:
            cached = True
        receipt = CACHE/(name+'.json')
        external_obj = CACHE/(name+'.olean')
        if not cached and not local and receipt.exists() and external_obj.exists():
            data = json.loads(receipt.read_text())
            if data.get('sha256') == sha(src) and data.get('dependencies') == deps and data.get('exit_code') == 0:
                shutil.copy2(external_obj, obj)
                log.write_text(data.get('lean_output', ''))
                cached = True
        if not cached:
            if local and re.search(r'(?m)^\s*(?:axiom|constant)\s|\b(?:sorry|admit|native_decide)\b', src.read_text()):
                raise RuntimeError('Unproved shortcut in '+name)
            run = subprocess.run([str(BIN/'lean'), '--root='+str(src.parent),
                '-DwarningAsError=true', '-o', str(obj), str(src)], env=env, cwd=MATHLIB,
                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log.write_text(run.stdout)
            if run.returncode:
                print(run.stdout, flush=True)
                raise RuntimeError('Compilation failed: '+name)
        output = log.read_text()
        axioms = {a.strip() for xs in re.findall(r'depends on axioms:\s*\[([^\]]*)\]', output) for a in xs.split(',') if a.strip()}
        if axioms - ALLOWED:
            raise RuntimeError('Unexpected axioms in '+name+': '+str(axioms-ALLOWED))
        records.append(dict(module=name, source=str(src), sha256=sha(src),
            dependencies=deps, fingerprint=fingerprint, local=local, cached=cached,
            object_sha256=sha(obj), log=str(log), axioms=sorted(axioms)))
        report = dict(status='BUILD_IN_PROGRESS', compiler=compiler, mathlib_commit=commit,
            modules=records, full_terminal_K_generator_proved=False)
        oldfile.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
        print(('REUSED ' if cached else 'CHECKED ')+name, flush=True)
    report['status'] = 'PASS_SEED_INCIDENCE_AND_WEIGHTED_RECOVERY'
    report['scope'] = 'Native seed/incidence/marked-lattice composition and exact weighted-incidence inverse; no new proof of all terminal K channel values.'
    oldfile.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
    print(report['status'], flush=True)

if __name__ == '__main__':
    main()
