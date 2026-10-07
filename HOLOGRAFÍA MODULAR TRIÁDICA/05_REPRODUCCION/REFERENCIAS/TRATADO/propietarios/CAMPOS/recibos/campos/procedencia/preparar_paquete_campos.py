#!/usr/bin/env python3
"""Build a successor of the sealed 154-module cut, retaining every prior byte."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_ARTICULO_I_TRAZA_GRADUADA_20260918'
ROOT = HERE.parent / 'PAQUETE_ARTICULO_I_CAMPOS_RETICULARES_20260918'
NAMES = (
    'LatticeChargeEnergy', 'LatticeEnergyGrading', 'LatticeEnergyShift',
    'LatticeModeWeights', 'LatticeEnergyModes', 'LatticeLowWeightParity',
    'LatticeEulerEnergy', 'LatticeCreationExponential',
    'LatticeAnnihilationExponential', 'LatticeCoxeterFock',
    'LatticeExponentialEnergy', 'LatticeAnnihilationEnergy',
    'LatticeChargedVertexField', 'LatticeChargedFieldEnergy', 'SelectedEnergyInput',
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
            source='CHARGED_FIELDS_CONTINUATION_20260918', role=role))
    add('versiones_previas/MANIFIESTO_TRAZA_SELLADO.json', before, 'EXACT_PREDECESSOR_MANIFEST')
    add('versiones_previas/README_TRAZA_SELLADO.md', (ROOT / 'README.md').read_bytes(),
        'EXACT_PREDECESSOR_ENTRY')
    readme = (HERE / 'README_CAMPOS_ENTREGA.md').read_bytes()
    (ROOT / 'README.md').write_bytes(readme)
    for row in mf['files']:
        if row['path'] == 'README.md':
            row.update(sha256=sha(readme), bytes=len(readme),
                role='CURRENT_ENTRY_PREDECESSOR_PRESERVED_UNDER_VERSIONES_PREVIAS')
    queries = []
    for name in NAMES:
        raw = (HERE / (name + '.lean')).read_bytes()
        add('deltas/campos/' + name + '.lean', raw, 'FIELD_CONTINUATION_SOURCE')
        queries.extend(re.findall(r'(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$', raw.decode()))
    if len(queries) != len(set(queries)):
        raise RuntimeError('Repeated continuation axiom query')
    add('reproducir_campos.py', (HERE / 'reproducir_campos_portable.py').read_bytes(),
        'CURRENT_PORTABLE_RUNNER')
    for name in ('CONTINUIDAD_CAMPOS_RETICULARES.md', 'COORDINACION_II_III_20260918.md',
                 'preparar_paquete_campos.py'):
        add('recibos/campos/procedencia/' + name, (HERE / name).read_bytes(),
            'INCREMENTAL_PROVENANCE')
    mf['charged_fields_successor'] = dict(
        status='PREPARED_NOT_YET_JOINTLY_VERIFIED',
        predecessor_manifest_sha256=sha(before),
        predecessor_files=len(json.loads(before)['files']),
        preserved_files_relocated={'README.md': 'versiones_previas/README_TRAZA_SELLADO.md'},
        modules=list(NAMES), axiom_queries=queries,
        complete_flm_formalization_claimed=False,
        main='HMT.I.SelectedEnergyInput.shared_action_electron_energy_and_fields')
    (ROOT / 'MANIFIESTO.json').write_text(json.dumps(mf, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(dict(status='FIELD_PACKAGE_PREPARED', root=str(ROOT),
        new_modules=len(NAMES), new_queries=len(queries)), ensure_ascii=False))

def seal():
    raw = (ROOT / 'MANIFIESTO.json').read_bytes()
    mf = json.loads(raw)
    if mf['charged_fields_successor']['status'] != 'PREPARED_NOT_YET_JOINTLY_VERIFIED':
        raise RuntimeError('Not an unsealed prepared successor')
    runpath = ROOT / 'resultados/lean_unificado/VERIFICATION.json'
    run = json.loads(runpath.read_text())
    if run['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or run['manifest_sha256'] != sha(raw):
        raise RuntimeError('No valid joint verification of this exact manifest')
    if not set(mf['charged_fields_successor']['axiom_queries']).issubset(run['axiom_probe']['declarations']):
        raise RuntimeError('An added declaration was not checked')
    for row in mf['files']:
        if sha((ROOT / row['path']).read_bytes()) != row['sha256']:
            raise RuntimeError('Source differs: ' + row['path'])
    for name, data in (
        ('recibos/campos/MANIFIESTO_COMPILADO.json', raw),
        ('recibos/campos/LEAN_CONJUNTO.json', runpath.read_bytes()),
    ):
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            raise RuntimeError('Refusing to overwrite frozen evidence')
        target.write_bytes(data)
        mf['files'].append(dict(path=name, sha256=sha(data), bytes=len(data),
            source='JOINT_LEAN_RUN', role='FROZEN_FIELD_EVIDENCE'))
    previous = json.loads((BASE / 'MANIFIESTO.json').read_text())
    for row in previous['files']:
        dest = ('versiones_previas/README_TRAZA_SELLADO.md' if row['path'] == 'README.md' else row['path'])
        if sha((ROOT / dest).read_bytes()) != row['sha256']:
            raise RuntimeError('Lost predecessor bytes: ' + row['path'])
    mf['charged_fields_successor'].update(status='SEALED_VERIFIED_FIELDS',
        modules_in_closure=run['local_module_count'],
        verified_declarations=len(run['axiom_probe']['declarations']),
        predecessor_bytes_preserved=True, receipt='recibos/campos/LEAN_CONJUNTO.json')
    final = (json.dumps(mf, indent=2, ensure_ascii=False)+'\n').encode()
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
                raise RuntimeError('ZIP content differs: ' + row['path'])
    print(json.dumps(dict(status='PASS_CHARGED_FIELDS_PACKAGE_SEALED',
        modules=run['local_module_count'], declarations=len(run['axiom_probe']['declarations']),
        files=len(mf['files']), zip=str(archive), zip_sha256=sha(archive.read_bytes()),
        manifest_sha256=sha(final)), ensure_ascii=False))

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--seal']:
        seal()
    else:
        raise SystemExit('Use --prepare or --seal.')
