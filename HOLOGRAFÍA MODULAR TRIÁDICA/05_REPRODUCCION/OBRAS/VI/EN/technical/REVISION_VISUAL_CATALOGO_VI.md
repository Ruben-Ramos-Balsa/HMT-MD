# Revisión visual final del catálogo documental del Artículo VI

## Identificación y alcance

PDF: `output/pdf/ARTICULO_VI_CATALOGO_ESTRUCTURAL_Y_METROLOGICO.pdf`.

SHA-256: `0e38f54e1735e6380112e1567bd6f0b13f11891df6293965a2b05228884184ad`.

Extensión: **570 páginas físicas**, correspondientes a portada y páginas impresas 1–569. Renderizado completo a 90 dpi con Poppler. Esta revisión comprueba la publicación material y su legibilidad: no es una certificación de las afirmaciones matemáticas o físicas ni del expediente de autonomía.

## Cobertura visual efectiva

La primera versión de 570 páginas fue revisada íntegramente mediante 95 planchas de contacto y ampliaciones focales. Tras la corrección tipográfica final, la comparación de las 570 imágenes RGB identifica **410 páginas cambiadas y 160 idénticas**. Se han vuelto a revisar las 410 cambiadas y, además, 142 idénticas: **552 páginas del render final**. Las 18 restantes (493–498, 541–546 y 559–564) son idénticas píxel a píxel a las imágenes ya revisadas. Por tanto, la cobertura material del sucesor es 570/570, sin atribuir una segunda inspección a esas 18 páginas.

Reparto de la revisión: páginas físicas 1–288 por `indice_articulos`; páginas 289–570 por `qa_catalogo_tramo_final`. En el render final se ampliaron específicamente las páginas 18, 242, 350, 474 y 528. La revisión anterior conserva otras ampliaciones de transiciones, fichas, tablas de masas y anchuras.

**Resultado visual:** no se detectan recortes, solapamientos ni campos ocultos en la cobertura descrita. Las fichas extensas continúan entre páginas con encabezado y aviso; las unidades, incertidumbres y etiquetas de procedencia permanecen visibles. No se observan filas cortadas por el borde de la página. Algunos campos largos ocupan varias líneas y algunas fichas comienzan al final de una página; su continuación está señalada y no implica pérdida de datos.

## Incidencia detectada y corrección comprobada

El primer render convertía guiones literales consecutivos en ligaduras tipográficas: por ejemplo, `+++---+++---` y el doble signo de `Deltabar(1700)--`. La primera tentativa `-{}-` no alteró ninguna de las 570 imágenes y no fue aceptada como corrección efectiva. Se conserva ese informe como antecedente en `qa/catalogo_signos_final/INCIDENCIA_LIGADURAS_PERSISTENTES.md`.

La protección final mediante `-\kern0pt{}-` sí conserva los caracteres consecutivos con LuaLaTeX y STIX. Las páginas físicas 474 y 528 muestran los dobles menos separados; las fichas ampliadas muestran los signos sucesivos individualizados. Además de la inspección visual, la extracción del PDF final permite comparar literalmente **las 324 secuencias de doce signos y las 324 firmas de familia** con sus registros JSON. Ambas comparaciones son exactas y completas.

## Controles documentales y técnicos

El control reproducible `technical/verificar_publicacion_catalogo.py` verifica el PDF final, no sólo la fuente TeX. Comprueba:

- Las 324 fichas de rutas, con ordinales 001–324 en su orden.
- Las 324 secuencias `tau12` de longitud 12 y las 324 firmas de familia, sin normalizar ni borrar signos.
- Los 471 registros de masas y los 384 registros de anchuras, incluidos todos sus ordinales y etiquetas de fuente.
- El signo doble literal de `Deltabar(1700)--` en ambas tablas.
- La huella del artefacto, las 570 páginas y la inclusión de las fuentes tipográficas.

El render completo registra cero cajas de texto fuera de la página y cero incidencias detectadas en el log final por el control técnico (desbordes, referencias indefinidas y glifos ausentes, entre sus patrones). Las imágenes y los datos geométricos permanecen en `qa/catalogo_signos_corregidos/`; los recibos y este informe se incluyen en la entrega sin necesidad de incorporar los 570 PNG al ZIP.

## Reproducción portable

Desde la carpeta raíz del Artículo VI, con Poppler instalado:

```sh
python3 technical/verificar_publicacion_catalogo.py --output technical/CONTROL_MATERIAL_CATALOGO_VI.json
```

Si las herramientas de Poppler no están en `PATH`, añadir `--poppler-bin /ruta/a/poppler/bin`. El script utiliza únicamente la biblioteca estándar de Python. La salida material satisfactoria no modifica el estatuto de los registros internos, las condiciones declaradas en las fuentes ni la función comparativa de las tablas metrológicas externas.

Se utilizó la habilidad de PDF para el flujo renderizado–inspección–corrección–reinspección. No se recompilaron ni modificaron fuentes matemáticas durante esta revisión delegada.
