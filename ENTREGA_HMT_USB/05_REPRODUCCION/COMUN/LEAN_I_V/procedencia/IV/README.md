# Artículo IV: dirección de K, pantallas y dualidad

Esta ampliación conecta las pruebas del artículo I con la realización concreta
del artículo IV. No reconstruye ni sustituye el núcleo anterior. No modifica
los PDF ni sus fuentes de edición.

## Resultado principal

`HMT.IV.ArticleIVSelectedScreens.article_IV_selected_screens` reúne, sin
recibir K ni su dirección como hipótesis nuevas:

- La lectura del registro seleccionado y la igualdad `uK = P3 (P11 K)`.
- Su norma exacta `(6638585 + 2275584 sqrt(5))/20` y su positividad.
- La proyección ortogonal P10, su idempotencia, simetría, imagen de dimensión
  diez, y la eliminación del modo uniforme y de la dirección uK.
- El cociente real identificado con el grafo `(P11 v, P10 v)`. Ese grafo
  conserva la primera coordenada y tiene dimensión once; la imagen de P10
  tiene dimensión diez.
- El plano hiperbólico añadido al mismo retículo seleccionado del artículo I,
  la restricción ortogonal y el cociente isotrópico, con rangos 26, 25 y 24.
- La composición de ambas pantallas con la dualidad del radio seleccionado.

Los teoremas `actual_coordinated_formula` y `actual_elliptic_duality`
expresan el mapa sobre el cociente literal del hiperplano y prueban su
entrelazamiento y la conservación de energía. Se conserva la prueba anterior
del transporte del dominio y del Hamiltoniano autoadjunto en
`SelectedRadiusTDuality`, sin repetirla.

## Organización de las pruebas

1. `k_direction/SelectedKDirection.lean`: lee el registro real de
   `SharedArticleIBase`; calcula la dirección, sus coordenadas y su norma.
2. `k_direction/P3ChartProjection.lean`: demuestra las identidades matriciales
   de simetría, idempotencia, anulación del vector uniforme y traza tres.
3. `OrthogonalKScreen.lean`: demuestra las dos proyecciones, rangos,
   descomposiciones ortogonales, isomorfismo del grafo, invariancia ante
   reescalado no nulo y covariancia ante isometrías que conservan el modo uniforme.
4. `lorentz_screen/SelectedLorentzScreen.lean`: utiliza el retículo seleccionado,
   construye el cociente isotrópico y las aplicaciones de dualidad.
5. `ArticleIVSelectedScreens.lean`: instancia y compone los resultados anteriores.

## Correspondencia con la carta finita

La tabla P3 está escrita explícitamente en Lean. El cálculo de su procedencia
como suma de caracteres de A5/C5 se reproduce en aritmética exacta
Q(sqrt(5)), mediante `k_direction/verify_p3_table.py` y la copia conservada de
`evidence/variacional.py`. Se comprueban las 144 entradas, el orden de la carta,
la dirección y su norma. Las identidades matriciales posteriores se demuestran
en Lean. No se presenta la comprobación Python de la suma de caracteres como
un teorema Lean de representaciones.

La aplicación clásica Leech–FLM del antecedente se conserva con su alcance
declarado. Esta ampliación no añade un axioma FLM ni identifica por sí sola
los rangos de las pantallas con una formalización completa de teoría M física.

## Reproducción

Esta carpeta es un incremento de integración: debe acompañar a la entrega
`PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922`, no sustituirla. El paquete
acumulativo reúne ambos. La misma biblioteca sirve para las ediciones española
e inglesa.

Se requiere Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`. Los objetos heredados comprobados
corresponden a macOS arm64; otras plataformas necesitan recompilar los
antecedentes desde sus fuentes.

```sh
python3 -I -S reproduce.py \
  --parent /ruta/PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922 \
  --lean /ruta/lean4.21/bin/lean \
  --mathlib-root /ruta/mathlib4 \
  --report-dir /ruta/nueva/comprobacion_IV
```

El resultado esperado es `PASS_ARTICLE_IV_SELECTED_SCREENS`. El recibo enumera
las fuentes, huellas, objetos y axiomas observados. No se recompilan los
antecedentes: se verifican sus huellas y se compilan los cinco módulos nuevos.
Los teoremas seleccionados conservan `Lean.ofReduceBool` de la selección
anterior. No hay `sorry` ni axiomas nuevos.
