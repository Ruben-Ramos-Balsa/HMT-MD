# Módulo finito y espacio graduado del sector torcido

La verificación integrada de este incremento ha terminado con `PASS_FINITE_MODULE_DELTA`: **17 módulos nuevos, 229 declaraciones públicas y 156 teoremas o lemas**, reutilizando 371 módulos anteriores autenticados. Las consultas de axiomas registran únicamente `Classical.choice`, `Quot.sound` y `propext`. Este resultado corresponde exactamente a las construcciones descritas a continuación.

## Continuidad de la construcción

La cadena conservada es **APP–TRIT–TPK → estado enriquecido → estructura discreta conjunta del continuo → retículo marcado heredado**. La selección regional e incidencial, el cociclo reticular y la realización conforme ya forman parte de los antecedentes. Este incremento trabaja sobre el mismo `Lattice o`, para `o : Fin 12`; no vuelve a seleccionar K ni sustituye el origen por una dimensión objetivo.

El recibo genealógico anterior se conserva íntegro. Sus objetos APP, TRIT, TPK, hojas, orientación, memoria y estructura conjunta siguen siendo el contexto heredado; los grupos, representaciones y operadores de este incremento se registran como **realizaciones posteriores sobre ese retículo**, no como operadores TPK renombrados. La teoría de representaciones y el álgebra tensorial actúan como lenguaje de prueba después de esa construcción, no como selectores de sus estados.

## Construcciones efectivas añadidas

### 1. El factor finito T no se introduce por su dimensión

La acción regular torcida se define con el mismo cociclo triangular del cociente finito ya construido. Se prueba su multiplicatividad y que la involución central actúa por menos la identidad. De esa representación se obtiene un constituyente simple no nulo; su inclusión entrelaza las acciones y conserva el carácter central.

La no degeneración del emparejamiento módulo dos permite calcular el carácter fuera del centro y en el centro. La ortogonalidad de caracteres da después la dimensión **4096** y la unicidad **salvo isomorfismo** de la representación irreducible con ese carácter central. La elección de un constituyente y una base usa elección clásica: el archivo no pretende entregar una tabla canónica de matrices de 4096 por 4096. Sí entrega el espacio, la acción y sus propiedades como objetos formales definidos.

Localizadores:

- `LatticeFiniteRepresentation.lean`: `finiteAction`, `finiteAction_mul`, `finiteAction_center`, `central_involution_negative`.
- `LatticeFiniteIrreducible.lean`: `simple_constituent_exists`, `simpleConstituent`, `inclusion_intertwines`, `finiteFDRep_simple`.
- `LatticeFiniteCharacter.lean`: `character_formula`, `character_pair_sum`.
- `LatticeFiniteDimension.lean`: `irreducible_dimension`, `irreducible_unique`.
- `LatticeFiniteGroundState.lean`: `finiteSpace_dimension`, `finiteSpace_unique`, `latticeOperator_product`, `extensionRepresentation_theta`, `displacement_acts_trivially`.

### 2. El portador tensorial conserva ambas acciones

Se forma `Carrier o = HalfFock o ⊗[ℂ] FiniteSpace o`. El factor de osciladores y el factor finito no se identifican entre sí. Los operadores de carga conservan el cociclo original y conmutan con los osciladores semienteros y con los modos conformes. La inclusión del suelo tiene una retracción explícita y es inyectiva; su dimensión vuelve a ser 4096. El suelo tiene peso 3/2 y es anulado por los modos de aniquilación indicados.

Las relaciones de Heisenberg y de Virasoro se transportan al tensor desde los operadores ya probados, con carga central 24. No se postulan de nuevo esas relaciones.

Localizadores: `LatticeTwistedOscillatorTensor.lean`, `half_heisenberg_tensor`, `virasoro_tensor_central_charge_twentyFour`, `tensor_factors_commute`; `LatticeTwistedCarrier.lean`, `ground_projection_embedding`, `groundSubspace_dimension`, `chargeOperator_product`, `ground_weight`, `virasoro_central_charge_twentyFour`.

### 3. La paridad y los pesos se comprueban sobre la base real

La convención de lift es `liftedTheta = −(fockTheta ⊗ id)`, de modo que el suelo es impar. Se prueban la involución, los proyectores complementarios y la conmutación con los modos conformes y los operadores de carga. Un oscilador aplicado al suelo pertenece al sector positivo.

Para una ocupación finita `a`, el modo conforme cero actúa con peso `(twiceWeight a + 3)/2`, donde `twiceWeight a = Σ (2n+1)a(n,i)`. La paridad del peso doble coincide con la paridad del número de osciladores. Por ello el sector positivo tiene pesos enteros al menos dos. Cada espacio de peso es finito-dimensional y estos espacios generan todo el sector positivo; no se impone un corte máximo de frecuencias.

Localizadores:

- `LatticeTwistedParity.lean`: `liftedTheta_square`, `parity_decomposition`, `liftedTheta_ground`, `liftedTheta_comm_conformal`.
- `LatticeHalfWeightBasis.lean`: `quadratic_zero_monomial`, `shifted_zero_monomial`.
- `LatticeTwistedLowWeights.lean`: `conformal_basis_weight`, `weight_zero_vanishes`, `weight_one_vanishes`.
- `LatticeTwistedGrading.lean`: `weightSpace_eq_eigenspace`, `conformal_eigenspace_finite`, `weights_span`.
- `LatticeTwistedBasisParity.lean`: `positive_basis_iff_odd`, `positive_eigenvalue_integer_ge_two`.
- `LatticeTwistedPositiveSector.lean`: `positiveSector_eq_projector_range`, `positive_virasoro_central_charge_twentyFour`, `positiveSector_nonzero`.
- `LatticeTwistedPositiveGrading.lean`: `positive_weight_finite`, `positive_weights_span`, `positive_eigenvalue_integer_ge_two`.

### 4. Los dos sectores se reúnen como espacio conforme

Se ensambla la suma directa del sector par no torcido y del sector positivo torcido, con la acción conforme componente a componente. Se prueban sobre ese espacio la carga central 24, el vacío, la creación del estado conforme, que el espacio de peso cero es exactamente la recta del vacío y que el espacio de peso uno es nulo.

Localizadores: `LatticeOrbifoldCarrier.lean`, `Space`, `virasoro_central_charge_twentyFour`, `modes_create_conformalState`, `weight_zero_vacuum_line`, `weight_one_zero`.

La graduación se transporta también a toda la suma: cada espacio de peso es finito-dimensional y los pesos naturales generan el portador. `LatticeOrbifoldGrading.lean` reúne estos resultados en `assembled_graded_carrier`; `weightEquiv` identifica cada peso con la suma de los dos pesos correspondientes y `weight_dimension` suma sus dimensiones.

### 5. El primer peso del sector torcido positivo se cuenta desde la base

El peso conforme dos corresponde exactamente a una única excitación de frecuencia 1/2 sobre el factor finito. La equivalencia `firstWeightLabelEquiv` identifica su base con las 24 direcciones oscilatorias multiplicadas por una base del factor finito ya construido. Por tanto, su dimensión es **24 × 4096 = 98.304**, sin introducir esa cifra como hipótesis ni truncar el portador.

Localizadores: `LatticeTwistedWeightTwo.lean`, `twiceWeight_one_iff`, `firstWeightLabelEquiv`, `positive_weight_two_finrank`, `positive_weight_two_dimension_product`. Esta cifra corresponde al sector torcido positivo de peso dos; no se presenta como la dimensión completa del peso dos de la suma ensamblada.

## Alcance de esta entrega

La procedencia de este incremento se clasifica como **CERTIFICADO_NUEVO** de construcciones del desarrollo autoral preexistente. No se atribuye una nueva prioridad al álgebra de representaciones, a los osciladores ni al teorema clásico FLM.

Este incremento construye el factor finito, el tensor, la paridad, sus espacios de peso y el portador conforme ensamblado. La suma directa no define por sí sola los productos de vértice entre sectores. No se afirma aquí la construcción completa del módulo reticular torcido con todos sus campos, del producto orbifold ni la identificación del grupo total de automorfismos con el Monstruo. Estas son operaciones posteriores distintas; no modifican las identidades ya demostradas y conservadas.

## Verificación y conservación

- Corte heredado: 371 módulos; recibo `orbifold_input/orbifold_closed_results/VERIFICATION.json`, SHA `f3fc574feea5f73d2e7234e7386d651af5e81075a368044361b1b65e3634a095`.
- Recibo integrado nuevo: `finite_incremental_results_20260922/VERIFICATION.json`, conservado en la entrega como `recibos/incremento/VERIFICATION.json`.
- SHA del recibo nuevo: `91f99be8104795a9b925ffc0451396d3b6d11cfb8978bc6a9701bff21d28644f`.
- Incremento verificado: 17 módulos, 229 declaraciones públicas y 156 teoremas o lemas. Corte acumulado autenticado: 388 módulos.
- Verificador nuevo: `verify_finite_module.py`; compila exclusivamente el cierre solicitado y consulta todas sus declaraciones públicas. Los antecedentes no se recompilan.
- La entrega conserva una vez los 2311 archivos del paquete anterior, más las fuentes, snapshots, objetos, consultas y recibos de este incremento. El manifiesto final identifica el inventario de entrega.

El FAIL histórico `FAIL_ARRANQUE_HMT: hash divergente: AGENTS.md` permanece registrado literalmente. `CONTINUIDAD_CONTRATO_20260921.json` y su nota documentan la actualización editorial exacta que reproduce en memoria la huella antigua, sin modificar instrucciones ni certificados. Esa conciliación no se convierte en un PASS global ni en evidencia matemática adicional.

`REPRODUCCION.md` indica las órdenes explícitas de comprobación y reproducción. Conectar un USB no ejecuta código automáticamente.
