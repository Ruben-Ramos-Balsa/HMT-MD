# Continuación de la traza, 18 de septiembre

No reiniciar K ni el portador. La base sellada sigue intacta en
`../PAQUETE_ARTICULO_I_CONTINUACION_VOA_20260918`.

Resultado ya compilado de esta continuación:
`HMT.I.SelectedGradedTrace.shared_action_electron_fields_and_graded_trace`.
Fuente `SelectedGradedTrace.lean`, recibo `SELECTEDGRADEDTRACE_VERIFICATION.json`.

La prueba identifica la restricción real de `fockTheta` a cada peso con
su traza. Las piezas son finitas por una codificación explícita de todas
las ocupaciones, no por un corte supuesto. Para todo peso d la traza es
el coeficiente d del producto formal de los inversos `(1+X^n)^24`.
El producto tiene truncamientos compatibles y únicos a profundidad arbitraria.
El rango24 procede del mismo retículo seleccionado, no de un valor añadido.
La entrada conserva las hipótesis exactas de la composición acción/electrón
y los campos de Heisenberg comprobados anteriormente.

Dependencias nuevas, en orden:

1. `LatticeFockMonomialParity`: base real monomial y acción de negación.
2. `WeightedOscillatorTrace`: piezas finitas por peso y producto geométrico.
3. `OscillatorEulerProduct`: inversos y producto formal a toda profundidad.
4. `WeightedEulerBridge`: igualdad entre traza finita y coeficiente formal.
5. `LatticeWeightFiniteness`: finitud del peso y equivalencia con ocupaciones.
6. `FockFiniteParityPiece`: restricción al subespacio real, no modelo aislado.
7. `SelectedGradedTrace`: composición con el mismo fundamento y retículo.
8. `LatticeChargeParityTrace`: negación sobre las cargas reticulares reales;
   la única carga fija es cero y se calcula la traza de cada conjunto finito
   estable, con entrelazamiento y subespacio real.

También compilados: `LatticeWeightShells` (finitud de capas de norma
del retículo), `LatticeFullGradedTrace` (traza por peso total del portador y
cobertura de todo el portador por esas piezas), y `SelectedFullGradedTrace`
(entrada común que conserva acción, electrón, campos y traza).
Esta operación sigue el párrafo814–825 de `sections/excepcional.tex` del
sucesor `EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source`.

La identidad de esta traza no se usa como sustituto de la construcción del
módulo torcido, del producto de orbifold o del teorema FLM. Tampoco convierte
un coeficiente196884 en una prueba de identificación con el Monstruo.

La búsqueda reutilizable está en `BUSQUEDA_LOCAL_FLM_Y_SERIES.json`:26.471
rutas Lean y8.037 contenidos distintos; ese registro describe su ámbito
de búsqueda, no declara ausencia matemática del resultado del LaTeX.

Coordinación: el revisor mantiene II/III; esta tarea trabaja únicamente
la continuación excepcional de I. No se han alterado los PDFs.
