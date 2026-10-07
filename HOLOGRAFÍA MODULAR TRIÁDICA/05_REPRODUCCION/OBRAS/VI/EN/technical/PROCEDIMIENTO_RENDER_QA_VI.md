# Preparación técnica y revisión visual de los dos volúmenes

Corte de inspección: 10 de septiembre de 2026. Este procedimiento no modifica
las fuentes, el preflight ni su estado. La compilación de lectura autorizada
por el editor principal se distingue de una entrega científicamente cerrada.

## Infraestructura verificada

- LuaHBTeX 1.18.0, TeX Live 2024; `latexmk` 4.83.
- Poppler 26.05.0: `pdfinfo`, `pdftoppm`, `pdffonts` y `pdftotext`.
- STIX Two Text regular, negrita, cursiva y negrita cursiva, y STIX Two Math,
  resueltas por `kpsewhich` en TeX Live.
- Todos los paquetes declarados en ambos maestros están disponibles, incluido
  `mathtools`, que aporta `\xmapsto`.
- Pillow 12.3.0 en el Python 3.12 del runtime documental. No se requiere PyMuPDF.

La caché tipográfica de la compilación de lectura es local a
`build_lectura/texcache`. No ejecutar dos primeras compilaciones simultáneas
sobre esa misma caché. El editor principal está realizando la compilación;
esta subtarea no la duplica.

## Reparto propuesto, ya reflejado en las fuentes maestras

**Artículo principal:** núcleo común, generación regional, aritmética de
historias, dependencias anteriores, persistencia, conjugación, atlas, operador
de masa, ocupación, familias, composición, lectura orbital, metrología,
conclusiones y apéndices demostrativos. Conserva además las tablas completas
de 13 multisecciones, 56 familias y 23 clases.

**Volumen de datos compañero:** repite esas tablas y añade las 324 fichas de
ruta, con 65 campos por ficha, y los 471 registros de masas y 384 de anchuras.
Su guía distingue estructuras internas y observaciones externas. No sustituye
ninguna demostración del artículo.

El comprobador del generador devuelve, en modo de sólo lectura,
`PASS_FUENTES_APENDICES_DOCUMENTALES_VI`, con las cantidades anteriores y sin
eliminar duplicados ni recalcular valores. La fuente del catálogo completo
tiene 28.656 líneas y 324 tablas de ficha, además de las tablas metrológicas.
Cabe prever **cientos de páginas**, no fijar una cifra antes de compilar:
cada ficha contiene 27 filas agrupadas, varias de ellas multilínea. Reducir
todo a una tabla de 65 columnas perjudicaría gravemente la lectura.

## Puntos técnicos que requieren inspección

1. Una fila de `longtable` no puede partirse entre páginas. Las secuencias,
   huellas y estados largos deben caber por fila; las tablas sí pueden continuar.
2. Comprobar las columnas más estrechas de masas y anchuras, en particular
   identificadores, incertidumbres asimétricas, unidades y estados.
3. Los capítulos del maestro principal empiezan tras `\clearpage`; sus
   subsecciones tienen reserva vertical. Revisar también los títulos no
   numerados de las 324 fichas, las cabeceras repetidas y los pies de continuación.
4. Confirmar glifos griegos en texto, signos, exponentes, identificadores con
   guiones bajos y la distinción entre raya y dato vacío.
5. Los índices y referencias necesitan convergencia de pasadas. Un primer PDF
   no es el corte visual definitivo.

La nota `README_APENDICES_CATALOGO.md` conserva la frase histórica «El artículo
principal no se ha editado». El maestro actual sí incluye la sección 11;
esa frase debe actualizarse al cerrar el expediente. No se ha modificado aquí.

## Ejecución portable del QA, sobre PDFs estables

El programa `technical/qa_pdf_lectura_vi.py` **no compila**. Necesita Python
con Pillow y los cuatro ejecutables Poppler en PATH o en `--poppler-bin`.
Recibe un PDF ya producido y una carpeta de resultados distinta de las fuentes.

```sh
python3 technical/qa_pdf_lectura_vi.py RUTA_ARTICULO.pdf qa/articulo --dpi 120 --log RUTA_ARTICULO.log
python3 technical/qa_pdf_lectura_vi.py RUTA_CATALOGO.pdf qa/catalogo --dpi 120 --log RUTA_CATALOGO.log
```

En este equipo, el intérprete y el directorio completo de Poppler son:

```text
/Users/ruben/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12
/Users/ruben/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin
```

Cada ejecución extrae metadatos, texto y fuentes; renderiza **todas** las
páginas a 120 dpi en lotes de 20; crea planchas de 6 páginas con ordinales
físicos; registra palabras que exceden el papel y avisos del log; y verifica
que el PDF no haya cambiado mientras se examinaba. El resultado no marca la
revisión visual como completada: ese paso corresponde al examinador.

## Cierre de revisión visual

- Recorrer todas las planchas y registrar sus intervalos revisados.
- Abrir a resolución completa todas las páginas con ecuaciones extensas,
  tablas densas, figuras, cambios de sección y cualquier anomalía detectada.
- Examinar inicio, continuación y final de cada tabla. Las planchas permiten
  localizar páginas; no sustituyen la inspección de texto pequeño.
- Repetir a 180–200 dpi los detalles cuya legibilidad no pueda decidirse.
- Resolver errores de compilación, glifos ausentes, referencias indefinidas,
  desbordes materiales y filas cortadas; distinguir los avisos inocuos.
- Conservar conteos de 324/471/384 y comprobar, en el texto extraído y las
  páginas, los ordinales iniciales, finales y las continuaciones.
- Guardar huellas y páginas de cada volumen sólo después de la última pasada.

Los controles de tablas y composición acreditan conservación documental y
legibilidad. No alteran el estado separado de autonomía demostrativa.
