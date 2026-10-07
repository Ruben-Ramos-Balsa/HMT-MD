#!/usr/bin/env python3
"""Seal the verified translation delta without compiling Lean or Mathlib.

The complete locality predecessor is copied unchanged. Only the twelve
sources listed in the pinned successful receipt enter the new source root.
A temporary relocated copy checks the replay defaults with --plan only.
The archive is checked by CRC and SHA-256 for every individual entry.
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
import zlib

sys.dont_write_bytecode = True
OLD_MANIFEST = '0e16f9ee2c2e5644ae96d036a2534f9f8e1b97d2437ba54a14ac65e2673f12f2'
TRANSLATION_RECEIPT = '58db187960f39204c9a885f8a70f593d132d17b6ea6460103647738811eef0aa'
README_SHA = '32a24a2bb981198f83d6eb64f25fbf8e89e8ca2fd2b65a62a7d963024a2f8b66'

WRAPPER = '''#!/usr/bin/env python3
"""Replay the checked state-field translation delta on its unchanged origin."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root / 'verificar_traslacion.py'
spec = importlib.util.spec_from_file_location('hmt_translation_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
for flag, value in [
    ('--modules', 'SelectedTranslationCoherence'),
    ('--source-root', root / 'lean'),
    ('--base', root / 'antecedente/antecedente/antecedente/antecedente'),
    ('--locality-root', root / 'antecedente/lean'),
    ('--locality-report-dir', root / 'antecedente/recibos/localidad_estados'),
    ('--generator-locality-report-dir', root / 'antecedente/recibos/localidad_generadores'),
    ('--coherence-root', root / 'antecedente/antecedente/lean'),
    ('--coherence-report-dir', root / 'antecedente/antecedente/recibos/coherencia'),
    ('--helper', root / 'antecedente/antecedente/verificar_delta.py'),
    ('--locality-helper', root / 'antecedente/verificar_localidad.py'),
    ('--report-dir', root / 'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag + '=') for a in args):
        defaults.extend([flag, str(value)])
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
'''


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n',
                          encoding='utf-8')


def inventory(root):
    rows = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Symlink not admitted: ' + str(path))
        if path.is_file():
            name = path.relative_to(root).as_posix()
            rows[name] = dict(path=name, sha256=sha(path), bytes=path.stat().st_size)
    return rows


def require_hash(path, expected):
    if sha(path) != expected:
        raise RuntimeError('Changed authenticated file: ' + str(path))


def causal_receipt(previous, dest, receipt):
    """Preserve the contextual contract and specialize the focal result only."""
    old_path = previous / 'recibos/CAUSAL_LOCALIDAD.json'
    causal = read(old_path)
    causal.update(artifact=str(dest / 'README.md'), artifact_sha256=sha(dest / 'README.md'),
        result_id='SELECTED_LATTICE_LOCAL_CREATIVE_TRANSLATION_20260921',
        verification_receipt='recibos/traslacion/VERIFICATION.json',
        verification_receipt_sha256=TRANSLATION_RECEIPT, compiled_modules=12,
        reused_authenticated_modules=0, authenticated_predecessor_modules=309,
        public_declarations=66, theorem_lemma_count=60)
    causal['inherited_context'] = dict(
        source='antecedente/recibos/CAUSAL_LOCALIDAD.json', sha256=sha(old_path),
        scope='The complete inherited genealogy and locality receipt remain unchanged. '
              'This focal receipt extends the same selected state-field map with the '
              'verified covariance and translated-state identities; it does not re-prove '
              'every contextual declaration or certify the full orbifold construction.')
    causal['genealogy']['tpk'].update(
        operator='Reuse selectedOrigin, the same lattice carrier, charged and Heisenberg '
                 'fields, translation operator T and constructed stateField Y.',
        action='Prove the Heisenberg and charged commutators, propagate covariance by '
               'pointwise finite normal-product telescoping and linear extension, '
               'then deduce Y(Tu)=derivativeField(Y(u)) by local creative-field uniqueness.')
    locators = causal['genealogy']['source_locators']
    causal['genealogy']['source_locators'] = [
        'antecedente/' + loc if loc.startswith('lean/') else loc for loc in locators]
    causal['genealogy']['source_locators'] += [
        'lean/LatticeHeisenbergTranslation.lean:translation_heisenberg_coefficient',
        'lean/LatticeChargedTranslation.lean:translation_charged_coefficient',
        'lean/LatticeNormalTranslation.lean:normalField_translation_covariant',
        'lean/LatticeCovariantFieldUniqueness.lean:creative_covariant_fields_unique',
        'lean/LatticeDerivativeLocality.lean:derivative_local',
        'lean/LatticeStateFieldTranslation.lean:stateField_translation_covariant',
        'lean/LatticeStateFieldTranslation.lean:stateField_translated_state',
        'lean/SelectedTranslationCoherence.lean:selected_local_translation_publication']
    focal = causal['focal_genealogical_receipt']
    focal['3_tpk_effective_composition'] = (
        'Same selected APP-origin publication -> same lattice carrier, vacuum, T and Y '
        '-> Heisenberg mode and charged-ground commutators -> creator propagation of '
        'the zero defect -> finite normal-product telescoping -> all-state covariance '
        '-> derivative locality and creative covariant-field uniqueness -> translated-state identity.')
    focal['4_coefficient_origins'] = (
        'The derivative coefficient k+1 and the existing divided-derivative binomial '
        'coefficients are used in proved commutator and telescoping identities. The '
        'sufficient derivative locality order N+1 follows from the crossing derivative. '
        'No target state, new lattice, covariance axiom or uniform frequency bound is supplied.')
    focal['7_produced_output'] = (
        'On the same selected carrier: T annihilates the vacuum; Y creates each state; '
        'the vacuum field is the identity; all state fields are mutually local; '
        '[T,Y(u)_k]=(k+1)Y(u)_(k+1) for every integral exponent; and '
        'Y(Tu)=derivativeField(Y(u)) for every state u, without new native evaluation.')
    focal['8_posterior_recognition_and_falsifier'] = (
        'Vertex-field and derivative terminology is posterior proof language on the '
        'inherited object. An assumed covariance conclusion, missing pointwise finiteness, '
        'wrong exponent, undischarged charged-ground hypothesis or changed selected '
        'carrier invalidates the chain. The pinned Lean receipt queries all 66 public '
        'declarations and permits the inherited native axiom only in the three exact '
        'SelectedTranslationCoherence declarations.')
    focal['9_material_owners'] = ['lean/' + receipt['sources'][name]['path']
                                 for name in receipt['dependency_order']]
    causal['formalization_scope'].update(
        new_result='Locality, creation, vacuum, all-state translation covariance and '
                   'the translated-state derivative identity for the same constructed Y.',
        not_claimed=['Full conformal structure, involution extension, twisted sector '
                     'and orbifold multiplication',
                     'Formal identification of the automorphism group with the Monster',
                     'A new proof of every inherited contextual declaration by this delta'],
        inherited_native_declarations=receipt['declarations_using_inherited_native_axiom'])
    return causal


def main():
    here = Path(__file__).resolve().parent
    out = next(path for path in here.parents if path.name == 'output')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path,
        default=out / 'PAQUETE_ARTICULO_I_TRASLACION_ESTADO_CAMPO_20260921')
    parser.add_argument('--plan', action='store_true', help='Authenticate packaging inputs only')
    args = parser.parse_args()
    dest = args.destination.expanduser().resolve()
    archive = dest.with_suffix('.zip')
    delivery = dest.parent / (dest.name + '_ENTREGA.json')
    zip_report = dest.parent / (dest.name + '_ZIP_VERIFICACION.json')
    if any(path.exists() for path in (dest, archive, delivery, zip_report)):
        raise RuntimeError('Refusing to overwrite an existing delivery or receipt')
    previous = out / 'PAQUETE_ARTICULO_I_LOCALIDAD_ESTADO_CAMPO_20260921'
    require_hash(previous / 'MANIFIESTO.json', OLD_MANIFEST)
    old = read(previous / 'MANIFIESTO.json')
    before = inventory(previous)
    if len(before) != 2013 or set(before) != {row['path'] for row in old['files']} | {'MANIFIESTO.json'}:
        raise RuntimeError('Expected the entire 2013-file predecessor with exact manifest coverage')
    for row in old['files']:
        if before.get(row['path']) != row:
            raise RuntimeError('Predecessor file differs from its manifest: ' + row['path'])
    receipt_dir = here / 'translation_closed_results'
    require_hash(receipt_dir / 'VERIFICATION.json', TRANSLATION_RECEIPT)
    receipt = read(receipt_dir / 'VERIFICATION.json')
    if (receipt['status'] != 'PASS_TRANSLATION_COHERENCE_DELTA'
            or receipt['inherited_module_count'] != 309
            or receipt['public_declaration_count'] != 66 or len(receipt['theorem_names']) != 60
            or not receipt['authenticated_inputs_unchanged']
            or receipt['predecessors_recompiled'] or receipt['mathlib_rebuilt']):
        raise RuntimeError('Expected the exact successful translation receipt')
    require_hash(here / 'verify_translation_coherence.py', receipt['runner_sha256'])
    require_hash(here / 'README_TRASLACION.md', README_SHA)
    nodes = receipt['sources']
    rows = {row['module']: row for row in receipt['modules']}
    if set(nodes) != set(rows) or len(nodes) != 12 or len(receipt['modules']) != 12:
        raise RuntimeError('Expected exactly twelve translation modules')
    for name, node in nodes.items():
        if node['path'] != name + '.lean':
            raise RuntimeError('Unexpected source path: ' + node['path'])
        require_hash(here / node['path'], node['sha256'])
        require_hash(receipt_dir / 'build' / (name + '.lean'), node['sha256'])
        require_hash(receipt_dir / 'build' / (name + '.olean'), rows[name]['object_sha256'])
        if rows[name]['exit_code'] or rows[name]['source_sha256'] != node['sha256']:
            raise RuntimeError('Unsuccessful focal module: ' + name)
    receipt_before = inventory(receipt_dir)
    result = dict(status='PASS_TRANSLATION_PACKAGE_INPUTS', previous_files=len(before),
        authenticated_predecessor_modules=309, translation_modules=12,
        public_declarations=66, theorem_lemma_count=60,
        compilation_repeated=False, destination=str(dest), zip=str(archive))
    if args.plan:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    print('Preserving all 2013 predecessor files; copying exact twelve-module delta.', flush=True)
    dest.mkdir(parents=True)
    shutil.copytree(previous, dest / 'antecedente')
    (dest / 'lean').mkdir()
    for name, node in nodes.items():
        shutil.copy2(here / node['path'], dest / 'lean' / node['path'])
    shutil.copytree(receipt_dir, dest / 'recibos/traslacion')
    shutil.copy2(here / 'verify_translation_coherence.py', dest / 'verificar_traslacion.py')
    shutil.copy2(here / 'README_TRASLACION.md', dest / 'README.md')
    (dest / 'reproducir.py').write_text(WRAPPER, encoding='utf-8')
    (dest / 'historia').mkdir()
    shutil.copy2(here.parent.parent / 'CONTINUIDAD_I.md', dest / 'historia/CONTINUIDAD_I.md')
    shutil.copy2(__file__, dest / 'historia/package_translation_coherence.py')
    coordination = out / 'CONTINUIDAD_NUCLEO_I_V_20260921'
    for name in ('MANDATO_AUTORAL_INTEGRO.md', 'PROCEDENCIA_K_Y_COORDINACION_I_V.md'):
        shutil.copy2(coordination / name, dest / 'historia' / name)
    skill = Path.home() / '.codex/skills/enforce-hmt-generated-constants'
    shutil.copy2(skill / 'references/MENSAJE_AUTORAL_INTEGRO_NO_REINICIO_20260831.txt',
                 dest / 'historia/MENSAJE_AUTORAL_INTEGRO_NO_REINICIO_20260831.txt')
    write(dest / 'recibos/CAUSAL_TRASLACION.json', causal_receipt(previous, dest, receipt))
    gate = skill / 'scripts/verify_generated_constants.py'
    audit = subprocess.run([sys.executable, '-I', '-S', str(gate), '--audit',
        str(dest / 'README.md'), '--receipt', str(dest / 'recibos/CAUSAL_TRASLACION.json')],
        text=True, capture_output=True)
    write(dest / 'recibos/CONTROL_CAUSAL_TRASLACION.json', dict(exit_code=audit.returncode,
        stdout=audit.stdout, stderr=audit.stderr, gate_sha256=sha(gate),
        artifact_sha256=sha(dest / 'README.md'),
        receipt_sha256=sha(dest / 'recibos/CAUSAL_TRASLACION.json'),
        is_lean_theorem_verification=False))
    if audit.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in audit.stdout:
        raise RuntimeError('Focal causal audit failed: ' + audit.stdout + audit.stderr)
    print('Causal audit passed; checking --plan from an external temporary copy.', flush=True)
    with tempfile.TemporaryDirectory(prefix='hmt-translation-replay-') as temp:
        relocated = Path(temp) / 'relocated_package'
        shutil.copytree(dest, relocated)
        command = [sys.executable, '-I', '-S', str(relocated / 'reproducir.py'),
                   '--plan', '--report-dir', str(Path(temp) / 'plan')]
        replay = subprocess.run(command, cwd=temp, capture_output=True, text=True)
        if replay.returncode:
            raise RuntimeError('Relocated replay failed: ' + replay.stdout + replay.stderr)
        plan = read(Path(temp) / 'plan/PLAN.json')
        if (plan['status'] != 'PASS_TRANSLATION_COHERENCE_SOURCE_PLAN_NOT_COMPILED'
                or plan['compiler_invoked'] or plan['modules']
                or plan['inherited_module_count'] != 309
                or plan['dependency_order'] != receipt['dependency_order']
                or plan['sources'] != nodes or not plan['authenticated_inputs_unchanged']):
            raise RuntimeError('Unexpected relocated replay plan')
        write(dest / 'recibos/REPRODUCCION_RELOCALIZADA.json', plan)
    if inventory(previous) != before or inventory(dest / 'antecedente') != before:
        raise RuntimeError('Complete predecessor preservation mismatch')
    if inventory(receipt_dir) != receipt_before or inventory(dest / 'recibos/traslacion') != receipt_before:
        raise RuntimeError('Focal receipt/build preservation mismatch')
    for node in nodes.values():
        require_hash(here / node['path'], node['sha256'])
        require_hash(dest / 'lean' / node['path'], node['sha256'])
    write(dest / 'VERIFICACION_CONSERVACION.json', dict(
        status='PASS_FULL_PREDECESSOR_AND_TRANSLATION_PRESERVATION',
        previous_files=list(before.values()), translation_files=list(receipt_before.values()),
        previous_manifest_sha256=OLD_MANIFEST, translation_receipt_sha256=TRANSLATION_RECEIPT,
        includes_entire_ii_iii_and_all_earlier_predecessors=True,
        later_conformal_involution_and_vertex_extension_sources_included=False))
    write(dest / 'MANIFIESTO.json', dict(schema='hmt.translation.coherence.successor.v1',
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        source_closure=receipt['dependency_order'], theorem_names=receipt['theorem_names'],
        exact_public_declarations=66, theorem_lemma_count=60,
        predecessor='antecedente', original_279_base='antecedente/antecedente/antecedente/antecedente',
        translation_receipt='recibos/traslacion/VERIFICATION.json',
        translation_receipt_sha256=TRANSLATION_RECEIPT,
        inherited_axiom_exception=receipt['inherited_axiom_exception'],
        files=list(inventory(dest).values())))
    complete = inventory(dest)
    print('Preservation and relocation passed; creating and checking the ZIP.', flush=True)
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for name in complete:
            bundle.write(dest / name, dest.name + '/' + name)
    entries = []
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None or len(bundle.namelist()) != len(complete):
            raise RuntimeError('ZIP CRC or entry-count mismatch')
        for name, row in complete.items():
            archive_name = dest.name + '/' + name
            data = bundle.read(archive_name)
            digest = hashlib.sha256(data).hexdigest()
            crc = zlib.crc32(data) & 0xffffffff
            info = bundle.getinfo(archive_name)
            if digest != row['sha256'] or crc != info.CRC or len(data) != row['bytes']:
                raise RuntimeError('ZIP entry changed: ' + name)
            entries.append(dict(path=archive_name, bytes=len(data), sha256=digest,
                                crc32=f'{crc:08x}', compressed_bytes=info.compress_size))
    write(zip_report, dict(status='PASS_ZIP_CRC_AND_SHA256_EVERY_ENTRY',
        archive=str(archive), archive_sha256=sha(archive), entries=entries))
    if inventory(dest) != complete or inventory(previous) != before:
        raise RuntimeError('An input or delivery file changed while checking the archive')
    result.update(status='PASS_TRANSLATION_COHERENCE_DELIVERY', files=len(complete),
        manifest_sha256=sha(dest / 'MANIFIESTO.json'), zip_sha256=sha(archive),
        zip_verification=str(zip_report), zip_verification_sha256=sha(zip_report),
        translation_receipt_sha256=TRANSLATION_RECEIPT,
        relocated_replay_plan_passed=True, causal_focal_audit_passed=True)
    write(delivery, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
