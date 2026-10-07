# Artículo I — incidencias temporales y orientaciones del vecino marcado

Este paquete conserva íntegra la entrega `PAQUETE_ARTICULO_I_LECTURA_CONJUNTA_20260920`
y añade dos composiciones de resultados del manuscrito. No cambia los PDF.
Los archivos anteriores permanecen por contenido; los README y manifiestos
anteriores quedan además en `versiones_previas`.

## Qué ejecuta esta continuación

1. Reutiliza APP–TRIT–TPK, los lectores regionales y sus prefijos producidos,
   la selección terminal, los cilindros, la incidencia y el vecino marcado.
2. `HistoricalIncidenceEvaluation` evalúa las diecinueve incidencias temporales
   impresas del repertorio terminal. Los tiempos, las posiciones, las clases
   de carga y las orientaciones son el calendario explícito del pasaje;
   las palabras se calculan desde los prefijos regionales. Se prueban las ocho
   lecturas únicas, la recuperación del conjunto no ordenado y su composición
   con el selector existente, sin volver a hacer su enumeración.
3. `FullSupportNeighborOrientations` prolonga la acción reticular a todas
   las orientaciones de soporte completo especificadas en el manuscrito.
   Conserva el código, el origen marcado y el vecino construidos previamente.

La cadena mantiene sus salidas internas como antecedentes de la etapa posterior.
No introduce valores metrológicos como generadores ni retira K por existir
otra presentación de alfa. El retorno de fase y el avance de memoria conservan
la distinción formal de las pruebas anteriores.

## Corrección aritmética localizada

La tabla de incidencias y sus palabras ternarias dan, por posiciones,

`55, 175, 498, 437, 98, 28, 687, 714`.

En una conversión decimal del texto se habían intercambiado los dos últimos:
`221110` en base tres vale `687`; `222110` vale `714`. La prueba Lean verifica
la lista correcta y rechaza la transpuesta. Esto no cambia el conjunto no
ordenado entregado al selector ni su resultado K. Se conserva el original
como procedencia; no se modifica silenciosamente un PDF sellado.

## Alcance exacto

La evaluación del calendario histórico no prueba su selección desde todas
las coordenadas microscópicas del estado enriquecido. Las simetrías del
vecino marcado no sustituyen la formalización del reconocimiento de Leech
ni la construcción FLM/Moonshine. Esta entrega no certifica todavía el
cierre Lean íntegro del artículo I. Tampoco declara que esos resultados
no existan en el corpus matemático.

Los certificados de conservación, los controles de metadatos y la compilación
son comprobaciones distintas. El alcance matemático se lee en los enunciados.
La evaluación nueva de incidencias usa el kernel; la composición con el
selector conserva su dependencia anterior, declarada, de `Lean.ofReduceBool`.

## Reproducción

Lean 4.21.0; Mathlib `308445d7985027f538e281e18df29ca16ede2ba3`.

```sh
python3 -I -S reproducir_incidencias_orientaciones.py --plan
python3 -I -S reproducir_incidencias_orientaciones.py --mathlib /ruta/mathlib4 --lean /ruta/lean
```

El plan reconstruye la clausura de imports. La ejecución comprueba huellas y
compila las fuentes necesarias; reutiliza objetos sólo cuando coinciden sus
fuentes, dependencias y compilador. Las cachés locales no sustituyen las
fuentes del ZIP. Los registros históricos conservan sus rutas de procedencia;
el ejecutor usa las rutas relativas de este paquete para la reproducción.
