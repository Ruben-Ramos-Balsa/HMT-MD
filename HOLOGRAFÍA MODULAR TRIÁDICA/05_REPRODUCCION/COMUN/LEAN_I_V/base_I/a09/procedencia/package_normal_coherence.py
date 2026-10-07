#!/usr/bin/env python3
"""Package the verified normal-product coherence extension, without recompiling.

Preserves the complete previous state-field delivery, including its own full
predecessor, and authenticates all current sources against the focal receipt.
The package is not built until that receipt is PASS. Existing output is never
overwritten. Narratives and the external finite-algebra auxiliary are copied
as provenance only, never promoted to imports of the principal Lean closure.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import zipfile

sys.dont_write_bytecode = True
PREVIOUS_NAME = 'PAQUETE_ARTICULO_I_ESTADO_CAMPO_20260920'
DELIVERY_NAME = 'PAQUETE_ARTICULO_I_COHERENCIA_CAMPOS_20260920'
PREVIOUS_MANIFEST_SHA = '83760d005118c3abd4916119a8b258f47aaf18efd7c7a006002852011e870450'
PREVIOUS_RECEIPT_SHA = '590b102eb1d5089d709d12e4345f4663837b29fe59be36ed53fe37d47691a6f3'
DEFAULT_AUXILIARY = Path('/Users/ruben/Documents/excelencia academica/output/'
                         'NORMAL_PRODUCT_COMMUTATION_20260920')

WRAPPER = '''#!/usr/bin/env python3
"""Replay the normal-coherence source closure with the preserved HMT base."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root / 'verificar_delta.py'
spec = importlib.util.spec_from_file_location('hmt_normal_coherence_verifier', path)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
arguments = sys.argv[1:]
defaults = []
for flag, value in [('--base', root / 'antecedente/antecedente'),
                    ('--source-root', root / 'lean'),
                    ('--report-dir', root / 'resultados')]:
    if not any(arg == flag or arg.startswith(flag + '=') for arg in arguments):
        defaults.extend([flag, str(value)])
sys.argv = [str(path), *defaults, *arguments]
raise SystemExit(verifier.main())
'''


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def files_under(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Symlink not admitted: ' + str(path))
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            result[relative] = dict(path=relative, sha256=sha(path), bytes=path.stat().st_size)
    return result


def main():
    source = Path(__file__).resolve().parent
    output = next((p for p in source.parents if p.name == 'output'), None)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous', type=Path, default=output / PREVIOUS_NAME if output else None)
    parser.add_argument('--destination', type=Path, default=output / DELIVERY_NAME if output else None)
    parser.add_argument('--receipt-dir', type=Path, default=source / 'normal_coherence_results')
    parser.add_argument('--readme', type=Path, default=source / 'README_COHERENCIA.md')
    parser.add_argument('--narrative', action='append', type=Path, default=[],
                        help='One of the two selected K narratives; repeat twice')
    parser.add_argument('--auxiliary', type=Path, default=DEFAULT_AUXILIARY)
    parser.add_argument('--plan', action='store_true', help='Authenticate inputs without copying or zipping')
    args = parser.parse_args()
    if args.previous is None or args.destination is None:
        raise RuntimeError('--previous and --destination must identify the delivery locations')
    previous = args.previous.expanduser().resolve()
    destination = args.destination.expanduser().resolve()
    archive = destination.with_suffix('.zip')
    if destination.exists() or archive.exists():
        raise RuntimeError('Refusing to overwrite an existing delivery: ' + str(destination))
    if sha(previous / 'MANIFIESTO.json') != PREVIOUS_MANIFEST_SHA:
        raise RuntimeError('Previous manifest does not match the sealed state-field edition')
    if sha(previous / 'recibos/estado_campo/VERIFICATION.json') != PREVIOUS_RECEIPT_SHA:
        raise RuntimeError('Previous proof receipt does not match its sealed edition')
    old = json.loads((previous / 'MANIFIESTO.json').read_text())
    before = files_under(previous)
    for row in old['files']:
        if before.get(row['path'], {}).get('sha256') != row['sha256']:
            raise RuntimeError('Changed previous manifested file: ' + row['path'])
    runner_path = source / 'verify_state_field.py'
    spec = importlib.util.spec_from_file_location('normal_coherence_runner', runner_path)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    verifier, _, base_sources, _, _ = runner.authenticate_base(previous / 'antecedente')
    nodes, order, inherited, external = runner.inventory(verifier, source, base_sources)
    receipt_dir = args.receipt_dir.expanduser().resolve()
    receipt_file = receipt_dir / 'VERIFICATION.json'
    receipt = json.loads(receipt_file.read_text())
    if receipt.get('status') != 'PASS_STATE_FIELD_DELTA':
        raise RuntimeError('Normal-coherence focal receipt is not PASS')
    if receipt.get('runner_sha256') != sha(runner_path):
        raise RuntimeError('Runner changed after focal compilation')
    if receipt.get('sources') != nodes or receipt.get('compile_order') != order:
        raise RuntimeError('Current source closure differs from the focal PASS receipt')
    if receipt.get('base_receipt_sha256') != runner.BASE_RECEIPT_SHA:
        raise RuntimeError('Wrong base receipt in focal verification')
    for name in old['delta_modules']:
        if name not in nodes or sha(previous / 'lean' / (name + '.lean')) != nodes[name]['sha256']:
            raise RuntimeError('An earlier state-field source has been removed or changed: ' + name)
    required = {'LatticeNormalProductCommutation', 'LatticeNormalProductBounds',
                'LatticeWordPermutation', 'LatticeNormalProductLinear',
                'LatticeStateFieldCoherence', 'SelectedStateField'}
    if not required <= set(nodes):
        raise RuntimeError('Required coherence/composition module absent')
    for row in receipt['modules']:
        path = receipt_dir / 'build' / (row['module'] + '.olean')
        if row['exit_code'] != 0 or sha(path) != row['object_sha256']:
            raise RuntimeError('Unverified focal object: ' + row['module'])
    narratives = [p.expanduser().resolve() for p in args.narrative]
    if len(narratives) != 2 or len(set(narratives)) != 2 or any(not p.is_file() for p in narratives):
        raise RuntimeError('Provide the two distinct existing K narratives with --narrative')
    auxiliary = args.auxiliary.expanduser().resolve()
    if not (auxiliary / 'NormalProductAlgebra.lean').is_file():
        raise RuntimeError('The preserved NormalProductAlgebra dossier was not found')
    if any('NormalProductAlgebra' in node['imports'] for node in nodes.values()):
        raise RuntimeError('Provenance-only auxiliary was unexpectedly promoted to a principal import')
    auxiliary_files = files_under(auxiliary)
    narrative_rows = [dict(source=str(p), name=p.name, sha256=sha(p), bytes=p.stat().st_size,
                           principal_lean_dependency=False) for p in narratives]
    if not args.readme.is_file():
        raise RuntimeError('Reviewed successor README not found')
    result = dict(status='PASS_NORMAL_COHERENCE_PACKAGE_INPUTS',
                  previous_files=len(before), previous_manifested_files=len(old['files']),
                  preserved_previous_modules=old['delta_modules'],
                  modules=order, genuinely_added_modules=[m for m in order if m not in old['delta_modules']],
                  public_declarations=receipt['public_declaration_count'],
                  theorem_count=len(receipt['theorem_names']),
                  focal_receipt_sha256=sha(receipt_file), narratives=narrative_rows,
                  auxiliary_files=len(auxiliary_files), destination=str(destination), zip=str(archive))
    if args.plan:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    destination.mkdir(parents=True)
    shutil.copytree(previous, destination / 'antecedente')
    (destination / 'lean').mkdir()
    for node in nodes.values():
        shutil.copy2(source / node['path'], destination / 'lean' / node['path'])
    shutil.copy2(runner_path, destination / 'verificar_delta.py')
    (destination / 'reproducir.py').write_text(WRAPPER, encoding='utf-8')
    shutil.copy2(args.readme, destination / 'README.md')
    shutil.copytree(receipt_dir, destination / 'recibos/coherencia')
    (destination / 'procedencia/narrativas_k').mkdir(parents=True)
    for index, path in enumerate(narratives, 1):
        target = destination / 'procedencia/narrativas_k' / f'{index:02d}_{path.name}'
        shutil.copy2(path, target)
        narrative_rows[index-1]['copied_to'] = target.relative_to(destination).as_posix()
    shutil.copytree(auxiliary, destination / 'procedencia/auxiliar_normal')
    shutil.copy2(Path(__file__), destination / 'procedencia/package_normal_coherence.py')
    for name in ('CAUSAL_COHERENCIA.json', 'CONTROL_CAUSAL_COHERENCIA.json', 'REVISION_COHERENCIA.md'):
        if (source / name).is_file():
            shutil.copy2(source / name, destination / 'recibos/coherencia' / name)
    if files_under(destination / 'antecedente') != before or files_under(previous) != before:
        raise RuntimeError('Previous delivery changed or was not preserved byte for byte')
    if files_under(destination / 'procedencia/auxiliar_normal') != auxiliary_files:
        raise RuntimeError('Auxiliary dossier was not preserved byte for byte')
    for row in narrative_rows:
        if sha(destination / row['copied_to']) != row['sha256'] or sha(row['source']) != row['sha256']:
            raise RuntimeError('Narrative changed during packaging')
    for name, node in nodes.items():
        if sha(source / node['path']) != node['sha256'] or sha(destination / 'lean' / node['path']) != node['sha256']:
            raise RuntimeError('Lean source changed during packaging: ' + name)
    preservation = dict(schema='hmt.normal.coherence.preservation.v1',
                        status='PASS_FULL_PREDECESSOR_PRESERVATION',
                        previous_manifest_sha256=PREVIOUS_MANIFEST_SHA,
                        previous_receipt_sha256=PREVIOUS_RECEIPT_SHA,
                        previous_files=list(before.values()),
                        narratives=narrative_rows, auxiliary_files=list(auxiliary_files.values()),
                        provenance_is_not_a_principal_lean_dependency=True)
    write_json(destination / 'VERIFICACION_CONSERVACION.json', preservation)
    inventory = files_under(destination)
    manifest = dict(schema='hmt.normal.coherence.successor.v1',
                    generated_at_utc=datetime.now(timezone.utc).isoformat(),
                    previous_directory='antecedente', original_279_base='antecedente/antecedente',
                    previous_manifest_sha256=PREVIOUS_MANIFEST_SHA,
                    previous_receipt_sha256=PREVIOUS_RECEIPT_SHA,
                    previous_modules_preserved=old['delta_modules'],
                    source_closure=order,
                    genuinely_added_modules=result['genuinely_added_modules'],
                    direct_inherited_imports=inherited, external_imports=external,
                    focal_receipt='recibos/coherencia/VERIFICATION.json',
                    focal_receipt_sha256=sha(receipt_file),
                    public_declarations=receipt['public_declaration_count'],
                    theorem_names=receipt['theorem_names'],
                    allowed_new_axioms=receipt['allowed_new_axioms'],
                    inherited_axiom_exception=receipt['inherited_axiom_exception'],
                    narratives=narrative_rows, auxiliary_is_principal_dependency=False,
                    files=list(inventory.values()))
    write_json(destination / 'MANIFIESTO.json', manifest)
    complete = files_under(destination)
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
        for relative in complete:
            zipped.write(destination / relative, arcname=destination.name + '/' + relative)
    with zipfile.ZipFile(archive) as zipped:
        if zipped.testzip() is not None or len(zipped.namelist()) != len(complete):
            raise RuntimeError('ZIP CRC or entry-count check failed')
        for relative, row in complete.items():
            if hashlib.sha256(zipped.read(destination.name + '/' + relative)).hexdigest() != row['sha256']:
                raise RuntimeError('ZIP member differs from source: ' + relative)
    result.update(status='PASS_NORMAL_COHERENCE_DELIVERY', files=len(complete),
                  manifested_files=len(inventory), zip_sha256=sha(archive),
                  manifest_sha256=sha(destination / 'MANIFIESTO.json'),
                  compilation_replayed_during_packaging=False,
                  all_focal_sources_and_objects_authenticated=True)
    write_json(destination.parent / (destination.name + '_ENTREGA.json'), result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
