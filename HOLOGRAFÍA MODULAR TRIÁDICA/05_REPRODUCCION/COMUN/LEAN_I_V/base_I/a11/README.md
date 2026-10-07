# Artículo I — covarianza, cargas y firma regional

Sucesor aditivo de `PAQUETE_ARTICULO_I_INCIDENCIAS_ORIENTACIONES_20260920`:
270 módulos anteriores, ocho módulos nuevos y `N30Transport`, ya conservado
en el paquete pero ahora incluido por sus imports en la clausura:
279 módulos en total.
Conserva por SHA-256 los 909 archivos del manifiesto anterior. El README
anterior se conserva íntegro en `versiones_previas`; también se archiva su
manifiesto. No se modifican originales, fuentes científicas ni PDF.

## Estado de la entrega

El ensamblado inicial es **NO SELLADO**. Los recibos focales copiados son
antecedentes reales, no una reproducción conjunta. El sellado requiere el
PASS de toda la clausura, el sondeo de las declaraciones nuevas, la
preservación de huellas, el control de metadatos causales y la comprobación
del ZIP. El estado efectivo se consulta en `MANIFIESTO.json` y en
`recibos/covariancia_firma/LEAN_CONJUNTO.json`, cuando este último exista.

## Composiciones incorporadas

- `CoxeterChargeCovariance`: Covarianza de cargas y modos cero bajo el lift de orden tres sobre el portador y cociclo existentes.

- `LatticeCoxeterFieldCovariance`: Covarianza de cada coeficiente del campo cargado con su fase explícita de cociclo, sin cambiar el portador.

- `ChargeChartCompatibility`: Igualdad para toda palabra natural de la carga dual y wordCharge después de transform6; conservación de los lectores históricos, sin identificar las acciones matriciales.

- `RegionalSynchronizationSignature`: Capacidades, firma regional [85,112,41,52], determinante -172, defecto normalizado 4 y reapertura desde prefijos generados de 600 trits; sin entrada K/S8.

- `AgendaSupport`: Recuperación invariante bajo igualdad de soportes y referencia singleton; conserva estas hipótesis y no genera la agenda histórica.

- `RegionalClockComposition`: Identificación de capacity con publicationClock para t < 23, pausa, reapertura y evaluación regional común.

- `N30BoundaryTransport`: Balance de extremos, incremento espacial, defecto de hoja y memoria sobre la misma trayectoria N30; retorno de fase a nueve pasos, no selector K ni identificación con toda la holonomía global.

- `LatticeCoxeterHeisenbergCovariance`: Covarianza para todos los modos enteros de Heisenberg sobre el mismo portador; reúne orden tres exacto, vacío fijo y conjugación de todos los campos cargados, reutilizando las pruebas precedentes.

El resultado previo `terminal_selection_unique` permanece central e íntegro:
selección conjunta excepcional–temporal `19446 → 79 → 1` sobre
`C_dec(W24,S8,panel)`, sin tomar `K` como entrada del selector. Esta
continuación no repite ese censo ni lo sustituye; tampoco lo reduce a una
inversión del valor terminal. Conserva su dominio y sus hipótesis documentadas.

Se mantienen la cadena APP–TRIT–TPK y sus salidas internas como antecedentes
de las operaciones posteriores. No se introducen valores metrológicos como
generadores. Los nuevos puentes de lectores, agenda, covarianza y frontera
complementan ese resultado; no se presentan como el productor microscópico
completo del dominio conjunto.

Las matrices regional y terminal no se identifican literalmente: se prueba
la igualdad de su funcional escalar de carga y su compatibilidad con el
lector. `AgendaSupport` conserva explícita la hipótesis de igualdad de
soportes y no produce la agenda histórica. La identificación regional de
relojes de `RegionalClockComposition` está probada en el intervalo `t < 23`;
no se presenta como igualdad global de calendarios de tipos diferentes.
`N30BoundaryTransport` conserva extremos, defecto de hoja y memoria sobre
una misma trayectoria. Su retorno de fase `Fin 3` a nueve pasos no identifica
por sí solo toda la dinámica enriquecida de la holonomía nonádica. Su control
negativo se conserva fuera de las raíces de módulos productivos.

## Alcance exacto

Esta entrega no declara cerrado el artículo I completo, la producción de la
agenda histórica desde toda la dinámica microscópica, la eliminación de la
interfaz S8, la construcción del sector torcido, el producto orbifold ni
FLM/Moonshine. No convierte esas reservas de formalización en afirmaciones
de ausencia matemática en el corpus.

La compilación, la conservación de archivos y el control de metadatos son
comprobaciones distintas. Los enunciados Lean conservan sus hipótesis. Los
módulos nuevos se sondean en todas sus declaraciones públicas; las pruebas
privadas utilizadas quedan incluidas por dependencia transitiva. Se exigen
únicamente `propext`, `Classical.choice` y `Quot.sound` en esos sondeos. La
clausura anterior conserva sus axiomas declarados, incluida la dependencia
previa del selector en `Lean.ofReduceBool`.

## Reproducción portable

Lean 4.21.0; Mathlib `308445d7985027f538e281e18df29ca16ede2ba3`.

```sh
python3 -I -S reproducir_covariancia_firma.py --plan
python3 -I -S reproducir_covariancia_firma.py --mathlib /ruta/mathlib4 --lean /ruta/lean
```

El ejecutor registra `causal_covariance_successor` y `deltas/covariancia_firma`
después de todas las secciones anteriores. Reconstruye el orden topológico
de imports; en particular, `RegionalSynchronizationSignature` precede a
`RegionalClockComposition`, y `HistoricalIncidenceEvaluation` precede a
`ChargeChartCompatibility` y `AgendaSupport`.

La copia local conserva la caché anterior. Su reutilización exige coincidencia
de fuente, dependencias, compilador y objeto; no se adoptan objetos focales
sin recibo de caché. El ZIP incluye fuentes y recibos, no la caché local de
`resultados`. Las rutas absolutas de los recibos originales son procedencia;
la reproducción usa rutas relativas al paquete y runtimes explícitos.

## Preparación administrativa

`package_covariant_signature.py` se prepara y revisa antes de ejecutarlo.
Sin `--seal` ensambla una carpeta nueva; con `--seal` valida la reproducción
conjunta y crea el ZIP. Rechaza sobrescribir una carpeta de ensamblado o una
entrega ya sellada. Los módulos, namespaces, alcances y recibos están
declarados como datos. `--extra-config archivo.json` permite añadir módulos
y recibos previamente revisados; no altera ni retira los predeterminados.
