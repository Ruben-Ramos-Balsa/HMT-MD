# Entrega reunida: generación del registro y continuidad de sus aplicaciones

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
