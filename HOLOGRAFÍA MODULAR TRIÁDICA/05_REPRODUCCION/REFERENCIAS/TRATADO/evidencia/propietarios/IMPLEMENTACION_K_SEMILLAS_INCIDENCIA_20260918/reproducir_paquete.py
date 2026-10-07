#!/usr/bin/env python3
"""Check the local snapshot and regenerate regional signatures without outside HMT data.

Document preservation, arithmetic reproduction and Lean compilation are distinct
checks. Original sources remain unchanged; only resultados/ receives new reports.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True

def require(test, message):
    if not test:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, report):
    folder = ROOT/'resultados'
    folder.mkdir(exist_ok=True)
    (folder/name).write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def check():
    manifest = json.loads((ROOT/'MANIFIESTO.json').read_text())
    errors = []
    for item in manifest['files']:
        file = ROOT/item['path']
        if not file.is_file() or digest(file) != item['sha256']:
            errors.append(item['path'])
    require(not errors, 'Snapshot mismatch: '+repr(errors))
    sources = ROOT/'fuentes/articulo_x'
    tex = list(sources.rglob('*.tex'))
    require(len(tex) == manifest['article_x_tex_count'], 'LaTeX count mismatch')
    seen, missing = set(), set()
    def visit(file):
        file = file.resolve()
        if file in seen:
            return
        seen.add(file)
        body = re.sub(r'(?<!\\)%[^\n]*', '', file.read_text())
        for match in re.finditer(r'\\(?:input|include)\s*\{([^}]+)\}', body):
            name = match.group(1)
            if '\\' in name or '#' in name:
                continue
            child = sources/name
            if not child.suffix:
                child = child.with_suffix('.tex')
            if child.is_file():
                visit(child)
            else:
                missing.add(str(child.relative_to(sources)))
    visit(sources/'main.tex')
    require(not missing, 'Missing included source: '+repr(sorted(missing)))
    verifier = load('snapshot_terminal_verifier', ROOT/'lean/terminal/verify.py')
    libraries = [ROOT/'lean/terminal', ROOT/'lean/regional', ROOT/'lean/incidencia', ROOT/'lean/biblioteca']
    external = {'Mathlib','Init','Lean','Std','Batteries','Aesop','Qq','Plausible','ProofWidgets','ImportGraph','LeanSearchClient'}
    visited = set()
    def module_file(name):
        for library in libraries:
            path = library/Path(*name.split('.')).with_suffix('.lean')
            if path.is_file():
                return path
        return None
    def inspect(name):
        if name in visited or name.split('.')[0] in external:
            return
        file = module_file(name)
        require(file is not None, 'Missing local Lean import: '+name)
        visited.add(name)
        for dependency in verifier.inspect_source(file):
            inspect(dependency)
    targets=[*verifier.FOCAL_MODULES,'GeneratedMarkedIncidence','WeightedIncidenceRecovery','CheckReaders']
    if module_file('SelectedRegionalIncidence'):
        targets.append('SelectedRegionalIncidence')
    for name in targets:
        inspect(name)
    reports = []
    for relative, field in [
        ('lean/terminal/VERIFICATION_INCREMENTAL.json','sources'),
        ('lean/terminal/REGIONAL_COMPOSITION_VERIFICATION.json','new_compositions')]:
        receipt = json.loads((ROOT/relative).read_text())
        require(receipt['status'].startswith('PASS_'), 'Receipt is not PASS: '+relative)
        for item in receipt[field]:
            name = item.get('path') or item['source']
            require(digest(ROOT/'lean/terminal'/name) == item['sha256'], 'Proof receipt mismatch: '+name)
        reports.append(receipt['status'])
    save('CONSERVACION_DOCUMENTAL.json', dict(
        status='PASS_CONSERVACION_FUENTES_Y_CLAUSURA_LOCAL',
        files=len(manifest['files']), tex_files=len(tex), included_tex=len(seen),
        preserved_other_tex=sorted(str(p.relative_to(sources)) for p in tex if p.resolve() not in seen),
        lean_modules_in_dependency_closure=len(visited), inherited_proof_receipts=reports,
        meaning='Checks preservation and source/import consistency; does not replace theorem compilation.'))

def n69():
    producer = load('snapshot_regional_producer', ROOT/'python/regenerate_n69_original.py')
    producer.READER = ROOT/'python/lectores_regionales.py'
    opened = []
    stage = ['generation']
    def audit(event, args):
        if event == 'open' and isinstance(args[0], (str, bytes)):
            path = str(args[0])
            opened.append((stage[0],path))
            require(not (stage[0] == 'generation' and 'N69_TESTIGO_POSTERIOR.csv' in path),
                    'Reference opened during generation')
    sys.addaudithook(audit)
    generated, evidence = producer.produce(100)
    stage[0] = 'comparison'
    with (ROOT/'datos/N69_TESTIGO_POSTERIOR.csv').open(newline='') as handle:
        reference = list(csv.DictReader(handle))
    require(len(reference) == len(generated), 'Different row counts')
    mismatch = [(i,key) for i,(a,b) in enumerate(zip(generated,reference))
                for key in producer.FIELDS if a[key] != b[key]]
    require(not mismatch, 'Regional signature mismatch: '+repr(mismatch[:10]))
    target = ROOT/'resultados'
    target.mkdir(exist_ok=True)
    with (target/'FIRMAS_REGIONALES_REGENERADAS.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=producer.FIELDS)
        writer.writeheader()
        writer.writerows(generated)
    external_hmt = [path for _,path in opened if '/Users/ruben/Documents/' in path
                    and not Path(path).resolve().is_relative_to(ROOT)]
    require(not external_hmt, 'External HMT file read: '+repr(external_hmt))
    save('REPRODUCCION_REGIONAL.json',dict(
        status='PASS_REPRODUCCION_REGIONAL_LOCAL', rows=len(generated),
        equal_fields=len(generated)*len(producer.FIELDS),
        generated_before_reference_read=True, external_hmt_reads=external_hmt,
        generation_files=sorted(set(path for phase,path in opened if phase=='generation')),
        streams_sha256={k:hashlib.sha256(v.encode()).hexdigest() for k,v in evidence['streams'].items()},
        scope='Reproduces the regional signature table from packaged regional readers; no terminal K target is read.'))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    p.add_argument('--n69', action='store_true')
    p.add_argument('--lean', action='store_true')
    p.add_argument('--mathlib', type=Path)
    p.add_argument('--lean-binary', default='lean')
    args=p.parse_args()
    if not (args.check or args.n69 or args.lean):
        p.error('Choose --check, --n69 or --lean')
    if args.check:
        check()
    if args.n69:
        n69()
    if args.lean:
        require(args.mathlib is not None, '--lean requires --mathlib')
        command=[sys.executable,'-I','-S',str(ROOT/'verificar_lean.py'),'--root',str(ROOT),
                 '--mathlib',str(args.mathlib.resolve()),'--lean',args.lean_binary,
                 ]
        raise SystemExit(subprocess.call(command))

if __name__=='__main__':
    main()
