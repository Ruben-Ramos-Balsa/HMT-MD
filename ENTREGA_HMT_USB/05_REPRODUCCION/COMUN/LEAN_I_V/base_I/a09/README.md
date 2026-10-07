# Coherencia de los campos sobre el retículo seleccionado

Esta entrega continúa la construcción estado–campo del Artículo I sobre
el mismo retículo marcado. Su resultado nuevo central es la independencia
del campo respecto al orden de una palabra de osciladores con las mismas
multiplicidades. La conmutación necesaria se demuestra sobre los campos
reales de Laurent; no se recibe como una condición sin comprobar.

## Continuidad de la construcción

Se conserva la cadena APP–TRIT–TPK, estado enriquecido, selección regional
conjunta, incidencia Witt–Golay, vecino reticular marcado y portador
`LatticeCarrier selectedOrigin`. No se modifica la selección de K, no se
cambia la orientación del origen, no se introduce un nuevo retículo y no
se sustituye el producto torcido ni la representación de Heisenberg.

La entrega anterior ya había construido el mapa lineal `stateField` en
todos los estados del portador y demostrado creación, vacío, inyectividad,
truncación puntual y coincidencia con los campos cargados y de Heisenberg
existentes. Aquella edición conservaba una cuestión precisa: demostrar
que cualquier orden de una misma ocupación da el mismo campo. Esta entrega
resuelve ese punto mediante operaciones sobre los coeficientes completos.

## Lo que se demuestra aquí

Para un coeficiente de Laurent `k` y un estado `v`, se desarrollan las
cuatro contribuciones de dos productos normales sucesivos: creación–
creación, creación–modo no negativo, modo no negativo–creación y dos
modos no negativos.

1. Se prueban cotas rectangulares para sus soportes en los dos índices.
   Esas cotas proceden de la truncación Laurent y de la acción de los
   modos sobre el vector, incluidos los modos cero. No se postula un
   corte global de frecuencias ni de estados.
2. Se distribuyen las aplicaciones lineales y se intercambian las dos
   sumas después de justificar su finitud puntual.
3. Los términos mixtos se emparejan; los otros utilizan las relaciones
   ya demostradas entre modos del mismo signo. Así se obtiene
   `normalField_commute` sin una premisa de conmutación adicional.
4. La igualdad de ocupaciones se identifica exactamente con `List.Perm`.
   Se concluyen `descendantField_perm`,
   `descendantField_eq_of_occupation` y `stateField_descendant` para
toda palabra finita, con cualquier frecuencia y longitud.

La linealidad compleja de la operación de producto normal se demuestra en
`LatticeNormalProductLinear.lean`; no se supone para extender la prueba.
`LatticeStateFieldCoherence.lean` obtiene después, para todo estado `u`,

```text
stateField (create(n,i) u) = normalField(i,n) (stateField u).
```

La identidad también se enuncia como igualdad de aplicaciones lineales.
Finalmente, `stateField_unique` demuestra que la coincidencia con los
campos cargados y esta recursión determinan el mapa estado–campo en todo
el portador. Su unicidad no se deduce sólo de la identidad de creación
en el vacío: se utiliza la recursión efectiva sobre la base de osciladores.

En particular, la última igualdad enlaza la asignación lineal sobre la
base con el producto normal de cualquier representante del mismo estado;
ya no depende del orden elegido por `Multiset.toList`.

Los lemas auxiliares condicionados de `LatticeWordPermutation.lean`
permanecen identificados como tales. El módulo
`LatticeNormalProductCommutation.lean` aporta la premisa mediante su
prueba efectiva y publica las conclusiones sin esa hipótesis.

## Material conservado y estatuto de los antecedentes

`antecedente/` reproduce íntegramente la entrega estado–campo anterior,
incluidas sus fuentes, recibos y objetos compilados. Su propio
`antecedente/` conserva la clausura original de 279 módulos. No se
reescribe ninguna declaración histórica de alcance: el resultado nuevo
se publica en esta ampliación.

`procedencia/narrativas_k/` reúne las dos narrativas de K indicadas por el
editor. `procedencia/auxiliar_normal/` conserva el auxiliar algebraico
`NormalProductAlgebra` y su documentación. Esos documentos no son imports
del desarrollo Lean principal ni sustituyen sus pruebas. En particular,
la indicación de «aplicación pendiente» del README original del auxiliar
describe su entrega histórica; los pasos sobre las sumas de Laurent se
prueban ahora en los módulos de esta ampliación.

Las fuentes `lean/` incluyen los siete módulos de estado–campo anteriores,
sin cambios, y las nuevas dependencias probatorias. Su orden exacto y el
inventario completo de declaraciones quedan en el manifiesto y en el
recibo focal; no se infiere cobertura a partir del número de archivos.

## Cadena escrita hasta Moonshine y alcance de esta comprobación

El LaTeX del Artículo I continúa desde el retículo par, autodual, positivo
y sin raíces de rango 24 hacia `V_Λ`, la involución, el sector torcido y el
producto orbifold. Aplica después el teorema de Frenkel–Lepowsky–Meurman
como reconocimiento clásico posterior de `V^natural`, del grupo Monstruo
y del carácter `J`. La existencia de esa cadena escrita no se niega ni se
reemplaza por un problema de selección de K.

La comprobación Lean de esta entrega acredita los enunciados concretos
del mapa estado–campo y su coherencia de presentación. No equivale por sí
sola a la localidad mutua o Jacobi para todos los descendientes, a la
estructura conforme completa, al sector torcido, al producto orbifold o
a la identificación formal del grupo de automorfismos con el Monstruo.
Esos resultados no se introducen aquí como axiomas para aparentar un cierre.

## Reproducción

Desde la carpeta desplegada:

```text
python3 -I -S reproducir.py --plan
python3 -I -S reproducir.py --lean /ruta/a/lean --mathlib /ruta/a/mathlib4
```

El envoltorio fija de manera predeterminada:

- `--base antecedente/antecedente`, para la base autenticada de 279 módulos;
- `--source-root lean`, para esta clausura adicional completa;
- `--report-dir resultados`, sin sobrescribir los recibos entregados.

`recibos/coherencia/VERIFICATION.json` conserva la ejecución focal que
identifica las fuentes, los comandos, las declaraciones y los axiomas.
`MANIFIESTO.json` registra todos los archivos y
`VERIFICACION_CONSERVACION.json` su conservación íntegra. Los controles
de bytes y los controles de pruebas tienen funciones distintas.

Se utiliza Lean 4.21.0 y Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3`. Los objetos heredados corresponden
al compilador arm64 de macOS identificado en el recibo. Una plataforma
diferente exige recompilar y autenticar las dependencias correspondientes;
el verificador no acepta binarios incompatibles como si estuvieran probados.

Los módulos generales sólo admiten los axiomas ordinarios `propext`,
`Classical.choice` y `Quot.sound`. La especialización del origen conserva
`Lean.ofReduceBool` donde lo hereda del selector finito anterior. No se
añade otra evaluación nativa ni se vuelve a ejecutar el censo de K.
