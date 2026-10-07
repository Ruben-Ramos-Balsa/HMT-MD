# Procedencia focal de CKM y PMNS

Fecha: 2026-09-06. Corte fijo: edición de 2249 páginas, `REVISION_EDITORIAL_HMT_MD_20260905`. Revisión documental y del código, sin ejecutar nuevamente los cálculos, sin modificar originales y sin dictamen global. Estatuto de esta recuperación: **RESULTADO_RECUPERADO**; no se atribuyen novedades matemáticas a la búsqueda.

La disciplina de continuidad y de Ley General de Masas se aplica separando construcción interna, datos de partida explícitos, realización física y comparación. No se convierte una limitación de localización o evaluación en inexistencia matemática, ni la unitariedad en validación física.

## 1. CKM: coeficientes recuperados y alcance de su necesidad

El propietario N42 no se seleccionó por una semejanza textual: el registro sellado identifica su ruta y SHA-256, y el original leído coincide con ese hash. N41 y N43 también quedan identificados por sus hashes en el mismo registro. N42 es cantera histórica fijada por el corte, no una autoridad posterior que lo sustituya. Véase [registro sellado, 408–422][registro].

[N42, 28–53][n42] declara el sexteto de cruce: tétrada de intersección de cardinal 4, umbral Steiner 5, pivote negativo de φ igual a 7, tamaños hexada/octada 6 y 8 y denominador TRIT 3. La fuente sucesora sellada los nombra `(b,p,q,h6,o8,t)=(4,5,7,6,8,3)`.

| Salida | Operación ofrecida | Qué queda fijado previamente |
|---|---|---|
| Fila 12: (2, −5, 28) | (2, −p, bq); 28=4·7 | Dos copias de A, resta del umbral en h, cruce b×q en Δ |
| Fila 23: (0, 7, −25/2) | (0, q, −p²/2) | Exclusión de A directo, pivote en h, semicuadrado bidireccional del cierre pentagonal |
| Fila 13: (1, −20, −2/3) | (1, −pb, −(o8−h6)/t) | Puente eléctrico directo, producto pentágono/complemento débil y reparto trítico de la diferencia 8−6 |
| Fase CP: δ=9A | Multiplicación por 9 | Regla de cierre de la rueda digital |

Localizadores: [N42, 55–94][n42reglas]; [sucesor CKM, 19–68][ckmreglas].

Hallazgo positivo: hay una operación de reconstrucción de cada coeficiente, no sólo una matriz citada sin propietario. El sucesor ofrece una prueba explícita por sustitución de las tres reglas sectoriales. Su teorema dice “Dadas las reglas anteriores y el sexteto”; la aclaración contigua restringe la unicidad a esas reglas y seis invariantes. Esa prueba fija las entradas **una vez declaradas las reglas**. No es una prueba de que el sexteto, por sí solo, fuerce la elección de esas operaciones, signos, multiplicidades 2/0/1 o el divisor 2 frente a todas las reglas alternativas. N42 presenta la regla δ=9A como cierre de rueda; en los cuerpos causales leídos no se desarrolla una selección única de ese funcional angular entre alternativas.

La fuente activa [24_08b, 4–40][transporte] y [10j, 797–844][leyckm] conserva exactamente esa matriz y evalúa

`(θ12,θ23,θ13)^T=M_CKM·(A,C*/6,(180/π_HMT)Δ4)^T; δCP=9A.`

La genealogía de las coordenadas angulares es otra capa: [05_constantes, 127–181][angulares] declara A en grados como 1000·α_HMT; C* procede del lector regional con selector 169, D_A, H5 y recurrencia; Δ4 se publica mediante la expresión en π_HMT y e_HMT allí escrita. La división por 6 y la conversión angular 180/π se aplican después. Este diagnóstico no vuelve a auditar esos generadores, coordinados en la tarea principal.

Las salidas publicadas en [10j, 829–844][leyckm] son:

`(13.003313589509, 2.398056157332, 0.213977382244, 65.676173123554)°`,  
`J=3.1189723326632974×10^-5`.

Se ofrece el falsador lineal `3857δ=9(1528θ12+3380θ23+801θ13)`. La matriz unitaria de mezcla se realiza después mediante las funciones trigonométricas explícitas; transporta el operador down a la base up y no selecciona sus autovalores ([10j, 957–982][leyv]). Invertibilidad, falsador y unitariedad son consecuencias de la matriz/reglas ya fijadas; no prueban por sí solos la necesidad originaria de estas reglas. El capítulo [c41, 73–175][c41] añade reflexión conjugada, métrica e inversa dados M; también advierte que conservar δ=9A bajo reflexión de hoja no equivale a conjugación CP física.

## 2. CKM: historia, ejecutables y acceso a datos externos

**Historia que puede afirmarse.** N41 ya contenía las cuatro fórmulas y su contraste PDG antes de la reconstrucción N42 ([N41, 45–58 y 85–128][n41]). N42 declara que reproduce N41 y cierra indicando que es una reconstrucción formal, sin haber recuperado la cita original perdida ([N42, 25 y 149][n42]). Por tanto:

- La construcción posterior explicita una genealogía aritmética que sustituye la anterior presentación de coeficientes como incógnita del paquete de especies.
- No demuestra retrospectivamente que el protocolo histórico fuera ciego; las fórmulas y el contraste ya estaban presentes.
- Tampoco hay base en estos propietarios para afirmar que los coeficientes CKM se obtuvieron mediante una optimización numérica. “Reconstrucción de fórmula preexistente con reglas declaradas” es más preciso que “ajuste probado”.
- N43 prueba variantes discretas concretas, no una enumeración exhaustiva de reglas ni una distribución estadística de alternativas ([N43, filas 2–9][n43]).

**Código efectivo localizado.** [verificar_md_core.py, 136–199][mdcore] sí evalúa los ángulos y J; no es sólo un control de tokens. Pero recibe en el propio cuerpo `alpha=1/137.035999084`, `C=2.123738338968646`, usa `math.pi/math.e` y escribe los coeficientes CKM literalmente. No carga el sexteto ni calcula sus reglas desde la incidencia. Es un evaluador numérico de la fórmula con esas entradas, no una ejecución material completa APP→TRIT→TPK→incidencia→coeficientes→CKM. Esto no cambia el rol causal que las demostraciones posteriores atribuyen a las constantes HMT: señala el límite de este archivo como certificado de esa genealogía.

En ese mismo programa existe una minimización respecto de un valor externo de impedancia (168–178), pero CKM usa luego el literal 5, no la variable `best_p` (189). No se debe inventar una arista de aquella minimización a los coeficientes CKM.

El ejecutable histórico de OBS-02 preservado como objeto hash [616338…py, 134–139 y 180–208][obs] lee las constantes literales de `build_hmt_obs.py` mediante AST y verifica las mismas fórmulas contra un CSV. Su cabecera limita expresamente el certificado a integridad/asignaciones/evaluación, no derivación de las firmas nominales. Tampoco reemplaza al generador causal del sexteto.

**Entrada externa posterior claramente localizada.** [verificar_ckm_comparacion_pdg_2026.py, 12–40 y 66–115][comparador] carga primero el JSON HMT y su certificado, y en la línea 72 abre el JSON externo. Comprueba valores internos ya fijados y parámetros PDG empaquetados; luego calcula residuos. Su comprobación `used_as_generator_input=False` es una aserción documental, no una reconstrucción histórica del origen de las reglas. El flujo leído no usa los valores PDG para cambiar M o los ángulos. La fuente [08_ckm_cp, 192–263][ckmexterno] separa comparación marginal y covarianza; no autoriza tratar los residuos marginales como observaciones independientes.

Conclusión focal CKM: están recuperados los seis datos, las reglas por canal, la evaluación y el punto del contraste externo. La promoción más fuerte no acreditada por esos cuerpos es **necesidad de las reglas desde las operaciones anteriores, sin darlas ya por fijadas**, junto con una ejecución trazable que consuma las salidas HMT generadas en lugar de literales equivalentes. No se afirma ausencia global de tal propietario.

## 3. PMNS: datos y selectores que sí están construidos

El transporte geométrico inicial no parte de ángulos PMNS. [24_08b, 42–119][marcos] declara el signo dodecafásico, comprime P3 sobre el sector negativo, obtiene tres autovalores positivos simples y construye el marco cargado por proyectores espectrales y normalización. El marco neutro se construye con los tres indicadores hexádicos proyectados y el factor polar `X(X*X)^(-1/2)`, con determinante de Gram `(5−√5)/40>0`.

Se recuperaron propietarios materiales de datos que no figuran como lista completa en ese módulo:

- [02_pantalla_accion, 112–177][p3] da doce representantes A5/C5, el carácter tridimensional y el proyector central `P3=(3/60)Σχ3(g^-1)ρ(g)`; publica K y su vector proyectado no nulo. No es un P3 meramente nominal.
- [capítulo 21, 496–523][hexadas] da B_K={4,6,9,10}, la hexada negativa {4,5,6,7,9,10} y las otras tres hexadas {1,3,4,6,9,10}, {2,4,6,9,10,11}, {4,6,8,9,10,12}. El mismo capítulo, 832–858, distingue el triple positivo no ordenado de su ordenamiento individual.
- [16c, 299–408 y 471–709][selector] conserva el sector superviviente 11→3→1; con B_K y u_K define la energía de orientación sobre diez normalizadores S3, publica máximo único con brecha exacta 1/3 y selecciona después (c*,r*) mediante una puntuación explícita. Reynolds y polar producen el entrelazador de rango 3. La prueba de unicidad está dada bajo ancla, testigos y regla variacional declarados.
- [16c, 733–831][recalibre] explicita la permutación de recalibración y la composición equivariante hacia Witt. Declara que ese cambio de calibre no se postula único. Se conserva así el entrelazamiento interno recuperado; no se reabre como una pieza inexistente.

Estas construcciones son evidencia positiva del portador y de los selectores de incidencia. No identifico automáticamente su marco ordenado con los autovectores numéricos de los dos operadores másicos completos: esa identificación requiere su propio localizador, no sólo igualdad de rango o traza.

La fase mínima de rango uno usa `Q_K=|b_K><b_K|` y `exp(iπ/6)`; inversión de orientación produce conjugación. La fuente publica los ángulos `(19.6807°,56.4970°,29.6224°)` y J=−0.0426621, y declara que ni las 36 permutaciones resuelven el ángulo pequeño. Son valores del **control negativo**, no la predicción física de la construcción posterior ([24_08b, 121–134][negativo]).

## 4. PMNS completo: qué determina los marcos y qué queda sin evaluación localizada

La construcción posterior sustituye ese portador mínimo por los marcos espectrales completos de Mℓ y Mν y publica `U_PMNS=Fℓ*Fν`. Con espectros simples, la unicidad es salvo fases y orden; con degeneración, la salida es una clase doble, no una matriz seleccionada arbitrariamente ([24_08b, 136–170][completo]; [10j, 984–1004][leyfull]).

El propietario de realización explicita `Mν=Pν·𝓜ν·Pν`, análogamente para ℓ, y atribuye los elementos al registro completo. Para el núcleo de registro ofrece una operación concreta: sumar los productos interiores de cinco observables (acarreo, hoja, orientación, vacancia y holonomía), cada uno normalizado por su norma global, omitiendo sumandos nulos; después agrega sobre L_a y N_b y calcula la polar ([realización pública, 624–709][kernel]; [10j, 1006–1033][leykernel]).

La cadena recuperada tiene dos funciones distintas que no deben fundirse: los marcos espectrales construyen U_PMNS; el determinante no nulo de la matriz G0 del registro certifica adicionalmente suficiencia/rango. El texto revisado de 24_08b lo dice explícitamente. 10j, 1027–1028, no afirma certificado el criterio hasta que se exhiban las entradas y el determinante. La realización pública, 707–709, advierte que el criterio de Gram no selecciona por sí solo los marcos.

**Límite numérico documentado:** en los cuerpos y ejecutables pertinentes examinados no se ha localizado una tabla completa de los valores Xi_r(c) enlazada con esas cinco normalizaciones, ni las entradas numéricas completas de Mℓ/Mν y sus marcos espectrales físicos, ni una ejecución efectiva de PMNS completo que produzca los ángulos/J desde esos registros. Sí se localizaron fórmulas operatorias y el criterio exacto. Esta es una limitación de la evidencia evaluable recuperada, no una afirmación de inexistencia matemática del transporte.

Se siguió asimismo la remisión al extractor neutro [11_05a1, 184–275][neutro]: lee por tick torsión en 9, bit bidireccional y corona; forma sumas firmadas, diferencias antipodales, signos y correlación de memoria; publica los coeficientes b120 y bζ de cada historia superviviente. El propio texto separa ese extractor y sus ramas relativas de la escala absoluta y del núcleo PMNS completo. Es una construcción anterior positiva, no una tabla ya evaluada de los marcos PMNS.

La búsqueda de implementación abarcó la fuente activa, las pruebas/datos de la base sellada y los objetos Python de la biblioteca preservada que respondían a PMNS/núcleo/marcos. Se leyeron los propietarios de mezcla y las remisiones anteriores, además del verificador focal del delta de cierres. Los controles documentales y los generadores de tablas de masas no se contaron como cálculo de PMNS. No se amplía esa búsqueda acotada a una conclusión sobre todo archivo histórico del proyecto.

Acceso externo PMNS: en la construcción mínima se abre el contraste después de congelar el portador; su fallo motiva el control negativo. En la construcción de registro se exige congelar parámetros antes de abrir ángulos externos ([24_08b, 157–160][completo]) y se prohíbe forzar invertibilidad con esos ángulos ([10j, 1029–1030][leykernel]). No se localizó en los ejecutables leídos un ajuste PMNS completo a esos datos; tampoco una nueva salida numérica física completa que pudiera compararse.

## 5. Función y significado estructural

Los objetos no cumplen una misma función por compartir números o dimensión. La interpretación siguiente reúne las funciones que los cuerpos anteriores les asignan, sin elevarla a una selección física nueva:

| Objeto | Función estructural documentada | Distinción necesaria |
|---|---|---|
| Sexteto y filas CKM | Traducen datos de cruce e incidencia a pesos de las tres coordenadas angulares; sus filas distinguen tres canales de mezcla | No son las firmas enteras de las rutas de masas ni seleccionan sus autovalores; N42, 126–145 |
| Vector (A,C*/6,Δ) y δ=9A | Publican coordenadas y fase que la realización trigonométrica convierte en transporte entre bases quark | La fase de cierre, la reflexión de hoja y la conjugación CP física tienen operaciones distintas; c41, 135–150 |
| P3, hexadas, testigos y selector variacional | Proporcionan soporte tridimensional, orientación y transporte de incidencia conservando el sector superviviente | Seleccionar el entrelazador con sus reglas no equivale a seleccionar los dos operadores másicos completos; 16c, 657–709 |
| Mℓ/Mν y sus marcos | Los operadores aportan contenido espectral; los marcos ordenan sus direcciones propias; U_PMNS compara los marcos | Mezcla y masa no son el mismo lector; 11_05a1, 168–182, y realización pública, 624–664 |
| K_reg y G0 | Retienen correlaciones entre los observables enriquecidos y permiten comprobar si separan tres direcciones | Es una vía auxiliar de certificado de rango; no convierte el determinante o la polar, por sí solos, en selección de marcos físicos; 10j, 1006–1033 |

## 6. Obligaciones focales que esta evidencia permite formular

1. CKM: conservar la reconstrucción N42 y su unicidad con estructura de partida explícita; para afirmar necesidad más fuerte, localizar la derivación de las reglas sectoriales —incluidos 2/0/1, signos, divisor 2 y δ=9A— desde las operaciones previas, sin introducirlas como reglas dadas.
2. CKM: enlazar el evaluador efectivo con las salidas generadas y el constructor de incidencia; el actual evaluador de literales no acredita ese enlace material.
3. PMNS: conservar el portador P3, las hexadas, los selectores y la recalibración ya construidos. Separarlos de la evidencia numérica específica de Mℓ/Mν, sus marcos y el transporte físico completo.
4. PMNS: para entregar valores físicos calculados, aportar el localizador del registro/operadores y su ejecución numérica; para acreditar además la vía auxiliar G0, exhibir sus entradas y determinante conforme al propio criterio rector. No usar como sustituto los valores descartados de rango uno, el mero rango 3 o un control textual.

## Localizadores materiales

[registro]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/03_CONTROL_ADMISION/PROPIETARIOS_PAQUETE/REGISTRO_CANONICO_HMT.json:408>
[n42]: </Users/ruben/Documents/New project/02_LECTURA/paquetes_descomprimidos/F082_gemma1/gemma1/N42_CKM_coeficientes_cruce_pi.tex:28>
[n42reglas]: </Users/ruben/Documents/New project/02_LECTURA/paquetes_descomprimidos/F082_gemma1/gemma1/N42_CKM_coeficientes_cruce_pi.tex:55>
[n41]: </Users/ruben/Documents/New project/02_LECTURA/paquetes_descomprimidos/F082_gemma1/gemma1/N41_CKM_cruce_canales.tex:45>
[n43]: </Users/ruben/Documents/New project/02_LECTURA/paquetes_descomprimidos/F082_gemma1/gemma1/N43_CKM_stress_variants.csv:2>
[ckmreglas]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/08_ckm_cp.tex:19>
[ckmexterno]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/08_ckm_cp.tex:192>
[angulares]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/ampliacion_20260818/05_constantes_fisicas_genealogia.tex:127>
[c41]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c41_ckm.tex:73>
[transporte]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/24_08b_transporte_ckm_pmns_rev11.tex:4>
[marcos]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/24_08b_transporte_ckm_pmns_rev11.tex:42>
[negativo]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/24_08b_transporte_ckm_pmns_rev11.tex:121>
[completo]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/24_08b_transporte_ckm_pmns_rev11.tex:136>
[leyckm]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_masas/10j_prueba_ley_general_masas_propietario_20260903.tex:797>
[leyv]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_masas/10j_prueba_ley_general_masas_propietario_20260903.tex:957>
[leyfull]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_masas/10j_prueba_ley_general_masas_propietario_20260903.tex:984>
[leykernel]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_masas/10j_prueba_ley_general_masas_propietario_20260903.tex:1006>
[kernel]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_masas/realizacion_equivariante_especies_operadores_masicos_publico.tex:624>
[p3]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/canonical/corredor/02_pantalla_accion.tex:112>
[hexadas]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/capitulo_21_c20_lineas_1_2612.tex:496>
[selector]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/delta_297/16c_entrelazador_dodecafase_witt.tex:471>
[recalibre]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/delta_297/16c_entrelazador_dodecafase_witt.tex:733>
[neutro]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/11_05a1_generaciones_quarks_neutrinos_rev2.tex:184>
[mdcore]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/python/verificar_md_core.py:136>
[comparador]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/python/verificar_ckm_comparacion_pdg_2026.py:66>
[obs]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/00_CORPUS_RECTOR_PRESERVADO/02_BIBLIOTECA_MAESTRA_EXHAUSTIVA/08_EVIDENCIA_EJECUTABLE_COMPLETA/01_PYTHON/OBJETOS/616338388f9560329a4f560a35d4e681ee01ca82f4469ea68be78694fd55076c.py:134>
