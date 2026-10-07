# Localidad del mapa estado–campo sobre el retículo seleccionado

Esta entrega conserva íntegro el paquete anterior y añade la prueba de
localidad para **todo par de estados** del mismo portador reticular. No
redefine la selección de K, su origen marcado, el retículo, el cociclo,
los campos cargados, los modos de Heisenberg ni el mapa estado–campo Y.

## Resultado y orden de reproducción

La secuencia conserva los antecedentes APP–TRIT–TPK y su publicación
excepcional ya seleccionada. A partir de esos mismos objetos se compone:

1. Las tres localidades generadoras ya probadas: cargada–cargada,
   Heisenberg–cargada y Heisenberg–Heisenberg.
2. El producto residual en las dos regiones de expansión. Se demuestran
   finitud puntual, cota Laurent y su igualdad exacta con `normalField`.
3. La convolución ordenada con cotas unilaterales. La cota doble del
   producto común se obtiene de la localidad, no se impone de antemano.
4. Las dos anulaciones del integrando de tres campos y el paso binomial.
   El residuo es exactamente el conmutador del campo construido.
5. `LatticeDongLocality.normalField_localAt`: orden suficiente p+q+s+n,
   deducido de las tres localidades originales; no se supone la localidad
   del nuevo producto normal.
6. `LatticeDescendantLocality.stateField_local`: localidad mutua para todo
   par de estados, por inducción sobre las palabras de osciladores y
   extensión lineal sobre la base del portador completo.
7. `SelectedDescendantLocality.selected_fields_local`: aplicación al mismo
   origen seleccionado por la incidencia regional de K y alfa.

No hay truncación uniforme de frecuencias, longitud de palabras o energía.
Cada intercambio de sumas se justifica sobre el vector concreto mediante
soporte finito. El código no introduce `sorry`, axiomas de localidad,
hipótesis de Jacobi ni una evaluación nativa nueva. Las dos declaraciones
del adaptador seleccionado heredan `Lean.ofReduceBool` del selector previo;
los resultados generales usan sólo los axiomas ordinarios enumerados en
el recibo.

## Contenido

- `antecedente/`: paquete completo de coherencia, inalterado, con sus
  propios antecedentes y selección terminal conservados.
- `lean/`: fuentes de este delta y los dos módulos generadores previos.
- `lean/dong/`: núcleos, binomio y localidad triple, con sus recibos.
- `recibos/localidad_generadores/`: corte previo de dos módulos.
- `recibos/localidad_estados/`: compilación y consultas públicas de este
  cierre de localidad.
- `integracion_II_III/`: las 25 incorporaciones ya compiladas sobre la
  misma base279, sus fuentes, objetos y controles originales. Su inclusión
  no repite su compilación ni modifica los manuscritos II o III.
- `historia/`: continuidad, prueba explicada y procedencia.
- `MANIFIESTO.json`: inventario de archivos y huellas.

La cantidad de archivos no define el alcance matemático. Los resultados
comprobados son los teoremas anteriores y sus dependencias registradas.
La construcción de los sectores torcidos, el producto orbifold y la
identificación FLM/Monstruo son etapas posteriores distintas de este
teorema de localidad. El desarrollo LaTeX de esas etapas se conserva;
este paquete no lo elimina ni lo sustituye por una afirmación sobre el
estado del código.

## Ejecutar

Se requiere Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`. Los objetos heredados se
autentican; no se reconstruyen la base ni Mathlib. Si se cambia la versión
del compilador debe reconstruirse primero la base mediante sus fuentes.

Desde la carpeta desplegada:

```sh
python3 -I -S reproducir.py --plan --report-dir /ruta/nueva/plan
python3 -I -S reproducir.py --lean /ruta/lean --mathlib /ruta/mathlib4 --report-dir /ruta/nueva/resultado
```

El directorio de resultado debe ser nuevo. La primera orden inspecciona
fuentes y huellas; **no compila**. La segunda consulta el núcleo Lean y
genera su propio recibo. No se usa un PASS de conservación documental
como sustituto de la comprobación de un teorema. La portada de los PDF y
los archivos entregados anteriormente no se modifican con esta entrega.

## Procedencia y continuidad

El selector terminal previo mantiene su dominio y su censo
19.446 → 79 → 1. La reconstrucción reversible no reemplaza esa selección.
El censo Bterm del integral, 7.567.952 → 331 → 2 → 1, tiene otro dominio;
no se identifica con el anterior. La matemática de campos aquí utilizada
es lenguaje de construcción y prueba posterior sobre el mismo retículo,
no una entrada que vuelva a seleccionar K o las constantes.

La nota `historia/PRUEBA_DONG_NORMALFIELD.md` conserva la deducción y su
progresión de formalización. El recibo final y las fuentes prevalecen
para saber qué declaraciones de esa progresión ya han compilado.
