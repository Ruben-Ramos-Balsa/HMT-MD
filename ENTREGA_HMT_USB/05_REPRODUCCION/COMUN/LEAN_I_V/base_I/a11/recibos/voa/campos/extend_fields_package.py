#!/usr/bin/env python3
"""Add proved current fields to the unsealed continuation, preserving history."""
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / 'PAQUETE_ARTICULO_I_CONTINUACION_VOA_20260918'
NAMES = ('LatticeFieldTruncation', 'LatticeHeisenbergModes',
         'LatticeHeisenbergField', 'SelectedHeisenbergInput')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    mf = ROOT / 'MANIFIESTO.json'
    raw = mf.read_bytes()
    manifest = json.loads(raw)
    if manifest.get('voa_compilation_sealed') or manifest.get('heisenberg_fields_added'):
        raise RuntimeError('Refusing to rewrite an existing extension')
    prior = ROOT / 'resultados/lean_unificado/VERIFICATION.json'
    run = json.loads(prior.read_bytes())
    assert run['status'] == 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE'
    assert run['manifest_sha256'] == sha(raw)
    for item in manifest['files']:
        assert sha((ROOT / item['path']).read_bytes()) == item['sha256'], item['path']
    def add(name, data, role, source='CURRENT_FIELD_EXTENSION'):
        target = ROOT / name
        if target.exists() or any(f['path'] == name for f in manifest['files']):
            raise RuntimeError('Cannot replace preserved file ' + name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        manifest['files'].append(dict(path=name, sha256=sha(data), bytes=len(data),
                                     source=source, role=role))
    add('versiones_previas/MANIFIESTO_ANTES_CAMPOS.json', raw, 'PREDECESSOR_MANIFEST')
    add('recibos/voa/LEAN_CONJUNTO_ANTES_CAMPOS.json', prior.read_bytes(), 'FROZEN_PREDECESSOR_EXECUTION')
    wrapper = ROOT / 'reproducir_voa.py'
    add('versiones_previas/reproducir_voa_antes_campos.py', wrapper.read_bytes(), 'PREDECESSOR_RUNNER')
    for name in NAMES:
        source = HERE / (name + '.lean')
        add('deltas/voa/' + source.name, source.read_bytes(), 'PROVED_FIELD_SOURCE', str(source))
    spec = importlib.util.spec_from_file_location('voa_builder_fields', HERE / 'package_voa_successor.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    verifier = builder.load_verifier()
    modules, _ = builder.source_inventory()
    probes = []
    for source in modules.values():
        probes.extend(builder.qualified_probes(source, verifier))
    data = builder.wrapper_source(list(modules), probes).encode()
    wrapper.write_bytes(data)
    for item in manifest['files']:
        if item['path'] == 'reproducir_voa.py':
            item.update(sha256=sha(data), bytes=len(data),
                        source='FIELD_WRAPPER_PRESERVING_PREDECESSOR')
    note = '''# Campos de Heisenberg del mismo retículo

La entrada ampliada es `deltas/voa/SelectedHeisenbergInput.lean`.
No sustituye `SelectedVOAInput` ni la base común: los importa.

`LatticeFieldTruncation` demuestra desde soporte finito la anulación de todos
los modos de aniquilación suficientemente altos sobre cada estado algebraico.
`LatticeHeisenbergModes` construye la familia de modos para todo índice entero
y demuestra sus conmutadores a partir de la forma integral del retículo.
`LatticeHeisenbergField` construye operadores de vértice en el sentido preciso
de Mathlib: aplicaciones lineales a series de Laurent. Prueba la identificación
de todos sus coeficientes, las propiedades de vacío y la localidad de orden dos
de los campos de Heisenberg, coeficiente a coeficiente en dos variables formales.

Esta localidad corresponde a esos campos generadores, no al sistema completo
que incluye los campos exponenciales del retículo. No se presenta como prueba
de Jacobi para toda la VOA, ni del módulo torcido, orbifold o teorema FLM.
Los teoremas están construidos sobre el mismo selectedOrigin, sin un nuevo K,
sin una matriz de Gram independiente y sin postular las relaciones de campo.

El recibo anterior, de 139 módulos, queda conservado. `reproducir_voa.py`
comprueba ahora toda la clausura ampliada. Los archivos del manuscrito y las
pruebas anteriores no se han modificado.
'''
    add('CAMPOS_HEISENBERG.md', note.encode(), 'CONSTRUCTED_FIELDS_EXACT_SCOPE')
    for name in ('FIELD_TRUNCATION_VERIFICATION.json',
                 'HEISENBERG_MODES_VERIFICATION.json',
                 'HEISENBERG_FIELDS_VERIFICATION.json',
                 'SELECTED_HEISENBERG_VERIFICATION.json',
                 'verify_field_truncation.py', 'verify_heisenberg_fields.py',
                 'verify_heisenberg_modes.py', 'verify_selected_heisenberg.py',
                 'extend_fields_package.py', 'package_voa_successor.py'):
        source = HERE / name
        if source.exists():
            add('recibos/voa/campos/' + name, source.read_bytes(), 'FIELD_PROVENANCE')
    manifest['heisenberg_fields_added'] = dict(modules=list(NAMES),
        previous_receipt='recibos/voa/LEAN_CONJUNTO_ANTES_CAMPOS.json',
        entry='deltas/voa/SelectedHeisenbergInput.lean', complete_flm_claimed=False)
    mf.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(status='FIELDS_ADDED_NOT_YET_COMBINED_VERIFIED',
        modules=list(NAMES), previous_sources_preserved=True, files=len(manifest['files']))))

if __name__ == '__main__':
    main()
