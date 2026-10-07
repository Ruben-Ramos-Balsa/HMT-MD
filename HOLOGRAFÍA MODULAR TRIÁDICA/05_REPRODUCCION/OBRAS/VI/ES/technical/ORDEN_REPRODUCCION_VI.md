# Orden de lectura y reproducción del Artículo VI

Este archivo acompaña el borrador completo de lectura y su catálogo, no una
declaración de cierre científico de todas las dependencias.
La cadena de lectura parte de APP, TRIT y TPK; el contraste convencional
pertenece a la etapa posterior de identificación y comparación. Los programas
de esta carpeta tienen alcances distintos y no se presentan como un único
generador completo por el mero hecho de ejecutarlos consecutivamente.

## 1. Núcleo y condiciones iniciales

Leer primero `sections/nucleo.tex` y sus tres desarrollos incluidos. Las
seis fuentes comunes se comparan, sin modificarlas, mediante:

```sh
python3 -I -S technical/preparar_nucleo_comun.py --check
```

Después se lee `sections/14_generacion_regional.tex` junto con su apéndice.
El programa siguiente enumera las condiciones iniciales y conserva el censo,
las fibras y la selección regional finita:

```sh
python3 -I -S technical/generar_catalogo_regional.py
```

Produce 104976 pares iniciales, 468 emisiones decimales, una imagen ternaria
de 243 elementos dentro del ambiente de 729, y 43 órbitas regionales. Su
recibo y las tablas completas no prueban por enumeración finita una
afirmación a profundidad ilimitada; las condiciones de prolongación se
exponen en el texto. El programa rechaza la ejecución optimizada si ésta
eliminaría sus controles.

## 2. Historias y coordenadas

Leer `15_aritmetica_historias.tex` antes de la interpretación de las
coordenadas y sus evaluaciones. Sus pruebas de composición, naturalidad y
refinamiento son generales. El testigo finito independiente se ejecuta con:

```sh
python3 -I -S technical/verificar_controles_historias_15.py
```

Seguir con `09_dependencias_anteriores.tex`. Los programas separan la
producción de la trayectoria central de 108 pasos, el prefactor de los
proyectores, la inversión del registro suministrado y las cotas de la escala:

```sh
python3 -I -S technical/verificar_controles_dependencias_09.py
```

En este control, las 25 incidencias son entradas de una **prueba inversa**.
El propio recibo declara `E108_produced: false`. Ejecutarlo después del censo
regional no convierte esas entradas en salidas del programa anterior. La
producción canónica del libro que debe enlazar ambas etapas está delimitada
en las dos notas de búsqueda y en `CONTRASTE_E108_CON_ARTICULO_II.md`.
La condición pendiente no se oculta ni se sustituye por una reconstrucción
retrospectiva. La normalización completa de alfa se conserva en el cuerpo;
una lista finita de sus cifras no reemplaza esa definición.

## 3. Partícula, atlas y operadores

Leer las secciones 02, 03, 04 y 05. La partícula persistente, la ruta
observable, la firma y el operador de masa son objetos diferentes. La
sección electrónica basal, la corrección de retorno y la carta dimensional
tampoco se intercambian.

```sh
python3 -I -S technical/verificar_construcciones_finitas.py
python3 -I -S technical/verificar_particula_mobius_kepler.py
```

Estos controles comprueban el atlas, las reconstrucciones, las involuciones
y los testigos de transporte en los dominios que indican sus recibos. No
seleccionan las etiquetas experimentales a partir de la masa observada.

## 4. Ocupación y familias

Leer la sección 13 para la completación graduada y las reglas de ocupación,
y después las secciones 08 y 10 para familias y composición. El modo
completo conserva espín, hoja, sabor y color:

```sh
python3 -I -S technical/verificar_fock_pauli.py
```

El programa realiza controles exactos de CAR, exclusión, censos y el defecto
de frontera de un corte bosónico; la demostración general permanece en el
manuscrito. Las condiciones de cada realización sectorial se conservan en
su sección y no se convierten en una predicción escalar universal.

## 5. Comparación, catálogos y estado editorial

Las secciones 06 y 07 desarrollan la relación orbital y el contraste
metrológico. Las tablas conservan por separado 471 registros de masas y
384 de anchuras: son observaciones de contraste, no el número de predicciones
del artículo. El catálogo completo permanece en el volumen compañero.

```sh
python3 -I -S technical/generar_apendices_catalogo.py --check
python3 -I -S technical/verificar_fuentes_vi.py
python3 -I -S technical/preflight_vi.py status
```

El control estático comprueba fuentes y referencias, no paginación. El
preflight conserva bloqueada la aceptación científica mientras las dependencias
no estén reunidas. Ninguno de los recibos finitos reemplaza ese cierre.

La edición material de lectura conserva públicamente ese alcance y se reproduce
mediante un programa separado, sin modificar el preflight:

```sh
python3 -I -S technical/compilar_lectura_vi.py --target all --passes 3
```

El resultado son el artículo de 117 páginas y su catálogo de 570 páginas. Los
recibos de compilación y revisión visual sólo acreditan esas operaciones.

## 6. Conservación sin sobreescritura

Un corte ya creado se verifica con:

```sh
python3 -I -S technical/conservar_corte_vi.py --check technical/cortes/20260910_01
```

Las ediciones posteriores deben crear un identificador sucesor. Las copias
guardan fuentes, datos y programas, incluidas las condiciones pendientes.
Los artículos I–V y el corpus de procedencia permanecen intactos.
