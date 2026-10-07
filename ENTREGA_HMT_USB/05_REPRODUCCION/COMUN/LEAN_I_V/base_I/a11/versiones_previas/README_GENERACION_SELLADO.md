# Artículo I — generación completa y orden normal de los campos reticulares

```sh
python3 -I -S reproducir_generacion.py --mathlib /ruta/mathlib4 --lean /ruta/lean
```

Requiere Python 3, Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`. El ejecutor verifica las fuentes,
recorre los imports en orden, reutiliza objetos sólo si coinciden sus huellas
y procedencia, compila los cambios y consulta los axiomas de los resultados.
El ZIP conserva todas las fuentes HMT de la clausura; no necesita una carpeta
privada adicional. Mathlib y Lean son dependencias externas declaradas.

## Cadena conservada

APP → TRIT → TPK → estado enriquecido → publicaciones regionales → registro
seleccionado → incidencia → retículo → cociclo y álgebra torcida → Fock →
campos cargados → composición de sus operadores. Se reutilizan la selección
y la inversión de K, las publicaciones de alfa, la acción y el electrón.
Los parámetros, dominios y condiciones de los enunciados anteriores no se
suprimen ni se convierten en conclusiones numéricas más fuertes.

No se introduce un coeficiente de Moonshine como entrada. Las fuentes de
los avances son la construcción reticular del artículo I y el transporte
operatorio APP–Witt U031 del integral. El emparejamiento que aparece en el
factor de contracción es el del mismo retículo previamente construido.

## Pruebas añadidas

- Transporte APP–Witt sobre las doce fibras racionales: biyección de etiquetas,
  conservación del emparejamiento y cuadrado conmutativo con el operador
  matricial de APP que interviene en el índice 54. No se confunde esta
  isometría racional con una identificación adicional de pegados enteros.
- Conmutadores de la traslación con los modos de creación y aniquilación,
  incluido el cruce de frecuencia uno al modo cero de carga.
- Generación del portador completo por las palabras finitas de los campos
  cargados y los modos oscilatorios actuando sobre el vacío. La prueba no
  se limita a un número finito de pesos, frecuencias o cargas.
- Reordenación de los coeficientes de creación y aniquilación en todos los
  grados. La recurrencia del exponencial de aniquilación se deriva en la
  subálgebra conmutativa generada por sus modos y se transporta al anillo
  original de endomorfismos.
- Factorización exacta de las dos series de operadores mediante el factor
  escalar determinado por el emparejamiento integral. La ecuación de ese
  factor y la unicidad de la recurrencia se prueban, no se suponen.
- Identificación del factor con potencias binomiales, su inversión y la
  cancelación polinómica finita de polos para todo par de cargas. La identidad
  resultante sigue referida a la región de expansión especificada; no se
  confunde con la localidad completa de los campos en dos regiones.

La entrada conjunta es `deltas/generacion/SelectedGeneratedFields.lean`.
Las nuevas pruebas usan únicamente los axiomas estándar indicados por Lean.
La consulta heredada a `Lean.ofReduceBool` permanece identificada en los
recibos del antecedente; no se oculta ni se utiliza en las pruebas nuevas.

## Alcance exacto

Estos resultados desarrollan hipótesis de la reconstrucción reticular de
campos: generación, truncación ya heredada, composición y traslación. No
certifican todavía el teorema completo de reconstrucción de una VOA, la
construcción del sector torcido, el producto del orbifold FLM ni la
identificación de su grupo de automorfismos con el Monstruo.

El LaTeX sí enuncia y aplica el teorema clásico FLM al retículo construido.
Esa aplicación bibliográfica no se ha convertido en un axioma Lean. El
presente paquete no declara formalizado lo que no comprueba su ejecutor.
Los PDF no han sido modificados.

Todos los archivos del paquete anterior se conservan byte por byte. Su
README está en `versiones_previas/README_COVARIANCIA_SELLADO.md`. El recibo
de compilación conjunta está en `recibos/generacion/LEAN_CONJUNTO.json`.
Los manifiestos de conservación y causalidad documentan procedencia; no
sustituyen las pruebas del núcleo de Lean.
