# Propuesta de incorporación del registro incidencial de 25 coordenadas

## Artefacto y alcance

`registro25.tex` es una propuesta separada de 381 líneas. No se ha modificado el
artículo III de 140 páginas, las copias del núcleo común de I, los archivos de II,
el manuscrito principal de la sucesora ni sus archivos de compilación. No se ha
compilado esta propuesta. Estatuto: **RESULTADO_RECUPERADO**, con reorganización
expositiva y renombrado de etiquetas; no se anuncia una nueva construcción primaria
de `E108`.

SHA-256 de la propuesta en este corte:
`18a1c2d8dc2a6d455aee7e2881c4ef0cc27cc0b2422f61d38d89acdd7dbfddab`.

## Fuentes consultadas y fijadas

Raíz de II revisión 05:

`/Users/ruben/Documents/New project/output/ARTICULO_II_AUTONOMIA_20260909_REVISION_05_TRABAJO/`

1. `manuscrito/sections/registro_incidencias.tex`, completo.
   SHA-256: `0ee9f04f60af3da36bb213fe90c36939e3771786622fcb023b15beb885bf496b`.
   Contiene visitas/trazas, recuentos, normalización, 25 coordenadas, prueba de los
   36 residuos, conjugación decimal, corrección de extremos y consecuencia de una
   reducción de período 54.
2. `manuscrito/sections/registro_imagen_integral.tex`, completo.
   SHA-256: `8405c2303b2f2f3bd80a47aa934e37073bbf4a91347f5f9df3647d37be3d7107`.
   Contiene caracterización de imagen, inversa, concordancia Hadamard, control
   negativo, órbitas, covariancia y composición de eventos.
3. `manuscrito/sections/registro_k.tex`, contexto de inserción y lectores.

Se contrastaron sólo en lectura las mismas fuentes en las revisiones
`ARTICULO_II_AUTONOMIA_20260909_REVISION_06_INTEGRACION` y
`ARTICULO_II_AUTONOMIA_20260909_REVISION_07_PULIDO`.
`registro_imagen_integral.tex` es idéntico por SHA-256 en las tres revisiones.
El archivo de incidencias de revisiones 06/07 tiene SHA-256
`b20bd06c5807a55d7f850c8ae863af89e9260b9adc885b9043434ecfc8e13bad`.
Su delta aclara los índices cíclicos, define `D3,D4,Q` y remite a la
reconstrucción posterior. La propuesta incluye esa aclaración; reemplaza las
remisiones futuras por demostraciones contiguas.

Antecedente técnico de la recuperación, consultado sin modificar:

`/Users/ruben/Documents/New project/output/REPARACION_DEPENDENCIAS_ARTICULO_I_20260909/registro_k/README.md`

Su constructor `constructor_incidencial.py` recibe visitas y trazas declaradas,
calcula los recuentos y conserva los cocientes. Sus pruebas sintéticas no se
presentan como ejecución de la familia canónica del registro terminal. El recibo
anterior mantiene `canonical_E108_produced: false`; la propuesta no modifica
ese alcance ni lo transforma en ausencia matemática global.

## Lugar exacto de inserción

En la copia de I de la sucesora:

`base_articulo_I/sections/registro_k.tex`

insertar mediante el mecanismo de integración del editor, **inmediatamente antes** de

```tex
\subsection{Dos lecturas del estado terminal}
\label{subsec:k-terminal}
```

Esto corresponde al entorno de la línea 173 en la copia actual. Conserva antes
de la propuesta el calendario, el registro orientado y la carta integral
`1+5+6`; después conserva íntegra la exposición original de las lecturas
terminales y sus 25 coordenadas. Es el lugar usado por el archivo de
incidencias en II revisión 07. La propuesta reúne allí también la prueba de
imagen que II dispone más adelante.

La incorporación debe ser aditiva. No borrar las coordenadas de referencia,
la lectura armónica o sus pruebas posteriores. La repetición de una identidad
señala dos funciones diferentes: construcción incidencial y comprobación del
testigo terminal.

## Contenido matemático recuperado

La secuencia de dominios se explicita:

1. Registro producido de visitas, multiplicidades y trazas orientadas.
2. Doce ternas enteras `(A_m,C_m,V_m)`.
3. División euclídea por 10, con residuos y cocientes conservados.
4. Doce bloques `z_m=100[A_m]_10+10[C_m]_10+[V_m]_10`.
5. Extractor `D(z)=(D3z,D4z,Q(z))`, de 25 coordenadas.
6. Imagen integral, inversa única y concordancia con `H12`/`Pi_H`.

La prueba de imagen impone 13 relaciones lineales y una congruencia módulo
12. La inversa usa `w_i=c_i-b_(i+1)`, sus sumas parciales y la carga; no
necesita `K` ni `alpha` objetivo. También se conserva el control negativo que
deja la lectura armónica inalterada pero viola la compatibilidad de canales.

La construcción desde los recuentos y la producción de los propios recuentos
son pasos distintos. La propuesta especifica lo que debe aportar el registro:
regla de selección de visitas, hojas y evaluación aritmética, clasificación de
frontera, multiplicidad, familia de trazas de longitud reducida
`120(1+3j)`, orientación y soporte finito (o definición alternativa de la suma).
No se rellenan estos datos con las 25 coordenadas observadas posteriormente.

La identidad de 36 residuos es válida en `Z^(12×3)`. No afirma independencia
de los 36 residuos en el subconjunto de historias admisibles de TPK.
La proposición de contribuciones aditivas es un criterio suficiente con reglas
de evento previamente fijadas; no impone linealidad a todo lector TPK.

## Diferencia con el apéndice B de III

`manuscrito/sections/11_nucleo_finito.tex` contiene dos dominios:

- Enumeración desde las condiciones iniciales de dos cursores, que produce
  firmas y emisiones mediante reglas declaradas.
- Reconstrucción `L_a=X_a^(-1)Y_a` sobre las cuatro matrices regionales de
  transiciones, seguida del control de los calendarios.

La evaluación incidencial propuesta utiliza otro registro: visitas y trazas
orientadas, con valores enteros y fronteras, hasta las 25 coordenadas. El
teorema de unicidad de `L0,L1` no demuestra por sí mismo esa evaluación, ni la
inversión de las 25 coordenadas demuestra la producción primaria de las
matrices regionales. El párrafo final de la propuesta remite al apéndice B y
conserva expresamente ambos dominios.

## Dependencias tipográficas y nombres

- 21 etiquetas nuevas, todas con prefijo `iii:r25:`; ninguna colisiona con
  etiquetas de `base_articulo_I`, `base_articulo_II` o `manuscrito` actuales.
- Una única referencia exterior: `iii:nucleo-finito`, ya presente en el
  apéndice B de III.
- No contiene `input`, rutas de figuras ni bibliografía nueva.
- Usa entornos `theorem`, `proposition`, `proof`, `align`, `equation`,
  `pmatrix`, `aligned`; todos existen en el preámbulo actual.
- Usa únicamente comandos matemáticos ordinarios y `mathbb`, `mathcal`,
  `mathbf`, `operatorname`, `eqref`, `ref`; no añade macros globales.
- Se usa `Z_0` caligráfico para el retículo de suma nula, en lugar del
  `L_0` de la fuente de II, para distinguirlo del levantamiento ternario.
- `A_m,C_m,V_m` se declaran como recuentos; no se identifican con el par
  angular, la constante de fase o el operador constitutivo.
- Los índices se anuncian primero como 1–12 y luego como 0–11 para la
  inversión; las operaciones son cíclicas en ambos casos.

Comprobación estática realizada: 381 líneas, 21 etiquetas únicas, cero
colisiones, referencia externa existente. Esta comprobación no es una
compilación ni una certificación matemática global. La evaluación científica,
la decisión del hook y la compilación/QA corresponden al editor de la sucesora.
