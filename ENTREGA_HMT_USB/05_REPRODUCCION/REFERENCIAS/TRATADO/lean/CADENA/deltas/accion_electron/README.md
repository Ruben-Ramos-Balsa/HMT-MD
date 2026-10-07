# Composición del registro seleccionado con acción y electrón

Ampliación formal del artículo I, de 18 de septiembre de 2026. Reutiliza la
biblioteca reunida en `HMT_ARTICULO_I_FUENTES_Y_PRUEBAS_ES_EN_REV04B` y la
selección de `TerminalSelector`; no cambia los PDF ni sus fuentes LaTeX.

## Resultado

`SelectedArticleIComposition.principal_action_electron_composition` conecta
la misma coordenada alfa, publicada a cualquier profundidad, con la década
determinantal de acción −34, las dos secciones de acción y el operador de masa
en la fibra electrónica central. No recibe una hipótesis `PublishedRegister`
ni construye un registro por inversión del valor esperado.

- `SelectedActionDomain.lean`: deriva las cotas necesarias desde la coordenada
  seleccionada, identifica la raíz analítica, obtiene el orden decimal, las
  secciones positivas, su cociente y la continuación regional completa.
- `ElectronOrientationBridge.lean`: formaliza el intercambio de orientaciones
  del par regional y la identidad entre los lectores π/φ² y φ/π². Reutiliza los
  coeficientes de propagación para el carácter exponencial posterior.
- `SelectedElectronPublication.lean`: enlaza la norma global APP √3/4, el
  déficit 22, la memoria 15, la torsión electrónica completa y el triple de
  retorno (80,54,6) con la composición electrónica y la acción del operador
  sobre su vector central. La unidad dimensional aparece una vez.
- `SelectedArticleIComposition.lean`: entrada común que reúne las
  publicaciones de alfa a toda profundidad y su uso en acción y electrón.

Los resultados originales de la norma, los recuentos, el cociente H4, las
secciones y el operador se importan; no se vuelven a demostrar ni se cuentan
como resultados nuevos de esta ampliación.

## Alcance y dependencias

El registro se obtiene por `SelectedFromRegionalInputs.regionalRegister`.
Ese constructor ya recibe N69, el panel y W24 producidos por los lectores
regionales, y conserva S8 no ordenado como interfaz explícita de la fuente.
Esta ampliación no modifica ni demuestra la producción anterior de S8.
La evaluación finita heredada utiliza `Lean.ofReduceBool`; no se describe
como reducción exclusiva por el núcleo de Lean.

La torsión de la composición es `ElectronComposition.regionalFull`.
`VacancyDeltaBounds.vacancyDelta` sigue perteneciendo a la carta analítica de
alfa y no se sustituye en la fórmula electrónica. Las bases dimensionales y
el refinamiento de los momentos internos permanecen como parámetros tipados.

La verificación de esta carpeta es incremental: compila todas sus fuentes
nuevas y registra las consultas de axiomas y los objetos importados. No es
una recompilación transitiva de toda la biblioteca ni un paquete USB autónomo;
es un suplemento para integrarlo en la entrega única del artículo.

## Reproducción del suplemento

Con Lean 4.21.0 y los objetos de las dependencias ya comprobadas en `LEAN_PATH`:

```sh
python3 -I -S verify_incremental.py --lean /ruta/al/lean --output /ruta/al/recibo
```

El recibo conserva fuente, hash, comando, resultado y axiomas de cada módulo.
La integración completa debe unir estos cuatro archivos a las fuentes
anteriores por nombre y hash, resolver sus imports y utilizar el lanzador
común de la entrega. No deben sustituirse las dependencias por copias de
objetos temporales.

## Correspondencia con el manuscrito

Fuente temática: `manuscript_es/sections/electron.tex`, ecuaciones
`eq:el-bisagra`, `eq:el-delta`, `eq:el-lector-determinantal`, `eq:el-decada`,
`eq:el-h5`, `eq:el-secciones-accion`, `eq:el-formula-completa` y
`eq:el-rango-uno`; continuación de la acción en `revision_planck.tex`.
La versión inglesa utiliza las mismas fórmulas y esta misma biblioteca formal.
