# Apéndices documentales del Artículo VI

## Archivos preparados

- `sections/11_apendices_catalogo.tex`: guía de lectura y tablas completas de las
  13 multisecciones, las 56 familias de ruta y las 23 clases documentadas. Está
  incorporada al artículo mediante `\input{sections/11_apendices_catalogo.tex}`.
- `sections/12_catalogo_datos_companero.tex`: las 324 rutas orientadas, con los
  65 campos de la unión literal de sus dos tablas, y los 471 registros de masa
  y 384 registros de anchura. Conserva todos los ordinales; no deduplica filas.
- `main_catalogo.tex`: fuente independiente para un volumen compañero de datos.
  Incluye las dos fuentes anteriores. Usa los paquetes ya empleados en el
  artículo, tablas multipágina y cuerpo de 10,5 puntos. Compilado en 570 páginas.
- `technical/apendices_catalogo_control.json`: recuentos, huellas de fuentes y
  salidas, correspondencia de ordinales, comprobaciones de campos comunes y
  validación estática del escapado y de las estructuras LaTeX.

La fuente 11 forma parte del artículo principal. La compilación del volumen
compañero y su revisión visual se registran por separado: estos controles de
fuente no certifican cortes de página, ausencia de desbordamientos ni diseño.
La anchura de las tablas se adapta a `\linewidth`, tanto con los márgenes del
artículo como con los del volumen compañero.

Las palabras de prosa y los rótulos no reciben fragmentación discrecional
artificial: su división corresponde al idioma de composición. Los identificadores
se pueden partir en sus delimitadores; sólo las cadenas numéricas largas, las
huellas y los códigos puros largos admiten partición en bloques de ocho caracteres.
Estas oportunidades de salto no cambian los caracteres de origen. «Celdas
(identificadores)» distingue la lista de identificadores del rango o del número
de celdas de cada registro.

La edición de lectura protege todos los guiones consecutivos de los valores
documentales contra las ligaduras de TeX. Así, las doce posiciones de una firma
y las cargas dobles conservan cada signo individual. El control
`literal_signs_not_ligated` reproduce esta corrección; los JSON permanecen intactos.

## Qué contiene cada nivel

Las tablas 13/56/23 publican campos pertinentes de incidencia, orientación,
clasificación y lectores. No sustituyen las demostraciones internas. Las
evaluaciones extensas y todos los campos originales siguen íntegros en sus
JSON y CSV de procedencia. Una familia de ruta no se cuenta como especie.

Cada una de las 324 fichas publica **todos los campos** de ambas tablas de
rutas: identidad, clasificación, retornos, memoria, firma, diferencias,
lectores, evaluaciones, separación de prefijos, secuencias, estados y huellas.
Los 45 campos comunes se cotejan literalmente para cada identificador antes
de representarlos una sola vez. Se conservan los ordinales de las dos tablas,
que tienen distinto orden. Si apareciese una clave repetida o una divergencia,
el generador se detendría para tipar la correspondencia; no la corregiría ni
deduplicaría silenciosamente.

Las 855 observaciones externas conservan identificador, descripción del
observable, especies, valor literal, presentación alternativa cuando difiere,
unidad, incertidumbres de ambos signos, tipo, confianza y notas de estado.
Las notas usan diccionarios reversibles que muestran el código literal y su
explicación. El corte PDG 2026, de fecha documental 2026-01-15, permanece
congelado. No se recalculan valores, no se consultan actualizaciones y no se
promueven registros condicionados a predicciones. Esquema y escala figuran
uniformemente como no disponibles en la instantánea; la condición se explica
antes de las tablas y se comprueba sobre cada fila.

## Regeneración y controles

Desde la raíz del Artículo VI:

```sh
python3 -I -S technical/generar_apendices_catalogo.py --self-test
python3 -I -S technical/generar_apendices_catalogo.py
python3 -I -S technical/generar_apendices_catalogo.py --check
```

`--check` reconstruye las fuentes esperadas en memoria, compara sus bytes y
no escribe. El generador sólo modifica sus cuatro salidas declaradas. No
modifica el catálogo preservado, el artículo principal, las pruebas ni las
fuentes de otras secciones. No invoca LaTeX, no crea PDF y no necesita red.

El rótulo `PASS_FUENTES_APENDICES_DOCUMENTALES_VI` certifica exclusivamente la
generación documental y los controles estáticos descritos. No es un veredicto
matemático, una certificación metrológica ni una validación visual.
