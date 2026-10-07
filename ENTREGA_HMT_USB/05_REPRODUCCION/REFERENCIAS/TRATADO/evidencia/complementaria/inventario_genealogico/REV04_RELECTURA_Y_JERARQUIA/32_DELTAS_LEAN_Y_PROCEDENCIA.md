# Deltas de construcción y formalización posteriores al mapa CF

Fecha: 19 de septiembre de 2026. Corte documental: paquete de integración comunicado a las 09:10 y situación comunicada a las 09:20; los sellos UTC de los recibos se reproducen literalmente cuando se citan. Este documento nuevo conserva REV01, REV02 y REV03 sin modificación. No ejecuta compilaciones, no modifica paquetes ni PDF y no emite un dictamen sobre CH.

## 1. Rectificación concreta del inventario anterior

La actualización sustancial afecta a **CF-016, CF-019 y CF-020**, junto al vínculo entre **CF-007 y CF-012**. Ya existen módulos posteriores que construyen los registros X/Y desde los lectores regionales, los prolongan a profundidad arbitraria, reconstruyen sus dos primeras elevaciones y componen los mismos bloques con cilindros, firmas, acarreos e incidencia. Por tanto, el corte de `TPKLifts.lean` aislado no puede trasladarse a toda la implementación disponible.

La precisión anterior sobre `TPKLifts.expansion` permanece: esa función concreta se satura en treinta trits. La prolongación arbitraria está implementada **en otros constructores**, ahora localizados. No hace falta reescribir la función finita ni renombrarla para reconocer ese desarrollo posterior.

La genealogía de esta reunión sigue siendo APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. El integral de 2.249 páginas, su reservorio, la serie y los desarrollos posteriores conservan su jerarquía. Este delta es un mapa de contratos focales dentro de esa construcción; no convierte sus componentes observables en sustitutos del estado completo ni separa las construcciones consustanciales del continuo.

**Estatuto:** resultados recuperados y formalizaciones reunidas de construcciones autorales preexistentes; los recibos identifican certificados ya ejecutados por sus propietarios. Este inventario no se atribuye esas pruebas ni declara una novedad matemática por haberlas localizado.

## 2. Propietarios y residencias de consulta

Las abreviaciones de esta tabla sirven sólo para leer localizadores. Por ejemplo, `D/GeneratedTransitionRecords.lean:20` es el archivo bajo la ruta absoluta D y su línea 20.

| Código | Ruta absoluta o enlace |
|---|---|
| CF | [Contratos REV03, archivo 23](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/23_CONTRATOS_FORMALIZACION_Y_CONSTRUCCION.md>) |
| P | `/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919` |
| D | `/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919/deltas/integracion` |
| B | `/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919/lean/biblioteca` |
| R | `/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919/lean/regional` |
| X | `/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919/fuentes/articulo_x` |
| W | [Propietario de APPRouteWinding](</Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_ENROLLAMIENTO_APP_20260919/APPRouteWinding.lean>) |
| C | [Propietario de RegionalCylinderTransition](</Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_REFINAMIENTO_CONJUNTO_20260919/RegionalCylinderTransition.lean>) |
| V | `/Users/ruben/Documents/New project/output/IMPLEMENTACION_VOA_MOONSHINE_20260918` |
| PR | `/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_PRODUCTOS_RETICULARES_20260919` |
| CE | `/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_CADENA_EXCEPCIONAL_20260919` |
| I20 | [Arquitectura operatoria TPK del integral](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/20_arquitectura_operatoria_tpk_actualizada.tex>) |

`RegionalTransitionRecords`, `JointRegionalFrontier`, `JointCylinderSignature` y `GeneratedTransitionRecords` tienen como propietarios originales archivos homónimos bajo V. Las copias bajo D coinciden byte a byte con los originales y con las huellas de `P/recibos/integracion/BLOQUE_FOCAL.json` en la lectura de este inventario. Lo mismo se comprobó para W y C frente a sus copias bajo D.

## 3. Continuidad material: qué ha cambiado y qué no

Los doce módulos de base de CF —APPArithmetic, TRITCore, TPKTransport, CommonComposition, EmissionCode, TPKEmission, TPKFiniteCursor, TPKCensus, TPKOrbits, TPKRegions, TPKSimpleRegions y TPKLifts— son idénticos entre la base compartida del 18 de septiembre y B. También lo es `RegionalPublicationComposition.lean`, con SHA-256 `d4b2488d42a4b3d6ff274758b40739d305b570db01f9958154d536fbdb3838dd`.

La actualización no consiste en una corrección silenciosa de esos archivos: **hay composiciones posteriores que el mapa CF no había inventariado**. En particular, CF-020 leyó y describió principalmente las líneas iniciales hasta la entrega al lector; las líneas 136–201 del mismo módulo ya contienen el productor de publicaciones, su terminación y la compatibilidad de prefijos.

| Contrato anterior | Delta efectivo | Formulación que debe conservar el árbol REV04 |
|---|---|---|
| CF-007 / CF-012 | `APPRouteWinding` compone coordenadas enteras, proyección finita y cociclo bidimensional | El retorno residual conserva dos números de enrollamiento; la dirección también interviene en la recuperación del cursor |
| CF-016 | `RegionalTransitionRecords` produce X/Y desde prefijos regionales; `GeneratedTransitionRecords` elimina la profundidad fija del constructor | X/Y no son exclusivamente cuatro tablas de entrada en la implementación reunida |
| CF-017 / CF-018 | Se reutiliza el solucionador e inversas ya probados, ahora aplicados a registros producidos | La unicidad sigue teniendo el dominio de matrices ternarias; las nuevas pruebas componen productor y recuperador |
| CF-019 | `publish`, `blockGenerated`, `recordGenerated` están definidos para toda profundidad natural | La saturación de `TPKLifts.expansion` no es el límite de los lectores regionales ni de la construcción de registros |
| CF-020 | B:136–201 y los módulos D completan búsqueda, publicación, truncamiento y refinamiento mixto | La entrega al lector no acaba en la existencia de un límite real: produce prefijos compatibles y sus bloques |

## 4. DF-001 — Enrollamiento bidimensional y retorno del cursor APP

**Fuente matemática preexistente:** X/sections/nucleo.tex:56–78. El grafo de Cayley del soporte aditivo tiene dos coordenadas cíclicas. Para una ruta cerrada, el desplazamiento entero dividido por nueve da las dos componentes de enrollamiento. El camino inverso cambia sus signos.

**Formalización:** W:1–161, importación `TPKFiniteCursor`. Las definiciones son `displacement`, `inverseRoute`, `endpoint`, `closed`, `winding`. `winding` usa `TPKTransport.boundaryCarry` en ambas coordenadas y se define antes de exigir cierre.

**Teoremas y condiciones:**

- `closed_displacement` (52) y `winding_closed_formula` (62) reciben `origin : Int × Int`, una lista cardinal y `h : closed origin w`. Concluyen desplazamiento `9*winding` y la fórmula por cociente.
- `winding_append` (72) es un cociclo: la segunda contribución se evalúa desde `endpoint origin a`, no otra vez desde el origen inicial.
- `inverse_endpoint` (78) y `winding_inverse` (84) invierten la ruta desde su extremo final. No se omite ese cambio de punto de partida.
- `two_coordinate_cycles` (103) conserva los ciclos sur y este con valores `(1,0)` y `(0,1)`; no reduce el toro a un círculo.
- `cursor_recovered_from_projection_and_winding` (113) exige igualdad de la proyección finita **incluida la dirección**, más igualdad de los dos cocientes enteros. Recupera el cursor entero; no afirma recuperar toda una ruta desde su extremo.
- `transported_projection_all_depths` (133) conserva el cuadrado de compatibilidad con la actualización observable TPK para todo `n : Nat`.
- `actual_tpk_return_retains_winding` (141) evalúa la trayectoria TPK efectiva desde dos cursores `(1,1,east)` y fase cero: tras 27 transiciones, el cursor aditivo está en `(1,10,west)`, vuelve a la posición residual e incrementa su cociente horizontal en uno.

**Evidencia:** [recibo focal original](</Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_ENROLLAMIENTO_APP_20260919/APPRouteWinding.receipt.json>), salida 0, once consultas de axiomas, sin recompilar la base. La copia también está incluida en el bloque focal y en la clausura de P. Esto amplía formalmente CF-007/012; no constituye una identificación de la proyección finita con el estado enriquecido completo.

## 5. DF-002 — Productor regional de prefijos a toda profundidad

**Fuente y módulo:** B/RegionalPublicationComposition.lean:136–201, ya existente en la base leída por CF. Importa TPKLifts, ClosureRegionBridge, PropagationSemigroup y AutoscaleBrackets. Los canales son clausura, propagación y autoescala, con selectores y leyes de lectura propios.

`Stops c scale k` compara los extremos enteros de las cotas racionales. `search_terminates` (142) demuestra que existe un índice de parada para toda escala positiva; `searchDepth` (147) lo obtiene con `Nat.find`; `publish` (150) publica el extremo inferior entero a escala `base^depth`.

Los teoremas `stopped_cell_correct` (154) y `publish_eq_prefix` (173) relacionan el resultado calculado con el valor regional. **El constructor usa cotas racionales; la prueba de corrección utiliza el valor previamente producido.** No se confunden esas dos posiciones causales.

`publications_compatible` (182) prueba, para `base>0` y naturales `n,m`,

\[
 \operatorname{publish}(c,b,n+m)\mathbin{\mathrm{div}}b^m
 =\operatorname{publish}(c,b,n).
\]

`publication_step` (187) descompone el siguiente prefijo en el anterior multiplicado por la base y su nuevo residuo. `recognized_publications` (195) efectúa después las identificaciones convencionales.

**Rectificación de lectura:** esta construcción ya está formalizada; CF-020 era un mapa abreviado de su enlace inicial. El hecho de que un import arrastre `TPKLifts` no implica que todos sus literales intervengan en el cuerpo de `publish`. Las dependencias efectivas de los constructores se comprueban por declaración, no sólo por la lista de módulos importados.

## 6. DF-003 — Registros X/Y producidos desde lectores regionales

La cadena finita efectiva, con sus propietarios, es:

```text
lectores y cotas regionales
 → RegionalSixHundred.generatedPrefix
 → GeneratedN69Rows.regionalPrefixes
 → blockFromPrefix → bandFromWord → wordFromPrefix
 → recordAt → regionalX0/Y0/X1/Y1
 → solveMatrix → regionalLift0/Lift1
```

**Primer propietario:** R/RegionalSixHundred.lean:20–85. `scale=3^600`; los índices de evaluación de las cotas son 104, 160 y 700 para clausura, propagación y autoescala. `generatedPrefix` evalúa la cota inferior; `expectedPrefix` sólo aparece en teoremas de igualdad. `generated_cell_computation`, `selected_depth_stops` y `generatedPrefix_is_publication` prueban que ese cálculo coincide con la publicación regional a profundidad 600. Los índices son índices de evaluación, no valores objetivo de las constantes.

**Extracción de bloques:** R/GeneratedN69Rows.lean:32–103. `blockFromPrefix p t=(p/729^(99-t))%729`; `bandFromWord` recupera los seis trits con anchura fija. `regionalPrefixes` procede de `generatedPrefix`; `regionalPrefixes_eq_inputs` compara después con los enteros preservados. `regionalPrefixes_are_publications` (92) enlaza esos enteros con `publish c 3 600`.

**Registro y solución:** [RegionalTransitionRecords](</Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919/deltas/integracion/RegionalTransitionRecords.lean:23>) importa `GeneratedN69Rows`. `recordAt` conserva, por cada canal, las filas en tiempos `t,t+1`, en el orden clausura, propagación, autoescala. Sus cuatro especializaciones son los tiempos 0,1,2,3.

- `evaluated_records` (41) comprueba los enteros preservados por `decide +kernel`.
- `regional_records_identified` (46) demuestra que los cuatro registros **construidos** son X0,Y0,X1,Y1.
- `regional_first_blocks_are_selected_seeds` (53) enlaza los bloques iniciales con la selección de semillas anterior.
- `regionalLift0`/`regionalLift1` (60–61) se definen mediante `solveMatrix` sobre los registros producidos.
- `regional_lifts_identified` (63), `regional_transition_equations` (67), `regional_lifts_unique` (75) y `regional_lifts_existUnique` (88) reúnen identidad, ecuaciones y unicidad. La unicidad exige matrices ternarias y las dos ecuaciones; no es unicidad sobre matrices naturales sin restricción.

**Control causal de implementación, separado de las pruebas:** `P/procedencia/integracion/RegionalRecordDependencyAudit.lean` inspecciona los cuerpos de las cuatro declaraciones productoras. El recibo `BLOQUE_FOCAL.json` conserva salida 0 y cuatro recorridos de 9.292 declaraciones sin alcanzar X/Y, L0/L1, biografías literales, prefijos objetivo ni constantes convencionales de la lista excluida. No se ha vuelto a ejecutar ese control en este inventario; se leyó su código y su recibo. Es una comprobación concreta de dependencias, no un certificado de todo el corpus.

**Corrección de CF-016:** es legítimo decir que `TPKLifts` aislado parte de cuatro registros literales. Ya no es legítimo añadir que no se dispone de un productor de esos registros: este delta lo proporciona desde las publicaciones regionales posteriores. El enunciado de igualdad con nueve actualizaciones completas `Upd∘Tra∘Sel` tiene otro dominio; este módulo no lo declara ni su alcance parcial constituye ausencia matemática del corpus.

## 7. DF-004 — Registros, bandas y firma sin límite de cien bloques

[JointRegionalFrontier](</Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919/deltas/integracion/JointRegionalFrontier.lean:17>) define para todo `t : Nat`:

\[
 b_{t,i}=\operatorname{publish}(c_i,729,t+1)\bmod729.
\]

`bandsGenerated` lo descompone en seis trits y `signatureGenerated` aplica el lector de firma conjunto. Los cien bloques históricos aparecen únicamente en las comparaciones `generated_block_eq_finite` y `signatureGenerated_eq_finite`, con hipótesis `t<100`.

Teoremas relevantes:

- `publish_base729_eq_base3` (25): equivalencia entre un nivel base729 y seis trits.
- `generated_block_from_longer_prefix` (37): cualquier prefijo más profundo recupera el bloque anterior, con `t<n`.
- `generated_column_reconstruction` (69): `q+3c` recupera la suma entera de las tres bandas.
- `generated_signed_axial` (74): conserva el residuo firmado clausura + propagación − autoescala.
- `signature_recovers_axis` (81) y `generated_axis_reconstruction` (89): recuperan el trit de autoescala desde q y a; no afirman recuperar las tres bandas completas desde esos dos campos.
- `generated_signature_bounds` (94) y `generated_dual_charge` (101): cotas de residuos/cocientes y carga dual de Witt del mismo bloque.

[GeneratedTransitionRecords](</Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919/deltas/integracion/GeneratedTransitionRecords.lean:20>) importa esa construcción y RegionalTransitionRecords. `wordGenerated` y `recordGenerated` están definidos para todo tiempo natural, sin recibir los prefijos de 600 trits.

`wordGenerated_eq_finite` (29) usa `time<100`; `recordGenerated_eq_finite` (34) exige `time+1<100`. Las comparaciones especializadas `generated_record_zero/one/two/three` identifican los cuatro registros iniciales. `generated_first_blocks_are_selected_seeds` (54) conserva el enlace anterior; `generated_transition_equations`, `generated_lifts_unique` y `generated_lifts_existUnique` (70, 78 y 89) conservan las ecuaciones y unicidad de las **dos elevaciones iniciales**.

**Ámbito que no debe extenderse por el nombre:** `recordGenerated` existe a profundidad arbitraria, pero el teorema de unicidad de las dos matrices se refiere a las parejas de registros `(0,1)` y `(2,3)`. No afirma que una misma L0 o L1 describa por sí sola todas las transiciones futuras. La construcción infinita de registros y la solución matricial inicial son dos garantías compuestas y distintas.

## 8. DF-005 — Refinamiento mixto de cilindros y elección del hijo

**Fuente matemática:** I20:645–677 da las recurrencias de cilindros ternario-decimales, sus condiciones estrictas de intersección y su actualización con o sin nueva tríada. `RegionalCylinderTransition` formaliza esa componente, con `L=6n`; no sustituye los demás campos del estado.

El tipo `CylinderState` (C:18) conserva profundidades ternaria y decimal y ambos prefijos enteros. `lowerDefect`, `upperDefect`, `Compatible`, `ternaryStep` y `jointStep` están en C:25–42. Para un bloque `u : Fin 729` y una tríada `d : Fin 1000`, `joint_defect_update` (56) demuestra

\[
 A'=729000A+u\,1000^{k+1}-d\,729^{n+1}.
\]

`generated` (64) toma los dos prefijos de `publish`; `nextTernary` y `nextDecimal` toman los residuos de las publicaciones siguientes. `ChildAdmissible` (75) comprueba las desigualdades racionales alcanzadas por la búsqueda terminante. No recibe una palabra objetivo.

- `child_admissible_iff` (99) identifica exactamente el hijo admisible.
- `unique_generated_child` (116) prueba su existencia y unicidad para todo canal y profundidad.
- `generated_ternary_step` (122) y `generated_joint_step` (127) demuestran compatibilidad entre la construcción directa de prefijos y la actualización.
- `generated_truncation` (134) recupera ambos prefijos mediante división por las potencias respectivas.
- `generated_compatible` (152) demuestra que los dos cilindros contienen el mismo valor regional ya producido.
- `generated_refinement` (177) reúne siguiente estado, compatibilidad, recuperación y ley entera del defecto para todos `n,k : Nat`.

**No confundir formulaciones:** está formalizada la elección mediante el intervalo racional y la actualización exacta del residuo resultante. No se atribuye aquí una regla autónoma que seleccione el próximo bloque usando únicamente `A` y borrando los demás campos o el lector regional. La noticia de las 09:20 sobre un trabajo en esa dirección queda como actividad posterior al paquete, no como una prueba ya incorporada ni como una inexistencia matemática.

## 9. DF-006 — Los mismos hijos producen cilindros, firma y carga

[JointCylinderSignature](</Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919/deltas/integracion/JointCylinderSignature.lean:17>) importa JointRegionalFrontier y RegionalCylinderTransition. No introduce una segunda selección: `jointChild n i=nextTernary (channelOfIndex i) n`.

`JointAdmissible` exige la admisibilidad por los tres canales; `signatureFromChildren` aplica el lector a sus bandas. Los siete teoremas son:

1. `joint_child_is_regional_block` (26), igualdad definicional entre ambos accesos al bloque.
2. `joint_admissible_iff` (29), caracterización de la terna admisible.
3. `unique_joint_children` (40), existencia y unicidad de esa terna.
4. `signature_of_admissible_children` (46), igualdad de la firma obtenida con `signatureGenerated`.
5. `admissible_children_refine_same_cylinders` (52), actualización de los mismos cilindros.
6. `admissible_children_preserve_column_carry` (60), recuperación de la suma entera mediante residuo y acarreo.
7. `admissible_children_preserve_witt_charge` (67), carga dual de Witt conservada.

Éste es el enlace demostrativo que debe añadirse al árbol: no una lista de «cilindro, memoria, firma» como componentes independientes, sino pruebas de que las operaciones se aplican a los mismos bloques producidos.

## 10. DF-007 — Continuación excepcional y productos del mismo origen seleccionado

Esta ficha registra el delta posterior sin rehacer el inventario K–alfa. Los dos paquetes pedidos, CE y PR, no son alternativas a la cadena regional: la prolongan sobre su origen seleccionado.

### Incidencia concreta y campos

`CE/deltas/union/SelectedExceptionalChain.lean` importa `SelectedGeneratedFields`, `ConcreteNativeFourPlusOne` y `SelectedRadiusTDuality`.

`ConcreteIncidencePublication` (25) reúne el censo 4 de hexadas, sus 4 octadas levantadas y la estrella de 5 octadas, incluida la octada restante, sobre la tétrada seleccionada; también incorpora la octada única determinada por el soporte negativo. `concrete_incidence_publication` (36) y `selected_incidence_and_generated_fields` (39) prueban esa composición con la generación de campos.

`shared_action_electron_exceptional_chain` (47) mantiene explícitos `U,massUnit : ℝ` positivos, `x,y : ℝ`, un `Reader` y `η : Refinement (internalMoments x y)`. Su conclusión reúne la publicación acción–electrón, entrada algebraica de vértices, Heisenberg, trazas graduadas, energía, campos cargados, covariancia, generación e incidencia concreta. Esos parámetros no desaparecen porque el teorema se reúna bajo una sola entrada. En este inventario se registra su tipo; no se reanaliza ni se vuelve a certificar la ley de masas.

### Productos del vacío a todos los grados

`PR/deltas/productos/LatticeVacuumContraction.lean` importa `LatticeNormalOrdering` y `LatticeContractionFactor`. `vacuum_contraction` (22) recibe `o : Fin 12`, `x,y : Lattice o`, `r,d : ℕ`. Evalúa sobre el vacío la identidad de orden normal ya probada: si `r≤d`, el resultado es la contracción escalar del emparejamiento entero por el modo de creación de grado `d-r`; si `d<r`, es cero.

`vacuum_contraction_degree_bound` (54) exige `d<r`; `vacuum_contraction_pairing_bound` (59) exige un emparejamiento igual a un natural `p` y `p<r`. No se borra la condición de signo implícita en esa igualdad con un natural.

`PR/deltas/productos/SelectedFieldProducts.lean:15–28` define `VacuumProductPublication` sobre `Lattice selectedOrigin` y prueba `selected_vacuum_products` y `selected_incidence_generation_and_products`. El origen es el mismo seleccionado; no se vuelve a recibir K como entrada ni se reelige un retículo para satisfacer el producto.

### Delta incluido después en P: localidad mixta

`D/LatticeAllMixedFields.lean:15–28` prueba `heisenberg_field_commutator` para todo modo entero `m,k`, con el retículo y emparejamiento ya construidos. Combina pruebas de modos positivos, cero y negativos; la identidad del conmutador no entra como hipótesis.

`D/LatticeMixedLocality.lean:17–23` compone esa identidad en `heisenberg_charged_locality`. `D/SelectedMixedFieldLocality.lean:19–34` la aplica al mismo `selectedOrigin` y reúne incidencia, generación, productos, localidad cargada y localidad mixta en `selected_incidence_generation_products_and_both_localities`.

**Límite documental positivo:** el paquete formaliza esos campos, productos y localidades; sus README excluyen atribuir a esta compilación la construcción completa FLM, el módulo torcido, el orbifold o la identificación final con el Monstruo. El carácter reflejado reticular tampoco se renombra como J. Ello describe el alcance del certificado Lean, no elimina las construcciones y demostraciones posteriores del corpus.

## 11. Prueba escrita, compilación registrada e inclusión en PDF

Estos tres estados deben conservar columnas distintas. Una fuente Lean con prueba no es todavía un recibo de ejecución; una compilación Lean tampoco introduce automáticamente una sección en un PDF.

| Material | Prueba en fuente | Evidencia de compilación leída | Inclusión en PDF acreditada por esta revisión |
|---|---|---|---|
| Enrollamiento APP | X/nucleo:56–78 y W | Recibo focal original; 11 consultas; salida 0; copia autenticada en P | El antecedente está incluido por `X/main.tex:112`; no se ha cotejado aquí un PDF compilado con el delta Lean |
| X/Y desde lectores | RegionalTransitionRecords, 7 consultas | BLOQUE_FOCAL, salida 0; control de dependencias conservado | Nota y fuentes del paquete; no actualización del PDF acreditada |
| Bandas/registros a toda profundidad | JointRegionalFrontier, 13 consultas; GeneratedTransitionRecords, 11 | BLOQUE_FOCAL, salidas 0; fuentes originales y copias coincidentes | No actualización del PDF acreditada |
| Cilindros y firma conjunta | RegionalCylinderTransition, 10; JointCylinderSignature, 7 | Recibo original C y BLOQUE_FOCAL | Antecedente I20 localizado; no inserción del delta en PDF acreditada |
| Cadena excepcional | SelectedExceptionalChain, 3 consultas | CE/recibos/union/LEAN_CONJUNTO.json: este módulo compilado, 213 reutilizados | CE declara que no modifica PDF |
| Productos del vacío | LatticeVacuumContraction, 5; SelectedFieldProducts, 2 | PR/recibos/productos/LEAN_CONJUNTO.json: 216 módulos reutilizados | PR declara que no modifica PDF |
| Integración P | 13 módulos focales, 81 consultas en BLOQUE_FOCAL | Clausura reunida de 251 módulos, todos reutilizados en LEAN_CONJUNTO | P/README declara que no modifica los PDF |

Las tres raíces PR, CE y P no contienen archivos `.pdf` ni `.fls` en el censo local de esta revisión. Conservan fuentes del artículo X, incluido su `main.tex`, y antecedentes LaTeX; esto prueba disponibilidad de fuentes, no inclusión de los nuevos deltas en una edición PDF externa. Los resultados preexistentes de X siguen en sus propietarios, no se declaran retirados por no recompilarse aquí.

### Detalle de los recibos

- CE: `PASS_PORTABLE_LEAN_SOURCE_CLOSURE`, 214 módulos; `SelectedExceptionalChain` compilado y 213 reutilizados; final UTC `2026-09-18T18:37:51.988515+00:00`.
- PR: mismo estado, 216 módulos; cero compilados y 216 reutilizados; final UTC `2026-09-18T18:46:35.644462+00:00`.
- P: mismo estado, 251 módulos; cero compilados y 251 reutilizados; final UTC `2026-09-19T09:06:21.974902+00:00`. `whole_pdf_formalized=false`, `mathlib_rebuilt=false` y `source_files_modified=false`.
- `P/recibos/integracion/BLOQUE_FOCAL.json`: `PASS_MIXED_FIELDS_AND_REGIONAL_ENRICHMENT_DELTA`, 13 módulos nuevos respecto de 238 antecedentes autenticados; 81 consultas; sus entradas registran ejecuciones focales con salida 0. No contradice la reutilización posterior: son dos momentos de evidencia distintos.
- W y C conservan además recibos originales `PASS_FOCUSED_FIELD_MODULE`, con `base_modules_recompiled=0`, compilador Lean 4.21.0 y alcance de fuente e imports directos. No se presentan como recompilación limpia de toda su base.

Los seis módulos de rutas/registros/cilindros aquí focalizados suman 59 consultas. Sus salidas impresas usan sólo `propext`, `Quot.sound` y `Classical.choice`, según cada declaración; dos ciclos elementales no usan axiomas. La integración excepcional que hereda el selector conserva `Lean.ofReduceBool`. Esa dependencia no se proyecta indiscriminadamente sobre todos los teoremas ni se oculta al reunir la cadena.

### Huellas de los seis deltas focales

| Módulo | SHA-256 de fuente, coincidente con BLOQUE_FOCAL |
|---|---|
| APPRouteWinding | `0dcccb396e5c8b95395d17170c7cef36daf0c3c60317e3e11cd2aad9a79c0a77` |
| RegionalTransitionRecords | `e08ab7178d1e80d215507fa12133cc20ac367961769e7ab121f32e0bdb5522fc` |
| JointRegionalFrontier | `3af30e92b05a35ad31f5ad5b5cb311477ddf67b286f1123d21a2cfa248d2d261` |
| RegionalCylinderTransition | `517f0b0246aac41823aa521a52bff9776080c997035f14f296a2a308fa4e6b8d` |
| JointCylinderSignature | `04374ccb5d7007896c087e42bcac826620dd2f28ca872664bb6d623cd49d16fe` |
| GeneratedTransitionRecords | `4fb67bb5e21f525ad0846be9dd287b4236471f4ebd77988f3c13fb96f5ef45b9` |

Se cotejaron aquí las fuentes, no se lanzó su compilador ni se reprodujo toda la clausura de objetos. Los recibos originales conservan huellas de objetos, comandos, imports y axiomas para esa reproducción.

## 12. Reglas antirregresión que se desprenden del delta

1. **No reiterar «X/Y sólo son tablas».** Es cierto para las definiciones aisladas de TPKLifts; es falso como descripción de la cadena disponible tras RegionalTransitionRecords y GeneratedTransitionRecords.
2. **No convertir cien bloques en límite.** `generatedRows` es una evaluación finita; `blockGenerated`, `recordGenerated` y `generated_refinement` tienen cuantificación arbitraria. Las hipótesis `<100` pertenecen sólo a las comparaciones con el testigo finito.
3. **No atribuir periodicidad matricial universal.** La producción de registros a cualquier profundidad no convierte las dos ecuaciones iniciales en una ley global de L0/L1 sin el enunciado correspondiente.
4. **No equiparar import con dependencia productora.** El control debe inspeccionar los cuerpos de las declaraciones, como hace el auditor de registros. Una conclusión de igualdad puede citar una tabla sin convertirla en entrada del constructor.
5. **No borrar el punto inicial al invertir.** Las leyes de ruta inversa se aplican desde el extremo final; la composición del enrollamiento transporta el origen intermedio.
6. **No trocar recuperación del cursor por recuperación de la ruta.** Proyección, dirección y cocientes recuperan el cursor. Las distintas rutas que lo alcanzan conservan su archivo propio.
7. **Conservar el mismo hijo y el mismo origen seleccionado.** JointCylinderSignature y SelectedMixedFieldLocality ya prueban composiciones concretas; no sustituirlas por componentes enumerados ni pedir de nuevo esas mismas igualdades.
8. **Distinguir compilación focal, adopción de caché y PDF.** La cifra 251 es tamaño de una clausura manifestada; no es número de nuevas compilaciones ni certificado de todas las afirmaciones del artículo.
9. **Aplicar el corte temporal.** El desarrollo sobre residuo interno comunicado como en curso a las 09:20 no se declara terminado por encontrar un archivo mutable, ni se presenta como vacío del corpus.

Estos son controles editoriales y de reutilización propuestos, no una garantía de que ningún sistema vuelva a equivocarse. El mecanismo práctico es enlazar cada afirmación al contrato y propietario de esta revisión antes de describirla como pendiente.

## 13. Lectura realizada y continuación

Se leyeron íntegros los seis módulos focales de D y los recibos originales W/C; RegionalSixHundred, GeneratedN69Rows, RegionalRecordDependencyAudit, SelectedExceptionalChain, SelectedFieldProducts, LatticeVacuumContraction, LatticeAllMixedFields, LatticeMixedLocality y SelectedMixedFieldLocality. Se cotejaron las secciones pertinentes de RegionalPublicationComposition, los README de PR/CE/P, la nota de procedencia de registros, el ejecutor `reproducir_integracion.py`, el mapa CF y los localizadores LaTeX indicados. Los JSON grandes se inspeccionaron por sus campos, módulos focales y huellas; no se afirma una nueva ejecución a partir de esa lectura.

Se aplicaron núcleo formal, continuidad y causalidad de constantes para conservar la posición de productores, lecturas y recuperadores. Se ejecutaron sólo los controles de protocolo `hmt_formal_kernel.py --verify` y `verify_generated_constants.py --self-check`, además de lecturas y cotejos de bytes. Sus PASS no se presentan como nuevas pruebas matemáticas.

La incorporación siguiente al árbol consiste en sustituir los pendientes documentales correspondientes de CF por **estos enlaces ya recuperados**, manteniendo separados los dominios. No requiere volver a pedir a sus autores el enrollamiento, la generación regional de X/Y, el refinamiento de cilindros ni la composición de firmas que ya constan aquí. La inclusión futura en PDF exige una edición autorizada con sus fuentes y un control material de esa edición; no se ha efectuado en esta revisión.
