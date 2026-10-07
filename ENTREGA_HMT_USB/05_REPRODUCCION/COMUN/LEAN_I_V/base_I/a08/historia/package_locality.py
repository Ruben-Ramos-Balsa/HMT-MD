#!/usr/bin/env python3
"""Seal the checked all-state locality delta, preserving every predecessor.

No Lean compilation is repeated here. Receipts, objects and source hashes
are checked before copying. The relocated executable is checked with --plan.
The separate II/III capsule is preserved with its own exact scope and receipt.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
OLD_MANIFEST = '5c799bba2dabf827a0320d1814241d4e237c4a9c50f97a596ceb8841e14502a8'
LOCALITY_RECEIPT = '867e422b5b95948f1ec34de21f73f61bb213f059c0ea521e9b9f7f133d60d05d'
II_III_RECEIPT = '60f209f162bd1db399839c65ea654795da332d83cfdca3a36dc4480604b4aab5'
II_III_CLOSURE = 'd2291c3dca9920407004458754c4b61af7773c786f01087e25a488cba181ecef'

WRAPPER = '''#!/usr/bin/env python3
"""Replay the all-state locality proof on the unchanged selected HMT carrier."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root / 'verificar_localidad.py'
spec = importlib.util.spec_from_file_location('hmt_locality_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
for flag, value in [
    ('--modules', 'SelectedDescendantLocality'),
    ('--source-root', root / 'lean'),
    ('--dong-root', root / 'lean/dong'),
    ('--coherence-root', root / 'antecedente/lean'),
    ('--coherence-report-dir', root / 'antecedente/recibos/coherencia'),
    ('--locality-report-dir', root / 'recibos/localidad_generadores'),
    ('--helper', root / 'antecedente/verificar_delta.py'),
    ('--base', root / 'antecedente/antecedente/antecedente'),
    ('--report-dir', root / 'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag + '=') for a in args):
        defaults.extend([flag, str(value)])
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
'''


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def write(p, value):
    Path(p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def inventory(root):
    rows = {}
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            raise RuntimeError('Symlink not admitted: ' + str(p))
        if p.is_file():
            name = p.relative_to(root).as_posix()
            rows[name] = dict(path=name, sha256=sha(p), bytes=p.stat().st_size)
    return rows


def require_hash(p, value):
    if sha(p) != value:
        raise RuntimeError('Changed authenticated file: ' + str(p))


def main():
    here = Path(__file__).resolve().parent
    out = next(p for p in here.parents if p.name == 'output')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path,
        default=out / 'PAQUETE_ARTICULO_I_LOCALIDAD_ESTADO_CAMPO_20260921')
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    dest = args.destination.resolve()
    archive = dest.with_suffix('.zip')
    if dest.exists() or archive.exists():
        raise RuntimeError('Refusing to overwrite a delivery')
    previous = out / 'PAQUETE_ARTICULO_I_COHERENCIA_CAMPOS_20260920'
    require_hash(previous / 'MANIFIESTO.json', OLD_MANIFEST)
    old = read(previous / 'MANIFIESTO.json')
    before = inventory(previous)
    for row in old['files']:
        if before.get(row['path'], {}).get('sha256') != row['sha256']:
            raise RuntimeError('Predecessor changed: ' + row['path'])
    receipt_dir = here / 'locality_closed_results'
    require_hash(receipt_dir / 'VERIFICATION.json', LOCALITY_RECEIPT)
    receipt = read(receipt_dir / 'VERIFICATION.json')
    if receipt['status'] != 'PASS_DESCENDANT_LOCALITY_DELTA':
        raise RuntimeError('Expected complete locality receipt')
    require_hash(here / 'verify_descendant_locality.py', receipt['runner_sha256'])
    nodes = receipt['sources']
    rows = {r['module']: r for r in receipt['modules']}
    if set(rows) != set(nodes) or len(nodes) != 11:
        raise RuntimeError('Unexpected locality closure')
    for name, node in nodes.items():
        require_hash(node['path'], node['sha256'])
        require_hash(receipt_dir / 'build' / (name + '.lean'), node['sha256'])
        require_hash(receipt_dir / 'build' / (name + '.olean'), rows[name]['object_sha256'])
        if rows[name]['exit_code'] != 0:
            raise RuntimeError('Unsuccessful focal module: ' + name)
    capsule = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/INTEGRACION_NUCLEO_I_V_20260921/II_III')
    cap_report = capsule / 'resultados_control_publico_20260921_02'
    require_hash(cap_report / 'VERIFICATION.json', II_III_RECEIPT)
    require_hash(cap_report / 'CIERRE_HUELLAS.json', II_III_CLOSURE)
    cap_receipt = read(cap_report / 'VERIFICATION.json')
    if cap_receipt['status'] != 'PASS_25_COMPILACIONES_COBERTURA_PUBLICA_Y_HUELLAS_II_III':
        raise RuntimeError('II/III receipt is not the final public-coverage receipt')
    for row in read(cap_report / 'CIERRE_HUELLAS.json')['delta_objects']:
        require_hash(row['path'], row['sha256'])
    cap_before = inventory(capsule)
    result = dict(status='PASS_LOCALITY_PACKAGE_INPUTS', previous_files=len(before),
        locality_modules=len(nodes), public_declarations=receipt['public_declaration_count'],
        theorem_lemma_count=len(receipt['theorem_names']), ii_iii_public_declarations=400,
        compilation_repeated=False, destination=str(dest), zip=str(archive))
    if args.plan:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    dest.mkdir(parents=True)
    shutil.copytree(previous, dest / 'antecedente')
    shutil.copytree(capsule, dest / 'integracion_II_III')
    (dest / 'lean/dong').mkdir(parents=True)
    for name, node in nodes.items():
        source = Path(node['path'])
        rel = source.relative_to(here)
        shutil.copy2(source, dest / 'lean' / rel)
    for name in ('LatticeFieldLocality', 'LatticeGeneratorLocality'):
        shutil.copy2(here / (name + '.lean'), dest / 'lean' / (name + '.lean'))
    for name in ('kernel_build', 'binomial_build', 'triple_build'):
        shutil.copytree(here / 'dong' / name, dest / 'lean/dong' / name)
    for name in ('verify_dong_kernel.py', 'verify_dong_binomial.py', 'verify_triple_locality.py'):
        shutil.copy2(here / 'dong' / name, dest / 'lean/dong' / name)
    shutil.copytree(here / 'resultados', dest / 'recibos/localidad_generadores')
    shutil.copytree(receipt_dir, dest / 'recibos/localidad_estados')
    shutil.copy2(here / 'verify_descendant_locality.py', dest / 'verificar_localidad.py')
    shutil.copy2(here / 'README_LOCALIDAD.md', dest / 'README.md')
    (dest / 'reproducir.py').write_text(WRAPPER, encoding='utf-8')
    (dest / 'historia').mkdir()
    shutil.copy2(here / 'dong/PRUEBA_DONG_NORMALFIELD.md', dest / 'historia/PRUEBA_DONG_NORMALFIELD.md')
    shutil.copy2(here.parent.parent / 'CONTINUIDAD_I.md', dest / 'historia/CONTINUIDAD_I.md')
    shutil.copy2(__file__, dest / 'historia/package_locality.py')
    coordination = out / 'CONTINUIDAD_NUCLEO_I_V_20260921'
    for name in ('MANDATO_AUTORAL_INTEGRO.md', 'PROCEDENCIA_K_Y_COORDINACION_I_V.md'):
        shutil.copy2(coordination / name, dest / 'historia' / name)
    causal = read(here.parent / 'state_field/normal_coherence_results/CAUSAL.json')
    causal.update(artifact=str(dest / 'README.md'), artifact_sha256=sha(dest / 'README.md'),
        result_id='SELECTED_LATTICE_ALL_STATE_LOCALITY_20260921',
        verification_receipt='recibos/localidad_estados/VERIFICATION.json',
        verification_receipt_sha256=LOCALITY_RECEIPT, compiled_modules=8,
        reused_authenticated_modules=3, public_declarations=160, theorem_lemma_count=132)
    causal['inherited_context'] = dict(
        source='antecedente/recibos/coherencia/CAUSAL.json',
        sha256=sha(previous / 'recibos/coherencia/CAUSAL.json'),
        scope='Inherited genealogy is preserved; the new Lean result is all-state locality on the same selected lattice, not a re-proof of every contextual declaration.')
    causal['genealogy']['tpk'].update(
        operator='Reuse selectedOrigin, charged fields, Heisenberg modes and stateField; compose their actual residual and normal products.',
        action='Prove both Dong integrand annihilators from the three original localities, identify the residue commutator, extend locality through every oscillator word and linearly to all states.')
    causal['genealogy']['source_locators'] += [
        'lean/LatticeResidueProducts.lean:heisenberg_residueField',
        'lean/LatticeDongLocality.lean:normalField_localAt',
        'lean/LatticeDescendantLocality.lean:stateField_local',
        'lean/SelectedDescendantLocality.lean:selected_fields_local']
    focal = causal['focal_genealogical_receipt']
    focal['3_tpk_effective_composition'] = 'Same selected origin -> same lattice carrier -> existing three generator localities -> residual fields and justified convolution -> both integrand annihilators -> Dong normal-field locality -> induction on words -> all-state linear extension.'
    focal['4_coefficient_origins'] = 'Residue kernels and divided derivatives retain the existing binomial coefficients. The sufficient locality order p+q+s+n follows by the proved binomial annihilator identity. No target state or uniform frequency cutoff is supplied.'
    focal['7_produced_output'] = 'Mutual locality of stateField for every pair of states of the same lattice carrier, specialized to selectedOrigin without new native evaluation.'
    focal['8_posterior_recognition_and_falsifier'] = 'Residue and locality terminology is a posterior proof language. Wrong residue indices, missing pointwise finiteness, an assumed Dong conclusion, or a different selected carrier would invalidate this chain; actual public declarations and axioms are checked in the focal receipt.'
    focal['9_material_owners'] = [str(Path('lean') / Path(n['path']).relative_to(here)) for n in nodes.values()]
    scope = causal['formalization_scope']
    scope.update(new_result='All-state mutual locality of the constructed state-field map on the same selected lattice.',
        not_claimed=['Full conformal structure, twisted sector and orbifold multiplication',
                     'Formal identification of the automorphism group with the Monster',
                     'A new proof of every inherited contextual declaration by this delta'])
    write(dest / 'recibos/CAUSAL_LOCALIDAD.json', causal)
    gate = Path.home() / '.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py'
    audit = subprocess.run([sys.executable, '-I', '-S', str(gate), '--audit',
        str(dest / 'README.md'), '--receipt', str(dest / 'recibos/CAUSAL_LOCALIDAD.json')],
        text=True, capture_output=True)
    write(dest / 'recibos/CONTROL_CAUSAL_LOCALIDAD.json', dict(exit_code=audit.returncode,
        stdout=audit.stdout, stderr=audit.stderr, gate_sha256=sha(gate),
        is_lean_theorem_verification=False))
    if audit.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in audit.stdout:
        raise RuntimeError('Causal focal audit failed: ' + audit.stdout + audit.stderr)
    with tempfile.TemporaryDirectory(prefix='hmt-locality-replay-') as temp:
        command = [sys.executable, '-I', '-S', str(dest / 'reproducir.py'),
                   '--plan', '--report-dir', str(Path(temp) / 'plan')]
        replay = subprocess.run(command, capture_output=True, text=True)
        if replay.returncode:
            raise RuntimeError('Relocation check failed: ' + replay.stdout + replay.stderr)
        plan = read(Path(temp) / 'plan/PLAN.json')
        if plan['status'] != 'PASS_DESCENDANT_LOCALITY_SOURCE_PLAN_NOT_COMPILED':
            raise RuntimeError('Unexpected relocated plan')
        write(dest / 'recibos/REPRODUCCION_RELOCALIZADA.json', plan)
    if inventory(previous) != before or inventory(dest / 'antecedente') != before:
        raise RuntimeError('Predecessor preservation mismatch')
    if inventory(capsule) != cap_before or inventory(dest / 'integracion_II_III') != cap_before:
        raise RuntimeError('II/III preservation mismatch')
    write(dest / 'VERIFICACION_CONSERVACION.json', dict(
        status='PASS_FULL_PREDECESSOR_AND_II_III_PRESERVATION',
        previous_files=list(before.values()), ii_iii_files=list(cap_before.values()),
        previous_manifest_sha256=OLD_MANIFEST, locality_receipt_sha256=LOCALITY_RECEIPT,
        ii_iii_receipt_sha256=II_III_RECEIPT, ii_iii_closure_sha256=II_III_CLOSURE))
    all_files = inventory(dest)
    write(dest / 'MANIFIESTO.json', dict(schema='hmt.all_state_locality.successor.v1',
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        source_closure=receipt['dependency_order'], theorem_names=receipt['theorem_names'],
        exact_public_declarations=receipt['public_declaration_count'],
        predecessor='antecedente', original_279_base='antecedente/antecedente/antecedente',
        locality_receipt='recibos/localidad_estados/VERIFICATION.json',
        locality_receipt_sha256=LOCALITY_RECEIPT,
        inherited_axiom_exception=receipt['inherited_axiom_exception'],
        files=list(all_files.values())))
    complete = inventory(dest)
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name in complete:
            z.write(dest / name, dest.name + '/' + name)
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None or len(z.namelist()) != len(complete):
            raise RuntimeError('ZIP CRC or entry-count mismatch')
        for name, row in complete.items():
            if hashlib.sha256(z.read(dest.name + '/' + name)).hexdigest() != row['sha256']:
                raise RuntimeError('ZIP changed file: ' + name)
    result.update(status='PASS_ALL_STATE_LOCALITY_DELIVERY', files=len(complete),
        manifest_sha256=sha(dest / 'MANIFIESTO.json'), zip_sha256=sha(archive),
        relocated_replay_plan_passed=True)
    write(dest.parent / (dest.name + '_ENTREGA.json'), result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
