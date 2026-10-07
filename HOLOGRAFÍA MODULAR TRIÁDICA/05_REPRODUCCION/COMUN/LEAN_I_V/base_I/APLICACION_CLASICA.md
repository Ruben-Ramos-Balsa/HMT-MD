# Del retículo HMT al álgebra Moonshine

Sea Λ_HMT el vecino definido por el código ternario de Witt y el vector radial
seleccionado por la bandera marcada. Las coordenadas, la orientación y la
marca son las mismas que las conservadas por el registro regional; no se
introduce un segundo retículo para la comparación.

## Parte propia comprobada en Lean

`selected_classical_hypotheses` demuestra positividad, rango24, finitud y
libertad sobre los enteros, paridad, integridad, autodualidad y mínimo4.
`same_generated_mark_and_lattice` identifica expresamente los objetos
seleccionados con los generados. `article_I_exceptional_interface` conserva
además la incidencia cuatro más uno y la realización algebraica sobre ese
mismo punto marcado.

El papel de54 se recoge de dos formas, ambas verificadas: como defecto
residual de las evaluaciones suma y producto de APP, y como norma del vector
radial del vecino. Las lecturas operatorias APP/Fock ya existentes tienen el
mismo valor. El cociente de la división euclídea se conserva mediante su
identidad separada. Esto no confunde una coincidencia escalar con una prueba
de todas las identidades de productos de vértice.

## Composición matemática con resultados clásicos

1. La clasificación de retículos pares unimodulares positivos de rango24
   identifica el caso sin raíces con el retículo de Leech Λ.
2. Se aplica a Λ_HMT, así identificado, la construcción estándar de FLM,
   con su extensión central, levantamiento de la negación, módulo torcido y
   paridad compatible. El resultado es el álgebra Moonshine V♮.
3. El teorema de FLM da carga central24, componente de peso1 nula y grupo de
   automorfismos isomorfo al Monstruo. El carácter graduado es J=j−744.
   El teorema de Borcherds sustenta la prolongación de Moonshine relativa a
   las trazas graduadas del Monstruo.

Esta composición es la que ya expresa el manuscrito. No requiere que los
autores vuelvan a demostrar los teoremas clásicos citados. Tampoco implica
que una implementación parcial e independiente de campos orbifold quede
automáticamente identificada, como álgebra, con la construcción FLM: para
la aplicación anterior se utiliza precisamente la construcción estándar.

La parte1 de clasificación y los teoremas de2–3 se aplican bibliográficamente.
No se introducen en el entorno Lean como axiomas inventados ni se presentan
como teoremas Lean compilados. El recibo computacional certifica la parte
propia y las propiedades que permiten esa aplicación, no el contenido
íntegro de los libros y artículos clásicos.

## Fuentes y localizadores

- Fuente autoral vigente cotejada: `sections/excepcional.tex`, subsecciones
  «Selección incidencial del vecino unimodular sin raíces» y «El álgebra de
  operadores de vértice y el Monstruo»; etiquetas `exc:teorema-leech`,
  `exc:flm`, `exc:moonshine`. Copia exacta en `fuentes_cotejadas/`.
- I. B. Frenkel, J. Lepowsky y A. Meurman, *Vertex Operator Algebras and the
  Monster*, Pure and Applied Mathematics134, Academic Press,1988.
- J. H. Conway y N. J. A. Sloane, *Sphere Packings, Lattices and Groups*,
  3.ªed., Springer,1999. DOI:10.1007/978-1-4757-6568-7.
- R. E. Borcherds, «Monstrous Moonshine and Monstrous Lie Superalgebras»,
  *Inventiones Mathematicae*109,405–444,1992. DOI:10.1007/BF01232032.

Las referencias externas aparecen después del generador HMT: no seleccionan
K, ni la bandera, ni los coeficientes del retículo.
