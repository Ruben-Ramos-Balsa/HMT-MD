# Consumidor seleccionado de V

Estado: `PASS_SELECTED_V_THERMAL_PUBLICATION`. Lean 4.21.0, `-DwarningAsError=true`, salida 0. No se modificaron manuscritos ni fuentes selladas, no se reconstruyó Mathlib.

La continuidad APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo se hereda de la publicación seleccionada de I. La acción reducida retornada es `SelectedAction.action_domain.hbarRet`; la velocidad es `SelectedConstitutivePublication.speed` en una carta dimensional positiva. Son salidas internas utilizadas después, no valores objetivo ni generadores externos.

La fuente reúne los teoremas ya existentes en especializaciones concretas:

- Dos polarizaciones `EuclideanSpace.single` ortonormales: operadores de número exteriores y simétricos sobre sus configuraciones genuinas; potencial químico nulo y energía positiva `hbar*c*r` en la ocupación bosónica.
- Límite periódico para número, energía y logaritmo de partición, con `a=beta*hbar*c`, `b=hbar*c`, dos polarizaciones y exclusión del modo cero antes de sumar; se conservan convergencia, sumabilidad e integrabilidad.
- Densidad de Planck y flujo de Stefan con las mismas acción y velocidad.

No se añade una teoría de radiación interactuante, una completación de Fock ni una traza de operador de Gibbs. Se mantienen explícitos las unidades positivas, beta, la realización libre homogénea tridimensional y el par térmico positivo del lector de Stefan. Se utiliza la sección retornada de acción; no se declara probada aquí toda V.

Los diez terminales auditados sólo usan `propext`, `Classical.choice`, `Quot.sound` y la dependencia `Lean.ofReduceBool` heredada de la selección regional. No se añaden axiomas ni `sorry`.

`SymmetricModes.lean` es copia exacta del antecedente (`e984a8466c33cd77ef593d0eba010d57c28b24443ad49e3a52e2e2a4c1489cc4`), compilada únicamente porque su objeto persistente no estaba conservado. No se alteró su demostración.

Archivos: `SelectedThermalPublication.lean`, `SelectedThermalPublication.log`, `VERIFICATION_COMPACT.json`; `VERIFICATION.json` conserva huellas de las dependencias. `verify.py` recompila sólo el consumidor y, si no existe, el objeto de la copia idéntica `SymmetricModes`.

La puerta causal de constantes del consumidor devuelve `PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY` con `CAUSAL.json`. La skill de continuidad restringió este delta a composición y especialización de resultados recuperados, conservando los dominios del manuscrito.

## Reproducción rápida

Desde la raíz del proyecto:

```bash
python3 -I -S output/CIERRE_ACUMULATIVO_II_V_20260922/V/verify.py
```

También admite `python3 -O -I -S`: las comprobaciones de hashes, revisión y ausencia de axiomas añadidos o `sorry` usan controles explícitos que no se eliminan con optimización. El verificador reutiliza los objetos presentes; sólo recompila el consumidor y, si falta su objeto, la copia exacta de `SymmetricModes`. La conexión adicional del transductor térmico generado en II pertenece al consumidor conjunto posterior, no al alcance de esta especialización de V.
