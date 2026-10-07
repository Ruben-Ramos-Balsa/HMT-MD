# Aritmética de historias: dependencia reunida para VI

Fecha: 2026-09-10. Estatuto: **RESULTADO_RECUPERADO / FORMALIZACION_REUNIDA**.

Se ha leído íntegramente (241líneas) el propietario

`/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910/sections/aritmetica_historias.tex`.

La nueva `sections/15_aritmetica_historias.tex` reúne en exposición propia el contenido anterior a «Retorno de fase, representación de Weyl y dos lecturas». La fuente I no se ha editado; tampoco `main.tex`,09 ni el núcleo común deVI.

## Correspondencia material

| VI | Fuente I | Contenido conservado |
|---|---|---|
| `hist:seccion` | líneas10–58 | Estados admisibles, restricciones de profundidad, sección compatible, lector y valor arquimediano. |
| `vi:hist:algebra` | líneas60–110 | Categoría de historias, fibras algebraicas, acción estricta, multiplicador central normalizado, cociclo y producto de soporte finito. |
| `vi:hist:asociatividad` | líneas112–151 | Prueba completa de asociatividad, unidad y ejemplo de acarreo nonádico con variable formal de memoria. |
| `hist:doble-varianza` | líneas153–198 | Precomposición, límite directo de observables, indicadores de fibras, unidad y evaluación de una sección. |

Se conservan exactamente las etiquetas canónicas `hist:seccion` y `hist:doble-varianza` que reclama el núcleo común. Las etiquetas auxiliares de la nueva sección llevan prefijo `vi:hist:`. La referencia a los cilindros apunta a `vi:dep:prefijos`, existente en09; no se mantiene la remisión deI a `sec:generacion`.

## Precisiones incorporadas

1. Se desarrolla la prueba de intersección de intervalos encajados mediante supremo e ínfimo. Determina el valor de una sección cuyo lector cumple las condiciones; no demuestra por definición de límite inverso ni existencia de todas las historias ni cobertura de toda la recta.
2. Se conservan como estructura explícita la acción estricta, la centralidad y la identidad del cociclo. No se declara que todo transporte TPK, incluidos los de bimódulos, se reduzca a esa presentación.
3. Se añade la formulación de identidades locales cuando hay infinitos objetos. Su prueba usa únicamente los extremos de una familia finita de flechas; no cambia el producto de soporte finito.
4. Se explicita `T^9=z` y, después de imponer `z^12=1`, la recuperación de las108posiciones. Esta construcción representa la memoria de calendario, no toda la memoria del estado.
5. El pullback del indicador se expresa como indicador de la fibra sin restricciones de cardinal. La suma de indicadores puntuales se afirma como suma algebraica finita sólo para fibras finitas. La preservación de la función unidad es incondicional.
6. La evaluación sobre el límite directo tiene su prueba por paso a una profundidad común. No se identifica ese álgebra con toda el álgebra de rutas, ni la conservación de la unidad con una medida probabilística sin normalización adicional.

## Corte temático

No se trasladan las líneas200–241 deI: representación de Weyl, operador de memoria y prolongación excepcional. Son dependencias de otra aplicación, no necesarias para las dos remisiones que se cierran enVI. La omisión es temática y conserva íntegras las pruebas de la aritmética de historias aquí utilizada.

Las fuentes históricas de la monografía de775páginas permanecen indicadas en la cabecera del propietarioI. No se afirma haber releído esas fuentes más extensas en esta incorporación focal ni se las usa para sustituir las pruebas contiguas de15.

## Comprobación

Control estático realizado:293líneas,17etiquetas únicas,9remisiones resueltas; la única remisión a otra sección es `vi:dep:prefijos`. Las dos etiquetas canónicas aparecen una sola vez en las fuentes deVI. Los entornos están correctamente anidados.

Se verificaron además por enteros los729triples del cociclo de acarreo y los11664productos del calendarioC108 en la representación fase/memoria. Estas comprobaciones protegen la transcripción; las demostraciones generales permanecen en15.

La sección está preparada para integración por el coordinador. No se ha compilado un PDF ni actualizado gates o manifiestos. Este archivo documenta procedencia y alcance, no certifica por sí solo la autonomía global del ArtículoVI.

Los controles quedaron materializados en `technical/verificar_controles_historias_15.py` y en los recibos normal y optimizado `RECIBO_CONTROLES_HISTORIAS_15.json` / `RECIBO_CONTROLES_HISTORIAS_15_OPTIMIZADO.json`. Se ejecutaron satisfactoriamente sin depender de instrucciones `assert`; el alcance y los comandos están en `technical/README_CONTROLES_09_15.md`.
