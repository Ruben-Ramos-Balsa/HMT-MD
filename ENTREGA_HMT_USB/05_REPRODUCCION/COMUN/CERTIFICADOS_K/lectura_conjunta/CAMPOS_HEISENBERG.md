# Campos de Heisenberg del mismo retículo

La entrada ampliada es `deltas/voa/SelectedHeisenbergInput.lean`.
No sustituye `SelectedVOAInput` ni la base común: los importa.

`LatticeFieldTruncation` demuestra desde soporte finito la anulación de todos
los modos de aniquilación suficientemente altos sobre cada estado algebraico.
`LatticeHeisenbergModes` construye la familia de modos para todo índice entero
y demuestra sus conmutadores a partir de la forma integral del retículo.
`LatticeHeisenbergField` construye operadores de vértice en el sentido preciso
de Mathlib: aplicaciones lineales a series de Laurent. Prueba la identificación
de todos sus coeficientes, las propiedades de vacío y la localidad de orden dos
de los campos de Heisenberg, coeficiente a coeficiente en dos variables formales.

Esta localidad corresponde a esos campos generadores, no al sistema completo
que incluye los campos exponenciales del retículo. No se presenta como prueba
de Jacobi para toda la VOA, ni del módulo torcido, orbifold o teorema FLM.
Los teoremas están construidos sobre el mismo selectedOrigin, sin un nuevo K,
sin una matriz de Gram independiente y sin postular las relaciones de campo.

El recibo anterior, de 139 módulos, queda conservado. `reproducir_voa.py`
comprueba ahora toda la clausura ampliada. Los archivos del manuscrito y las
pruebas anteriores no se han modificado.
