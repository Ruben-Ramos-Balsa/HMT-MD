#!/usr/bin/env python3
"""Package one verified finite-module increment after cut 371; never compile.

The entire 2311-file half-integer/Virasoro predecessor is copied exactly once.
The receipt and final human README must both be explicitly pinned. Counts and
source names come from that successful receipt, not from development globs.
--plan validates inputs without creating a package. Actual sealing performs a
single relocated source plan, then verifies every ZIP entry by CRC and SHA.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile
import zlib

sys.dont_write_bytecode = True
OLD_MANIFEST = '32d7cdb8d337a7d0bced4d88f3e279f516de7376169222fd17930b8f49a91437'
PREVIOUS_PACKAGER = '46635a40234cd1eaa2a5273fcd4649152c4365c16d71365c157937a0147fe83e'
PACKAGING_HELPER = '1ab909fed05cd8dfbde1d5d2a65a8caa1a84d88d3b35e9b1d9d1d80f9bb52d84'
RUNNER_SHA = '08e919e68c1928ae1d8b09e232e1b95ba2cc313427c9a000a2d0acbd4424d846'
CONTRACT_RECEIPT_SHA = 'c20ac7c59abf9845aba1a7c01878e432b3b7437e6e48f386ddd27c418ce4eaad'
CONTRACT_NOTE_SHA = '402c1fddb654ef0e49bb6133dccfa3bd420b1b25629794cd390b0b5936ab8800'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wrapper(requested):
    return '''#!/usr/bin/env python3
"""Replay only the delivered finite-module delta; never auto-run from USB."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
old = root/'antecedente'
vertex = old/'antecedente'
path = root/'verificar_modulo_finito.py'
spec = importlib.util.spec_from_file_location('hmt_finite_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules', *''' + repr(requested) + ''']
for flag, value in [
    ('--finite-root', root/'lean/finite'),
    ('--orbifold-root', old/'lean/orbifold'),
    ('--twisted-root', old/'lean/twisted'),
    ('--orbifold-helper', old/'verificar_orbifold.py'),
    ('--orbifold-report-dir', old/'recibos/incremento'),
    ('--products-helper', vertex/'verificar_productos.py'),
    ('--vertex-helper', vertex/'verificar_conforme.py'),
    ('--vertex-root', vertex/'lean/vertex'),
    ('--conformal-root', vertex/'lean/conformal'),
    ('--involution-root', vertex/'lean/involution'),
    ('--products-report-dir', vertex/'recibos/productos'),
    ('--conformal-report-dir', vertex/'recibos/conforme'),
    ('--involution-report-dir', vertex/'recibos/involucion'),
    ('--translation-root', vertex/'antecedente/lean'),
    ('--translation-report-dir', vertex/'antecedente/recibos/traslacion'),
    ('--locality-root', vertex/'antecedente/antecedente/lean'),
    ('--locality-report-dir', vertex/'antecedente/antecedente/recibos/localidad_estados'),
    ('--generator-locality-report-dir', vertex/'antecedente/antecedente/recibos/localidad_generadores'),
    ('--coherence-root', vertex/'antecedente/antecedente/antecedente/lean'),
    ('--coherence-report-dir', vertex/'antecedente/antecedente/antecedente/recibos/coherencia'),
    ('--helper', vertex/'antecedente/antecedente/antecedente/verificar_delta.py'),
    ('--locality-helper', vertex/'antecedente/antecedente/verificar_localidad.py'),
    ('--translation-helper', vertex/'antecedente/verificar_traslacion.py'),
    ('--base', vertex/'antecedente/antecedente/antecedente/antecedente/antecedente'),
    ('--report-dir', root/'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag, str(value)]
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
'''


def reproduction_readme(receipt):
    return f'''# Reproducción del incremento entregado

Esta carpeta y su ZIP contienen los mismos archivos. Descomprima el ZIP una
sola vez si utiliza esa presentación. Conectar un USB **no ejecuta nada**:
las órdenes siguientes se lanzan explícitamente desde una terminal situada
en esta carpeta.

```sh
python3 -I -S reproducir.py --plan --report-dir plan_nuevo
python3 -I -S reproducir.py --report-dir resultados_nuevos
```

La primera orden autentica fuentes, dependencias y objetos; no compila y no
equivale a demostrar. La segunda compila únicamente los {len(receipt['modules'])}
módulos nuevos del recibo y consulta sus {receipt['public_declaration_count']}
declaraciones públicas. Ambas reutilizan los 371 módulos anteriores después
de autentificarlos; no reconstruyen Mathlib. Use un directorio de resultados
nuevo para cada ejecución: los recibos originales quedan en `recibos/`.

El runtime externo debe ser Lean 4.21.0 y el checkout de Mathlib cuyo commit
figura en `recibos/incremento/VERIFICATION.json`, junto con su biblioteca y
dependencias ya compiladas. No se descarga ni instala software automáticamente.
En otra máquina se pueden indicar sus ubicaciones:

```sh
python3 -I -S reproducir.py --lean /ruta/bin/lean --mathlib /ruta/mathlib4 \\
  --report-dir resultados_nuevos
```

`README.md` explica los resultados y su alcance. `lean/` contiene las nuevas
fuentes; `antecedente/` conserva íntegra la entrega anterior; el manifiesto
identifica cada archivo. El control documental causal, la preservación de
archivos y las comprobaciones Lean son controles distintos. Este ejecutor
reproduce las declaraciones enumeradas, no añade una afirmación de cierre
completo del producto orbifold, FLM o del grupo de automorfismos del Monstruo.
'''


def main():
    here = Path(__file__).resolve().parent
    outputs = next(p for p in here.parents if p.name == 'output')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destination', type=Path,
        default=outputs/'PAQUETE_ARTICULO_I_MODULO_FINITO_TORCIDO_20260921')
    p.add_argument('--verification', type=Path,
        default=here/'finite_incremental_results/VERIFICATION.json')
    p.add_argument('--receipt-sha256', required=True)
    p.add_argument('--readme', type=Path, default=here/'README_MODULO_FINITO.md')
    p.add_argument('--readme-sha256', required=True)
    p.add_argument('--causal-receipt', type=Path, required=True,
        help='Approved focal metadata; copied verbatim, not generated by this builder')
    p.add_argument('--causal-receipt-sha256', required=True)
    p.add_argument('--genealogy-receipt', type=Path)
    p.add_argument('--genealogy-receipt-sha256')
    p.add_argument('--genealogy-check', type=Path)
    p.add_argument('--genealogy-check-sha256')
    p.add_argument('--require-modules', nargs='*', default=[])
    p.add_argument('--plan', action='store_true')
    args = p.parse_args()
    dest, verification, readme, causal_source = [x.expanduser().resolve()
        for x in (args.destination, args.verification, args.readme, args.causal_receipt)]
    reportdir = verification.parent
    if verification.name != 'VERIFICATION.json':
        raise RuntimeError('The integrated receipt must be named VERIFICATION.json')
    previous = outputs/'PAQUETE_ARTICULO_I_SECTOR_TORCIDO_VIRASORO_20260921'
    old_packager = here.parent/'orbifold_input/package_orbifold_input.py'
    if hashlib.sha256(old_packager.read_bytes()).hexdigest() != PREVIOUS_PACKAGER:
        raise RuntimeError('Previous packaging implementation changed')
    previous_packager = load(old_packager, 'frozen_orbifold_packaging')
    helper_path = here.parent/'translation_coherence/package_translation_coherence.py'
    if hashlib.sha256(helper_path.read_bytes()).hexdigest() != PACKAGING_HELPER:
        raise RuntimeError('Packaging inventory helper changed')
    if previous_packager.PACKAGING_HELPER != PACKAGING_HELPER:
        raise RuntimeError('Inconsistent inherited packaging helper')
    helper = previous_packager.load(helper_path, 'frozen_inventory_packaging')
    helper.require_hash(previous/'MANIFIESTO.json', OLD_MANIFEST)
    old = helper.read(previous/'MANIFIESTO.json')
    before = helper.inventory(previous)
    if len(before) != 2311 or set(before) != {r['path'] for r in old['files']} | {'MANIFIESTO.json'}:
        raise RuntimeError('Expected the entire manifest-covered 2311-file predecessor')
    for row in old['files']:
        if before.get(row['path']) != row:
            raise RuntimeError('Changed predecessor: '+row['path'])
    helper.require_hash(verification, args.receipt_sha256)
    receipt = helper.read(verification)
    if (receipt['status'] != 'PASS_FINITE_MODULE_DELTA'
            or receipt['inherited_module_count'] != 371
            or not receipt['authenticated_inputs_unchanged']
            or receipt['predecessors_modified'] or receipt['predecessors_recompiled']
            or receipt['mathlib_rebuilt'] or not receipt['compiler_invoked']):
        raise RuntimeError('Final integrated PASS is required before copying or sealing')
    runner_path = here/'verify_finite_module.py'
    helper.require_hash(runner_path, RUNNER_SHA)
    if receipt['runner_sha256'] != RUNNER_SHA:
        raise RuntimeError('Receipt does not belong to the frozen increment runner')
    helper.require_hash(readme, args.readme_sha256)
    helper.require_hash(causal_source, args.causal_receipt_sha256)
    causal = helper.read(causal_source)
    if (Path(causal['artifact']).resolve() != dest/'README.md'
            or causal.get('artifact_sha256') != args.readme_sha256
            or causal.get('verification_receipt_sha256') != args.receipt_sha256):
        raise RuntimeError('Approved causal metadata must identify this destination, README and verification')
    contract_files = [
        (here/'CONTINUIDAD_CONTRATO_20260921.json', CONTRACT_RECEIPT_SHA),
        (here/'CONTINUIDAD_CONTRATO_20260921.md', CONTRACT_NOTE_SHA)]
    for source, digest in contract_files:
        helper.require_hash(source, digest)
    genealogy_files = []
    if any((args.genealogy_receipt, args.genealogy_receipt_sha256,
            args.genealogy_check, args.genealogy_check_sha256)):
        if not all((args.genealogy_receipt, args.genealogy_receipt_sha256,
                args.genealogy_check, args.genealogy_check_sha256)):
            raise RuntimeError('Supply both genealogy documents with their exact SHA256')
        for source, digest, name in (
                (args.genealogy_receipt, args.genealogy_receipt_sha256, 'GENEALOGIA_V4.json'),
                (args.genealogy_check, args.genealogy_check_sha256, 'CONTROL_GENEALOGIA_V4.json')):
            source = source.expanduser().resolve()
            helper.require_hash(source, digest)
            genealogy_files.append((source, digest, name))
    runner = load(runner_path, 'frozen_finite_verifier')
    products = runner.load(here.parent/'vertex_extension/verify_vertex_products.py',
        runner.PRODUCTS_RUNNER_SHA, 'frozen_products_packaging')
    vertex = runner.load(here.parent/'vertex_extension/verify_vertex_extension.py',
        products.PREDECESSOR_RUNNER_SHA, 'frozen_vertex_packaging_verifier')
    state = runner.load(here.parent/'state_field/verify_state_field.py',
        products.HELPER_SHA, 'frozen_state_packaging_verifier')
    verifier, *_ = state.authenticate_base(Path(receipt['base']))
    vertex.check_probe(verifier, receipt, receipt['public_declaration_owners'])
    if (receipt['allowed_delta_axioms'] != sorted(ORDINARY)
            or not set(receipt['axioms']) <= ORDINARY):
        raise RuntimeError('Unexpected increment axiom policy')
    roots = dict(finite=here)
    rows = {row['module']:row for row in receipt['modules']}
    if (len(rows) != len(receipt['modules']) or rows.keys() != receipt['sources'].keys()
            or set(receipt['dependency_order']) != rows.keys()
            or len(receipt['dependency_order']) != len(rows)):
        raise RuntimeError('Inconsistent increment module closure')
    if not set(args.require_modules) <= rows.keys():
        raise RuntimeError('Required module omitted from the integrated receipt')
    sources, owners = {}, {}
    for name, node in receipt['sources'].items():
        rootkey, relative = node['root'], node['path']
        if rootkey not in roots or relative != name+'.lean':
            raise RuntimeError('Unsafe new source path: '+str(node))
        source = roots[rootkey]/relative
        row = rows[name]
        helper.require_hash(source, node['sha256'])
        helper.require_hash(reportdir/'build'/(name+'.lean'), node['sha256'])
        helper.require_hash(reportdir/'build'/(name+'.olean'), row['object_sha256'])
        if row['exit_code'] or row['source_sha256'] != node['sha256']:
            raise RuntimeError('Failed or changed module: '+name)
        sources[name] = dict(source=source, root=rootkey, path=relative, sha256=node['sha256'])
        owners[name] = 'lean/'+rootkey+'/'+relative
    report_before = helper.inventory(reportdir)
    archive = dest.with_suffix('.zip')
    delivery = dest.parent/(dest.name+'_ENTREGA.json')
    zip_report = dest.parent/(dest.name+'_ZIP_VERIFICACION.json')
    if (dest.is_relative_to(previous) or previous.is_relative_to(dest)
            or dest.is_relative_to(reportdir) or reportdir.is_relative_to(dest)):
        raise RuntimeError('Destination overlaps predecessor or integrated report')
    if any(x.exists() for x in (dest, archive, delivery, zip_report)):
        raise RuntimeError('Refusing to overwrite an existing successor or seal')
    result = dict(status='PASS_FINITE_PACKAGE_INPUTS', previous_files=len(before),
        added_source_modules=len(sources), authenticated_modules=371+len(sources),
        public_declarations=receipt['public_declaration_count'],
        theorem_lemma_count=len(receipt['theorem_names']), destination=str(dest),
        compilation_repeated=False, receipt_sha256=args.receipt_sha256,
        readme_sha256=args.readme_sha256, causal_receipt_sha256=args.causal_receipt_sha256)
    if args.plan:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    dest.mkdir(parents=True)
    shutil.copytree(previous, dest/'antecedente')
    for row in sources.values():
        target = dest/'lean'/row['root']/row['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(row['source'], target)
    shutil.copytree(reportdir, dest/'recibos/incremento')
    for source, digest, name in genealogy_files:
        shutil.copy2(source, dest/'recibos'/name)
        helper.require_hash(dest/'recibos'/name, digest)
    shutil.copy2(runner_path, dest/'verificar_modulo_finito.py')
    shutil.copy2(readme, dest/'README.md')
    (dest/'reproducir.py').write_text(wrapper(receipt['requested_modules']), encoding='utf-8')
    (dest/'REPRODUCCION.md').write_text(reproduction_readme(receipt), encoding='utf-8')
    history = dest/'historia'
    history.mkdir()
    shutil.copy2(__file__, history/'package_finite_module.py')
    for source, digest in contract_files:
        shutil.copy2(source, history/source.name)
        helper.require_hash(history/source.name, digest)
    causalpath = dest/'recibos/CAUSAL.json'
    shutil.copy2(causal_source, causalpath)
    helper.require_hash(causalpath, args.causal_receipt_sha256)
    gate = Path.home()/'.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py'
    audit = subprocess.run([sys.executable, '-I', '-S', str(gate), '--audit',
        str(dest/'README.md'), '--receipt', str(causalpath)], text=True, capture_output=True)
    helper.write(dest/'recibos/CONTROL_CAUSAL.json', dict(exit_code=audit.returncode,
        stdout=audit.stdout, stderr=audit.stderr, gate_sha256=helper.sha(gate),
        artifact_sha256=helper.sha(dest/'README.md'), receipt_sha256=helper.sha(causalpath),
        is_lean_theorem_verification=False))
    if audit.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in audit.stdout:
        raise RuntimeError('Causal audit failed: '+audit.stdout+audit.stderr)
    with tempfile.TemporaryDirectory(prefix='hmt-finite-relocation-', dir=dest.parent) as temp:
        temp = Path(temp)
        relocated = temp/'paquete_relocalizado'
        dest.rename(relocated)
        try:
            replay = subprocess.run([sys.executable, '-I', '-S', str(relocated/'reproducir.py'),
                '--plan', '--report-dir', str(temp/'plan')], cwd=temp, text=True, capture_output=True)
            if replay.returncode:
                raise RuntimeError('Relocated replay failed: '+replay.stdout+replay.stderr)
            plan = helper.read(temp/'plan/PLAN.json')
            if (plan['status'] != 'PASS_FINITE_MODULE_SOURCE_PLAN_NOT_COMPILED'
                    or plan['compiler_invoked'] or plan['modules']
                    or plan['inherited_module_count'] != 371
                    or plan['sources'] != receipt['sources']
                    or plan['dependency_order'] != receipt['dependency_order']
                    or plan['public_declaration_owners'] != receipt['public_declaration_owners']
                    or not plan['authenticated_inputs_unchanged']):
                raise RuntimeError('Relocated source closure differs from the compiled closure')
            helper.write(relocated/'recibos/REPRODUCCION_RELOCALIZADA.json', plan)
        finally:
            relocated.rename(dest)
    if helper.inventory(previous) != before or helper.inventory(dest/'antecedente') != before:
        raise RuntimeError('Predecessor preservation mismatch')
    if (helper.inventory(reportdir) != report_before
            or helper.inventory(dest/'recibos/incremento') != report_before):
        raise RuntimeError('Integrated receipt/build changed while packaging')
    for row in sources.values():
        helper.require_hash(row['source'], row['sha256'])
        helper.require_hash(dest/'lean'/row['root']/row['path'], row['sha256'])
    helper.require_hash(readme, args.readme_sha256)
    helper.require_hash(dest/'README.md', args.readme_sha256)
    helper.require_hash(dest/'verificar_modulo_finito.py', RUNNER_SHA)
    helper.require_hash(causal_source, args.causal_receipt_sha256)
    helper.require_hash(causalpath, args.causal_receipt_sha256)
    for source, digest in contract_files:
        helper.require_hash(source, digest)
        helper.require_hash(history/source.name, digest)
    for source, digest, name in genealogy_files:
        helper.require_hash(source, digest)
        helper.require_hash(dest/'recibos'/name, digest)
    helper.write(dest/'VERIFICACION_CONSERVACION.json', dict(
        status='PASS_COMPLETE_2311_FILE_PREDECESSOR_AND_VERIFIED_INCREMENT',
        previous_manifest_sha256=OLD_MANIFEST, previous_files=list(before.values()),
        increment_files=list(report_before.values()), source_modules=owners,
        source_compilation_repeated=False, predecessor_copied_exactly_once=True))
    helper.write(dest/'MANIFIESTO.json', dict(schema='hmt.finite.module.successor.v1',
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        predecessor='antecedente', previous_manifest_sha256=OLD_MANIFEST,
        verification_receipt='recibos/incremento/VERIFICATION.json',
        verification_receipt_sha256=args.receipt_sha256,
        exact_source_modules=owners, total_authenticated_modules=result['authenticated_modules'],
        new_declaration_axioms=sorted(ORDINARY), files=list(helper.inventory(dest).values())))
    complete = helper.inventory(dest)
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for name in complete:
            bundle.write(dest/name, dest.name+'/'+name)
    entries = []
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None or len(bundle.namelist()) != len(complete):
            raise RuntimeError('ZIP CRC or count mismatch')
        for name, row in complete.items():
            path = dest.name+'/'+name
            data = bundle.read(path)
            digest, crc = hashlib.sha256(data).hexdigest(), zlib.crc32(data) & 0xffffffff
            info = bundle.getinfo(path)
            if digest != row['sha256'] or len(data) != row['bytes'] or crc != info.CRC:
                raise RuntimeError('ZIP entry changed: '+name)
            entries.append(dict(path=path, bytes=len(data), sha256=digest, crc32=f'{crc:08x}'))
    helper.write(zip_report, dict(status='PASS_ZIP_CRC_AND_SHA256_EVERY_ENTRY',
        archive=str(archive), archive_sha256=helper.sha(archive), entries=entries))
    if (helper.inventory(dest) != complete or helper.inventory(previous) != before
            or helper.inventory(reportdir) != report_before):
        raise RuntimeError('A source/delivery changed during sealing')
    helper.require_hash(readme, args.readme_sha256)
    result.update(status='PASS_FINITE_MODULE_DELIVERY', files=len(complete),
        manifest_sha256=helper.sha(dest/'MANIFIESTO.json'), zip_sha256=helper.sha(archive),
        zip_verification=str(zip_report), zip_verification_sha256=helper.sha(zip_report),
        relocated_plan_passed=True, causal_focal_audit_passed=True, mathematical_certificates_created=False)
    helper.write(delivery, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
