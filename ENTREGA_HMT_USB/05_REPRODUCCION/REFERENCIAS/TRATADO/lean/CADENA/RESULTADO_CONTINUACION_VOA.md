# Continuación comprobada del artículo I

Entrada: `deltas/voa/SelectedHeisenbergInput.lean`.
Teorema compuesto:
`HMT.I.SelectedHeisenbergInput.shared_action_electron_heisenberg_fields`.

La clausura declarada de 143 módulos pasó en Lean 4.21.0:
4 módulos compilados en esta ejecución y 139 reutilizados tras
comprobar fuentes, dependencias, objetos y compilador. Se verificaron
210 declaraciones explícitas en la consulta final.
Estos números describen el control, no sustituyen el alcance de los teoremas.
En la primera compilación de esta continuación se compilaron 17
módulos y se reutilizaron 122 de la base. El control final de nombres
de aquella ejecución necesitó una corrección de cualificación de espacios de
nombres; no se cambió ninguna prueba. Se conservaron su recibo y el posterior
PASS conjunto de 139 módulos. El control actual incorpora además los campos.

## Resultados incorporados

- El agregado de la diferencia producto–suma se calcula en las dos hojas de
  APP. Su coeficiente unitario es −3; la lectura orientada de U030 tiene índice
  54. La ecuación polinómica de compatibilidad tiene una única solución entera
  positiva, 12.
- El operador finito de grado dos actúa sobre 24 + 300 coordenadas. Sus dos
  trazas son −12 y 66, con total 54; el acoplamiento orientado también tiene
  traza 54. El falsador del propio corpus conserva ese índice pero cambia el
  peso digital a 63. No se identifica una traza con una dimensión.
- Sobre el mismo `selectedOrigin` y el mismo retículo se construyen el cociclo,
  la extensión central y el álgebra compleja torcida. Sus leyes se prueban;
  no son campos supuestos de un certificado vacío.
- Se construye el portador algebraico de osciladores con modos y grados sin
  cota. Cada vector es una combinación finita. Se prueban las relaciones de
  conmutación, los modos cero, los desplazamientos del retículo y su acción
  sobre el producto tensorial. El vacío es no nulo.
- Se construye la involución del cociclo elegido y del portador, junto con
  los proyectores par e impar. Se prueban involutividad, idempotencia,
  anulación cruzada y descomposición.
- La entrada común conserva la composición de acción y electrón, sin
  sustituir el registro ni repetir las pruebas de K. El contrato de regresión
  del fundamento se compila dentro de la misma clausura.
- Desde soporte finito se demuestra la truncación puntual de los modos de
  aniquilación. Se construyen los campos de Heisenberg como aplicaciones
  lineales a series de Laurent, con todos sus coeficientes enteros. Se prueban
  las propiedades de vacío y la localidad de orden dos de esos campos,
  coeficiente a coeficiente en dos variables, a partir de los conmutadores.

## Frontera exacta

La compatibilidad de las trazas con la norma radial no se promueve a un
entrelazador de operadores. No se ha identificado formalmente aquí el bloque
matricial finito con una componente graduada del portador simétrico infinito.
La involución pertenece al cociclo triangular construido; no afirma por sí
sola una normalización diagonal específica de FLM.

La localidad de los campos de Heisenberg sí está probada. La correspondencia
estado–campo completa de la VOA, incluidos los campos exponenciales del
retículo, Jacobi para toda la VOA, el módulo torcido, el producto del orbifold
y la identificación de su grupo con el
Monstruo no son conclusiones de esta entrega Lean. El LaTeX los trata por
aplicación de FLM; la cita no se ha convertido en un axioma Lean. Esta
continuación no se presenta como una formalización terminada de Moonshine.

Se conserva sin alterar el alcance de S8 y de las interfaces de la base. El
selector finito heredado usa `Lean.ofReduceBool`; las pruebas nuevas del índice
orientado utilizan reducción del núcleo y no añaden ese axioma. No se admite
`sorry`, `admit` ni un axioma HMT nuevo.

No se ha cambiado ningún PDF. Los archivos manifestados de la base anterior
permanecen idénticos. Las fuentes LaTeX se conservan como procedencia, no como
pruebas Lean por el hecho de copiarlas. Mathlib no se ha reconstruido.

## Reproducción

`python3 -I -S reproducir_voa.py --mathlib /ruta/mathlib4 --lean /ruta/lean`

El README especifica las versiones. El ZIP contiene todas las fuentes HMT de
la clausura, el contrato, la documentación y los recibos. Lean y Mathlib son
dependencias externas declaradas. El recibo congelado está en
`recibos/voa/LEAN_CONJUNTO.json`.
