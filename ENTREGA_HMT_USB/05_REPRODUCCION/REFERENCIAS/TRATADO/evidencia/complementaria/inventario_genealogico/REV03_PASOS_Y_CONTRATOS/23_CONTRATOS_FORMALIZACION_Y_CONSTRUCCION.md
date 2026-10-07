# Contratos de construcción y formalización: APP, TRIT, emisión, semillas y levantamientos

Fecha: 19 de septiembre de 2026. Revisión documental focal, preparatoria del desarrollo exhaustivo REV03. No modifica fuentes, PDF, REV01 ni REV02; no compila una nueva biblioteca ni crea una prueba Lean nominal.

## 1. Objeto, perímetro y evidencia material

El objeto de este mapa es hacer explícito **qué produce cada implementación, desde qué entradas y mediante qué composición**, antes de reutilizarla en el desarrollo posterior de HMT–MD. El orden preservado es APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo → salidas correlacionadas. El corte documental de este archivo llega a las semillas regionales, los levantamientos ternarios y sus cinco prefijos finitos; no redefine el alcance de la tesis ni emite un dictamen sobre CH.

La autoridad temática sigue siendo el integral de 2.249 páginas y su reservorio, la serie, la narración y los desarrollos posteriores. Los doce módulos comparados y los dos documentos de REV01/REV02 son índices de acceso a ese material, no un sustituto del corpus ni el perímetro de la futura exposición.

Se han distinguido cuatro clases de evidencia:

1. **Demostración y ley declaradas en LaTeX**, con localizadores y operaciones.
2. **Definición y teorema efectivamente escritos en Lean**, con tipos e importaciones.
3. **Recibo previo de compilación**, enlazado a los bytes actuales de fuente y objeto.
4. **Programa Python**, cuya lectura permite distinguir construcción, comparación y escritura de resultados; no se atribuye una ejecución nueva a un programa que aquí sólo se ha leído.

En esta revisión se han contrastado los doce módulos APP–TRIT–emisión–semillas–levantamientos entre la biblioteca compartida, el directorio de formalización y la entrega del artículo I REV04B. Los doce son idénticos byte a byte entre esas tres residencias. Sus doce fuentes y doce objetos `.olean` coinciden asimismo con las huellas del recibo compartido. Esto permite reutilizar la evidencia identificada **sin afirmar una recompilación realizada hoy**. El recibo del 17 de septiembre registra `cache_hit: true` y `exit_code: 0` para estos módulos.

El recibo global permite `Lean.ofReduceBool` en el selector terminal posterior; los doce módulos focales enumerados aquí no lo muestran entre los axiomas impresos de sus declaraciones. No se traslada la política de axiomas del selector a toda la biblioteca ni a la inversa.

## 2. Registro de propietarios y rutas

Los códigos de esta tabla son abreviaciones documentales: `B/APPArithmetic.lean:40` significa la ruta absoluta de B, seguida de ese archivo y de su línea 40. No son nombres matemáticos de objetos HMT.

| Código | Propietario material |
|---|---|
| N | [Núcleo común, `nucleo.tex`](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/sections/nucleo.tex>) |
| T | [Desarrollo de TRIT](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/trit_desarrollo.tex>) |
| U | [Desarrollo operatorio TPK](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/tpk_desarrollo_integrado.tex>) |
| E | [Emisión y condiciones iniciales, `extension.tex`](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/extension.tex>) |
| G | [Regiones y levantamientos, `generacion.tex`](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/generacion.tex>) |
| F | [Censo de firmas](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/libro/censo_firmas_emision.tex>) |
| I | [Registro de transiciones del integral](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex>) |
| B | `/Users/ruben/Documents/New project/output/PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA/lean/biblioteca` |
| W | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization` |
| S | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage18_article_I/delivery/HMT_ARTICULO_I_FUENTES_Y_PRUEBAS_ES_EN_REV04B/lean` |
| R | [Recibo Lean compartido](</Users/ruben/Documents/New project/output/PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA/recibos/base_compartida/LEAN_CONJUNTO.json>) |
| P1 | [Recurrencia Python del emisor](</Users/ruben/Documents/New project/PUBLICACION_HMT/HOLOGRAFIA_MODULAR_TRIADICA/pruebas/python/verificar_catalogo_app.py>) |
| P2 | [Contraste de firmas y preimágenes en X](</Users/ruben/Documents/New project/output/PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA/fuentes/articulo_x/supplement/emission/verify_signatures.py>) |
| P3 | [Reconstrucción finita del artículo I](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage18_article_I/delivery/HMT_ARTICULO_I_FUENTES_Y_PRUEBAS_ES_EN_REV04B/documentation/supplement/common/finite_owner/verificar_nucleo_finito.py>) |
| P4 | [Generador nonádico histórico](</Users/ruben/Documents/New project/certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py>) |

Las rutas B/W/S no se consideran idénticas por su nombre: la igualdad de los doce archivos se comprobó en esta revisión. La residencia B es la utilizada para los contratos y la huella de R; W y S permiten reconocer la continuidad de la implementación.

## 3. Grafo de importación y clases de funciones

```text
Std ── APPArithmetic ──┐
Std ── TRITCore ───────┼── CommonComposition ──┐
Std ── TPKTransport ───┤                       ├── TPKEmission
      ModalIncidence ─┘      Std ─ EmissionCode┘
                                               │
                                         TPKFiniteCursor
                                               │
                                           TPKCensus
                                               │
                                           TPKOrbits
                                               │
                                           TPKRegions
                                               │
                                        TPKSimpleRegions
                                               │
                                           TPKLifts
```

`ModalIncidence` es una dependencia real de `CommonComposition`; no debe omitirse al preparar un entorno aislado. La importación de un módulo no implica que cada teorema utilice todas sus declaraciones, ni que la mera presencia de una importación pruebe el enlace causal buscado. El enlace se identifica por el término de prueba y su tipo.

La siguiente clasificación evita cuatro sustituciones indebidas:

| Función | Clase operativa | Qué no sustituye |
|---|---|---|
| `APPArithmetic.evaluate`, `TRITCore.balanced`, `TPKTransport.step`, `TPKEmission.emitStep` | Evaluación local, cambio de representación y transporte cronológico explícito | La generación completa del continuo por el solo hecho de llamarse «estado» |
| `TPKFiniteCursor.signature`, `TPKCensus.emitted`, `TPKRegions.rows` | Construcción de firmas, imagen finita y metadatos desde la recurrencia | Un catálogo leído como entrada sin reconstruir sus fibras |
| `EmissionCode.recoverS`, `recoverE`; inversas de `TPKLifts` | Recuperación desde un objeto ya producido | La selección del objeto anterior a esa recuperación |
| `TPKLifts.solveMatrix`, `calendar` | Resolución de una relación finita y selección entre calendarios, con registro de transiciones explícito | La producción de ese registro a partir de la actualización completa, que requiere su contrato propio |
| Lectores racionales regionales posteriores | Realización y evaluación de una salida ya seleccionada | La selección retrospectiva mediante cifras convencionales objetivo |

## 4. Contratos elementales ya formalizados

### CF-001 — Marca positiva y reconstrucción APP

- **Entrada:** `APPArithmetic.Digit := Fin 9`, con `value i = i.val+1`; para `reconstruct` la entrada es `n : Nat` y se exige `0 < n`.
- **Construcción:** `rho9`, `q9`, `Lifted`, `lift`, `decode`. La salida guarda por separado residuo positivo y cociente.
- **Garantía Lean:** `rho9_range`, `reconstruct`, `quotient_source_formula`, `decode_lift`, `lift_injective_positive` (B/APPArithmetic.lean:31–90).
- **Fuente matemática:** N:20–54. La hipótesis positiva no se elimina porque la función Lean esté definida también en cero; el teorema de reconstrucción conserva expresamente esa hipótesis.
- **Python:** P1:`dr9`, `plus_value`, `times_value` (29–47) calcula la lectura residual de marcas positivas. P1 no devuelve en esas funciones un objeto `Lifted`; la reconstrucción de cociente tiene un contrato adicional en Lean.

### CF-002 — Dos evaluaciones, dos residuos y dos cocientes

- **Entrada:** par de marcas `i j : APPArithmetic.Digit`.
- **Operaciones:** `sumEval`, `productEval`, `sumResidue`, `productResidue`, `sumQuotient`, `productQuotient`, `PairedEvaluation`, `evaluate`.
- **Salida:** dos registros levantados, no un residuo común que funda las dos hojas.
- **Garantía Lean:** `reconstruct_sum`, `reconstruct_product`, `paired_reconstruction`, `paired_symmetry` (B/APPArithmetic.lean:94–143).
- **Fuente:** N:29–54. **Prueba de distinción:** `paired_residual_collision` y `residue_does_not_determine_quotient` (212–221) impiden deducir identidad de historia desde igualdad de residuos.
- **Uso posterior:** `CommonComposition.readVisit` toma la evaluación aditiva del cursor aditivo y la multiplicativa del cursor multiplicativo; no presupone que ambos cursores estén en la misma casilla.

### CF-003 — Suma de representantes y cociclo de acarreo

- **Entrada:** marcas `a b c : Digit`; el representante de la clase cero es `zeroClass := 8`, cuya marca positiva es 9.
- **Operaciones:** `addPositive`, `carry`, `section_add` y `carry_reconstruction`.
- **Garantía:** `addPositive_associative`, `addPositive_identity`, `carry_cocycle`, `carry_identity` (B/APPArithmetic.lean:146–187). Este último da acarreo 1 con la sección positiva, no 0.
- **Fuente:** N:82–106. Se debe conservar la sección elegida al comparar esta identidad con una sección normalizada que represente la clase cero por 0.
- **No equivalencia:** este acarreo modular no es automáticamente el archivo íntegro de una historia ni la memoria dodecafásica.

### CF-004 — Censo de las seis lecturas APP

- **Entrada:** el soporte completo `Fin 9 × Fin 9`, por `sumOverDigits` y `totalOverSupport`.
- **Salidas probadas:** `census_sum=810`, `census_product=2025`, `census_sum_residue=405`, `census_product_residue=459`, `census_sum_quotient=45`, `census_product_quotient=174`.
- **Composición probada:** `integrated_defect`, `integrated_defect_value` (B/APPArithmetic.lean:189–210). Se conserva `2025−810 = 54+9·129`; 54 no es por sí solo la diferencia de las sumas enteras.
- **Fuente:** N:108–121. Los teoremas están evaluados con `decide`; las cifras no entran como hipótesis de los enunciados.
- **Contrato editorial:** los seis totales deben conservar sus seis etiquetas; no agruparlos bajo «suma APP» sin distinguir evaluación, residuo y cociente.

### CF-005 — TRIT balanceado reversible

- **Entrada:** `n : Int`; salida `Digit × Int`, donde `Digit={r:Int // −1≤r ∧ r≤1}`.
- **Operaciones:** `quotient n=(n+1)/3`, `residue n=n−3*quotient n`, `balanced`, `reconstruct`.
- **Garantía:** `residue_bounds`, `reconstruction`, `reconstruct_balanced`, `balanced_unique`, `balanced_reconstruct`, `reconstruct_injective` (B/TRITCore.lean:13–57).
- **Conservación:** `zero_residue_retains_carry` y `visible_residue_not_injective` (111–119); `pairAdd`, `pairMul`, `reconstruct_pairAdd`, `reconstruct_pairMul`, `carry_cocycle` (128–171).
- **Fuente:** N:170–178 y T. El producto conserva los términos cruzados y el producto de cocientes; no es la multiplicación de dos residuos aislados.
- **Despliegue elemental de REV03:** [aritmética trítica, pasos TRIT-001.01–05](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/20_TRIT_OPERACIONES_Y_PRUEBAS.md>) desarrolla en lenguaje matemático estas identidades, con sus casos y ejemplos. Su control Python finito es distinto de las pruebas universales ya identificadas en TRITCore.

### CF-006 — Selector de fase y realización cuadrática

- **Entrada:** entero para `phase`; plano entero `Plane := Int × Int` y parámetro `τ : Int` para `J`.
- **Salidas:** `phase_nonadic_values` da `[1,−1,0,1,−1,0,1,−1,0]`; `J τ (x,y)=(-τ*y,x)`.
- **Garantía:** `residue_eq_phase`, `phase_periodic`, `J_square`, `iterateJ_even`, `iterateJ_odd`, `elliptic_square`, `parabolic_square`, `hyperbolic_square` (B/TRITCore.lean:63–85, 178–235).
- **Fuente:** N:182–235 y T. Este módulo demuestra la realización cuadrática **entera** y sus potencias. No contiene por sí solo una formalización del exponencial real, de las funciones trigonométricas ni de la interpretación temporal física.
- **Enlace ya probado:** `CommonComposition.additive_selector_matches`, `multiplicative_selector_matches`, `neutral_selector_matches` (28–39) identifican exactamente el calendario del transporte con el selector TRIT.

### CF-007 — Transporte de dos cursores y frontera espacial

- **Entrada:** `ObservableLift` con dos `Cursor` de coordenadas enteras y una `Phase := Fin 108`; cada cursor lleva `Direction`.
- **Operaciones:** `active`, `halfTurn`, `orient`, `stepCursor`, `step`, `unstep`. El cursor activo se desplaza; al completar cada bloque de 27 transiciones se invierte la orientación.
- **Garantía:** `cursor_unstep_step`, `cursor_step_unstep`, `unstep_step`, `step_unstep` (B/TPKTransport.lean:41–124).
- **Memoria:** `HistoryLift`, `recordStep`, `recorded_projection`, `recorded_length`, `recorded_no_reset`, `recorded_prefix_preserved` (136–168) conservan la lista de estados anteriores.
- **Frontera:** `residue9`, `quotient9`, `lifted_coordinate_reconstruct`, `boundaryCarry`, `boundary_transport`, `boundary_cocycle` (187–207).
- **Fuente:** E:8–20 y U. **Corte formal explícito:** `ObservableLift` es un levantamiento del transporte observable con su archivo, no una declaración de que esos tres campos sean todo el estado enriquecido del corpus.

### CF-008 — Composición APP–TRIT–transporte en cada profundidad

- **Entrada:** par de marcas APP o un estado observable levantado.
- **Operaciones:** `appTrit`, `cursorMark`, `readCursor`, `readVisit`, `visitTrit`.
- **Garantía:** `app_trit_additive`, `app_trit_multiplicative`, `cursor_positive_chart`, `cursor_mark_periodic`, `visit_additive_reconstruction`, `visit_multiplicative_reconstruction`, `every_visit_reconstructs` (B/CommonComposition.lean:11–98).
- **Dominio de universalidad:** todo `n : Nat` para la iteración del transporte definido, no sólo las primeras seis ventanas.
- **Importaciones:** APPArithmetic, TRITCore, TPKTransport y ModalIncidence. El módulo existe precisamente para no sustituir la composición por la mera coexistencia de cuatro nombres.
- **Fuente:** N y E:20–37. La marca positiva es la de la coordenada entera más 1, compatible con la indexación de cursores desde cero.

### CF-009 — Muestra anterior al desplazamiento y archivo cronológico

- **Entrada:** `ObservableLift`; `Sample` guarda `before`, `kind` y `arithmetic`.
- **Operaciones:** `classify`, `sample`, `additiveReading`, `exponentReading`, `Execution`, `emitStep`, `samples`.
- **Garantía:** `emitStep_reads_before`, `samples_length`, `execution_current`, `execution_memory`, `execution_no_reset`, `samples_append`, `execution_concatenates` (B/TPKEmission.lean:17–165).
- **Lector multiplicativo:** `log9_unit_table`, `log9_radical`, `log9_inverse_on_units` (35–52), con extensión 0 a 3,6,9; `sample_retains_evaluations` conserva el origen de esa lectura.
- **Fuente:** E:20–29. **Python productor:** P1:`channel_signature` y `direct_u6` (50–107) leen antes de mover; P2 compara ambas implementaciones sobre todos los pares cuando se ejecuta su `main`.

### CF-010 — Ventana nonádica y ley decimal

- **Entrada:** nueve muestras consecutivas, desde cualquier fase formalizada.
- **Operaciones:** `phaseCount`, `WindowTotals`, `totals`, `window`, `decimalValue`, `block`.
- **Garantía:** `phaseCount_nine`, `nine_events_each`, `every_nine_window`, `window_neutral`, `decimalValue_bound`, `block_source_formula` (B/TPKEmission.lean:174–247).
- **Salida:** `block : ObservableLift → Fin 1000`, con cifras `S mod10`, `(S+E) mod10`, `(3S+5E+7Z) mod10`.
- **Fuente:** E:29–49, ecuaciones `eq:emisor-seis`, `eq:acoplamiento`, `eq:psi-catalogo`. Los coeficientes 3,5,7 pertenecen a la ley emisora declarada; esta ficha no les inventa una derivación adicional. El 1 de la forma reducida proviene de `7*3 mod10`.
- **Preservación:** sumar muestras es una lectura; `Execution` conserva su orden. La igualdad del total no implica igualdad de los archivos.

### CF-011 — Acoplamiento e inversa de firmas

- **Entrada:** dos dígitos de `Fin 10` o dos firmas `Fin 6 → Fin 10`; salida código `Fin 1000` o palabra de seis códigos.
- **Operaciones:** `EmissionCode.encode`, `hundreds`, `tens`, `units`, `recoverS`, `recoverE`, `encodeWord`.
- **Garantía:** `recoverS_encode`, `recoverE_encode`, `encode_injective`; y, sobre el emisor, `TPKEmission.block_as_encode`, `block_recovers_signatures`, `word_as_encodeWord`, `word_recovers_signatures`, `equal_words_equal_signatures` (B/EmissionCode.lean:17–97; B/TPKEmission.lean:249–284).
- **Fuente:** E:39–65. **Python:** P1:`combine` y `recover_signatures` (110–134).
- **Hipótesis y alcance:** la inversa recupera las firmas. No recupera una semilla única entre las 104.976: las fibras de semillas tienen multiplicidad y quedan conservadas como tales en el censo posterior.

### CF-012 — Cociente espacial finito con cuadrado de compatibilidad

- **Entrada:** cursores enteros y fase; salida cursores `Fin 9 × Fin 9` con dirección y fase.
- **Operaciones:** `projectCursor`, `liftCursor`, `projectState`, `project`, `jointStep`, `signatureVector`, `seedObservable`.
- **Garantía:** `project_lift`, `project_stepCursor`, `projectState_step`, `projectState_iterate`, `project_iterate`, `reading_at_depth`, `sumReadings_project`, `signatureVector_project`, `signatures_two_cursor`, `word_from_finite_factors` (B/TPKFiniteCursor.lean:73–276).
- **Optimización probada:** `runTicks_correct`, `fastWindow_correct`, `runWindows_range`, `signatureFast_eq` (279–337). El cálculo rápido está vinculado al lector original, no aceptado por una igualdad de resultados aislada.
- **Fuente:** E:8–65. **Pérdida del cociente:** `project` olvida vueltas espaciales; éstas siguen en el levantamiento entero. `project_lift` no afirma la identidad contraria sobre un cursor entero arbitrario.

### CF-013 — Enumeración de semillas y catálogo emitido

- **Entrada:** todas las posiciones `Fin 9 × Fin 9` y cuatro direcciones; fase inicial 0, cuya primera fase publicada corresponde a 1.
- **Operaciones:** `directions`, `seeds`, `signatures`, `signatureImage`, `multiplicity`, `couple`, `emitted`.
- **Garantía:** `seeds_complete`, `seeds_nodup`, `seeds_cardinality`, `paired_seed_cardinality`, `signatureImage_exact`, `couple_is_TPK_word`, `emitted_exact`, `emitted_full_TPK_image` (B/TPKCensus.lean:28–111).
- **Censos probados:** `signatures_additive_checked`, `signatures_multiplicative_checked`, `additive_image_cardinality`, `multiplicative_image_cardinality`, `additive_fibre_profile`, `multiplicative_fibre_profile`, `emitted_cardinality`, `emitted_nodup` (798–831).
- **Fuente:** E:8–65 y F. Los literales `additiveRows` y `multiplicativeRows` son testigos de evaluación comparados por teorema con `signatures`; no reemplazan al generador en su definición.
- **Python:** P1:`channel_signature`, `direct_u6`, `combine`; P3:`signature`, `census` (25–88). P3 construye primero y sólo después compara el catálogo preservado.

### CF-014 — Publicación ternaria orientada y acción diedral

- **Entrada:** palabra emitida; `ternary` aplica `(-U_i) mod3`, no una conversión posicional global del entero decimal.
- **Garantía:** `ternary_full_TPK_image`, `ternary_image_cardinality`, `ternary_fibre_profile` (B/TPKCensus.lean:113–142, 832–847).
- **Acción:** `TPKOrbits.rotate`, `swap`, `act`; `rotate_cube`, `dihedral_relation`, `action_composition`, `psi_equivariant`; `emission_closed`, `produced_closed`, `orbit_count`, `orbit_cover`, `representative_unique`, `quotient_classification`, `weighted_orbit_count` (B/TPKOrbits.lean:27–123, 898–1077).
- **Salida:** 243 palabras entre las 729 posibles y 43 órbitas de la imagen; 38 de tamaño 6 y 5 de tamaño 3.
- **Fuente:** G:8–25 y el propietario integral de órbitas enlazado en SR-013/SR-014 del inventario anterior. **Python:** P4:`psi`, `word_orbit`, `select_structural_orbits` (142–389).
- **Distinción:** 43 órbitas finitas no significa 43 retornos nonádicos; tampoco el signo de Ψ puede cambiarse sin transportar la orientación.

### CF-015 — Fibras completas, metadatos y selección regional

- **Entrada:** imágenes de firmas y sus preimágenes generadas; no una lista externa de tres palabras escogidas por su decimal.
- **Operaciones:** `TPKRegions.makeRow`, `rows`, `fibre`, `seedMass`, `sortedMasses`, `isClosure`, `closureOrbits`, `hasOrientation`, `orientedClosure`.
- **Garantía:** `row_source_factorization`, `rows_emit_exactly`, `rows_count`, `total_seed_mass`, `metadata_valid`, `closure_orbit_unique`, `orientation_unique`, `closure_five_regions`, `closure_mass_partition` (B/TPKRegions.lean:183–199, 672–802).
- **Propagación y autoescala:** `TPKSimpleRegions.radicalSingletons`, `closureCensus`, `propagationOrbits`, `autoscaleOrbits`, `orientSelected`; los teoremas `radical_membership`, `propagation_selection_spec`, `autoscale_selection_spec`, `propagation_orbit_unique`, `autoscale_orbit_unique`, `selected_words_produced` conservan soporte diagonal, censo y orientación (26–235).
- **Salida:** semillas orientadas de clausura `010211`, propagación `201101`, autoescala `121200`; fibras y multiplicidades anteriores permanecen identificadas.
- **Fuente:** G:8–43. El predicado de clausura incluye el perfil `432+4*144`; el sector mínimo exige soporte diagonal `{0,3,6}`; el calibre `d=6, ES` fija la orientación. Suprimir una de estas condiciones cambia el selector.

### CF-016 — Registro de transiciones: objeto anterior al cálculo matricial

- **Objeto matemático:** bloques `b_j^χ=Π_6(x_j^χ)` con `x_(j+1)^χ=U_(9j+9)…U_(9j+1)(x_j^χ)`; `U_t=Upd_t∘Tra_t∘Sel_t` en I. Las filas de `X0,Y0,X1,Y1` son las transiciones de tres regiones, dos por cada tramo.
- **Fuente explícita:** G:45–86 e I:45–123, etiqueta `eq:registro-transiciones-tpk-explicito-rev10`. Las cuatro matrices completas están publicadas, junto al teorema `thm:reconstruccion-lifts-calendario-rev10`.
- **Contrato implementado en Lean:** B/TPKLifts.lean:99–123 contiene las cuatro matrices como definiciones literales. El encabezado declara expresamente que el módulo reconstruye los levantamientos desde esos registros y no implementa allí su producción por `Sel/Tra/Upd`.
- **Contrato Python:** P3:`transport` lee las matrices de I mediante `matrix`; P4 contiene L0/L1 embebidas. Ninguno de estos dos caminos debe describirse como si generara las cuatro matrices desde la ejecución enriquecida en ese mismo programa.
- **Consecuencia para REV03:** mantener la generación descrita por el corpus y localizar su ejecución fila a fila como contrato distinto de CF-017. El corte de una implementación no se convierte en inexistencia de la operación matemática, y la operación declarada tampoco se convierte, sin enlace, en un teorema Lean ya escrito.

### CF-017 — Reconstrucción única de L0 y L1

- **Entrada implementada:** `X0,Y0,X1,Y1 : TPKLifts.Matrix`, matrices de seis filas de `Word`. Cada `Word` usa naturales; `Ternary`/`TernaryMatrix` expresa la pertenencia al dominio de residuos 0,1,2.
- **Operaciones productoras:** `allWords`, `applyColumn`, `solveColumn`, `solveMatrix`; `L0 := solveMatrix X0 Y0`, `L1 := solveMatrix X1 Y1` (B/TPKLifts.lean:13–133).
- **Garantía:** `L0_reconstructed`, `L1_reconstructed`, `transition_equations`, `reconstructed_lifts_ternary`, `L0_unique`, `L1_unique` (149–188). La unicidad exige `TernaryMatrix M` y la ecuación matricial correspondiente; no es una unicidad entre matrices naturales arbitrarias sin reducción.
- **Fuente:** G:45–86 e I:94–123. **Python:** P3:`inverse_det`, `mm`, `rowmul`, `transport` (99–164) obtiene las matrices por eliminación exacta módulo 3 y contrasta los determinantes 1 y 2.
- **Distinción:** `L0Witness`/`L1Witness` son formas normales posteriores contrastadas con el solucionador; no son las definiciones de L0/L1 en Lean. `headD` posee una salida por defecto, pero los teoremas sobre estas matrices certifican el caso válido y único.

### CF-018 — Inversas de los levantamientos

- **Entrada:** palabra ternaria y una de las dos matrices reconstruidas.
- **Garantía:** `record_inverses_checked`, `reconstruction_inverse_formula`, `lift_inverse_matrices_checked`, `word_inverse_checked`, `word_inverse` (B/TPKLifts.lean:191–253).
- **Salida recuperada:** la palabra anterior en el mismo dominio de seis residuos; las igualdades se comprueban sobre las 729 palabras y se generalizan por `allWords_complete` a cualquier palabra que satisfaga `Ternary`.
- **Fuente:** I, reconstrucción por matriz invertible. Esta recuperación local no reconstruye por sí sola todo el registro de la condición inicial que dio la palabra: para ello se conservan las fibras y la historia anteriores.
- **No permuta papeles:** una inversa certificada es una ley de recuperación; no es un selector independiente de semillas ni un reemplazo de CF-016.

### CF-019 — Calendario 0011, trayectoria finita y truncamiento

- **Entrada:** `selectedSeeds` se compone realmente desde los selectores CF-015. Las biografías de referencia se forman desde las filas de CF-016.
- **Operaciones:** `chooseLift`, `run`, `referenceBiographies`, `binaryCalendars`, `compatible`, `acceptedCalendars`, `calendar`, `biographies`, `flattenWords`, `expansion`.
- **Garantía:** `selected_seeds_checked`, `record_stitching`, `accepted_calendars_checked`, `calendar_reconstructed`, `calendar_unique`, `biographies_match_records`, `five_prefix_lengths`, `initial_block_preserved`, `four_step_truncation` (B/TPKLifts.lean:255–381).
- **Dominio del censo:** los 16 calendarios binarios de longitud cuatro. El único compatible con las tres biografías es `[false,false,true,true]`, es decir L0,L0,L1,L1.
- **Profundidad precisa:** `expansion_length` dice `6*(min n 4+1)`. Este `expansion` se satura en 30; no se lo debe citar como si ya fuera la prolongación arbitraria completa. `run_length`, `run_ternary` y `run_take` sí son genéricos para una lista finita de elecciones dada.
- **Fuente:** G:69–86 e I:103–145. P3 examina además las 144 perturbaciones unitarias de entradas matriciales; ese ensayo Python no se atribuye a un teorema Lean de perturbaciones que aquí no se ha localizado.

### CF-020 — Entrega al lector regional posterior

- **Módulo existente:** `HMT.I.RegionalPublicationComposition`, que importa TPKLifts, ClosureRegionBridge, PropagationSemigroup y AutoscaleBrackets.
- **Enlaces concretos:** `unique_selected_seed`, `selected_seeds_are_shared`, `selected_seed_in_biography` (B/RegionalPublicationComposition.lean:26–49); conectan selección regional y prefijo finito sin sustituir las semillas por nombres de constantes.
- **Paso de lectura:** `value`, `lower`, `upper`, `produced_brackets`, `eventual_publication`, `joint_eventual_publication` (54–125) son contratos posteriores de realización racional/real. Las identificaciones convencionales aparecen como teoremas de reconocimiento, no como entradas al catálogo.
- **Corte conservado:** el encabezado 14–16 mantiene expresamente el contrato de transiciones X/Y de TPKLifts. Importarlo no borra sus premisas ni formaliza retroactivamente una actualización enriquecida que el módulo no define.
- **Alcance de esta ficha:** sólo fija la conexión de entrega; no intenta inventariar aquí todos los lectores ni la coordenada alfa, tratados en el tramo K–alfa del inventario global.

## 5. Relación exacta entre los programas Python

| Programa | Entradas efectivas | Construye | Recupera o contrasta | Salida al ejecutar |
|---|---|---|---|---|
| P1 | Regla de panel, direcciones, calendario, LOG9; después CSV de referencia | Firmas por `channel_signature`, emisiones por `direct_u6` y `combine` | `recover_signatures`, igualdad con catálogo, fibras y ensayos de coordenadas | Certificado `catalogo_app_exhaustivo.json` |
| P2 | Funciones P1 preservadas localmente y `FIRMAS_EMISION.json` | Recurrencia por 324 semillas de cada hoja; 104.976 pares directos/factorizados | Preimágenes, multiplicidades, cardinales | Informe por salida estándar; no se ejecuta aquí |
| P3 | Regla de emisión; registro LaTeX X/Y; catálogo para contraste posterior | `census()` genera emisiones; `transport()` calcula X inversa por Y | Determinantes, matrices impresas, 16 calendarios y 144 mutaciones | Recibo solicitado por `--receipt`; no se ejecuta aquí |
| P4 | Catálogo de 468 emisiones, L0/L1 y AW embebidas, leyes racionales del lector | Selección orbital/regional y prolongación certificada del lector | Censos, cierres, regiones, límites y lectura decimal posterior | Certificado y ledger de 396 bloques; no se ejecuta aquí |

P4:182 abre el catálogo y P4:64–92 fija L0/L1 y calendario. Por tanto, «reconstruye el censo» en la cabecera de ese programa significa que verifica su estructura y sus cifras **desde el catálogo recibido**; para la generación de las 104.976 parejas se conecta P1/P2/P3 o TPKCensus. Esta conexión evita tanto acusar erróneamente de tabla objetivo a todo el sistema como atribuir a un archivo una función generadora que no realiza.

Los imports de P1/P2/P3/P4 pertenecen a la biblioteca estándar Python en los pasajes inspeccionados: `collections`, `itertools`, `pathlib`, `json`, `csv`, `fractions`, `hashlib`, `re`, `argparse`, `importlib.util`, `typing`. P4 declara que no importa `math`, `decimal`, `mpmath`, `sympy` ni `numpy`. Esta ausencia no certifica por sí sola causalidad; la causalidad se determina leyendo entradas, funciones y composición.

## 6. Entorno local observado, sin instalación ni recompilación

La inspección ejecutó únicamente órdenes de versión y lecturas de manifiestos, toolchains, fuentes, objetos y huellas. No invocó `lake update`, `lake build`, descarga de caché ni recompilación de Mathlib.

| Componente | Observación local del 19 de septiembre |
|---|---|
| Lean | `/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean`; versión 4.21.0, `arm64-apple-darwin23.6.0`, commit `6741444a63ee`, Release |
| Lake | Mismo directorio; versión `5.0.0-6741444`, Lean 4.21.0 |
| Toolchains instaladas | La inspección de `~/.elan/toolchains` encontró `leanprover--lean4---v4.21.0` |
| Mathlib | `/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4`, commit `308445d7985027f538e281e18df29ca16ede2ba3`; `lean-toolchain` pide 4.21.0 |
| Paquete compartido B | No tiene `lakefile.lean`, `lakefile.toml` ni `lean-toolchain` en su raíz; usa reproductor propio y LEAN_PATH explícito. Esto no equivale a ausencia de entorno |
| Directorio W y entrega S | No se encontró lakefile ni lean-toolchain en las raíces examinadas; las recetas de empaquetado fijan el compilador, no un supuesto `lake build` desde cualquier carpeta |
| TerminalSelector | En `/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_ARTICULO_I_20260917/TerminalSelector` tampoco hay lakefile o toolchain de raíz; conserva su verificador y objetos propios |
| Suplemento Lean de X | `fuentes/articulo_x/supplement/lean/lean-toolchain` del paquete compartido declara `leanprover/lean4:v4.21.0` |
| pdfLaTeX | `/Library/TeX/texbin/pdflatex`, pdfTeX 1.40.26, TeX Live 2024 |
| XeLaTeX | `/Library/TeX/texbin/xelatex`, XeTeX 0.999996, TeX Live 2024 |
| LuaLaTeX | `/Library/TeX/texbin/lualatex`, LuaHBTeX 1.18.0, TeX Live 2024 |
| latexmk | `/Library/TeX/texbin/latexmk`, versión 4.83 |
| Tectonic | No localizado en PATH en esta inspección |
| Python | `/usr/bin/python3`, Python 3.9.6 |

R conserva el `LEAN_PATH` completo, incluida la carpeta de objetos unificados, Mathlib y sus dependencias Cli, batteries, Qq, aesop, proofwidgets, importGraph, LeanSearchClient y plausible. Las doce pruebas focales son del tramo `Std` y módulos internos; la prolongación `RegionalPublicationComposition` sí arrastra resultados analíticos de Mathlib. No se debe imponer esta dependencia analítica a un módulo elemental que no la utiliza, ni borrarla en una entrega que sí importa aquel lector.

Que el binario exista no garantiza que toda compilación futura sea inmediata: influyen la coincidencia de fuentes y objetos, LEAN_PATH, versión de dependencia, recursos, receta de construcción y paquetes tipográficos. La evidencia actual permite preparar un entorno controlado, no prometer ausencia de incidencias futuras.

## 7. Evidencia de compilación reutilizable y huellas focales

Todos los módulos de esta tabla coinciden con W y S, con la fuente registrada en R y con el objeto actual de R. Para los doce, R registra salida 0 y reutilización de caché. Axiomas agregados de las declaraciones impresas: `P=propext`, `Q=Quot.sound`, `C=Classical.choice`. La columna no afirma que todo teorema use todos ellos.

| Módulo | SHA-256 de la fuente | Axiomas en R |
|---|---|---|
| APPArithmetic | `0681e5ffe5e985b50d4b7a80a74cf2ab09c41d5804f9f9858b53911b3de85e49` | P |
| TRITCore | `3716cee573117b17f6de69c9050a4b4023c5be9cd8c4a9ed32a1115dac2f6b62` | P,Q,C |
| TPKTransport | `035af221b4d468ab21d82aa5e257320510bb4a5028db17efa9b7facb6a02e508` | P,Q |
| CommonComposition | `f1c7ccffb8f4f5ead47fe3e37fb6309b22f7df272682587696b3e20360bbe3f0` | P,Q,C |
| EmissionCode | `d43a6372404e3a92a41fa31ff286389832dc5da876b2b8ba24225e82b48a2025` | P,Q |
| TPKEmission | `4adc068749947daeeba282a2fd26771f3400fdfdf42c2238d8a3e59970659c3f` | P,Q |
| TPKFiniteCursor | `48b43b21b70fdf9295039574faa2448e12eab3fbc9f99263c0afdbdb4c4ff9e6` | P,Q |
| TPKCensus | `8b5d549e818914856cbfda5f832ca5748ef3c2ee93c5132ae7b954514241dd32` | P,Q,C |
| TPKOrbits | `a48d19597247fdd418bbe8fda62e9ec67796be0075932cd52397b6afc1cdfb52` | P,Q,C |
| TPKRegions | `233842009c37b76122e047ac7826cabdb24e70bb87f80a4141ba66fc8cb3b12b` | P,Q |
| TPKSimpleRegions | `a567706e7db59bb3d2a5abe92f6bc703f429c13da1f07fa64950d9d4aac5098c` | P,Q,C |
| TPKLifts | `835d423fb1a1d57d4646fbc5f1e154b3c4ffdd10bebb8c7d8ba8249aa6dcb6bd` | P,Q |

`#print axioms` figura en las fuentes y su salida en R. La evidencia no se reduce a buscar la palabra `sorry`: el enunciado, sus entradas, importaciones, hipótesis y alcance forman parte del contrato. Los teoremas elementales citados no equivalen a certificar íntegramente el artículo I, X o el corpus.

## 8. Contratos de enlace que REV03 debe desplegar, sin llamarlos pruebas ya incorporadas

Los puntos siguientes son **tareas de reunión documental y formalización de enlace**, no teoremas que este inventario acaba de probar:

1. **Actualizar el estado completo antes de publicar la fila.** Para cada fila X/Y, fijar estado anterior, dominio, operación Sel/Tra/Upd, nueve transiciones, proyección Π6 y registro conservado. El contrato debe señalar al propietario operatorio del integral, no conformarse con repetir `b=Π6(x)`.
2. **Separar campo de memoria y campo observado.** Los teoremas `recorded_no_reset` y `execution_memory` conservan una lista concreta. Para usarla como realización de la memoria enriquecida del TPK hace falta especificar qué campos quedan incluidos y su mapa hacia el estado completo; no cambiarle el nombre al tipo observable.
3. **Respetar los tipos de inversa.** `recoverS/recoverE` recupera firmas; `word_inverse` recupera palabras ternarias; `project_lift` recupera un cursor finito. Cada inversa debe aparecer con su dominio, sin prometer recuperación de una semilla individual desde una fibra múltiple.
4. **No extender `expansion` por abuso del cuantificador.** Su fórmula se satura en 30. El contrato de profundidad arbitraria pertenece a la prolongación y a los lectores/cilindros posteriores, con memoria y decisión de frontera propias.
5. **No suprimir la procedencia de los coeficientes.** Mod9, mod3, pesos decimales, 3/5/7, 27/54/108 y la orientación ES deben figurar en la ley que realmente los usa. Un número entero sin fuente no se justifica sólo por aparecer también en otra parte del corpus.
6. **Conectar las implementaciones, no sus rótulos.** Si P4 recibe un catálogo generado por P1 o Lean, registrar su hash, los campos utilizados y la igualdad de contenido; si recibe matrices reconstruidas, registrar la prueba y las entradas X/Y de dicha reconstrucción.
7. **Vincular el delta al recibo correcto.** Una futura modificación de estos módulos invalida la igualdad de bytes aquí registrada para el archivo cambiado. Debe producir su propia compilación o conservar expresamente el estatuto de fuente aún no recompilada.

## 9. Controles antirregresión propuestos y verificaciones realizadas

### Comprobaciones realizadas en esta revisión

- Lectura de los contratos y fuentes focales citados; cotejo de doce módulos entre B, W y S.
- Concordancia de las doce fuentes y los doce objetos actuales con R.
- Inspección de imports, teoremas concretos y axiomas impresos del recibo.
- Lectura de las funciones Python y separación entre producción del catálogo, comparación y reconstrucción desde registro.
- Versiones de Lean, Lake, motores TeX, latexmk, Python y commit de Mathlib.
- `hmt_formal_kernel.py --verify`: salida `PASS_NUCLEO_FORMAL_HMT_PERMANENTE`.
- `verify_generated_constants.py --self-check`: salida `PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY`.

Estas dos puertas son controles de protocolo, no pruebas nuevas de los contratos ni sustitutos de la lectura.

### Ensayos que conviene incorporar al arnés de conservación

- Comprobar que la reconstrucción APP sólo se invoque con su hipótesis positiva o con un tratamiento explícito de cero.
- Detectar cambios en las seis etiquetas de totales APP y en `carry zeroClass a=1`.
- Comparar «leer antes de mover» frente al orden invertido, conservando muestras para localizar el primer desacuerdo.
- Mantener simultáneamente el productor directo y la factorización por firmas; conservar las 648 preimágenes de cursores y las 104.976 parejas en el alcance del ensayo.
- Verificar Ψ con signo negativo, sus fibras y el soporte diagonal regional; no limitarse a comprobar las tres palabras finales.
- Separar en el recibo la entrada X/Y, la solución de L0/L1 y el testigo matricial posterior.
- Exigir que la receta que diga «L0/L1 generadas» enlace la actualización regional anterior, y que la que diga «reconstruidas» nombre el registro usado.
- Comprobar que 16 calendarios y 144 mutaciones conservan sus ámbitos respectivos; no convertir el ensayo Python en una declaración Lean inexistente.
- Rechazar una declaración editorial de profundidad arbitraria respaldada únicamente por `expansion_length = 6*(min n 4+1)`.
- Mantener por resultado la fuente, tipo de prueba, imports, axiomas, hash de fuente y hash de objeto. Un PASS documental no debe presentarse como ejecución nueva.

## 10. Lectura realizada y continuación delimitada

Se leyeron para esta revisión: el mapa previo de semillas SR-001 en adelante; los cuerpos focales de APP/TRIT/TPKEmission/TPKFiniteCursor/TPKLifts/CommonComposition/EmissionCode; declaraciones, definiciones de selección y pruebas terminales de TPKCensus/TPKOrbits/TPKRegions/TPKSimpleRegions; el enlace inicial de RegionalPublicationComposition; E:8–100, G:8–115, I:45–155; P1:1–150, P2 completo, P3 completo y los pasajes de P4 correspondientes a entradas, selección, matrices y prolongación finita. Se inspeccionaron también el recibo R y los objetos de sus doce módulos focales. No se presenta esta selección como lectura íntegra del corpus.

La continuación documental concreta es localizar y reunir el detalle de ejecución del estado enriquecido que produce cada transición X/Y, junto a los propietarios U/I y los deltas existentes; después se podrá describir exactamente su contrato de exportación a TPKLifts. La formalización del resto de la estructura discreta del continuo y del tramo K–alfa permanece enlazada al inventario global, no subordinada a estos doce archivos ni excluida por este corte.

**Resultado de la revisión:** existe una cadena formal explícita desde la evaluación APP y la lectura TRIT hasta el emisor, las firmas, sus fibras y la selección de semillas; existen además reconstrucción única, inversas y calendario de L0/L1 con registros declarados. Hacer visibles ambos contratos y su enlace preciso permite reutilizar el trabajo sin reempezarlo, sin saltar de una inversa a un generador y sin atribuir a una formalización parcial el alcance de toda HMT.
