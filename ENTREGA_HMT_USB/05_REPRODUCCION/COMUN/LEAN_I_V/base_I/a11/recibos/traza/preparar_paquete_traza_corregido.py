#!/usr/bin/env python3
"""Add a checked trace continuation; never mutate the sealed predecessor."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_ARTICULO_I_CONTINUACION_VOA_20260918'
ROOT = HERE.parent / 'PAQUETE_ARTICULO_I_TRAZA_GRADUADA_20260918'
NAMES = (
    'LatticeFockMonomialParity', 'WeightedOscillatorTrace',
    'OscillatorEulerProduct', 'WeightedEulerBridge', 'LatticeWeightFiniteness',
    'FockFiniteParityPiece', 'SelectedGradedTrace', 'LatticeChargeParityTrace',
    'LatticeWeightShells', 'LatticeFullGradedTrace', 'SelectedFullGradedTrace',
)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def prepare():
    if ROOT.exists():
        raise RuntimeError('Refusing to overwrite an existing successor')
    before = (BASE / 'MANIFIESTO.json').read_bytes()
    mf = json.loads(before)
    for row in mf['files']:
        if sha((BASE / row['path']).read_bytes()) != row['sha256']:
            raise RuntimeError('Predecessor modified: ' + row['path'])
    for name in NAMES:
        source = HERE / (name + '.lean')
        if not source.is_file():
            raise RuntimeError('Continuation source not yet assembled: ' + name)
        if re.search(r'(?m)^\s*(axiom|sorry|admit)\b', source.read_text()):
            raise RuntimeError('Unexpected proof placeholder: ' + name)
    shutil.copytree(BASE, ROOT)
    def add(path, data, role):
        if any(r['path'] == path for r in mf['files']):
            raise RuntimeError('Would replace a manifested source: ' + path)
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        mf['files'].append(dict(path=path, sha256=sha(data), bytes=len(data),
            source='GRADED_TRACE_CONTINUATION_20260918', role=role))
    add('versiones_previas/MANIFIESTO_VOA_SELLADO.json', before, 'EXACT_PREDECESSOR_MANIFEST')
    old_readme = (ROOT / 'README.md').read_bytes()
    add('versiones_previas/README_VOA_SELLADO.md', old_readme, 'EXACT_PREDECESSOR_ENTRY')
    readme = (HERE / 'README_TRAZA_ENTREGA.md').read_bytes()
    (ROOT / 'README.md').write_bytes(readme)
    for row in mf['files']:
        if row['path'] == 'README.md':
            row.update(sha256=sha(readme), bytes=len(readme),
                role='CURRENT_ENTRY_PREDECESSOR_PRESERVED_UNDER_VERSIONES_PREVIAS')
    queries = []
    for name in NAMES:
        raw = (HERE / (name + '.lean')).read_bytes()
        add('deltas/traza/' + name + '.lean', raw, 'COMPILED_TRACE_SOURCE')
        queries.extend(re.findall(r'(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$', raw.decode()))
    if len(queries) != len(set(queries)):
        raise RuntimeError('Repeated trace axiom query')
    add('reproducir_traza.py', (HERE / 'reproducir_traza_portable.py').read_bytes(), 'CURRENT_PORTABLE_RUNNER')
    for name in ('CONTINUIDAD_TRAZA_GRADUADA.md', 'BUSQUEDA_LOCAL_FLM_Y_SERIES.json',
                 'preparar_paquete_traza.py'):
        add('recibos/traza/procedencia/' + name, (HERE / name).read_bytes(), 'INCREMENTAL_PROVENANCE')
    source_root = HERE.parent / 'EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections'
    for name in ('excepcional.tex', 'moonshine_comparacion.tex'):
        add('fuentes/traza/' + name, (source_root / name).read_bytes(), 'LATEX_PROVENANCE_NOT_A_LEAN_AXIOM')
    if 'voa_compilation_sealed' in mf:
        mf['predecessor_voa_compilation_sealed'] = mf.pop('voa_compilation_sealed')
    mf['graded_trace_successor'] = dict(
        status='PREPARED_NOT_YET_JOINTLY_VERIFIED',
        predecessor_manifest_sha256=sha(before),
        predecessor_files=len(json.loads(before)['files']),
        preserved_files_relocated={'README.md': 'versiones_previas/README_VOA_SELLADO.md'},
        modules=list(NAMES), axiom_queries=queries,
        complete_flm_formalization_claimed=False,
        main='HMT.I.SelectedFullGradedTrace.shared_action_electron_fields_and_full_trace')
    (ROOT / 'MANIFIESTO.json').write_text(json.dumps(mf, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(status='TRACE_PACKAGE_PREPARED', root=str(ROOT),
        new_modules=len(NAMES), new_queries=len(queries)), ensure_ascii=False))

def seal():
    raw = (ROOT / 'MANIFIESTO.json').read_bytes()
    mf = json.loads(raw)
    if mf['graded_trace_successor']['status'] == 'SEALED_VERIFIED_TRACE':
        raise RuntimeError('Already sealed')
    runpath = ROOT / 'resultados/lean_unificado/VERIFICATION.json'
    run = json.loads(runpath.read_text())
    if run['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or run['manifest_sha256'] != sha(raw):
        raise RuntimeError('No valid joint verification for the exact source manifest')
    if not set(mf['graded_trace_successor']['axiom_queries']).issubset(run['axiom_probe']['declarations']):
        raise RuntimeError('A trace declaration was not checked')
    for row in mf['files']:
        if sha((ROOT / row['path']).read_bytes()) != row['sha256']:
            raise RuntimeError('Manifested source differs: ' + row['path'])
    for name, data in (
        ('recibos/traza/MANIFIESTO_COMPILADO.json', raw),
        ('recibos/traza/LEAN_CONJUNTO.json', runpath.read_bytes()),
        ('recibos/traza/preparar_paquete_traza_corregido.py', Path(__file__).read_bytes()),
    ):
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            raise RuntimeError('Refusing to overwrite frozen trace evidence')
        target.write_bytes(data)
        mf['files'].append(dict(path=name, sha256=sha(data), bytes=len(data),
            source='JOINT_LEAN_RUN', role='FROZEN_TRACE_EVIDENCE'))
    previous = json.loads((BASE / 'MANIFIESTO.json').read_text())
    for row in previous['files']:
        dest = ('versiones_previas/README_VOA_SELLADO.md' if row['path'] == 'README.md' else row['path'])
        if sha((ROOT / dest).read_bytes()) != row['sha256']:
            raise RuntimeError('Lost predecessor bytes: ' + row['path'])
    mf['graded_trace_successor'].update(status='SEALED_VERIFIED_TRACE',
        modules_in_closure=run['local_module_count'],
        verified_declarations=len(run['axiom_probe']['declarations']),
        predecessor_bytes_preserved=True,
        receipt='recibos/traza/LEAN_CONJUNTO.json')
    final = (json.dumps(mf, indent=2, ensure_ascii=False) + '\n').encode()
    (ROOT / 'MANIFIESTO.json').write_bytes(final)
    archive = ROOT.with_suffix('.zip')
    if archive.exists():
        raise RuntimeError('Refusing to overwrite ZIP')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in sorted({r['path'] for r in mf['files']} | {'MANIFIESTO.json'}):
            z.write(ROOT / name, Path(ROOT.name) / name)
        if z.testzip():
            raise RuntimeError('ZIP CRC failed')
        for row in mf['files']:
            if sha(z.read(str(Path(ROOT.name) / row['path']))) != row['sha256']:
                raise RuntimeError('ZIP file differs: ' + row['path'])
    print(json.dumps(dict(status='PASS_GRADED_TRACE_PACKAGE_SEALED',
        modules=run['local_module_count'], declarations=len(run['axiom_probe']['declarations']),
        files=len(mf['files']), zip=str(archive), zip_sha256=sha(archive.read_bytes()),
        manifest_sha256=sha(final)), ensure_ascii=False))

def restore_conserved():
    mf = json.loads((ROOT / 'MANIFIESTO.json').read_text())
    if mf['graded_trace_successor']['status'] != 'PREPARED_NOT_YET_JOINTLY_VERIFIED':
        raise RuntimeError('Cannot restore into a sealed successor')
    before = json.loads((BASE / 'MANIFIESTO.json').read_text())
    restored = []
    for row in before['files']:
        target = ROOT / row['path']
        if target.exists():
            continue
        raw = (BASE / row['path']).read_bytes()
        if sha(raw) != row['sha256']:
            raise RuntimeError('Predecessor bytes differ')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        restored.append(row['path'])
    print(json.dumps(dict(restored_exact_predecessor_bytes=restored), ensure_ascii=False))

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--seal']:
        seal()
    elif sys.argv[1:] == ['--restore-conserved']:
        restore_conserved()
    else:
        raise SystemExit('Use --prepare or --seal; neither overwrites a sealed predecessor.')
