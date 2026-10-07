# Artículo VI, REV02: navegación del catálogo

Revisión editorial de navegación y conservación literal, 10 de septiembre de 2026.
Esta comprobación no evalúa las masas ni cambia su estatuto documental.

## Artefacto revisado

- PDF: `build_navegacion/ARTICULO_VI_CATALOGO_REV02_NAVEGACION.pdf`.
- Páginas físicas: **608**; portada sin numerar, seguida de 607 páginas impresas.
- SHA-256: `f8e08f34fd852b2bddd9e4d92191bdf56032165e5b7cd945c355d7ed4d5263e8`.
- Fuente de las fichas: `sections/12_catalogo_datos_companero.tex`.
- SHA-256 de esa fuente: `fface06da019ede7e7b4651e7521a1a14c671249e86d9b526fd41b5bfef88b5e`.

La compilación se ha hecho en una carpeta separada de REV02. No se ha sustituido
el PDF original ni se han editado el manuscrito principal, el núcleo común o las
secciones de otros responsables. La paginación adicional procede del índice y
del espacio reservado para que el título de cada ficha permanezca con su tabla;
no se han añadido registros ni reducido la tipografía.

## Implementación

1. Índice completo de 324 identificadores, en orden de la tabla unificada, con
   enlaces y páginas impresas calculadas por LaTeX. Ocupa las páginas impresas
   17–22 (físicas 18–23).
2. Árbol de marcadores PDF: 81 celdas, con 4 rutas orientadas por celda; total de
   324 marcadores de ruta. Cada ficha declara celda, fila, columna y orientación.
3. Identificador, ordinal y orientación en todas las cabeceras de continuación;
   el pie de continuación también conserva el identificador.
4. Enlace de retorno al índice desde cada ficha.
5. Reserva de espacio antes de cada ficha. La revisión intermedia detectó un
   título aislado de su tabla; la edición final lo corrige, y un control de las
   324 páginas de destino exige título y primera fila de datos en la misma página.
6. Se conserva la protección de signos literales mediante `\kern0pt{}` entre
   guiones consecutivos; no se sustituyen las firmas por ligaduras tipográficas.

## Controles reproducibles

`technical/verificar_navegacion_catalogo.py` produjo
`technical/NAVEGACION_CATALOGO_REV02.json` con resultado
`PASS_NAVEGACION_PDF_CATALOGO`. El CSV
`technical/INDICE_RUTAS_PAGINAS_REV02.csv` conserva el mapa de los 324
identificadores a su página física e impresa.

Se comprobaron materialmente:

- 324 cuerpos de fichas idénticos, campo por campo en su fuente LaTeX, a la
  edición anterior: 65 campos por ruta.
- Inventario metrológico íntegro sin cambios: 471 masas y 384 anchuras.
- Archivos `technical/catalogo_*.json` y apéndice 11 idénticos a la edición
  anterior; se conservan 13 multisecciones, 56 familias y 23 clases.
- 81 marcadores de celda y 324 marcadores de ruta presentes en el PDF.
- 324 destinos con el identificador correcto, el título y la primera fila de
  la tabla presentes en la página de destino.
- 324 referencias del índice visible concordantes con los destinos y las
  etiquetas AUX de páginas impresas.
- 324 instancias de continuación con identificador de ruta y orientación.
- Registro final de compilación sin `Overfull`, `Underfull`, referencias
  indefinidas, destinos duplicados, caracteres ausentes o aviso de recompilación
  por cambio de etiquetas.

Comandos (desde la carpeta REV02):

```sh
python3 -I -S technical/generar_apendices_catalogo.py --self-test
python3 -I -S technical/generar_apendices_catalogo.py --companion-only --check
python3 technical/verificar_navegacion_catalogo.py \
  --predecessor ../ARTICULO_VI_PARTICULAS_Y_MASAS_20260910 \
  --pdf build_navegacion/ARTICULO_VI_CATALOGO_REV02_NAVEGACION.pdf
```

El último comando requiere `pypdf`; se ejecutó con el intérprete del runtime
local que lo incluye. `--companion-only` comprueba que la sección 11 no variaría
antes de regenerar exclusivamente el catálogo compañero y su recibo.

## Inspección visual focal

Se renderizaron y leyeron a 100 dpi **17 páginas físicas** de la edición final:
1, 2, 18–27, 264–265 y 508–510. Comprenden portada, índice general, las seis
páginas del índice de rutas, las primeras fichas y sus continuaciones, la celda
central 41 y el final de las fichas con la transición al inventario externo.

El índice es legible y conserva las columnas de identificador/página. Las
fichas revisadas muestran sus cabeceras y pies identificados sin solapamientos;
los títulos no quedan aislados de sus tablas. La celda 41 comienza en la página
impresa 263, y la ruta 324 en la 507. El inventario externo comienza en la 509.
No se detectaron recortes, filas cortadas horizontalmente ni pérdida visible
de campos en estas páginas.

Esta es una inspección visual **focal**, complementada por los controles
automáticos de los 324 destinos y continuaciones. No se presenta como una nueva
lectura visual individual de las 608 páginas ni como una certificación científica.

Habilidades aplicadas: `preserve-hmt-continuity`, `verify-hmt-mass-law` y `pdf`;
su efecto fue mantener los datos y estados de procedencia, separar la navegación
de la verificación matemática y comprobar el PDF después de la generación.
