# Mapa estado–campo local y covariante del retículo seleccionado

La construcción reticular conserva el origen HMT seleccionado, K, el
retículo, el cociclo, los osciladores, el vacío y el mismo mapa Y. Esta
incorporación demuestra sus identidades de traslación sobre **todos** los
estados, sin limitarse al vacío ni a una familia de frecuencias.

El punto de partida APP–TRIT–TPK, el estado enriquecido y su publicación
excepcional están en el antecedente íntegro. No se usa FLM para seleccionar
retroactivamente el registro, ni se suministra una matriz de Gram nueva.

## Resultado reunido

`SelectedTranslationCoherence.selected_local_translation_publication`
reúne sobre el mismo portador:

- el operador T anula el vacío;
- cada campo Y(u) es regular sobre el vacío y su coeficiente constante es u;
- el campo del vacío es la identidad;
- los campos Y(u), Y(v) son locales para cualquier par de estados;
- `[T,Y(u)_k]=(k+1)Y(u)_(k+1)` para todo exponente entero k;
- `Y(Tu)=dY(u)/dz` para todo estado u.

La última igualdad se deduce de las propiedades anteriores mediante una
prueba de unicidad de campos locales, creativos y covariantes. No aparece
como condición en la definición del mapa Y.

## Cadena de pruebas

1. `LatticeHeisenbergTranslation`: conmutador con cada modo integral,
   incluido el paso del modo uno al modo de carga cero.
2. `LatticeTranslationChargedGround`: evaluación de la covarianza sobre
   toda carga pura; conserva cociclo, carga entrante y apareamiento.
3. `LatticeTranslationDefect` y `LatticeChargedTranslation`: propagación
   del defecto nulo por los creadores hasta todo el portador, usando la
   generación ya demostrada del espacio. La condición de suelo se descarga.
4. `LatticeNormalTranslation`: conmutadores efectivos de ambos sumandos,
   identidad binomial y telescopado puntualmente finito. Así el producto
   normal conserva la covarianza para todo orden de derivada.
5. `LatticeTranslationLinear`: cierre lineal y extensión por la misma base.
6. `LatticeLocalFieldUniqueness`: la localidad con los campos generados y
   la anulación completa sobre el vacío fuerzan que el campo sea cero.
7. `LatticeCovariantFieldUniqueness`: la covarianza propaga el coeficiente
   cero y permite identificar campos creativos para el mismo estado.
8. `LatticeFieldDerivative` y `LatticeDerivativeLocality`: derivada como
   campo Laurent genuino; localidad heredada con orden suficiente N+1.
9. `LatticeStateFieldTranslation`: extensión a todas las palabras y todos
   los estados, y deducción de la igualdad entre traslación y derivación.
10. `SelectedTranslationCoherence`: especialización al origen ya seleccionado.

No hay una cota uniforme añadida sobre palabras, energía o frecuencias.
Cada intercambio o telescopado usa soporte finito en el vector pertinente.
No hay `sorry`, axiomas nuevos de covarianza, ni evaluaciones nativas nuevas.
La especialización seleccionada conserva la dependencia nativa heredada
de su selector; el recibo identifica exactamente sus declaraciones.

## Organización y reproducción

`antecedente/` conserva completo el paquete de localidad, incluidos sus
antecedentes y la integración II/III; `lean/` contiene esta continuación;
`recibos/traslacion/` contiene fuentes compiladas, objetos, logs y consulta
de todas las declaraciones públicas. `MANIFIESTO.json` registra las huellas.

Lean 4.21.0 y Mathlib commit
`308445d7985027f538e281e18df29ca16ede2ba3` son dependencias externas
versionadas. No se reconstruyen al ejecutar este delta. En una carpeta
nueva de resultados:

```sh
python3 -I -S reproducir.py --plan --report-dir /ruta/nueva/plan
python3 -I -S reproducir.py --lean /ruta/lean --mathlib /ruta/mathlib4 --report-dir /ruta/nueva/resultados
```

La primera orden autentica; la segunda compila y consulta el núcleo Lean.
Un control de archivos no sustituye al recibo de teoremas. Los nombres
internos de carpetas conservadas documentan procedencia y no cambian la
nomenclatura matemática ni la cadena causal del artículo.

## Relación con el manuscrito

La sección «El álgebra de operadores de vértice y el Monstruo» del LaTeX
construye el álgebra reticular sobre N_alpha, presenta la involución, el
sector torcido y el orbifold, y aplica el teorema FLM con las hipótesis
reticulares comprobadas. Esa composición escrita se conserva íntegra.
Aquí se añaden pruebas Lean de las identidades reticulares especificadas;
no se convierte la identificación escrita FLM/Monstruo en un axioma nuevo
ni se declara que este recibo compruebe también el producto orbifold.
