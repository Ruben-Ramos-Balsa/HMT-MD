# Correspondencia estado–campo sobre el retículo seleccionado

Esta entrega desarrolla en Lean la correspondencia estado–campo del portador
reticular que ya procede de la selección conjunta y de la incidencia del
Artículo I. No vuelve a seleccionar `K`, no introduce otro retículo y no
modifica los PDF ni el paquete anterior sellado.

## Cadena que se conserva

La cadena material de partida es APP–TRIT–TPK, estado enriquecido, lectura
regional y selección terminal conjunta, incidencia Witt–Golay y vecino
reticular marcado. El origen `selectedOrigin` y el portador
`LatticeCarrier selectedOrigin` son exactamente los ya construidos. Las
coordenadas, el cociclo, el producto del álgebra de grupo torcida, los modos,
el vacío y los campos cargados se importan de esa construcción.

La procedencia matemática es **arquitectura autoral preexistente** y
**resultado recuperado** del apartado `exc:voa` del LaTeX del Artículo I.
Las pruebas Lean aquí incorporadas son **certificados nuevos** de esa
construcción. La teoría convencional de campos formales es el lenguaje de
prueba posterior; no selecciona el registro ni las incidencias HMT.

## Qué demuestra el código nuevo

1. Construye la derivada dividida del campo de Heisenberg con sus
   coeficientes binomiales, incluidos los modos negativos y el intervalo
   en que el binomial se anula.
2. Define el producto normal ordenado de esa derivada con cualquier campo
   de Laurent del mismo portador. Prueba la finitud de ambas sumas sobre
   cada estado y un límite inferior de exponentes para cada entrada.
3. Construye un campo para toda palabra finita de osciladores sobre cada
   carga reticular. Prueba que es regular sobre el vacío y que su
   coeficiente constante produce exactamente el estado de esa palabra.
4. Representa cada ocupación de la base existente mediante una palabra
   con las mismas multiplicidades y extiende la asignación linealmente a
   **todos** los estados del portador.
5. Prueba que el mapa lineal `stateField` recupera cada estado en el vacío,
   es inyectivo y conserva la truncación Laurent puntual. El campo del
   vacío es la identidad. Los estados fundamentales cargados dan los
   mismos campos cargados anteriores; los estados de un oscilador dan
   los mismos campos de Heisenberg derivados.
6. Especializa estas pruebas al origen seleccionado y las reúne con las
   localidades cargada y mixta de los campos generadores ya demostradas.

No hay límite fijo de frecuencia, de longitud de palabra, de ocupación ni
de peso. Cada vector algebraico tiene soporte finito; eso no es una
truncación global del espacio. Las sumas localmente finitas son operaciones
efectivas, no resultados postulados mediante axiomas.

## La llegada escrita a Moonshine y el alcance formal

El LaTeX del Artículo I continúa desde el mismo retículo par, autodual,
positivo y sin raíces de rango 24 hasta
`V_Λ = M(1) ⊗ C_ε[Λ]`, la involución, el sector torcido y el producto
orbifold de `V_Λ⁺ ⊕ (V_Λᵀ)⁺`. Después aplica el teorema clásico de
Frenkel–Lepowsky–Meurman para reconocer `V^natural`, el grupo Monstruo y
el carácter `J`. El texto identifica expresamente FLM como reconocimiento
posterior y no como una nueva demostración de ese teorema dentro del artículo.
La segunda realización por orden tres también está conservada en
`moonshine_comparacion.tex`, junto con la equivalencia de las presentaciones.

Por tanto, **la cadena escrita hasta Moonshine no se declara ausente**.
Tampoco se identifica una referencia bibliográfica con una prueba aceptada
por el núcleo de Lean. Esta entrega acredita la correspondencia
estado–campo y las propiedades enumeradas arriba. No acredita todavía
Jacobi/localidad para todos los descendientes, la estructura conforme
completa, el sector torcido y el producto orbifold, ni la identificación
formal de su grupo de automorfismos con el Monstruo. Estos nombres no se
han usado como axiomas ni como conclusiones ficticias de las pruebas.

La elección de una lista para cada multiconjunto da una presentación
concreta de los campos. Se demuestra la independencia del **estado**
respecto al orden de los creadores. La independencia del **campo** respecto
a toda permutación de esa lista requiere la conmutación correspondiente de
productos normales y no se infiere sólo de la creatividad o la inyectividad.

## Reproducción y conservación

`reproducir.py` autentica las fuentes y objetos de las 279
dependencias del paquete anterior, compila exclusivamente los módulos
nuevos en orden topológico e interroga cada declaración pública con
`#print axioms`. Las pruebas generales sólo admiten `propext`,
`Classical.choice` y `Quot.sound`. La especialización a `selectedOrigin`
conserva adicionalmente `Lean.ofReduceBool`, ya declarado por el selector
finito anterior; aquí no se añade otra selección nativa.

El recibo distingue compilación, huellas, declaraciones y axiomas. Su
éxito no se presenta como formalización íntegra del artículo ni de los
teoremas clásicos citados. La entrega preserva el antecedente completo,
sus fuentes LaTeX, Python, datos, recibos y Lean, sin alterarlos.

Orden del paquete desplegado:

- `antecedente/`: paquete precedente completo, sin modificaciones; su
  `README.md` conserva el arranque causal y sus pruebas.
- `lean/`: los siete módulos nuevos, recompilados en orden de importación.
- `recibos/estado_campo/VERIFICATION.json`: ejecución conjunta conservada,
  con declaraciones y axiomas efectivos.
- `MANIFIESTO.json` y `VERIFICACION_CONSERVACION.json`: huellas del paquete
  y comparación íntegra del antecedente.

Desde la carpeta desplegada:

```text
python3 -I -S reproducir.py --plan
python3 -I -S reproducir.py --lean /ruta/a/lean --mathlib /ruta/a/mathlib4
```

El primer comando comprueba el plan sin compilar. El segundo recompila los
módulos nuevos y escribe un recibo nuevo en `resultados/`, sin modificar el
recibo de entrega. No exige otro ZIP HMT. Lean 4.21.0 y Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3` son dependencias de software.
El caché heredado corresponde al compilador arm64 de macOS especificado en
el recibo; no puede reutilizarse como si fuera un binario de otra plataforma.
El verificador rechaza un compilador incompatible en vez de emitir un PASS.
