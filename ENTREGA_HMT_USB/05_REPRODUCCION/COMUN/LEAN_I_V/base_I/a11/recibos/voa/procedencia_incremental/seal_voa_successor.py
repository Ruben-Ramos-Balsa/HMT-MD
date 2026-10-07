#!/usr/bin/env python3
"""Freeze a successful declared-closure execution, then produce its ZIP."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent / 'PAQUETE_ARTICULO_I_CONTINUACION_VOA_20260918'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    mf = ROOT / 'MANIFIESTO.json'
    raw = mf.read_bytes()
    manifest = json.loads(raw)
    if manifest.get('voa_compilation_sealed'):
        raise RuntimeError('This successor execution is already sealed')
    runfile = ROOT / 'resultados/lean_unificado/VERIFICATION.json'
    run = json.loads(runfile.read_text())
    if run.get('status') != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE':
        raise RuntimeError('The complete declared closure has not passed')
    if run['manifest_sha256'] != sha(raw):
        raise RuntimeError('Execution used a different source manifest')
    required = {
        'HMT.I.SelectedVOAInput.shared_action_electron_vertex_input',
        'HMT.I.APPFockIndex.generated_app_fock_index',
        'HMT.I.APPFockIndex.degree_two_operator_trace',
        'HMT.I.SelectedVOAInput.app_fock_selected_radial_compatibility',
        'HMT.IV.LatticeOscillatorFock.carrier_mode_ccr',
        'HMT.IV.LatticeParityCarrier.carrierTheta_square',
        'HMT.I.SelectedHeisenbergInput.shared_action_electron_heisenberg_fields',
        'HMT.IV.LatticeHeisenbergField.heisenbergField_locality_order_two',
    }
    if not required.issubset(run['axiom_probe']['declarations']):
        raise RuntimeError('A principal declaration was not checked')
    for item in manifest['files']:
        if sha((ROOT / item['path']).read_bytes()) != item['sha256']:
            raise RuntimeError('Manifested file changed: ' + item['path'])
    for item in run['sources']:
        if sha((ROOT / item['path']).read_bytes()) != item['sha256']:
            raise RuntimeError('Compiled source changed: ' + item['path'])
    def add(name, data, role):
        if any(item['path'] == name for item in manifest['files']):
            raise RuntimeError('Would overwrite a preserved file: ' + name)
        target = ROOT / name
        if target.exists():
            raise RuntimeError('Target already exists: ' + name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        manifest['files'].append(dict(path=name, sha256=sha(data), bytes=len(data),
            source='SUCCESSFUL_VOA_CONTINUATION_RUN', role=role))
    add('versiones_previas/MANIFIESTO_ANTES_COMPILACION_VOA.json', raw,
        'EXACT_MANIFEST_USED_BY_LEAN')
    add('recibos/voa/LEAN_CONJUNTO.json', runfile.read_bytes(), 'FROZEN_LEAN_EXECUTION')
    fresh = len(run['compiled_modules'])
    reused = len(run['cached_modules'])
    historical_file = ROOT / 'recibos/voa/COMPILACION_CON_PROBE_NO_CUALIFICADO.json'
    historical = json.loads(historical_file.read_text())
    earlier_fresh = sum(not item['cache_hit'] for item in historical['modules'])
    earlier_reused = sum(item['cache_hit'] for item in historical['modules'])
    note = f'''# Continuación comprobada del artículo I

Entrada: `deltas/voa/SelectedHeisenbergInput.lean`.
Teorema compuesto:
`HMT.I.SelectedHeisenbergInput.shared_action_electron_heisenberg_fields`.

La clausura declarada de {run['local_module_count']} módulos pasó en Lean 4.21.0:
{fresh} módulos compilados en esta ejecución y {reused} reutilizados tras
comprobar fuentes, dependencias, objetos y compilador. Se verificaron
{len(run['axiom_probe']['declarations'])} declaraciones explícitas en la consulta final.
Estos números describen el control, no sustituyen el alcance de los teoremas.
En la primera compilación de esta continuación se compilaron {earlier_fresh}
módulos y se reutilizaron {earlier_reused} de la base. El control final de nombres
de aquella ejecución necesitó una corrección de cualificación de espacios de
nombres; no se cambió ninguna prueba. Se conservaron su recibo y el posterior
PASS conjunto de 139 módulos. El control actual incorpora además los campos.

## Resultados incorporados

- El agregado de la diferencia producto–suma se calcula en las dos hojas de
  APP. Su coeficiente unitario es −3; la lectura orientada de U030 tiene índice
  54. La ecuación polinómica de compatibilidad tiene una única solución entera
  positiva, 12.
- El operador finito de grado dos actúa sobre 24 + 300 coordenadas. Sus dos
  trazas son −12 y 66, con total 54; el acoplamiento orientado también tiene
  traza 54. El falsador del propio corpus conserva ese índice pero cambia el
  peso digital a 63. No se identifica una traza con una dimensión.
- Sobre el mismo `selectedOrigin` y el mismo retículo se construyen el cociclo,
  la extensión central y el álgebra compleja torcida. Sus leyes se prueban;
  no son campos supuestos de un certificado vacío.
- Se construye el portador algebraico de osciladores con modos y grados sin
  cota. Cada vector es una combinación finita. Se prueban las relaciones de
  conmutación, los modos cero, los desplazamientos del retículo y su acción
  sobre el producto tensorial. El vacío es no nulo.
- Se construye la involución del cociclo elegido y del portador, junto con
  los proyectores par e impar. Se prueban involutividad, idempotencia,
  anulación cruzada y descomposición.
- La entrada común conserva la composición de acción y electrón, sin
  sustituir el registro ni repetir las pruebas de K. El contrato de regresión
  del fundamento se compila dentro de la misma clausura.
- Desde soporte finito se demuestra la truncación puntual de los modos de
  aniquilación. Se construyen los campos de Heisenberg como aplicaciones
  lineales a series de Laurent, con todos sus coeficientes enteros. Se prueban
  las propiedades de vacío y la localidad de orden dos de esos campos,
  coeficiente a coeficiente en dos variables, a partir de los conmutadores.

## Frontera exacta

La compatibilidad de las trazas con la norma radial no se promueve a un
entrelazador de operadores. No se ha identificado formalmente aquí el bloque
matricial finito con una componente graduada del portador simétrico infinito.
La involución pertenece al cociclo triangular construido; no afirma por sí
sola una normalización diagonal específica de FLM.

La localidad de los campos de Heisenberg sí está probada. La correspondencia
estado–campo completa de la VOA, incluidos los campos exponenciales del
retículo, Jacobi para toda la VOA, el módulo torcido, el producto del orbifold
y la identificación de su grupo con el
Monstruo no son conclusiones de esta entrega Lean. El LaTeX los trata por
aplicación de FLM; la cita no se ha convertido en un axioma Lean. Esta
continuación no se presenta como una formalización terminada de Moonshine.

Se conserva sin alterar el alcance de S8 y de las interfaces de la base. El
selector finito heredado usa `Lean.ofReduceBool`; las pruebas nuevas del índice
orientado utilizan reducción del núcleo y no añaden ese axioma. No se admite
`sorry`, `admit` ni un axioma HMT nuevo.

No se ha cambiado ningún PDF. Los archivos manifestados de la base anterior
permanecen idénticos. Las fuentes LaTeX se conservan como procedencia, no como
pruebas Lean por el hecho de copiarlas. Mathlib no se ha reconstruido.

## Reproducción

`python3 -I -S reproducir_voa.py --mathlib /ruta/mathlib4 --lean /ruta/lean`

El README especifica las versiones. El ZIP contiene todas las fuentes HMT de
la clausura, el contrato, la documentación y los recibos. Lean y Mathlib son
dependencias externas declaradas. El recibo congelado está en
`recibos/voa/LEAN_CONJUNTO.json`.
'''
    add('RESULTADO_CONTINUACION_VOA.md', note.encode(), 'EXACT_SCOPE_AND_RESULT')
    readme = '''# Entrada vigente del paquete Lean del artículo I

Este README gobierna la ejecución de esta continuación. Los textos de inicio
heredados (`INICIO_AQUI.md`, `LEEME_PRIMERO.md` y las entregas previas) se
conservan íntegros como antecedentes; no sustituyen esta entrada.

## Un único recorrido

`APP → TRIT → TPK → estado enriquecido → publicaciones regionales → registro
seleccionado → incidencia y retículo → álgebra torcida → osciladores y campos`.
Los supuestos y dominios exactos de cada flecha son los de sus teoremas Lean.
Los valores de llegada no se añaden como entradas nuevas de esta continuación.
No reiniciar la inversión de K ni sus lectores: se reutilizan sus fuentes y
sus pruebas dentro de la misma clausura.

Ejecutar desde esta carpeta:

```sh
python3 -I -S reproducir_voa.py --mathlib /ruta/mathlib4 --lean /ruta/lean
```

Lean debe ser 4.21.0. El commit de Mathlib está declarado en `README_VOA.md`.
El ejecutor verifica las huellas, resuelve los imports, compila o reutiliza
objetos sólo si coinciden sus fuentes y dependencias y consulta los axiomas
de las declaraciones explícitas. No reconstruye Mathlib. El entorno de Lean
y la biblioteca Mathlib son dependencias externas, no archivos ocultos del
proyecto. El ZIP incluye las fuentes HMT de toda la clausura declarada.

La entrada matemática es `deltas/voa/SelectedHeisenbergInput.lean`; conserva
la composición acción/electrón/incidencia y agrega los campos construidos.
`RESULTADO_CONTINUACION_VOA.md` explica los resultados y su límite exacto.
`recibos/voa/LEAN_CONJUNTO.json` conserva la ejecución conjunta sellada;
las ejecuciones futuras escriben `resultados/lean_unificado/VERIFICATION.json`.

La localidad de los campos de Heisenberg está demostrada. Este paquete no
declara formalizados el sistema completo de campos exponenciales, el módulo
torcido, el orbifold de FLM ni su identificación con el Monstruo. La presencia
de la fuente LaTeX de esos resultados conserva su procedencia; no los convierte
automáticamente en teoremas Lean. No se ha añadido un axioma para suplirlos.
'''
    add('README.md', readme.encode(), 'CURRENT_SINGLE_ENTRY_AND_REPRODUCTION')
    causal_path = ROOT / 'recibos/voa/CAUSAL_RECEIPT.json'
    if not causal_path.is_file():
        candidates = [p for p in ROOT.rglob('*.json') if p.name == 'RECIBO_CAUSAL_VOA.json']
        if not candidates:
            raise RuntimeError('Cannot locate the prepared causal metadata receipt')
        causal_path = candidates[0]
    causal = json.loads(causal_path.read_text())
    causal['artifact'] = str(ROOT / 'RESULTADO_CONTINUACION_VOA.md')
    causal['artifact_sha256'] = sha(note.encode())
    causal['result_id'] = 'SELECTED_LATTICE_FOCK_VOA_CONTINUATION_RUN_20260918'
    causal['mathematical_result'] += (
        ' The continuation also constructs actual Heisenberg fields as linear maps '
        'to vector-valued Laurent series, proves pointwise lower truncation, '
        'all-integer commutators, vacuum properties and coefficientwise order-two '
        'locality in their Heisenberg sector. This is not the full lattice VOA.')
    for name in ('LatticeFieldTruncation', 'LatticeHeisenbergModes',
                 'LatticeHeisenbergField', 'SelectedHeisenbergInput'):
        causal['genealogy']['source_locators'].append(str(ROOT / 'deltas/voa' / (name + '.lean')))
    new_causal = 'recibos/voa/RECIBO_CAUSAL_EJECUCION.json'
    add(new_causal, (json.dumps(causal, indent=2, ensure_ascii=False) + '\n').encode(),
        'CAUSAL_METADATA_NOT_A_PROOF')
    gate = subprocess.run([sys.executable, '-I', '-S',
        '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
        '--audit', str(ROOT / 'RESULTADO_CONTINUACION_VOA.md'),
        '--receipt', str(ROOT / new_causal)], text=True, capture_output=True)
    if gate.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in gate.stdout:
        raise RuntimeError('Causal metadata gate failed: ' + gate.stdout + gate.stderr)
    add('recibos/voa/CONTROL_CAUSAL_EJECUCION.txt', (gate.stdout + gate.stderr).encode(),
        'CAUSAL_METADATA_CHECK')
    local = Path(__file__).resolve().parent
    for name in ('APP_FOCK_SOURCE_MAP.md', 'APPFockRigidity.receipt.json',
                 'APPFockIndex.receipt.json', 'SELECTED_ALGEBRA_VERIFICATION.json',
                 'WITT_NEGATION_VERIFICATION.json', 'FOCK_VERIFICATION.json',
                 'seal_voa_successor.py'):
        add('recibos/voa/procedencia_incremental/' + name, (local / name).read_bytes(),
            'INCREMENTAL_PROVENANCE_NOT_A_SUBSTITUTE_FOR_COMBINED_RUN')
    manifest['voa_compilation_sealed'] = dict(status=run['status'],
        source_manifest_sha256=run['manifest_sha256'], modules=run['local_module_count'],
        compiled=fresh, reused=reused, earlier_compiled=earlier_fresh,
        earlier_reused=earlier_reused,
        main='HMT.I.SelectedHeisenbergInput.shared_action_electron_heisenberg_fields',
        receipt='recibos/voa/LEAN_CONJUNTO.json', complete_flm_formalization_claimed=False)
    final = (json.dumps(manifest, indent=2, ensure_ascii=False) + '\n').encode()
    mf.write_bytes(final)
    archive = ROOT.with_suffix('.zip')
    if archive.exists():
        raise RuntimeError('Refusing to overwrite an existing archive')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in sorted({item['path'] for item in manifest['files']} | {'MANIFIESTO.json'}):
            z.write(ROOT / name, Path(ROOT.name) / name)
        if z.testzip():
            raise RuntimeError('ZIP CRC verification failed')
        for item in manifest['files']:
            if sha(z.read(str(Path(ROOT.name) / item['path']))) != item['sha256']:
                raise RuntimeError('ZIP content mismatch: ' + item['path'])
    print(json.dumps(dict(status='PASS_VOA_CONTINUATION_PACKAGE_SEALED',
        modules=run['local_module_count'], fresh=fresh, reused=reused,
        declarations=len(run['axiom_probe']['declarations']), files=len(manifest['files']),
        zip=str(archive), zip_sha256=sha(archive.read_bytes()),
        manifest_sha256=sha(final)), ensure_ascii=False))

if __name__ == '__main__':
    main()
