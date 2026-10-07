# Registros generados, refinamiento conjunto y localidad de campos

Este paquete conserva la cadena formal anterior y reúne nuevas conexiones
comprobadas. La secuencia de referencia es APP → TRIT → TPK → estado
enriquecido → estructura discreta conjunta del continuo. La generación
regional, sus publicaciones y la incidencia se mantienen en su orden causal;
los registros publicados no se introducen como entradas del productor.

## Lo que se incorpora

1. **Registros y elevaciones.** `GeneratedTransitionRecords` construye sus
   filas directamente desde los bloques producidos a cualquier profundidad.
   Prueba su coincidencia con los registros conservados y la existencia y
   unicidad de las dos elevaciones ternarias. Los 600 trits anteriores sirven
   como comprobación de igualdad, no como límite de generación ni como
   argumento del nuevo constructor.
2. **Cilindros, firma y acarreo.** `RegionalCylinderTransition` demuestra
   existencia y unicidad del hijo mediante desigualdades racionales, la
   compatibilidad de las publicaciones ternaria y decimal, la recuperación
   de ambos prefijos y la actualización entera exacta del defecto cilíndrico.
   `JointRegionalFrontier` y `JointCylinderSignature` prueban que esos mismos
   hijos producen la firma conjunta, conservan el acarreo y publican la carga
   dual de Witt. No hay una segunda selección ni una tabla objetivo interpuesta.
3. **Rutas APP.** `APPRouteWinding` recupera el desplazamiento entero y el
   enrollamiento; demuestra composición, inversión y el cociclo de borde.
   Distingue la posición residual de la información de transporte conservada.
4. **Campos del retículo seleccionado.** Se demuestra el conmutador mixto
   para todos los índices enteros y, a partir de él, la localidad mixta.
   `SelectedMixedFieldLocality` la integra con la incidencia concreta, la
   generación de campos, los productos sobre el vacío y la localidad cargada
   ya comprobados sobre el mismo `selectedOrigin`.

Las identidades con `X0,Y0,X1,Y1,L0,L1` son conclusiones demostradas. No se
asume que Paley y Hadamard, aislados de los registros y sus reglas, determinen
esas elevaciones. La generación no recibe valores convencionales de
constantes, cifras objetivo ni valores metrológicos.

## Reproducción desde las fuentes

Se requiere Python 3, Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`, con sus dependencias compiladas.
Desde esta carpeta:

```sh
python3 -I -S reproducir_integracion.py --plan
python3 -I -S reproducir_integracion.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean
```

El primer comando comprueba el inventario, las huellas y los imports. El
segundo verifica los datos de incidencia y compila la clausura completa en
orden de dependencias, escribiendo el recibo en
`resultados/lean_unificado/VERIFICATION.json`. No basta ejecutar sólo el plan.
Si hay una caché local, se reutiliza únicamente cuando concuerdan fuente,
compilador, dependencias y huella del objeto. Una recepción nueva compila las
fuentes: el ZIP no distribuye la caché actual de `.olean` como sustituto.
Se conservan tres objetos históricos `FoundationContract` como antecedentes,
sin incorporarlos a la ruta de imports de la reproducción actual.

El recibo enumera los axiomas utilizados. No se añaden `axiom`, `sorry` ni
`admit`. Se mantiene explícita la dependencia heredada de `Lean.ofReduceBool`
en el selector finito y en las conclusiones que lo importan; no se presenta
ese tramo como reducción exclusiva por el núcleo.

## Alcance preciso de la integración

El estado enriquecido sigue siendo el objeto de la cadena HMT, no se sustituye
por un registro escalar. Aquí se reúnen pruebas de componentes efectivas:
ruta, prefijos compatibles, cilindros, firma, acarreo e incidencia. La
compatibilidad de estas lecturas está demostrada por los módulos indicados.
Esto no prueba todavía que todas las fibras del operador enriquecido
`Upd∘Tra∘Sel` coincidan con esta realización tras nueve actualizaciones
elementales; esa identificación no se añade como axioma ni como definición.

La localidad de campos queda demostrada en su dominio. Este paquete no
certifica aún la construcción completa FLM, el módulo torcido, el orbifold
ni la identificación final con Moonshine. No modifica el texto de los PDF
ni cambia el alcance de sus afirmaciones: documenta exactamente la extensión
Lean ejecutada y conserva sus antecedentes.

## Continuidad y organización

`deltas/integracion/` contiene las nuevas fuentes; `recibos/integracion/`
contiene los recibos focales y el de la compilación conjunta. Todas las
fuentes y pruebas anteriores permanecen con sus huellas. El README anterior
se conserva íntegro en `versiones_previas/README_LOCALIDAD_SELLADO.md`.
El manifiesto y los controles editoriales prueban conservación y orden;
las pruebas matemáticas corresponden a los enunciados efectivamente compilados.
Estatuto de estas incorporaciones: **formalización reunida y certificados
nuevos de construcciones autorales preexistentes**.
