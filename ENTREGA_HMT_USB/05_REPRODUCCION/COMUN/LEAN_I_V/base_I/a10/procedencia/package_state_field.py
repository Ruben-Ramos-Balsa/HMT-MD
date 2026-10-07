#!/usr/bin/env python3
"""Build an additive, self-contained state-field delivery from a verified delta.

The sealed 279-module predecessor is copied in full under antecedente/,
including its authenticated compiled objects. No predecessor file is edited.
Execution is refused unless the focal source/axiom receipt is PASS and matches
every current delta source. Existing delivery directories are never replaced.
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
DELIVERY_NAME = 'PAQUETE_ARTICULO_I_ESTADO_CAMPO_20260920'


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def files_under(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Symlink not admitted in a sealed delivery: ' + str(path))
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            result[relative] = dict(path=relative, sha256=sha(path), bytes=path.stat().st_size)
    return result


def readme(receipt, predecessor_count):
    modules = '\n'.join('- `' + name + '.lean`' for name in receipt['compile_order'])
    return f'''# Construcción del mapa estado–campo sobre el retículo marcado HMT

Esta entrega amplía de manera aditiva el paquete de covariancia y firma del
20 de septiembre de 2026. El antecedente permanece completo e inalterado:
{predecessor_count} archivos físicos, incluidos las fuentes manifestadas,
sus pruebas anteriores, documentación, recibos y objetos compilados.

## Orden de lectura y reproducción

1. `antecedente/README.md` conserva el arranque y la cadena ya verificada.
   `antecedente/MANIFIESTO.json` y el recibo
   `antecedente/recibos/covariancia_firma/LEAN_CONJUNTO.json` identifican las
   279 dependencias activas. No se repite ni se sustituye el selector de K.
2. `lean/` contiene únicamente esta ampliación: palabras de osciladores,
   derivadas divididas, productos normalmente ordenados y el mapa lineal
   estado–campo sobre el portador que ya estaba construido. Su creación
   desde el vacío se demuestra a partir de los campos cargados existentes.
3. `recibos/estado_campo/VERIFICATION.json` registra las fuentes, comandos,
   salidas, declaraciones y axiomas de la ejecución focal. Los nombres de
   teoremas son el alcance exacto de esa comprobación.
4. Ejecutar desde esta carpeta:

   ```text
   python3 -I -S reproducir.py --plan
   python3 -I -S reproducir.py --lean /ruta/a/lean --mathlib /ruta/a/mathlib4
   ```

El primer comando comprueba las fuentes y las dependencias sin compilar.
El segundo autentica el antecedente y sólo recompila las fuentes nuevas,
en orden de importación. Los recibos nuevos se escriben en `resultados/`;
los originales quedan preservados en `recibos/`. No requiere descomprimir
ningún otro paquete HMT. Mathlib y Lean son dependencias de software externas.

Los objetos del antecedente fueron compilados con Lean 4.21.0 para
arm64-apple-darwin y con Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3`. Su reutilización exige el mismo
compilador binario; cambiar de plataforma requiere reproducir previamente
esa base con el compilador correspondiente, no omitir la autenticación.

## Fuentes nuevas verificadas

{modules}

La ejecución focal enumera {receipt['public_declaration_count']} declaraciones
públicas y {len(receipt['theorem_names'])} teoremas/lemas. Los seis módulos de
construcción usan sólo los axiomas ordinarios `propext`, `Classical.choice` y
`Quot.sound` según cada declaración. La composición `SelectedStateField`
hereda además `Lean.ofReduceBool` del origen seleccionado ya comprobado.
No incorpora axiomas nuevos, `sorry` ni `admit`. El antecedente mantiene su
frontera de confianza original, incluido `Lean.ofReduceBool` donde lo declara
su selector finito; no se oculta ni se transforma en una prueba por reducción
exclusivamente del núcleo.

## Conservación y estatuto

`MANIFIESTO.json` contiene la huella de cada archivo de esta entrega y el
orden de importación del delta. `VERIFICACION_CONSERVACION.json` documenta
la igualdad de todos los archivos copiados del antecedente. La conservación
de archivos y la comprobación de teoremas son controles diferentes.

Las fórmulas de los productos normales y de la realización sobre
M(1) tensor C_epsilon[Lambda] proceden del desarrollo existente del artículo.
La aportación de esta entrega es su implementación y comprobación en Lean,
no una atribución de novedad a esa construcción. Los resultados certificados
son exactamente los enunciados presentes en las fuentes y en el recibo;
la compilación no certifica automáticamente otros teoremas del manuscrito.
'''


def main():
    source = Path(__file__).resolve().parent
    output = next((p for p in source.parents if p.name == 'output'), None)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path,
                        default=output / 'PAQUETE_ARTICULO_I_COVARIANCIA_Y_FIRMA_20260920'
                        if output else None)
    parser.add_argument('--destination', type=Path,
                        default=output / DELIVERY_NAME if output else None)
    parser.add_argument('--plan', action='store_true', help='Validate inputs only; do not copy or zip')
    parser.add_argument('--readme', type=Path,
                        default=source / 'README_ESTADO_CAMPO.md',
                        help='Use this reviewed README if present; otherwise use the package template')
    args = parser.parse_args()
    if args.base is None or args.destination is None:
        raise RuntimeError('--base and --destination are required outside the project output tree')
    base = args.base.expanduser().resolve()
    destination = args.destination.expanduser().resolve()
    archive = destination.with_suffix('.zip')
    if destination.exists() or archive.exists():
        raise RuntimeError('Refusing to replace an existing delivery or ZIP: ' + str(destination))
    runner_path = source / 'verify_state_field.py'
    spec = importlib.util.spec_from_file_location('state_field_focal_runner', runner_path)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    verifier, old, base_sources, _, _ = runner.authenticate_base(base)
    nodes, order, inherited, extra_external = runner.inventory(verifier, source, base_sources)
    receipt_path = source / 'resultados/VERIFICATION.json'
    receipt = json.loads(receipt_path.read_text())
    if receipt.get('status') != 'PASS_STATE_FIELD_DELTA':
        raise RuntimeError('Focal delta has not passed its complete compilation and axiom probe')
    if receipt.get('runner_sha256') != sha(runner_path):
        raise RuntimeError('Runner changed since the focal proof receipt; rerun focal verification')
    if receipt.get('sources') != nodes or receipt.get('compile_order') != order:
        raise RuntimeError('Current source inventory differs from the successful focal receipt')
    if 'SelectedStateField' not in nodes:
        raise RuntimeError('The selected-origin composition must be present before packaging')
    if len(nodes) > 7:
        raise RuntimeError('Review the declared seven-module package scope before adding further modules')
    if receipt.get('base_receipt_sha256') != runner.BASE_RECEIPT_SHA:
        raise RuntimeError('Focal verification used a different base')
    for row in receipt['modules']:
        obj = source / 'resultados/build' / (row['module'] + '.olean')
        if sha(obj) != row['object_sha256'] or row['exit_code'] != 0:
            raise RuntimeError('New compiled object differs from receipt: ' + row['module'])
    before = files_under(base)
    old_manifest = json.loads((base / 'MANIFIESTO.json').read_text())
    for row in old_manifest['files']:
        if before.get(row['path'], {}).get('sha256') != row['sha256']:
            raise RuntimeError('Predecessor preservation check failed: ' + row['path'])
    plan = dict(status='PASS_STATE_FIELD_PACKAGE_INPUTS', predecessor_files=len(before),
                predecessor_manifested_files=len(old_manifest['files']),
                delta_modules=order, destination=str(destination), zip=str(archive),
                focal_receipt_sha256=sha(receipt_path))
    if args.plan:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return 0
    destination.mkdir(parents=True)
    shutil.copytree(base, destination / 'antecedente')
    (destination / 'lean').mkdir()
    for name, node in nodes.items():
        shutil.copy2(source / node['path'], destination / 'lean' / node['path'])
    shutil.copy2(runner_path, destination / 'reproducir.py')
    (destination / 'procedencia').mkdir()
    shutil.copy2(Path(__file__), destination / 'procedencia/package_state_field.py')
    shutil.copytree(source / 'resultados', destination / 'recibos/estado_campo')
    if args.readme.is_file():
        shutil.copy2(args.readme, destination / 'README.md')
    else:
        (destination / 'README.md').write_text(readme(receipt, len(before)), encoding='utf-8')
    for name in ('CAUSAL.json', 'CONTROL_CAUSAL.json', 'REVISION_MATEMATICA.md'):
        if (source / name).is_file():
            shutil.copy2(source / name, destination / 'recibos/estado_campo' / name)
    after = files_under(destination / 'antecedente')
    if before != after or files_under(base) != before:
        raise RuntimeError('Full predecessor byte-preservation check failed during packaging')
    for name, node in nodes.items():
        if sha(destination / 'lean' / node['path']) != node['sha256']:
            raise RuntimeError('New source changed during copy: ' + name)
    preservation = dict(schema='hmt.state.field.byte.preservation.v1',
                        status='PASS_FULL_PREDECESSOR_PRESERVATION',
                        predecessor_files=len(before), manifested_files=len(old_manifest['files']),
                        source_manifest_sha256=runner.BASE_MANIFEST_SHA,
                        source_receipt_sha256=runner.BASE_RECEIPT_SHA,
                        files=list(before.values()), source_directory_modified=False)
    write_json(destination / 'VERIFICACION_CONSERVACION.json', preservation)
    inventory = files_under(destination)
    manifest = dict(schema='hmt.state.field.successor.v1',
                    generated_at_utc=datetime.now(timezone.utc).isoformat(),
                    predecessor_directory='antecedente', predecessor_modules=279,
                    predecessor_manifest_sha256=runner.BASE_MANIFEST_SHA,
                    predecessor_receipt_sha256=runner.BASE_RECEIPT_SHA,
                    focal_receipt='recibos/estado_campo/VERIFICATION.json',
                    focal_receipt_sha256=sha(receipt_path),
                    delta_modules=order, direct_inherited_imports=inherited,
                    extra_external_imports=extra_external,
                    public_declarations=receipt['public_declaration_count'],
                    theorem_names=receipt['theorem_names'],
                    allowed_new_axioms=receipt['allowed_new_axioms'],
                    inherited_axiom_exception=receipt['inherited_axiom_exception'],
                    files=list(inventory.values()))
    write_json(destination / 'MANIFIESTO.json', manifest)
    complete = files_under(destination)
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
        for relative in complete:
            zipped.write(destination / relative, arcname=destination.name + '/' + relative)
    with zipfile.ZipFile(archive) as zipped:
        if zipped.testzip() is not None:
            raise RuntimeError('ZIP CRC check failed')
        if len(zipped.namelist()) != len(complete):
            raise RuntimeError('ZIP entry count differs from the delivery')
        for relative, row in complete.items():
            digest = hashlib.sha256(zipped.read(destination.name + '/' + relative)).hexdigest()
            if digest != row['sha256']:
                raise RuntimeError('ZIP byte comparison failed: ' + relative)
    result = dict(status='PASS_STATE_FIELD_DELIVERY', directory=str(destination), zip=str(archive),
                  zip_sha256=sha(archive), manifest_sha256=sha(destination / 'MANIFIESTO.json'),
                  files=len(complete), manifested_files=len(inventory),
                  predecessor_files=len(before), predecessor_manifested_files=len(old_manifest['files']),
                  delta_modules=order, public_declarations=receipt['public_declaration_count'],
                  theorem_count=len(receipt['theorem_names']), focal_receipt_sha256=sha(receipt_path),
                  compilation_replayed_during_packaging=False,
                  focal_sources_and_objects_authenticated=True)
    write_json(destination.parent / (destination.name + '_ENTREGA.json'), result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
