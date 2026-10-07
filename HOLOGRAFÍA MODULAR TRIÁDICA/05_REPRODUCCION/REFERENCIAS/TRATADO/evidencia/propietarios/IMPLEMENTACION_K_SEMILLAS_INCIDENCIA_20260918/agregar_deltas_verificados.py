#!/usr/bin/env python3
"""Preserve later certified deltas without relabelling the earlier full build."""
from pathlib import Path
import hashlib
import json
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'PAQUETE_CONTINUIDAD_K_UNIDAD_20260918'
REG=HERE.parent/'IMPLEMENTACION_N69_REGIONAL_20260918'
ACTION=Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_ARTICULO_I_20260917/ActionElectron')
SUPPLEMENT=HERE.parent/'EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/supplement'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    path=ROOT/'MANIFIESTO.json'
    raw_manifest=path.read_bytes()
    manifest=json.loads(raw_manifest)
    if manifest.get('relocation_verification',{}).get('status')!='PASS_SOURCE_PRESERVATION_REGIONAL_REPRODUCTION_AND_LEAN_CLOSURE':
        raise RuntimeError('The base reproduction must be sealed first')
    def record(relative,data,source,role):
        destination=ROOT/relative
        if destination.exists() and destination.read_bytes()!=data:
            raise RuntimeError('Refusing to replace an existing delta: '+relative)
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(data)
        item=dict(path=relative,sha256=digest(data),bytes=len(data),source=source,role=role)
        previous=next((x for x in manifest['files'] if x['path']==relative),None)
        if previous is None:
            manifest['files'].append(item)
        elif previous['sha256']!=item['sha256']:
            raise RuntimeError('Manifest delta conflict')
    def copy(source,relative,role,expected=None):
        data=source.read_bytes()
        if expected is not None and digest(data)!=expected:
            raise RuntimeError('Delta proof/source mismatch: '+str(source))
        record(relative,data,str(source),role)
        if source.read_bytes()!=data:
            raise RuntimeError('Concurrent source change: '+str(source))
    # Keep the already verified base manifest as a byte-identical antecedent.
    # Existing proof receipts, Lean sources and source snapshots are untouched.
    record('versiones_previas/manifiestos/'+digest(raw_manifest)+'.json',raw_manifest,
           'MANIFEST_BEFORE_LATER_DELTAS','PRESERVED_BASE_MANIFEST')
    witt=json.loads((REG/'WittReaderCompatibility.receipt.json').read_text())
    if witt['status']!='PASS_WITT_READER_COMPATIBILITY':
        raise RuntimeError('Witt compatibility is not PASS')
    copy(REG/'WittReaderCompatibility.lean','deltas/witt/WittReaderCompatibility.lean',
         'LATER_INCREMENTAL_PROOF',witt['source_sha256'])
    copy(REG/'WittReaderCompatibility.receipt.json','deltas/witt/VERIFICATION.json','INHERITED_LATER_RECEIPT')
    action=json.loads((ACTION/'verification/VERIFICATION.json').read_text())
    if action['status']!='PASS_SELECTED_ACTION_ELECTRON_INCREMENTAL':
        raise RuntimeError('Action/electron composition is not PASS')
    for item in action['source_inputs'].values():
        source=Path(item['path'])
        copy(source,'deltas/accion_electron/'+source.name,'LATER_INCREMENTAL_PROOF',item['sha256'])
    for source,relative in [(ACTION/'README.md','deltas/accion_electron/README.md'),
        (ACTION/'verification/VERIFICATION.json','deltas/accion_electron/VERIFICATION.json'),
        (ACTION/'verify_incremental.py','deltas/accion_electron/verify_incremental.py'),
        (ACTION/'CAUSAL_RECEIPT.json','deltas/accion_electron/CAUSAL_RECEIPT.json')]:
        copy(source,relative,'LATER_DOCUMENTATION_OR_RECEIPT')
    for item in action['results']:
        logfile=ACTION/'verification'/(item['module']+'.log')
        copy(logfile,'deltas/accion_electron/logs/'+logfile.name,'INHERITED_COMPILATION_LOG',item['log_sha256'])
    # The article's complete supplement is preserved, not selected by extension
    # or by whether a component belongs to the focal Lean compilation.
    supplement_files=sorted(p for p in SUPPLEMENT.rglob('*') if p.is_file())
    if not SUPPLEMENT.is_dir() or not supplement_files:
        raise RuntimeError('Article X supplement is absent or empty')
    supplement_bytes=0
    for source in supplement_files:
        relative='fuentes/articulo_x/supplement/'+source.relative_to(SUPPLEMENT).as_posix()
        copy(source,relative,'ARTICLE_X_COMPLETE_SUPPLEMENT')
        supplement_bytes+=next(x['bytes'] for x in manifest['files'] if x['path']==relative)
    copy(HERE/'reproducir_deltas.py','reproducir_deltas.py','LATER_TARGET_CONFIGURATION')
    note='''# Entrega reunida: generación del registro y continuidad de sus aplicaciones

El punto de entrada conceptual es **INICIO_AQUI.md**. La nota matemática está en **NOTA_DE_COMPOSICION.tex** y el artículo X íntegro en **FUENTES_INTEGRAS_PARA_LECTURA.md**, junto con sus 155 fuentes LaTeX originales en `fuentes/articulo_x/`.

El suplemento completo del artículo X se conserva, sin selección ni modificación, en `fuentes/articulo_x/supplement/`. Incluye sus controles, antecedentes, desarrollo de alfa, censo terminal, emisiones, exploración, fuentes Lean y recursos auxiliares. Esta incorporación documental mantiene íntegro el artículo principal y sus materiales de apoyo; no atribuye al suplemento una ejecución que no se haya realizado.

## Ejecución conjunta reproducida

La cadena regional–terminal y su composición incidencial se recompilaron desde una carpeta distinta, con todas sus dependencias locales. El recibo está en `recibos/reproduccion/LEAN_REUBICADO.json`. Las firmas regionales se regeneraron antes de abrir su testigo histórico: cien filas, 1.100 campos coincidentes, sin lecturas de archivos HMT externos al paquete. El control de conservación y el de reproducción tienen recibos distintos.

## Ampliaciones posteriores conservadas

Estas ampliaciones llegaron después de iniciarse aquella compilación conjunta. Mantienen sus propios recibos incrementales y **no se presentan como módulos incluidos en esa ejecución anterior**.

- **Compatibilidad de las cartas de Witt:** `deltas/witt/`. La permutación de coordenadas (0,1,2,4,5,3) relaciona las dos matrices declaradas; los funcionales algebraicos de carga total coinciden. Se conserva el alcance 6×6, sin identificar por ello cualquier codificación de bucle.
- **Acción y electrón desde el mismo registro:** `deltas/accion_electron/`. La misma coordenada α que tiene publicaciones a toda profundidad determina la década de acción −34 y se utiliza en las dos secciones de acción y en el operador de la fibra electrónica central. El teorema conserva las unidades positivas, el lector y el refinamiento como parámetros explícitos. Las cuatro fuentes nuevas tienen 35 consultas de axiomas registradas. Sus dependencias locales anteriores están incluidas en `lean/biblioteca/` y en la cadena regional–terminal.

La **ruta recomendada para el conjunto formal ampliado** es `reproducir_deltas.py`. El comando `reproducir.py --lean` se conserva como reproducción de la **base de 74 módulos y 13 objetivos focales**. Los dos deltas posteriores conservan sus fuentes y recibos; no se ha ampliado silenciosamente el alcance de aquel comando ni del recibo base. Esta distinción impide confundir conservación documental, recompilación de la base y compilación incremental de las ampliaciones.

Para comprobar la clausura ampliada sin compilar, ejecutar `python3 -I -S reproducir_deltas.py --plan`. Para compilarla, usar `python3 -I -S reproducir_deltas.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean`. Este adaptador amplía únicamente los directorios y objetivos del mismo verificador; conserva todas las comprobaciones de caché, fuentes y axiomas. Reutiliza los objetos de la ejecución base sólo cuando sus huellas siguen siendo válidas.

El control documental del conjunto se realiza con `python3 -I -S reproducir.py --check`. La planificación del adaptador no es una compilación. Los controles particulares conservados en el suplemento no se ejecutan automáticamente por añadir sus archivos al paquete.

## Tesis y conservación editorial

Se mantienen juntos APP, TRIT, TPK, estado enriquecido y estructura discreta del continuo; el centro, las regiones, el registro y sus lectores conservan su jerarquía. La relación entre el bloque central, las vacancias, las orientaciones y las firmas regionales está desarrollada en `sections/centro_electronico_registros.tex` del artículo incluido. Las pruebas de conservación evolutiva, recuperación, incidencia y realizaciones dimensionales permanecen completas.

Los PDF entregados no se han modificado. Las observaciones recientes del autor se conservan literalmente en `APORTACIONES_AUTORALES_INTEGRAS.md`. El manifiesto conserva por archivo su origen, función y huella, y distingue la base reproducida de los deltas posteriores.
'''
    record('ENTREGA.md',note.encode(),'GENERATED_DELIVERY_NOTE','DELIVERY_ENTRY')
    entry=ROOT/'INICIO_AQUI.md'
    entry_before=entry.read_bytes()
    old_entry=next((x for x in manifest['files'] if x['path']=='INICIO_AQUI.md'),None)
    if old_entry is None or old_entry['sha256']!=digest(entry_before):
        raise RuntimeError('Entry does not match its preserved manifest record')
    record('versiones_previas/entrada_antes_deltas/'+digest(entry_before)+'.md',entry_before,
           'INICIO_AQUI_BEFORE_LATER_DELTAS','PRESERVED_PREVIOUS_ENTRY')
    entry_addition='''

## Actualización de la entrega: artículo X completo y ruta conjunta recomendada

El artículo X es el eje de esta entrega. A sus 155 fuentes LaTeX íntegramente conservadas se añade ahora **todo su suplemento original** en `fuentes/articulo_x/supplement/`, sin omisiones ni modificaciones. El manifiesto enumera individualmente esos materiales, sus orígenes y sus huellas. Su inclusión no modifica las fuentes anteriores ni los recibos de ejecución.

Para trabajar con la base formal **y las ampliaciones posteriores** de compatibilidad de Witt, acción y electrón, la ruta recomendada es el adaptador:

```sh
python3 -I -S reproducir.py --check
python3 -I -S reproducir_deltas.py --plan
python3 -I -S reproducir_deltas.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean
```

El último comando es una compilación y sólo debe ejecutarse cuando se desee reproducir el conjunto ampliado. `--plan` comprueba las fuentes y dependencias sin compilar. El control `--check` conserva su función documental sobre todos los archivos del manifiesto.

El comando `reproducir.py --lean` explicado anteriormente corresponde exclusivamente a la **base de 74 módulos y 13 objetivos focales**. Su resultado original permanece en `recibos/reproduccion/LEAN_REUBICADO.json`. Las ampliaciones están en `deltas/` y mantienen sus propios recibos incrementales; no se atribuyen a aquella ejecución base. Los controles propios del suplemento permanecen conservados, pero no se ejecutan por el mero hecho de incorporarlos.

`ENTREGA.md` reúne estas distinciones operativas. Todo el contenido previo de este documento se mantiene arriba y su copia anterior se conserva en `versiones_previas/entrada_antes_deltas/`.
'''
    entry_after=entry_before+entry_addition.encode('utf-8')
    entry.write_bytes(entry_after)
    old_entry.update(sha256=digest(entry_after),bytes=len(entry_after),
                     source='PRESERVED_ENTRY_WITH_APPEND_ONLY_DELIVERY_UPDATE',role='PACKAGE_ENTRY')
    manifest['manifest_before_later_deltas_sha256']=digest(raw_manifest)
    manifest['later_deltas']=[dict(name='WittReaderCompatibility',status=witt['status'],
        part_of_base_relocation_run=False),dict(name='SelectedActionElectron',status=action['status'],
        part_of_base_relocation_run=False)]
    manifest['article_x_supplement']=dict(source=str(SUPPLEMENT),
        path='fuentes/articulo_x/supplement',files=len(supplement_files),bytes=supplement_bytes,
        preservation='COMPLETE_BYTE_IDENTICAL_COPY',executed_in_this_addition=False,
        part_of_base_relocation_run=False)
    path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    archive=ROOT.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for name in sorted({item['path'] for item in manifest['files']}|{'MANIFIESTO.json'}):
            z.write(ROOT/name,Path(ROOT.name)/name)
        if z.testzip():
            raise RuntimeError('ZIP integrity failure')
    print(json.dumps(dict(status='PASS_LATER_DELTAS_PRESERVED',files=len(manifest['files']),
        zip=str(archive),sha256=digest(archive.read_bytes())),ensure_ascii=False))

if __name__=='__main__':
    main()
