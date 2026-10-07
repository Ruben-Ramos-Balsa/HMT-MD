# Cobertura de transporte nonádico y momentos circulares

Conversión editorial íntegra del contenido matemático. No se han modificado los dos Markdown originales; no se ha compilado el PDF ni certificado la positividad global.

## Fuentes conservadas

- ampliacion/expediente/01_COSTURA_NONADICA_BALANCE_Y_CRITERIO_DE_TRANSPORTE.md — SHA-256 `6302c34641372208d9040a53f28de1defe51be035769ea76a725f08e69274b86`.
- ampliacion/expediente/AGENTE_MOMENTOS_CIRCULARES.md — SHA-256 `779593e125f50a267b215aa7048a644b67694c15f18b64ace75082b9ecd0c48a`.

## Correspondencia por secciones

| Fuente | Sección | Líneas | Destino |
|---|---:|---:|---|
| Costura | 1 | 5–20 | \ref{tm-add-c1} |
| Costura | 2 | 21–70 | \ref{tm-add-c2} |
| Costura | 3 | 71–103 | \ref{tm-add-c3} |
| Costura | 4 | 104–111 | \ref{tm-add-c4} |
| Costura | 4.1 | 112–163 | \ref{tm-add-c4-1} |
| Costura | 5 | 164–190 | \ref{tm-add-c5} |
| Costura | 6 | 191–211 | \ref{tm-add-c6} |
| Costura | 7 | 212–221 | Comentario técnico de procedencia; contenido matemático sustantivo conservado en cuerpo. |
| Momentos | 1 | 9–53 | \ref{tm-add-m1} |
| Momentos | 2 | 54–83 | \ref{tm-add-m2} |
| Momentos | 2.1 | 84–120 | \ref{tm-add-m2-1} |
| Momentos | 2.2 | 121–159 | \ref{tm-add-m2-2} |
| Momentos | 3 | 160–184 | \ref{tm-add-m3} |
| Momentos | 3.1 | 185–219 | \ref{tm-add-m3-1} |
| Momentos | 3.2 | 220–236 | \ref{tm-add-m3-2} |
| Momentos | 4 | 237–295 | \ref{tm-add-m4} |
| Momentos | 5 | 296–352 | \ref{tm-add-m5} |
| Momentos | 6 | 353–383 | \ref{tm-add-m6} |
| Momentos | 6.1 | 384–406 | \ref{tm-add-m6-1} |
| Momentos | 6.2 | 407–424 | \ref{tm-add-m6-2} |
| Momentos | 6.3 | 425–477 | \ref{tm-add-m6-3} |
| Momentos | 7 | 478–521 | \ref{tm-add-m7} |
| Momentos | 8 | 522–544 | \ref{tm-add-m8} |

## Control de no ablación

- Todas las definiciones, fórmulas, condiciones, pruebas y ejemplos de ambos originales se conservan en el cuerpo. Las reiteraciones matemáticas se mantienen; no se han fusionado resultados por simple semejanza.
- 54 bloques de ecuaciones preservados, con igualdad de secuencia y tokens matemáticos salvo espacios y reemplazo de los cinco rótulos locales `tag` por etiquetas prefijadas. Todas las referencias a esas ecuaciones se convierten a `eqref`.
- 34 etiquetas únicas: prefijo `tm-add-` y tres anclajes de integración pedidos por el editor (`sec:transporte-momentos`, `tm-add:invariancia-weil`, `tm-add:familias-transportadas`); 16 referencias internas resueltas en la propia sección.
- Las tres proposiciones y sus pruebas de Costura se convierten a entornos `proposition` y `proof`, sin retirar pasos.
- Los listados administrativos de propietarios, rutas y estados históricos pasan íntegros a comentarios LaTeX: Costura §7, Momentos §1 y el registro de ejecución de §8. No sustituyen pruebas en el texto visible.
- El balance público de los 1.046 controles mantiene dimensiones, parámetros, truncamientos, ejecución normal/optimizada y límites de la comprobación. Los nombres de archivos y comandos quedan completos en comentarios y en los originales del expediente.
- Las cabeceras fechadas y denominaciones de nota de agente se conservan como procedencia en comentarios; el título público es científico. La apertura y los enlaces entre subsecciones son adiciones narrativas sin promoción del alcance.
- El lector auxiliar conserva `a>b>1/2`; el caso `a=1/2` mantiene su advertencia de convergencia polar. Se conserva la condición de fases levantadas en el refinamiento y la diferencia entre convergencia débil de estados y fuerte de vectores.
- La cota local se recibe explícitamente del complemento de Schur. Se conserva el requisito de momentos mixtos para sumar subespacios transportados; no se extrapola la positividad local a todo el dominio.

## Destino

`ampliacion/transporte_y_momentos.tex` — SHA-256 `e886fd56cbd560b88e8968a1f6d416619024ac06a4dd23a6d3e69c93c83ebfc0`.

## Comprobaciones pendientes de composición

La compilación, la paginación y la revisión visual corresponden al editor principal. No se ha modificado el núcleo común, ningún otro artículo, índice ni PDF.
