#!/usr/bin/env python3
"""Package one verified orbifold-input/half-integer increment; never compile.

The entire 2228-file vertex-conformal predecessor is copied exactly once.
The receipt and final human README must both be explicitly pinned. Counts and
source names come from that successful receipt, not from development globs.
--plan validates inputs without creating a package. Actual sealing performs a
single relocated source plan, then verifies every ZIP entry by CRC and SHA.
"""
import argparse
import copy
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
OLD_MANIFEST = '9adef915383dded4ba6a1e26a50828f501264472ac154914f098e76091aae3d0'
PREVIOUS_PACKAGER = 'b27ae758a6e6763eb4d7b190d935a78c9b089e2fce80a934ad4c7c158b801892'
PACKAGING_HELPER = '1ab909fed05cd8dfbde1d5d2a65a8caa1a84d88d3b35e9b1d9d1d80f9bb52d84'
RUNNER_SHA = 'de7770bccc4291cc483b2a7b5e7b6a8f43005c96253fc7ad17f368ef7f56ab08'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wrapper(requested):
    return '''#!/usr/bin/env python3
"""Replay only the delivered increment after authenticating its predecessors."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
old = root/'antecedente'
path = root/'verificar_orbifold.py'
spec = importlib.util.spec_from_file_location('hmt_orbifold_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules', *''' + repr(requested) + ''']
for flag, value in [
    ('--orbifold-root', root/'lean/orbifold'),
    ('--twisted-root', root/'lean/twisted'),
    ('--products-helper', old/'verificar_productos.py'),
    ('--vertex-helper', old/'verificar_conforme.py'),
    ('--vertex-root', old/'lean/vertex'),
    ('--conformal-root', old/'lean/conformal'),
    ('--involution-root', old/'lean/involution'),
    ('--products-report-dir', old/'recibos/productos'),
    ('--conformal-report-dir', old/'recibos/conforme'),
    ('--involution-report-dir', old/'recibos/involucion'),
    ('--translation-root', old/'antecedente/lean'),
    ('--translation-report-dir', old/'antecedente/recibos/traslacion'),
    ('--locality-root', old/'antecedente/antecedente/lean'),
    ('--locality-report-dir', old/'antecedente/antecedente/recibos/localidad_estados'),
    ('--generator-locality-report-dir', old/'antecedente/antecedente/recibos/localidad_generadores'),
    ('--coherence-root', old/'antecedente/antecedente/antecedente/lean'),
    ('--coherence-report-dir', old/'antecedente/antecedente/antecedente/recibos/coherencia'),
    ('--helper', old/'antecedente/antecedente/antecedente/verificar_delta.py'),
    ('--locality-helper', old/'antecedente/antecedente/verificar_localidad.py'),
    ('--translation-helper', old/'antecedente/verificar_traslacion.py'),
    ('--base', old/'antecedente/antecedente/antecedente/antecedente/antecedente'),
    ('--report-dir', root/'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag, str(value)]
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
'''


def causal_successor(helper, previous, dest, receipt, receipt_sha, owners):
    old_path = previous/'recibos/CAUSAL_VERTEX_CONFORME.json'
    causal = copy.deepcopy(helper.read(old_path))
    causal.update(artifact=str(dest/'README.md'), artifact_sha256=helper.sha(dest/'README.md'),
        result_id='LATTICE_PARITY_FINITE_QUOTIENT_HALF_INTEGER_VIRASORO_20260921',
        verification_receipt='recibos/incremento/VERIFICATION.json',
        verification_receipt_sha256=receipt_sha, compiled_modules=len(receipt['modules']),
        authenticated_predecessor_modules=354, reused_authenticated_modules=354,
        public_declarations=receipt['public_declaration_count'],
        theorem_lemma_count=len(receipt['theorem_names']))
    causal['inherited_context'] = dict(source='antecedente/recibos/CAUSAL_VERTEX_CONFORME.json',
        sha256=helper.sha(old_path), scope='The complete prior genealogy is preserved, '
        'not re-proved by this metadata. The delta reuses its marked lattice, '
        'cocycle and vertex-field realization without a new K selection.')
    causal['posterior_realization'] = dict(
        operator='Reuse the same marked lattice, pairing, integral coordinates, '
        'cocycle and theta; retain its untwisted fixed subspace and construct '
        'half-integer oscillator operators from the same symmetric algebra.',
        action='Restrict products and weights to the fixed subspace; construct '
        'the negation quotient from the existing central extension and its '
        'parity pairing; form locally finite half-integer quadratic modes and '
        'derive the vacuum shift and recorded Virasoro commutators. These are '
        'posterior realizations, not renamed TPK operators.')
    causal['genealogy']['source_locators'] = [
        'antecedente/'+x if x.startswith(('lean/', 'antecedente/')) else x
        for x in causal['genealogy']['source_locators']]
    causal['genealogy']['source_locators'] += sorted(owners.values())
    focal = causal['focal_genealogical_receipt']
    # Preserve the inherited APP/TRIT/TPK objects and effective-composition
    # field literally. New field/Fock/group operations are typed separately;
    # they are not installed retrospectively as new TPK generators.
    focal['4_coefficient_origins'] = (
        'Half-integer frequencies come from the negation-twisted indexing '
        'm+1/2, and the Gram inverse is inherited from the same pairing. '
        'The rank/16 vacuum shift is forced by the (1,-1) commutator, '
        'not supplied as an independently fitted value. At the proved rank '
        '24 the vacuum shift is 3/2. The central coefficient is obtained '
        'from the actual quadratic modes and their vacuum contractions.')
    focal['5_conserved_information'] = (
        'The selected origin, lattice, Gram pairing, cocycle, theta and '
        'upstream enriched-history provenance remain unchanged. All 2228 '
        'previous files are preserved exactly once. The fixed subspace, '
        'half-integer Fock realization and finite quotient have distinct '
        'declared types; no false identification of carriers is used.')
    focal['7_produced_output'] = (
        'The exact public assertions in the successful increment receipt: '
        'fixed-space products and grading; finite negation quotient and '
        'its recorded center/parity properties; half-integer oscillator '
        'fields, quadratic operators, vacuum shift and Virasoro identities. '
        'No stronger orbifold product or automorphism-group conclusion is '
        'deduced from the number of source files.')
    focal['8_posterior_recognition_and_falsifier'] = (
        'Half-integer and Virasoro terminology recognizes the operators '
        'after their identities are proved. A changed lattice or cocycle, '
        'incorrect half-frequency, unproved normal-sum finiteness, inserted '
        'vacuum shift, failed kernel identity or new native axiom invalidates '
        'this delta. The finite quotient is not its irreducible module, and '
        'these results do not by themselves prove the full twisted lattice '
        'module, orbifold multiplication, FLM theorem or Aut(Vnatural)=Monster.')
    focal['9_material_owners'] = sorted(owners.values())
    scope = causal['formalization_scope']
    scope.update(new_result=focal['7_produced_output'],
        same_carrier_as_predecessor=False, same_marked_lattice_as_predecessor=True,
        new_K_selection=False, new_native_evaluation=False,
        ordinary_modules_axioms=sorted(ORDINARY),
        selected_specialization_inherits=[], inherited_native_declarations=[],
        not_claimed=['Full twisted lattice module and orbifold multiplication',
            'FLM theorem or full automorphism-group identification with the Monster',
            'Fresh proof of all inherited contextual assertions'])
    causal['added_source_modules'] = sorted(owners)
    return causal


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
declaraciones públicas. Ambas reutilizan los 354 módulos anteriores después
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
        default=outputs/'PAQUETE_ARTICULO_I_SECTOR_TORCIDO_VIRASORO_20260921')
    p.add_argument('--report-dir', type=Path, default=here/'orbifold_closed_results')
    p.add_argument('--receipt-sha256', required=True)
    p.add_argument('--readme', type=Path, default=here/'README_SECTOR_TORCIDO.md')
    p.add_argument('--readme-sha256', required=True)
    p.add_argument('--genealogy-receipt', type=Path)
    p.add_argument('--genealogy-receipt-sha256')
    p.add_argument('--genealogy-check', type=Path)
    p.add_argument('--genealogy-check-sha256')
    p.add_argument('--require-modules', nargs='*', default=[])
    p.add_argument('--plan', action='store_true')
    args = p.parse_args()
    dest, reportdir, readme = [x.expanduser().resolve()
        for x in (args.destination, args.report_dir, args.readme)]
    previous = outputs/'PAQUETE_ARTICULO_I_VERTEX_CONFORME_20260921'
    old_packager = here.parent/'vertex_extension/package_vertex_conformal.py'
    if hashlib.sha256(old_packager.read_bytes()).hexdigest() != PREVIOUS_PACKAGER:
        raise RuntimeError('Previous packaging implementation changed')
    previous_packager = load(old_packager, 'frozen_vertex_packaging')
    helper_path = here.parent/'translation_coherence/package_translation_coherence.py'
    if hashlib.sha256(helper_path.read_bytes()).hexdigest() != PACKAGING_HELPER:
        raise RuntimeError('Packaging inventory helper changed')
    if previous_packager.PACKAGING_HELPER != PACKAGING_HELPER:
        raise RuntimeError('Inconsistent inherited packaging helper')
    helper = previous_packager.load(helper_path, 'frozen_inventory_packaging')
    helper.require_hash(previous/'MANIFIESTO.json', OLD_MANIFEST)
    old = helper.read(previous/'MANIFIESTO.json')
    before = helper.inventory(previous)
    if len(before) != 2228 or set(before) != {r['path'] for r in old['files']} | {'MANIFIESTO.json'}:
        raise RuntimeError('Expected the entire manifest-covered 2228-file predecessor')
    for row in old['files']:
        if before.get(row['path']) != row:
            raise RuntimeError('Changed predecessor: '+row['path'])
    helper.require_hash(reportdir/'VERIFICATION.json', args.receipt_sha256)
    receipt = helper.read(reportdir/'VERIFICATION.json')
    if (receipt['status'] != 'PASS_ORBIFOLD_INPUT_DELTA'
            or receipt['inherited_module_count'] != 354
            or not receipt['authenticated_inputs_unchanged']
            or receipt['predecessors_modified'] or receipt['predecessors_recompiled']
            or receipt['mathlib_rebuilt'] or not receipt['compiler_invoked']):
        raise RuntimeError('Final integrated PASS is required before copying or sealing')
    runner_path = here/'verify_orbifold_input.py'
    helper.require_hash(runner_path, RUNNER_SHA)
    if receipt['runner_sha256'] != RUNNER_SHA:
        raise RuntimeError('Receipt does not belong to the frozen increment runner')
    helper.require_hash(readme, args.readme_sha256)
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
    runner = load(runner_path, 'frozen_orbifold_verifier')
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
    roots = dict(orbifold=here, twisted=here.parent/'twisted_sector')
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
    result = dict(status='PASS_ORBIFOLD_PACKAGE_INPUTS', previous_files=len(before),
        added_source_modules=len(sources), authenticated_modules=354+len(sources),
        public_declarations=receipt['public_declaration_count'],
        theorem_lemma_count=len(receipt['theorem_names']), destination=str(dest),
        compilation_repeated=False, receipt_sha256=args.receipt_sha256,
        readme_sha256=args.readme_sha256)
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
    shutil.copy2(runner_path, dest/'verificar_orbifold.py')
    shutil.copy2(readme, dest/'README.md')
    (dest/'reproducir.py').write_text(wrapper(receipt['requested_modules']), encoding='utf-8')
    (dest/'REPRODUCCION.md').write_text(reproduction_readme(receipt), encoding='utf-8')
    history = dest/'historia'
    history.mkdir()
    shutil.copy2(__file__, history/'package_orbifold_input.py')
    shutil.copy2(here/'PLAN_EMPAQUETADO_SUCESOR.md', history/'PLAN_EMPAQUETADO_SUCESOR.md')
    causalpath = dest/'recibos/CAUSAL.json'
    helper.write(causalpath, causal_successor(helper, previous, dest, receipt,
        args.receipt_sha256, owners))
    gate = Path.home()/'.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py'
    audit = subprocess.run([sys.executable, '-I', '-S', str(gate), '--audit',
        str(dest/'README.md'), '--receipt', str(causalpath)], text=True, capture_output=True)
    helper.write(dest/'recibos/CONTROL_CAUSAL.json', dict(exit_code=audit.returncode,
        stdout=audit.stdout, stderr=audit.stderr, gate_sha256=helper.sha(gate),
        artifact_sha256=helper.sha(dest/'README.md'), receipt_sha256=helper.sha(causalpath),
        is_lean_theorem_verification=False))
    if audit.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in audit.stdout:
        raise RuntimeError('Causal audit failed: '+audit.stdout+audit.stderr)
    with tempfile.TemporaryDirectory(prefix='hmt-orbifold-relocation-', dir=dest.parent) as temp:
        temp = Path(temp)
        relocated = temp/'paquete_relocalizado'
        dest.rename(relocated)
        try:
            replay = subprocess.run([sys.executable, '-I', '-S', str(relocated/'reproducir.py'),
                '--plan', '--report-dir', str(temp/'plan')], cwd=temp, text=True, capture_output=True)
            if replay.returncode:
                raise RuntimeError('Relocated replay failed: '+replay.stdout+replay.stderr)
            plan = helper.read(temp/'plan/PLAN.json')
            if (plan['status'] != 'PASS_ORBIFOLD_INPUT_SOURCE_PLAN_NOT_COMPILED'
                    or plan['compiler_invoked'] or plan['modules']
                    or plan['inherited_module_count'] != 354
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
    helper.require_hash(dest/'verificar_orbifold.py', RUNNER_SHA)
    for source, digest, name in genealogy_files:
        helper.require_hash(source, digest)
        helper.require_hash(dest/'recibos'/name, digest)
    helper.write(dest/'VERIFICACION_CONSERVACION.json', dict(
        status='PASS_COMPLETE_2228_FILE_PREDECESSOR_AND_VERIFIED_INCREMENT',
        previous_manifest_sha256=OLD_MANIFEST, previous_files=list(before.values()),
        increment_files=list(report_before.values()), source_modules=owners,
        source_compilation_repeated=False, predecessor_copied_exactly_once=True))
    helper.write(dest/'MANIFIESTO.json', dict(schema='hmt.orbifold.input.successor.v1',
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
    result.update(status='PASS_ORBIFOLD_HALF_VIRASORO_DELIVERY', files=len(complete),
        manifest_sha256=helper.sha(dest/'MANIFIESTO.json'), zip_sha256=helper.sha(archive),
        zip_verification=str(zip_report), zip_verification_sha256=helper.sha(zip_report),
        relocated_plan_passed=True, causal_focal_audit_passed=True)
    helper.write(delivery, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
