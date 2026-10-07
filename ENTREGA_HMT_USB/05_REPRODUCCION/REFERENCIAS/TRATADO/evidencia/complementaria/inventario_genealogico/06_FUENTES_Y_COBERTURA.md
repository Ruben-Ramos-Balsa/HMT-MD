# Fuentes, cotejo y cobertura de lectura

## Alcance del censo documental inicial

La selección contiene 56 raíces explícitas: paquetes registrados de la serie y adyacentes, el integral con su base conservada, el reservorio, los sucesores focales de IX/X, desarrollos de K, geometría positiva, memoria, espejo y diagonal, núcleo común y narración. Ninguna de esas raíces ha resultado inaccesible en el censo. Sus carpetas y sus funciones figuran en `censo/RAICES.json`.

El censo enumera **116.287 rutas de archivo**. Incluye traducciones, antecedentes, copias en paquetes y archivos auxiliares: no son 116.287 resultados distintos. De esas rutas, 84.471 archivos textuales tienen huella de contenido. La agrupación de duplicados permite reconocer copias sin eliminar ninguna de sus procedencias.

Los 1.435.385 localizadores candidatos detectados incluyen títulos, etiquetas, inclusiones, entornos de prueba y declaraciones de código. Son entradas de búsqueda automática, **no fichas matemáticas ya examinadas**. La lectura semántica no puede reducirse a esos marcadores: hay argumentos sin encabezado y un mismo resultado puede tener muchos marcadores.

Los JSONL se comprimen sin pérdida para ahorrar espacio. Se pueden recuperar íntegramente con `gzip -dc`; la compresión no abrevia, sintetiza ni modifica el texto registrado. Las fuentes originales permanecen en sus carpetas.

## Instrumentos del expediente

- `censo/ARCHIVOS.jsonl.gz`: ruta, pertenencia a raíces, tamaño, extensión y huella textual cuando corresponde.
- `censo/LOCALIZADORES_CANDIDATOS.jsonl.gz`: localizador, línea y texto íntegro de la línea detectada.
- `censo/DUPLICADOS_POR_CONTENIDO.json`: agrupaciones de huellas, sin eliminación de copias.
- `censo/CANDIDATOS_INTRODUCCIONES_Y_NUCLEOS.json`: candidatos a cotejar entre artículos; no acredita identidad ni inclusión en PDF.
- `censo/GRAFO_TPK_FUENTE_INTEGRA.json`: copia íntegra del grafo consultado.
- `censo/FICHAS_NUCLEO_TIPADO.json`: nodos, relaciones y resultados externos tipados extraídos sin resumir sus campos.
- `censo/RESUMEN.json`: cómputos, alcance y errores de recorrido.

## Matriz de cobertura semántica

| Fuente | Función en el inventario | Estado de esta entrega |
|---|---|---|
| Núcleo formal y grafo tipado | Tipos, operaciones, dependencias y conservación | Consultados; 39 nodos y 107 relaciones preservados en copia; propietarios requieren lectura propia |
| Núcleo común `sections/nucleo.tex` | Primer desglose APP–TRIT–TPK | Archivo completo leído, 29 fichas iniciales; inclusiones declaradas aparte |
| Fuentes de emisión, selección y R36 | Censos, cinco regiones, elevaciones y frontera | Lectura focal documentada en 02 |
| Coinducción y geometrías | Relojes, prolongación, retorno, espacios de realización | Lectura focal documentada en 03 |
| K, alfa e incidencia | Descriptor, selector, clausuras y realizaciones | Lectura focal documentada en 04 |
| Integral completo, síntesis y cadena compacta | Base extensa y diferencias expositivas | Censados; lectura íntegra comparada para este inventario todavía no terminada |
| Introducciones y núcleos de los diez artículos | Concordancia con la base extensa | Candidatos localizados; cotejo global por completar |
| Reservorio estructural | Ampliaciones no necesariamente incorporadas al integral | Localizado y censado; revisión integral por completar |
| Narración coinductiva | Explicaciones y detalles a vincular con pruebas | Ediciones localizadas y censadas; nueva lectura sistemática por completar |
| Sucesores IX/X y pendientes retrospectivos | Preservación e integración posterior | Pendientes recuperados de su informe; no se modifica ni recertifica su matemática |

## Qué se completará en siguientes iteraciones

Control focal reproducido en esta entrega: `tools/comprobar_app_elemental.py` recorre las 81 celdas y verifica los seis totales de APP-016, la descomposición de APP-017, el ejemplo de APP-008 y las dos lecturas de APP-019. Su salida es `PASS_APP_ELEMENTAL_FOCAL`. También se contrastaron esos puntos con el núcleo común mediante una lectura independiente. El control no verifica por extensión los demás resultados ni sustituye sus pruebas.

1. Cotejo material de las introducciones y sus inclusiones reales; registrar copias idénticas, ampliaciones y variantes sin elegir por longitud.
2. Lectura del reservorio completo y asignación de sus resultados a fichas; localizar sus propietarios y saber qué está ya en el integral o sólo en un desarrollo posterior.
3. Subinventario de cada transformación elemental, comenzando por APP y los cambios de carta indicados por el autor.
4. Vinculación bidireccional de dependencias: de cada operación a sus consumidores y de cada resultado a todos sus antecedentes efectivos.
5. Inventario de figuras, ejemplos y pruebas que un lector necesita para reproducir el recorrido, aunque no constituyan un teorema con nombre.

No se fija una cifra final de fichas ni se considera completo el inventario por haber cerrado el censo de archivos.

## Concordancias recuperadas al reunir los tramos

1. **Frontera R36.** SR-032–SR-035 conservan el rastreo inicial, donde el ejecutable de selección no había sido localizado. CG-006 aporta ahora `generate_target_free_r36`, el selector propietario y el recibo `recibo_r36_smoke_8.json`: el enlace Python deja de estar pendiente en este expediente. Sigue sin anunciarse una formalización Lean de ese selector. La exposición LaTeX selecciona la orientación semiabierta; el ejecutable minimiza longitudes de recorrido 23/20. Ambos dan la misma terna, pero la equivalencia exacta de esos criterios debe recibir su propia subficha antes de tratarlos como un único argumento.
2. **APP y geometrías.** APP-004–019 y CG-001–003/012 se solapan deliberadamente desde fuentes distintas: el primero desglosa operaciones elementales; el segundo explicita sus consumidores geométricos. Se conservan ambas procedencias. La siguiente revisión añadirá relaciones de concordancia entre IDs, sin borrar uno de los textos por duplicación aparente.
3. **Elevaciones y generación de K.** SR-028–031, CG-005 y KA-003 distinguen la producción TPK de los registros de transición y la reconstrucción de las matrices desde esos registros. La existencia de una prueba de inversión no elimina la obligación expositiva de mostrar la producción de cada fila. Esta lectura no declara ausente el mecanismo del corpus.
4. **Coinducción y alfa.** CG-008 identifica el residuo interno inicial y su actualización; KA-014–018 describe las publicaciones de alfa a toda profundidad y su dependencia de la precoordenada. Las dos descripciones deben componerse mediante sus objetos, no sólo por el nombre de la constante. Conservar ambas evita sustituir una etapa por un lector analítico posterior.

Estas concordancias son parte de la revisión activa solicitada: una pieza localizada en un tramo actualiza la situación documental de los demás, sin reiniciar el trabajo ni borrar el rastreo anterior.
