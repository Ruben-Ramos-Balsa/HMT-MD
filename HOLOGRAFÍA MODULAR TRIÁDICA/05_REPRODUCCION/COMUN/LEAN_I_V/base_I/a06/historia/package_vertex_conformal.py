#!/usr/bin/env python3
"""Package the frozen, verified vertex/conformal successor without compiling.

The 2076-file translation predecessor is copied once and preserved byte for
byte. Sources and full receipts/builds for involution (2), conformal (17),
and the exact successful products closure are then added. A relocated --plan
uses the existing verifier and its configurable paths. No FLM claim is made.
Nothing is copied or sealed unless the final products receipt is PASS and its
SHA-256 is explicitly supplied. --plan authenticates inputs without writing.
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
OLD_MANIFEST = '34060cbd1691968f4f17df7b592440f159a52f793f626266fc762863e172e3b6'
PACKAGING_HELPER = '1ab909fed05cd8dfbde1d5d2a65a8caa1a84d88d3b35e9b1d9d1d80f9bb52d84'
INVOLUTION_RECEIPT = 'ba709864f60103749e18864ff1c2261d0e718a21e4cbdfbeda1990e344d55318'
CONFORMAL_RECEIPT = 'd77a961bb9fed30a971654096d311de8f94d3058ad017a8e8397a3b091bcac43'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wrapper(requested):
    return '''#!/usr/bin/env python3
"""Replay only the new vertex/conformal closure on authenticated predecessors."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root/'verificar_productos.py'
spec = importlib.util.spec_from_file_location('hmt_vertex_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args = sys.argv[1:]
defaults = []
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules', *''' + repr(requested) + ''']
for flag, value in [
    ('--vertex-root', root/'lean/vertex'),
    ('--conformal-root', root/'lean/conformal'),
    ('--involution-root', root/'lean/involution'),
    ('--translation-root', root/'antecedente/lean'),
    ('--translation-report-dir', root/'antecedente/recibos/traslacion'),
    ('--locality-root', root/'antecedente/antecedente/lean'),
    ('--locality-report-dir', root/'antecedente/antecedente/recibos/localidad_estados'),
    ('--generator-locality-report-dir', root/'antecedente/antecedente/recibos/localidad_generadores'),
    ('--coherence-root', root/'antecedente/antecedente/antecedente/lean'),
    ('--coherence-report-dir', root/'antecedente/antecedente/antecedente/recibos/coherencia'),
    ('--helper', root/'antecedente/antecedente/antecedente/verificar_delta.py'),
    ('--locality-helper', root/'antecedente/antecedente/verificar_localidad.py'),
    ('--translation-helper', root/'antecedente/verificar_traslacion.py'),
    ('--vertex-helper', root/'verificar_conforme.py'),
    ('--involution-report-dir', root/'recibos/involucion'),
    ('--conformal-report-dir', root/'recibos/conforme'),
    ('--base', root/'antecedente/antecedente/antecedente/antecedente/antecedente'),
    ('--report-dir', root/'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag, str(value)]
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
'''


def make_readme(receipt, count):
    names = '\n'.join('- `'+name+'`' for name in receipt['requested_modules'])
    native = receipt.get('declarations_using_inherited_native_axiom', [])
    native_text = ('La especialización seleccionada conserva `Lean.ofReduceBool` '
        'únicamente en las declaraciones enumeradas por el recibo: ' +
        ', '.join('`'+name+'`' for name in native) + '.') if native else (
        'Ninguna declaración de este bloque nuevo utiliza `Lean.ofReduceBool`.')
    return f'''# Continuación reticular: productos de campos y estructura conforme

Este paquete conserva íntegros los **2076 archivos** del sucesor de traslación
en `antecedente/`. Añade la involución comprobada de todos los campos, el cierre
conforme de 17 módulos y el cierre exacto de productos/Virasoro del recibo final.
Las fuentes añadidas son {count} módulos; las copias en los recibos son sus
testigos de compilación, no desarrollos alternativos.

## Resultado y cadena de reproducción

Se reutiliza el mismo origen seleccionado por APP–TRIT–TPK, el mismo estado
enriquecido, el retículo marcado, la base integral, el cociclo, el vacío y el
mapa estado–campo. No se vuelve a seleccionar K ni se introduce una función
modular o un valor objetivo como generador. La estructura discreta conjunta
del continuo y su procedencia permanecen en el antecedente sin disgregación.

La secuencia nueva es: inversa del Gram derivada → estado cuadrático ω →
modos reales de su campo → `L₀=E` y `L₋₁=T` → conmutador con todos los modos
de Heisenberg → defecto central y recurrencia cúbica → término central
calculado sobre todas las cargas puras → relaciones completas de Virasoro,
con carga central 24 leída del rango ya construido. Los productos residuales
se identifican con los campos de los estados correspondientes; se conserva
la restricción al sector fijo no torcido de la involución.

El recibo `recibos/productos/VERIFICATION.json` contiene
{receipt['public_declaration_count']} declaraciones públicas y
{len(receipt['theorem_names'])} teoremas/lemas del último incremento, después
de autenticar 340 módulos antecedentes. Sus entradas solicitadas son:

{names}

La cadena anterior no es una afirmación de cierre del sector torcido,
la multiplicación orbifold, la identificación del Monster o el teorema FLM.
Esos objetos no se obtienen renombrando el portador ni suponiendo una
interfaz que reciba su conclusión. El alcance exacto está en las declaraciones
Lean, no en el número de archivos. {native_text}

## Contenido

- `lean/vertex`, `lean/conformal`, `lean/involution`: fuentes nuevas reunidas
  según sus propietarios; no se editan las fuentes anteriores.
- `antecedente/`: paquete anterior completo, incluidos sus antecedentes,
  fuentes, demostraciones, programas y documentos de procedencia.
- `recibos/`: registros completos, consultas y objetos compilados autenticados.
  Los `.olean` históricos se conservan; no sustituyen las fuentes ni sus pruebas.
- `MANIFIESTO.json`: ruta, tamaño y SHA-256 de cada archivo entregado.
- `reproducir.py`: entrada única que configura las rutas internas relativas.

## Ejecución

Desde la carpeta desplegada:

```sh
python3 -I -S reproducir.py --plan --report-dir plan_nuevo
python3 -I -S reproducir.py --report-dir resultados_nuevos
```

`--plan` autentica y resuelve las dependencias, pero **no compila ni demuestra**.
La segunda orden compila únicamente el incremento nuevo y consulta todas sus
declaraciones públicas. Los directorios de resultados deben ser nuevos.
Los 340 módulos anteriores se reutilizan tras verificar sus fuentes, objetos,
recibos, compilador y dependencias; Mathlib no se reconstruye.

Se necesita el entorno externo de Lean 4.21.0 y el checkout de Mathlib fijado
por `compiler.mathlib_commit` en el recibo. No se copia otra biblioteca por
cada lema ni se descarga software automáticamente. En otra máquina indique:

```sh
python3 -I -S reproducir.py --lean /ruta/bin/lean --mathlib /ruta/mathlib4 \\
  --report-dir resultados_nuevos
```

Todas las opciones `--*-root`, `--*-report-dir`, `--base` y `--*-helper`
siguen disponibles para una reorganización explícita. Las fuentes y recibos
de esta entrega son autocontenidos; el compilador y la biblioteca estándar
matemática son requisitos del entorno, no pruebas nuevas suministradas como
axiomas. La comprobación causal documental y la conservación de archivos
son controles distintos de la comprobación de los teoremas por Lean.
'''


def make_causal(helper, previous, dest, receipt, receipt_sha, owners, added):
    old_path = previous/'recibos/CAUSAL_TRASLACION.json'
    causal = copy.deepcopy(helper.read(old_path))
    causal.update(artifact=str(dest/'README.md'), artifact_sha256=helper.sha(dest/'README.md'),
        result_id='SELECTED_LATTICE_VERTEX_PRODUCTS_CONFORMAL_20260921',
        verification_receipt='recibos/productos/VERIFICATION.json',
        verification_receipt_sha256=receipt_sha, compiled_modules=len(receipt['modules']),
        authenticated_predecessor_modules=340, reused_authenticated_modules=340,
        public_declarations=receipt['public_declaration_count'],
        theorem_lemma_count=len(receipt['theorem_names']))
    causal['inherited_context'] = dict(source='antecedente/recibos/CAUSAL_TRASLACION.json',
        sha256=helper.sha(old_path), scope='The complete original genealogy is preserved. '
        'This delta starts at its already constructed lattice field map and does not '
        'recertify every contextual assertion or assert the twisted orbifold/FLM result.')
    # The inherited TPK composition remains byte-for-byte equivalent as data.
    # Fock/field operators are a posterior realization, not renamed TPK operators.
    causal['posterior_realization'] = dict(
        operator='Reuse the same selectedOrigin, marked lattice, integral pairing, '
        'cocycle, carrier, T, E, theta and stateField Y after the inherited '
        'APP–TRIT–TPK generation.',
        action='Derive Gram inverse and the quadratic state, identify its L0 and L-1 '
        'with E and T, calculate all Heisenberg/Virasoro commutators with pointwise '
        'finite sums, identify residual products with the actual state fields, and '
        'restrict the constructed operators to the untwisted theta-fixed sector.')
    causal['genealogy']['source_locators'] = [
        'antecedente/'+x if x.startswith(('lean/', 'antecedente/')) else x
        for x in causal['genealogy']['source_locators']]
    causal['genealogy']['source_locators'] += sorted(owners.values())
    focal = causal['focal_genealogical_receipt']
    focal['3_tpk_effective_composition'] = (
        str(focal['3_tpk_effective_composition']) +
        ' Posterior realization on the same already constructed carrier '
        '(these field operators are not TPK operators): ' +
        causal['posterior_realization']['action'])
    focal['4_coefficient_origins'] = ('Gram inverse identities follow from the '
        'proved positive pairing. The central cubic follows from the actual '
        'endomorphism commutators; its scalar is evaluated on every charge ground '
        'state and extended by creators. Central charge 24 is the already proved '
        'rank of the same marked lattice, not an inserted target.')
    focal['5_conserved_information'] = ('The same selected origin, marked charge '
        'lattice, cocycle, oscillator occupations, enriched-history provenance, '
        'field map, vacuum, E, T and theta are retained. All 2076 previous files '
        'remain unchanged. No state, orientation or memory is reset.')
    focal['7_produced_output'] = ('Conformal state and real modes with L0=E and '
        'L-1=T; full Virasoro commutators at central charge 24; field identities '
        'for all integer residual products; and the recorded untwisted fixed-space '
        'restrictions. The exact additional assertions are the Lean declarations '
        'listed in the successful products receipt.')
    focal['8_posterior_recognition_and_falsifier'] = ('Conformal/Virasoro terminology '
        'recognizes the constructed operators only after their identities are '
        'proved. A changed origin, assumed final commutator, missing pointwise '
        'finiteness, wrong coefficient or new native axiom invalidates this delta. '
        'No full FLM, twisted sector or Monster identification is inferred.')
    focal['9_material_owners'] = sorted(owners.values())
    causal['formalization_scope'].update(new_result=focal['7_produced_output'],
        not_claimed=['Twisted-sector construction and orbifold multiplication',
                    'FLM theorem or identification with the Monster',
                    'Fresh proof of all inherited contextual assertions'],
        inherited_native_declarations=receipt.get('declarations_using_inherited_native_axiom', []))
    causal['added_source_modules'] = added
    return causal


def main():
    here = Path(__file__).resolve().parent
    outputs = next(p for p in here.parents if p.name == 'output')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destination', type=Path, default=outputs/'PAQUETE_ARTICULO_I_VERTEX_CONFORME_20260921')
    p.add_argument('--products-report-dir', type=Path, default=here/'products_closed_results')
    p.add_argument('--products-receipt-sha256', required=True)
    p.add_argument('--plan', action='store_true')
    args = p.parse_args()
    dest = args.destination.expanduser().resolve()
    reportdir = args.products_report_dir.expanduser().resolve()
    previous = outputs/'PAQUETE_ARTICULO_I_TRASLACION_ESTADO_CAMPO_20260921'
    helper_path = here.parent/'translation_coherence/package_translation_coherence.py'
    if hashlib.sha256(helper_path.read_bytes()).hexdigest() != PACKAGING_HELPER:
        raise RuntimeError('Packaging helper changed')
    helper = load(helper_path, 'frozen_translation_packaging')
    helper.require_hash(previous/'MANIFIESTO.json', OLD_MANIFEST)
    old = helper.read(previous/'MANIFIESTO.json')
    before = helper.inventory(previous)
    if len(before) != 2076 or set(before) != {r['path'] for r in old['files']} | {'MANIFIESTO.json'}:
        raise RuntimeError('Expected the entire manifest-covered 2076-file predecessor')
    for row in old['files']:
        if before.get(row['path']) != row:
            raise RuntimeError('Changed predecessor: '+row['path'])
    helper.require_hash(reportdir/'VERIFICATION.json', args.products_receipt_sha256)
    products = helper.read(reportdir/'VERIFICATION.json')
    if (products['status'] != 'PASS_VERTEX_PRODUCTS_DELTA' or products['inherited_module_count'] != 340
        or not products['authenticated_inputs_unchanged'] or products['predecessors_modified']
        or products['predecessors_recompiled'] or products['mathlib_rebuilt']):
        raise RuntimeError('Final products PASS is required before copying or sealing')
    runner = here/'verify_vertex_products.py'
    helper.require_hash(runner, products['runner_sha256'])
    product_runner = load(runner, 'frozen_vertex_products')
    vertex_helper = product_runner.load(here/'verify_vertex_extension.py',
        product_runner.PREDECESSOR_RUNNER_SHA, 'frozen_vertex_extension_packaging')
    state_helper_path = here.parent/'state_field/verify_state_field.py'
    state_helper = product_runner.load(state_helper_path, product_runner.HELPER_SHA,
        'frozen_state_helper_packaging')
    verifier, *_ = state_helper.authenticate_base(Path(products['base']))
    vertex_helper.check_probe(verifier, products, products['public_declaration_owners'],
        product_runner.SELECTED_NAMESPACE)
    roots = dict(vertex=here, conformal=here.parent/'conformal_structure',
        involution=here.parent/'involution_coherence')
    stages = [('involucion', roots['involution']/'involution_closed_results',
               INVOLUTION_RECEIPT, 'PASS_INVOLUTION_COHERENCE_DELTA', 2),
              ('conforme', here/'conformal_closed_results', CONFORMAL_RECEIPT,
               'PASS_VERTEX_EXTENSION_DELTA', 17),
              ('productos', reportdir, args.products_receipt_sha256,
               'PASS_VERTEX_PRODUCTS_DELTA', len(products['modules']))]
    sources, owners, receipt_inventories = {}, {}, {}
    for label, folder, digest, status, count in stages:
        helper.require_hash(folder/'VERIFICATION.json', digest)
        r = helper.read(folder/'VERIFICATION.json')
        unchanged = (r['predecessor_sources_objects_unchanged'] if label == 'involucion'
                     else r['authenticated_inputs_unchanged'])
        if (r['status'] != status or not unchanged or r['predecessors_modified']
            or r['predecessors_recompiled'] or r['mathlib_rebuilt']):
            raise RuntimeError('Bad stage receipt: '+label)
        rows = {row['module']: row for row in r['modules']}
        if len(rows) != count or len(r['modules']) != count or set(rows) != set(r['sources']):
            raise RuntimeError('Unexpected stage module closure: '+label)
        vertex_helper.check_probe(verifier, r, r.get('public_declaration_owners'),
            product_runner.SELECTED_NAMESPACE if label == 'productos' else None)
        for name, node in r['sources'].items():
            rootkey = node.get('root', 'involution')
            relative = Path(node['path']).name
            if relative != name+'.lean' or rootkey not in roots:
                raise RuntimeError('Unsafe module path: '+str(node))
            source = roots[rootkey]/relative
            row = rows[name]
            helper.require_hash(source, node['sha256'])
            helper.require_hash(folder/'build'/(name+'.lean'), node['sha256'])
            helper.require_hash(folder/'build'/(name+'.olean'), row['object_sha256'])
            if row['exit_code'] or row['source_sha256'] != node['sha256'] or name in sources:
                raise RuntimeError('Failed or duplicated module: '+name)
            sources[name] = dict(source=source, root=rootkey, path=relative, sha256=node['sha256'])
            owners[name] = 'lean/'+rootkey+'/'+relative
        receipt_inventories[label] = helper.inventory(folder)
    required = {'LatticeVirasoroRelations', 'LatticeStateFieldProducts', 'LatticeEvenConformal',
                'SelectedConformalVertex'}
    if not required <= sources.keys():
        raise RuntimeError('The requested products/Virasoro/even/selected closure is incomplete')
    archive = dest.with_suffix('.zip')
    delivery = dest.parent/(dest.name+'_ENTREGA.json')
    zip_report = dest.parent/(dest.name+'_ZIP_VERIFICACION.json')
    if any(x.exists() for x in (dest, archive, delivery, zip_report)):
        raise RuntimeError('Refusing to overwrite an existing successor or seal')
    result = dict(status='PASS_VERTEX_CONFORMAL_PACKAGE_INPUTS', previous_files=len(before),
        added_source_modules=len(sources), authenticated_modules=340+len(products['modules']),
        product_public_declarations=products['public_declaration_count'],
        product_theorems=len(products['theorem_names']), destination=str(dest),
        compilation_repeated=False, products_receipt_sha256=args.products_receipt_sha256)
    if args.plan:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    dest.mkdir(parents=True)
    shutil.copytree(previous, dest/'antecedente')
    for row in sources.values():
        target = dest/'lean'/row['root']/row['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(row['source'], target)
    for label, folder, *_ in stages:
        shutil.copytree(folder, dest/'recibos'/label)
    shutil.copy2(runner, dest/'verificar_productos.py')
    shutil.copy2(here/'verify_vertex_extension.py', dest/'verificar_conforme.py')
    (dest/'reproducir.py').write_text(wrapper(products['requested_modules']), encoding='utf-8')
    (dest/'README.md').write_text(make_readme(products, len(sources)), encoding='utf-8')
    history = dest/'historia'
    history.mkdir()
    shutil.copy2(__file__, history/'package_vertex_conformal.py')
    shutil.copy2(helper_path, history/'package_translation_coherence.py')
    shutil.copy2(here/'README_CONFORMAL.md', history/'DESARROLLO_CONFORME_Y_PRODUCTOS.md')
    shutil.copy2(here.parent.parent/'CONTINUIDAD_I.md', history/'CONTINUIDAD_I.md')
    shutil.copy2(here.parent/'involution_coherence/verify_involution_coherence.py',
        history/'verify_involution_coherence.py')
    causalpath = dest/'recibos/CAUSAL_VERTEX_CONFORME.json'
    helper.write(causalpath, make_causal(helper, previous, dest, products,
        args.products_receipt_sha256, owners, sorted(sources)))
    gate = Path.home()/'.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py'
    audit = subprocess.run([sys.executable, '-I', '-S', str(gate), '--audit',
        str(dest/'README.md'), '--receipt', str(causalpath)], text=True, capture_output=True)
    helper.write(dest/'recibos/CONTROL_CAUSAL_VERTEX.json', dict(exit_code=audit.returncode,
        stdout=audit.stdout, stderr=audit.stderr, gate_sha256=helper.sha(gate),
        artifact_sha256=helper.sha(dest/'README.md'), receipt_sha256=helper.sha(causalpath),
        is_lean_theorem_verification=False))
    if audit.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in audit.stdout:
        raise RuntimeError('Causal audit failed: '+audit.stdout+audit.stderr)
    # Relocate the one new copy, rather than duplicate all historical payloads.
    with tempfile.TemporaryDirectory(prefix='hmt-vertex-relocation-', dir=dest.parent) as temp:
        temp = Path(temp)
        relocated = temp/'paquete_relocalizado'
        dest.rename(relocated)
        try:
            replay = subprocess.run([sys.executable, '-I', '-S', str(relocated/'reproducir.py'),
                '--plan', '--report-dir', str(temp/'plan')], cwd=temp, text=True, capture_output=True)
            if replay.returncode:
                raise RuntimeError('Relocated replay failed: '+replay.stdout+replay.stderr)
            plan = helper.read(temp/'plan/PLAN.json')
            if (plan['status'] != 'PASS_VERTEX_PRODUCTS_SOURCE_PLAN_NOT_COMPILED'
                or plan['compiler_invoked'] or plan['modules'] or plan['inherited_module_count'] != 340
                or plan['sources'] != products['sources']
                or plan['dependency_order'] != products['dependency_order']
                or not plan['authenticated_inputs_unchanged']):
                raise RuntimeError('Relocated source closure differs from the compiled closure')
            helper.write(relocated/'recibos/REPRODUCCION_RELOCALIZADA.json', plan)
        finally:
            relocated.rename(dest)
    if helper.inventory(previous) != before or helper.inventory(dest/'antecedente') != before:
        raise RuntimeError('Predecessor preservation mismatch')
    for label, folder, *_ in stages:
        if (helper.inventory(folder) != receipt_inventories[label]
            or helper.inventory(dest/'recibos'/label) != receipt_inventories[label]):
            raise RuntimeError('Stage receipt/build changed: '+label)
    for row in sources.values():
        helper.require_hash(row['source'], row['sha256'])
        helper.require_hash(dest/'lean'/row['root']/row['path'], row['sha256'])
    helper.write(dest/'VERIFICACION_CONSERVACION.json', dict(
        status='PASS_COMPLETE_2076_FILE_PREDECESSOR_AND_ALL_VERIFIED_DELTAS',
        previous_manifest_sha256=OLD_MANIFEST, previous_files=list(before.values()),
        stage_files={k:list(v.values()) for k,v in receipt_inventories.items()},
        source_modules=owners, source_compilation_repeated=False,
        full_ii_iii_and_earlier_payload_preserved=True))
    helper.write(dest/'MANIFIESTO.json', dict(schema='hmt.vertex.conformal.successor.v1',
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        predecessor='antecedente', previous_manifest_sha256=OLD_MANIFEST,
        products_receipt='recibos/productos/VERIFICATION.json',
        products_receipt_sha256=args.products_receipt_sha256,
        exact_source_modules=owners, total_authenticated_modules=result['authenticated_modules'],
        inherited_axiom_exception=products['inherited_axiom_exception'],
        files=list(helper.inventory(dest).values())))
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
    if helper.inventory(dest) != complete or helper.inventory(previous) != before:
        raise RuntimeError('A source/delivery changed during sealing')
    result.update(status='PASS_VERTEX_CONFORMAL_DELIVERY', files=len(complete),
        manifest_sha256=helper.sha(dest/'MANIFIESTO.json'), zip_sha256=helper.sha(archive),
        zip_verification=str(zip_report), zip_verification_sha256=helper.sha(zip_report),
        relocated_plan_passed=True, causal_focal_audit_passed=True)
    helper.write(delivery, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
