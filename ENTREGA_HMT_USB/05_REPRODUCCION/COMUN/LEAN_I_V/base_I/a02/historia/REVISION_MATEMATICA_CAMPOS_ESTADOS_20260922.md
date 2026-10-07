# Revisión focal de los campos torcidos y de su asignación de estados

Fecha: 22 de septiembre de 2026. Estatuto: revisión matemática por lectura de fuentes. No se ha ejecutado Lean, no se ha repetido una compilación y no se ha modificado ninguna fuente matemática durante esta revisión. Los recibos ejecutables correspondientes constituyen evidencia distinta de este informe.

La revisión sigue la realización posterior sobre el mismo retículo, cociclo y portadores heredados. No redefine su procedencia HMT, no vuelve a seleccionar el registro K ni reabre los certificados antecedentes.

## Fuentes examinadas

En este mismo directorio se leyeron íntegramente:

- `LatticeTwistedNormalProduct.lean` y `LatticeTwistedNormalDerivative.lean`.
- `LatticeTwistedNormalTerms.lean`, `LatticeTwistedNormalBounds.lean` y `LatticeTwistedNormalCommutation.lean`.
- `LatticeTwistedRawStateField.lean` y `LatticeTwistedWordCoherence.lean`.
- `LatticeTwistedCorrection.lean`, `LatticeTwistedCorrectionConformal.lean` y `TwistedCorrectionScalarKernel.lean`.
- `LatticeTwistedCorrectedStateField.lean` y `LatticeTwistedNormalConformalBridge.lean`.
- Para el enlace final: `LatticeTwistedRawConformal.lean` y `LatticeTwistedStateConformal.lean`.

## Comprobaciones focales

1. **Derivación en la variable correcta.** En `LatticeTwistedNormalDerivative`, `dividedFactor(e,n)` es el producto descendente de `e/2` dividido por `n!`. La fórmula de `derivativeCoefficient` desplaza el exponente en `2n`, y `derivativeCoefficient_succ` utiliza el factor `k/2+1`. Son las fórmulas de la derivada dividida respecto de `z`, con `z=t²`, no respecto de `t`: `(1/n!) ∂z^n(t^e) = binom(e/2,n) t^(e−2n)`.

2. **Separación de modos creadores y aniquiladores.** En `LatticeTwistedNormalProduct` y `LatticeTwistedNormalTerms`, el modo `−a−1` aporta el exponente `2a−1` y el modo `a` el exponente `−2a−3`. Por ello, los índices del campo restante son respectivamente `k−2a+1` y `k+2a+3`; las derivadas añaden `2n`. La separación se conserva por el signo del modo oscilatorio original, sin reclasificarlo por el signo del exponente después de derivar.

3. **Productos normales iterados y sumas dobles.** `cc`, `ca`, `ac` y `aa` son las cuatro contribuciones de la expansión efectiva. `cc_rectangle`, `ca_rectangle`, `ac_rectangle` y `aa_rectangle` proporcionan un rectángulo finito para cada coeficiente y cada vector de entrada, antes de usar `finsum_comm_of_rectangle`. Las conmutaciones de dos creadores y de dos aniquiladores proceden de las relaciones de Heisenberg de igual signo. Los términos `ca` y `ac` se intercambian como acciones a izquierda y derecha del campo intermedio: no se omite un conmutador mixto entre dos modos contiguos. No se afirma una cota uniforme independiente del vector.

4. **Independencia de la palabra y recursión en el portador completo.** `rawDescendantField_perm` deduce la invariancia por permutaciones de la conmutación demostrada del producto normal. `rawStateField_stateForWord` identifica la elección de representante de ocupación con cualquier palabra que representa ese estado. `rawStateField_create_intertwines` y `rawStateField_create` extienden la recursión a cada estado del portador reticular por la base existente. La recursión no aparece como hipótesis de estos resultados.

5. **Corrección conforme e índices de la variable ramificada.** `correctionScalar_one_one` evalúa el coeficiente `1/16`; `gram_trace_vacuum` contrae la matriz de Gram inversa con la matriz de Gram y obtiene el rango. `correctionExponential_conformalState` demuestra que sobre el estado conforme sólo sobreviven los grados de corrección `0` y `2`: el segundo aporta `(rank/16)` veces el vacío. En `LatticeTwistedCorrectedStateField`, el término de grado `d` se lee en `k+2d`, de modo que `d=2` produce `t⁻⁴=z⁻²`. El puente normal conforme evalúa el modo de índice `m` en el exponente `−2m−4`, de forma compatible con esa corrección.

6. **Núcleo escalar y alcance de los parámetros.** `TwistedCorrectionScalarKernel` demuestra la ecuación de Euler del núcleo, la identidad logarítmica para el promedio de las dos raíces normalizadas y su unicidad con término constante cero en cada bidegrado; no utiliza una tabla finita de coeficientes como sustituto de esa identidad. Los resultados genéricos que reciben un campo `B` o una asignación lineal `W` mantienen explícito ese alcance. No reciben como hipótesis la conmutación normal que concluyen, una identidad de Jacobi ni el producto completo del orbifold.

## Enlace final comprobado por lectura

`LatticeTwistedStateConformal.lean` reúne realmente la corrección de `ω` con los modos conformes ya construidos, mediante dos pasos separados:

- `twistedStateField_conformalState_correction` reduce la suma de correcciones a su soporte `{0,2}` y demuestra, para cada exponente `k`, que el campo corregido de `ω` es el campo sin corregir más `δ(k,−4) (rank/16) Id`.
- `twistedStateField_conformalState_coefficient` compone esa igualdad con `rawStateField_conformalState_coefficient`, que identifica el campo sin corregir con el modo cuadrático transportado. Al evaluar en `k=−2m−4`, la corrección sólo interviene si `m=0`, y el resultado es exactamente `conformalMode o m`.

El desplazamiento conforme no se introduce como valor objetivo en este enlace: se obtiene de la evaluación previa de la corrección y coincide con el desplazamiento de los modos semienteros heredados. La igualdad final no se usa como premisa de la prueba.

## Conclusión y límite de esta revisión

En los pasajes examinados no se ha localizado un error concreto de signo, índice, intercambio de sumas o circularidad entre hipótesis y conclusión. La lectura comprueba las composiciones descritas y sus dominios; no constituye una nueva ejecución del compilador ni un certificado independiente de la totalidad de las dependencias.

Este informe no atribuye a estos módulos una construcción íntegra del producto mixto del orbifold, la identidad de Jacobi torcida completa o la identificación del grupo de automorfismos con Monster. Tampoco disminuye el alcance positivo de las identidades de campos y modos que las fuentes sí demuestran.
