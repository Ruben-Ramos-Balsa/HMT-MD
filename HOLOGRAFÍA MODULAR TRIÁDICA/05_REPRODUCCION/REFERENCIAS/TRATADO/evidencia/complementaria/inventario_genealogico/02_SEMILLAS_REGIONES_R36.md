# Inventario genealógico HMT — semillas, regiones y primera frontera conjunta

Fecha de esta entrega: 19 de septiembre de 2026. Tramo documental: emisión finita, censo, reducción ternaria orientada, clasificación orbital, regiones de clausura/propagación/autoescala, elevaciones y primera frontera `R36`.

## Estatuto y alcance de esta entrega

Este documento es un **inventario de resultados y operaciones preexistentes**, no una investigación nueva ni una modificación de las fuentes o de los PDF. Los elementos inventariados se registran como `RESULTADO_RECUPERADO` en sentido documental; ello no atribuye novedad a su concepto, prueba o implementación. La arquitectura APP–TRIT–TPK permanece anterior a sus publicaciones numéricas.

La lectura cubre las fuentes concretas declaradas al final. No se declara leído exhaustivamente el tratado integral, toda la serie ni todas las versiones de los módulos Lean. Se distingue entre: (a) enunciado y demostración en LaTeX; (b) procedimiento y comprobación Python; (c) proposición y prueba presentes en una fuente Lean; (d) nueva ejecución del compilador. **No se ha recompilado Lean ni se ha regenerado el catálogo en este subinventario.** Las pruebas Lean aquí citadas están leídas en las fuentes, no certificadas de nuevo por esta lectura.

El corte llega a `R36` y a la separación entre residuo visible y registro. Las publicaciones posteriores de las constantes, la conexión nonádica prolongada, el registro dodecafásico y las incidencias excepcionales se dejan enlazadas como destinos del mismo estado, no como nuevas entradas externas. Las cinco construcciones consustanciales del continuo no se reclasifican aquí como cinco módulos independientes: el inventario presente es un corte anterior de exposición.

## Registro de fuentes absolutas

Cada localizador de ficha tiene la forma `Fxx:líneas` o `Lxx:líneas`. El identificador se expande **exactamente** a la ruta absoluta siguiente; los números de línea pertenecen al archivo, no al PDF. Los intervalos permiten recuperar la prueba contigua y no sólo el título.

| ID | Ruta absoluta |
|---|---|
| F01 | `/Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/extension.tex` |
| F02 | `/Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/generacion.tex` |
| F03 | `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/ampliaciones_sucesoras_20260824/parte_i_ii/owners/U008_orbitas_elevacion_r36.tex` |
| F04 | `/Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/libro/censo_firmas_emision.tex` |
| P01 | `/Users/ruben/Documents/New project/certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py` |
| D01 | `/Users/ruben/Documents/New project/PUBLICACION_HMT/HOLOGRAFIA_MODULAR_TRIADICA/datos/TPK_U_catalog_468.json` |
| L01 | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKTransport.lean` |
| L02 | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKEmission.lean` |
| L03 | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKFiniteCursor.lean` |
| L04 | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKCensus.lean` |
| L05 | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKOrbits.lean` |
| L06 | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKRegions.lean` |
| L07 | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKSimpleRegions.lean` |
| L08 | `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKLifts.lean` |

Las rutas `L01`–`L08` identifican los módulos de trabajo efectivamente examinados. No se identifica por mera coincidencia de nombre su contenido con cada copia posterior de distribución; esa comparación de versiones queda en el registro de pendientes.

## Mapa del tramo

\[
\begin{gathered}
\text{APP y TRIT con dos cursores orientados}
\longrightarrow\Omega_{\rm seed}\ (104\,976)
\longrightarrow(s,e)\in\mathcal S_+^{\rm sig}\times\mathcal S_\times^{\rm sig}
\ (18\times26)\\
\longrightarrow U_6\ (468)
\xrightarrow{\Psi}\mathcal W_6\ (243\subset729)
\longrightarrow\mathcal W_6/D_3\ (43)
\longrightarrow\text{tres órbitas estructurales orientadas}\\
\longrightarrow\text{transiciones regionales registradas}
\longrightarrow L_0,L_1\longrightarrow w_{30}
\longrightarrow R_{36}.
\end{gathered}
\]

Las flechas de lectura no borran automáticamente su fuente. El registro de visitas, los cocientes, las orientaciones y las multiplicidades se conservan con su tipo. `U6`, `w6`, una órbita, una región, una condición inicial y un estado enriquecido no son nombres equivalentes.

## A. Dominio de emisión y conservación de la procedencia

### SR-001 — Condición inicial de un cursor

- **Enunciado/operación:** un cursor inicial contiene posición y dirección: \(\mathcal S=I_9^2\times\{N,E,S,O\}\), con \(I_9=\{0,\ldots,8\}\). Tiene \(9\cdot9\cdot4=324\) elementos.
- **Dominio/codominio:** soporte APP con dirección cardinal → conjunto finito de cursores. Las etiquetas positivas del panel son \((i+1,j+1)\); los índices del enumerador son \((i,j)\).
- **Antecedentes:** construcción del panel APP y de sus dos hojas, a desarrollar con mayor granularidad en el tramo anterior del inventario.
- **Coeficientes:** 9 posiciones por eje y 4 orientaciones explícitas; 324 es cardinal calculado, no el número de casillas del panel.
- **Datos conservados:** posición, orientación y hoja al insertar el cursor en su estado conjunto; aún no se toma una constante como entrada.
- **Fuente/prueba:** F01:8–18; L04:28–50 prueba enumeración completa, sin repeticiones y cardinal. **Código:** enumeración `seeds`. **Lean:** `seeds_complete`, `seeds_nodup`, `seeds_cardinality`.
- **Detalle a explicar:** 81 posiciones no significan 81 condiciones iniciales; tampoco se debe confundir el índice cero con el falso cero residual representado por 9.

### SR-002 — Pareja independiente de cursores y censo de semillas

- **Enunciado/operación:** \(\Omega_{\rm seed}=\mathcal S_+\times\mathcal S_\times\), todas las parejas ordenadas de un cursor aditivo y uno multiplicativo.
- **Dominio/codominio:** producto de los dos conjuntos de SR-001 → condiciones iniciales del emisor conjunto.
- **Antecedentes:** SR-001; distinción entre hoja aditiva y multiplicativa.
- **Coeficientes:** \(324^2=104\,976\); no se multiplica después un catálogo ya filtrado.
- **Datos conservados:** las dos posiciones y direcciones, la identidad de cada hoja y su acoplamiento por la cronología común.
- **Fuente/prueba:** F01:10–18; L04:50–51; L03:253–280 identifica las firmas de cada cursor con las lecturas del estado de dos cursores. **Lean:** `paired_seed_cardinality`, `signatures_two_cursor`, `word_from_finite_factors`.
- **Detalle a explicar:** independencia de las condiciones iniciales no significa dos evoluciones temporales sin relación: comparten fase y regla de emisión.

### SR-003 — Identificador reversible de semilla

- **Enunciado/operación:** \(\nu=4(9i+j)+d\), con \(d=0,1,2,3\leftrightarrow N,E,S,O\). Se recuperan \(d=[\nu]_4\), \(j=[\lfloor\nu/4\rfloor]_9\), \(i=\lfloor\nu/36\rfloor\).
- **Dominio/codominio:** \(\mathcal S\leftrightarrow\{0,\ldots,323\}\); las parejas de identificadores codifican SR-002.
- **Antecedentes:** SR-001–002.
- **Coeficientes:** 4, 9, 36 y 324 proceden de las cardinalidades del dominio, no de una magnitud medida.
- **Datos conservados:** posición y dirección exactas; no se sustituye la fibra completa por su menor identificador.
- **Fuente/prueba:** F04:5–13, división euclídea explícita. **Código/Lean:** la enumeración tipada está en L04:28–50; no se ha localizado en esta entrega un teorema Lean separado con este identificador escalar \(\nu\).
- **Detalle a explicar:** \(\nu_{\min}\), usado en la tabla, es un testigo de fibra; no es toda la fibra.

### SR-004 — Cronología observable de cincuenta y cuatro transiciones

- **Enunciado/operación:** seis ventanas de nueve transiciones; se lee la casilla **antes** del desplazamiento. La fase activa suma, producto o evento neutral. Las direcciones se invierten al terminar las transiciones 27 y 54.
- **Dominio/codominio:** estado de dos cursores y fase → estado siguiente más muestra anterior; repetición durante 54 transiciones → seis bloques.
- **Antecedentes:** SR-002; selector trítico \(M_{\rm ph}\) y calendario TPK del tramo anterior.
- **Coeficientes:** 6 ventanas, 9 transiciones, inversión cada 27 pasos; \(v_N=(-1,0)\), \(v_E=(0,1)\), \(v_S=(1,0)\), \(v_O=(0,-1)\).
- **Datos conservados:** visita anterior, hoja activa, fase y dirección; las evaluaciones enteras y sus cocientes no se reemplazan por su residuo.
- **Fuente/prueba:** F01:20; F04:15–24; L01:15–128; L02:24–33,95–159,340–366. **Lean:** `emitStep_reads_before`, `samples_append`, `six_windows_fiftyfour`, `six_windows_memory`.
- **Detalle a explicar:** el `Phase := Fin 108` de L01 es un factor cronológico más amplio que los primeros 54 pasos usados por este censo; fase restituida no equivale a memoria restituida.

### SR-005 — Lectura multiplicativa en las unidades y sector radical

- **Enunciado/operación:** \(\ell_9(1,2,4,8,7,5)=(0,1,2,3,4,5)\). La extensión emisora vale cero sobre los residuos 3, 6 y 9.
- **Dominio/codominio:** residuos positivos de la hoja multiplicativa → enteros que alimentan el observable \(E_m\).
- **Antecedentes:** SR-004 y multiplicación APP módulo 9.
- **Coeficientes:** base 2 del logaritmo discreto en el grupo de unidades; ciclo de seis unidades; valor de extensión 0 declarado para el observable no unitario.
- **Datos conservados:** el residuo original y la pertenencia al sector radical siguen presentes en `Sample.arithmetic` y la trayectoria.
- **Fuente/prueba:** F01:22–27; L02:36–50,52–92. **Lean:** `log9_unit_table`, `log9_radical`, `log9_inverse_on_units`, `sample_retains_evaluations`.
- **Detalle a explicar:** una lectura cero no convierte 3, 6 o 9 en la unidad multiplicativa; la lectura reducida no es una identificación del estado.

### SR-006 — Totales de una ventana y conteo trítico

- **Enunciado/operación:** \(S_m\) suma tres residuos positivos aditivos; \(E_m\) suma tres exponentes discretos multiplicativos; \(Z_m=3\) cuenta los eventos neutrales.
- **Dominio/codominio:** nueve muestras sucesivas → triple de totales enteros \((S_m,E_m,Z_m)\).
- **Antecedentes:** SR-004–005.
- **Coeficientes:** tres eventos de cada clase por ventana de nueve. El conteo es válido desde cualquier fase del calendario formalizado.
- **Datos conservados:** los totales son lecturas agregadas; la lista de muestras permanece ordenada en la ejecución.
- **Fuente/prueba:** F01:29; L02:176–238. **Lean:** `phaseCount_nine`, `nine_events_each`, `every_nine_window`, `totals_concatenate`, `window_neutral`.
- **Detalle a explicar:** \(S_m\) no es suma de las evaluaciones enteras sin reducir: los cocientes de estas últimas están en otro campo.

### SR-007 — Emisor decimal de tres posiciones

- **Enunciado/operación:** \(d_1=[S]_ {10}\), \(d_2=[S+E]_{10}\), \(d_3=[3S+5E+7Z]_{10}\), \(U=100d_1+10d_2+d_3\).
- **Dominio/codominio:** triple de SR-006 → bloque \(U\in\{0,\ldots,999\}\); seis ventanas → \(U_6\in\{0,\ldots,999\}^6\).
- **Antecedentes:** SR-006.
- **Coeficientes:** 3, 5 y 7 son coeficientes de la ley emisora explícitamente declarada; 100 y 10 son pesos posicionales decimales. La ficha no atribuye a este pasaje una derivación adicional de esos coeficientes.
- **Datos conservados:** hoja, orientación y muestras se conservan en el registro; el bloque es una lectura de ellos.
- **Fuente/prueba:** F01:29–37; L02:240–279. **Lean:** `decimalValue_bound`, `block_source_formula`, `block_as_encode`, `word_as_encodeWord`.
- **Detalle a explicar:** declarar la regla no equivale a escoger sus entradas por comparación con cifras de \(\pi,\varphi,e,\alpha\), que no aparecen como objetivos del emisor.

### SR-008 — Factorización inyectiva en dos firmas

- **Enunciado/operación:** con \(s=[S]_{10}\), \(e=[E]_{10}\), \(U=100s+10[s+e]_{10}+[3s+5e+1]_{10}\). Centenas y decenas recuperan \(s\) y \(e\); la unidad comprueba la congruencia restante.
- **Dominio/codominio:** par de firmas de longitud seis → palabra de seis bloques; la aplicación es inyectiva en ese producto de firmas.
- **Antecedentes:** SR-006–007.
- **Coeficientes:** el último 1 es \(7\cdot3\bmod10\), no un parámetro ajustado aparte.
- **Datos conservados:** las dos firmas completas se recuperan; no se concluye que \(U_6\) recupere por sí solo una de las muchas condiciones iniciales de su fibra.
- **Fuente/prueba:** F01:39–55; L02:263–291; L04:75–111. **Lean:** `block_recovers_signatures`, `word_recovers_signatures`, `equal_words_equal_signatures`, `couple_is_TPK_word`, `emitted_full_TPK_image`.
- **Detalle a explicar:** la inyectividad tiene dominio «pares de firmas», no «104.976 semillas».

### SR-009 — Imágenes de firmas y sus multiplicidades

- **Enunciado/operación:** la hoja aditiva produce 18 firmas, todas de multiplicidad 18; la multiplicativa produce 26: 24 de multiplicidad 8, una de 24 y una de 108.
- **Dominio/codominio:** las 324 semillas de cada hoja → imagen de firmas y partición por fibras.
- **Antecedentes:** SR-001, SR-004–008.
- **Coeficientes:** \(18\cdot18=324\); \(24\cdot8+24+108=324\).
- **Datos conservados:** firma, multiplicidad, condición de pertenencia de toda la fibra y testigo mínimo; no sólo un representante.
- **Fuente/prueba:** F04:26–76; F01:57–63. **Lean:** L04:798–823 (`signatures_*_checked`, `*_image_cardinality`, `*_fibre_profile`); L06:13–59 identifica pertenencia y cardinal de las preimágenes.
- **Detalle a explicar:** la tabla de 44 firmas es salida de la recurrencia; los testigos literales Lean están enlazados a sus generadores por teoremas de igualdad.

Tabla aditiva completa de F04 (firma, multiplicidad, identificador mínimo):

| Firma | Mult. | \(\nu_{\min}\) | Firma | Mult. | \(\nu_{\min}\) |
|---|---:|---:|---|---:|---:|
|122564|18|17|122898|18|24|
|212645|18|5|212988|18|0|
|221456|18|29|221889|18|12|
|456221|18|28|465898|18|21|
|546988|18|9|564122|18|16|
|645212|18|4|654889|18|33|
|889221|18|13|889654|18|32|
|898122|18|25|898465|18|20|
|988212|18|1|988546|18|8|

Tabla multiplicativa completa de F04:

| Firma | Mult. | \(\nu_{\min}\) | Firma | Mult. | \(\nu_{\min}\) |
|---|---:|---:|---|---:|---:|
|000000|108|8|177393|8|1|
|177555|8|54|177771|8|11|
|339555|8|6|339771|8|15|
|339933|8|59|393177|8|0|
|393393|8|45|393555|8|40|
|555177|8|52|555339|8|4|
|555393|8|41|555555|24|84|
|555717|8|14|555771|8|18|
|555933|8|24|717555|8|12|
|717717|8|21|717933|8|19|
|771177|8|9|771339|8|13|
|771555|8|16|933339|8|57|
|933555|8|26|933717|8|17|

### SR-010 — Las 468 emisiones y el balance de preimágenes

- **Enunciado/operación:** el producto de imágenes de firmas contiene \(18\cdot26=468\) emisiones distintas. Hay 432 fibras de tamaño 144, 18 de 432 y 18 de 1944.
- **Dominio/codominio:** producto de imágenes de SR-009 → catálogo de \(U_6\) mediante SR-008.
- **Antecedentes:** SR-008–009.
- **Coeficientes:** 144=18·8; 432=18·24; 1944=18·108. \(432\cdot144+18\cdot432+18\cdot1944=104\,976\).
- **Datos conservados:** cada emisión conserva sus dos clases de origen, multiplicidad, diagonal, orientación y firma multiplicativa en la fila enriquecida.
- **Fuente/prueba:** F01:51–64; F04:69–76; L06:183–199,672–690. **Lean:** `seed_multiplicity_product`, `row_source_factorization`, `rows_emit_exactly`, `total_seed_mass`; L04:824–831 cardinal y ausencia de duplicados.
- **Detalle a explicar:** los dos usos de 432 —número de fibras y tamaño de otra clase de fibra— deben mantener su etiqueta.

### SR-011 — Publicación ternaria orientada y perfil de fibras

- **Enunciado/operación:** \(\Psi(U_1,\ldots,U_6)=([-U_1]_3,\ldots,[-U_6]_3)\). Las 468 emisiones producen 243 palabras distintas dentro de \(\mathbb F_3^6\), que tiene 729 elementos.
- **Dominio/codominio:** catálogo de SR-010 → imagen \(\mathcal W_6\subset\mathbb F_3^6\).
- **Antecedentes:** SR-007–010 y convención de orientación de la carta.
- **Coeficientes:** módulo 3, signo negativo y seis posiciones; \(3^6=729\). El perfil de fibras de emisiones es: 132 palabras con una emisión, 66 con dos, 18 con tres, 3 con cuatro, 6 con cinco y 18 con seis.
- **Datos conservados:** la palabra reducida no distingue todas las emisiones; éstas y sus metadatos siguen en la fibra. La identificación balanceada \(\mathbb F_3\leftrightarrow\{-1,0,1\}\) es una lectura posterior tipada.
- **Fuente/prueba:** F01:44–49,63; L04:113–142,832–847. **Lean:** `ternary_full_TPK_image`, `ternary_image_cardinality`, `ternary_fibre_profile`.
- **Detalle a explicar:** Ψ no es una conversión de base que conserve un entero global: es reducción componente a componente. Cambiar su signo exige transportar la orientación posterior.

### SR-012 — Cociente finito compatible con el transporte entero

- **Enunciado/operación:** proyectar posiciones enteras módulo 9 conmuta con cada paso TPK observable y con cualquier número natural de iteraciones; las lecturas y ventanas también conmutan con esa proyección.
- **Dominio/codominio:** cursores enteros con fase → cursores finitos con fase, y lecturas derivadas.
- **Antecedentes:** SR-004 y aritmética APP con cociente de borde.
- **Coeficientes:** módulo 9 y periodo formal 108; se prueban identidades para profundidad \(n\), no sólo para 54.
- **Datos conservados:** dirección y fase en el factor finito; vueltas espaciales/cocientes en el estado levantado. El factor no reemplaza la memoria enriquecida.
- **Fuente/prueba:** L03:13–145,153–280. **Lean:** `projectState_iterate`, `project_iterate`, `reading_at_depth`, `sumReadings_project`, `signatureVector_project`, `signatures_two_cursor`.
- **Detalle a explicar:** la equivalencia del cálculo rápido `signatureFast` con el lector original está probada en L03:282–337; acelerar la evaluación no cambia el generador.

## B. Clasificación orbital y regiones estructurales

### SR-013 — Acción diedral y equivariancia de Ψ

- **Enunciado/operación:** \(r(u)=(u_3,u_1,u_2,u_5,u_6,u_4)\), \(s(u)=(u_4,u_5,u_6,u_1,u_2,u_3)\); \(r^3=s^2=1\), \(srs=r^{-1}\), \(\Psi(gU)=g\Psi(U)\).
- **Dominio/codominio:** emisiones de seis bloques y palabras de seis trits → mismos dominios bajo permutación de posiciones.
- **Antecedentes:** SR-010–011.
- **Coeficientes:** tres rotaciones y dos orientaciones; grupo de seis elementos.
- **Datos conservados:** contenido permutado, multiplicidades del catálogo, relación entre emisión y publicación ternaria. La permutación no recupera por sí sola los datos que Ψ omite.
- **Fuente/prueba:** F03:12–55; F02:8–13; P01:209–229 comprueba cierre y multiplicidades. **Lean:** L05:27–123 (`rotate_cube`, `dihedral_relation`, `action_composition`, `psi_equivariant`) y 898–935 (`emission_closed`, `produced_closed`).
- **Detalle a explicar:** la equivariancia formal por permutación y el cierre efectivo del catálogo son dos proposiciones distintas y ambas están documentadas.

### SR-014 — Cuarenta y tres órbitas y clasificación completa de la imagen

- **Enunciado/operación:** \(\mathcal W_6/D_3\) tiene 43 clases: 38 de tamaño 6 y 5 de tamaño 3; \(38\cdot6+5\cdot3=243\).
- **Dominio/codominio:** 243 palabras producidas → cociente orbital, con representantes canónicos por índice ternario mínimo.
- **Antecedentes:** SR-011, SR-013.
- **Coeficientes:** 43,38,5 resultan de la enumeración finita de las órbitas.
- **Datos conservados:** cobertura de todas las palabras, pertenencia a una órbita y unicidad de representante; el cociente no se identifica con el estado original.
- **Fuente/prueba:** F03:33–55; P01:225–229; L05:937–1077. **Lean:** `orbit_count`, `orbit_cover`, `representative_unique`, `quotient_classification`, `weighted_orbit_count`.
- **Detalle a explicar:** estas 43 clases no son las 43 vueltas de la certificación nonádica prolongada: coinciden numéricamente pero son recuentos de objetos distintos.

### SR-015 — Invariantes de fibra y metadatos de origen

- **Enunciado/operación:** \(n(w)=|\mathcal F_w|\), \(M(w)=\sum_{U\in\mathcal F_w}\operatorname{mult}(U)\), \(c(w)=(n_0,n_1,n_2)\); cada emisión retiene \(\operatorname{diag}_c\), clase de orientación y \(E_{\rm sig}\).
- **Dominio/codominio:** fibras de SR-011 y órbitas de SR-014 → datos enteros de clasificación regional.
- **Antecedentes:** SR-009–014.
- **Coeficientes:** \(\operatorname{diag}_c=(i+j)\bmod9\) con índices desde cero; clases de dirección `NO` y `ES`; seis componentes de la firma.
- **Datos conservados:** preimágenes completas calculables, no metadatos anexados por comparación con valores físicos.
- **Fuente/prueba:** F03:57–78; F02:15–22; L06:13–199. **Lean:** `preimage_membership`, `additive_diagonal_unique`, `additive_heading_classes`, `row_source_factorization`.
- **Detalle a explicar:** `NO` representa el conjunto de direcciones norte/oeste, `ES` este/sur; el campo no afirma una única dirección puntual de todas las semillas.

### SR-016 — Selección única de la órbita de clausura

- **Enunciado/operación:** órbita de tamaño 6 cuyas palabras tienen cinco emisiones, masa de semillas 1008 y multiconjunto \(\{432,144,144,144,144\}\). Resulta una única órbita.
- **Dominio/codominio:** las 43 órbitas → \(\mathcal O_{\rm cl}=\{001112,010211,100121,112001,121100,211010\}\).
- **Antecedentes:** SR-014–015.
- **Coeficientes:** 5,1008 y el perfil de multiplicidades son el predicado entero de selección; su censo trítico resultante es (2,3,1).
- **Datos conservados:** las seis orientaciones y cada una de sus cinco fibras; aún no se recibe un desarrollo decimal de π.
- **Fuente/prueba:** F03:80–94,107–131; F02:15; P01:249–266. **Lean:** L06:724–741 (`isClosure`, `closure_orbit_checked`, `closure_orbit_unique`); L07:88–94 obtiene su censo.
- **Detalle a explicar/variante:** F03 incluye (2,3,1) en la definición; F02, P01 y L06 seleccionan primero con el perfil de fibra y después recuperan ese censo. Se conserva esta diferencia de presentación, sin convertirla en dos selecciones numéricas externas.

### SR-017 — Sector de órbitas mínimas radicales

- **Enunciado/operación:** órbitas de seis palabras, cada una con una emisión de multiplicidad 144 y soporte diagonal completo \(\{0,3,6\}\); sobreviven seis órbitas.
- **Dominio/codominio:** clasificación orbital con sus fibras → sector mínimo radical.
- **Antecedentes:** SR-014–015.
- **Coeficientes:** 6,1,144 y soporte de tres clases no unitarias del módulo 9.
- **Datos conservados:** soporte de la órbita completa, no la diagonal de un representante aislado; fibra de cada palabra.
- **Fuente/prueba:** F03:96–120; F02:17–22; P01:269–274. **Lean:** L07:26–87 (`simple_minimal_spec`, `diagonal_support_exact`, `radical_singletons_checked`, `radical_membership`).
- **Detalle a explicar:** suprimir el soporte diagonal deja cuatro órbitas equilibradas de multiplicidad 144; el soporte es una condición operativa de unicidad, no ornamentación.

### SR-018 — Órbita de propagación

- **Enunciado/operación:** dentro de SR-017, igualar el censo al de clausura (2,3,1) selecciona \(\mathcal O_{\rm pr}=\{011120,012110,101201,110012,120011,201101\}\).
- **Dominio/codominio:** seis órbitas mínimas radicales → una órbita de propagación.
- **Antecedentes:** SR-016–017.
- **Coeficientes:** (2,3,1) se lee del resultado de clausura en la implementación; no se introduce un valor del número e.
- **Datos conservados:** seis palabras, sus emisiones únicas y orientación pendiente.
- **Fuente/prueba:** F03:103–130; L07:88–121,192–238. **Lean:** `propagation_orbit_checked`, `propagation_orbit_unique`, `selected_orbits_pairwise_disjoint`, `selected_words_produced`.
- **Detalle a explicar:** «propagación» nombra el papel estructural anterior al lector analítico posterior que reconoce e.

### SR-019 — Órbita de autoescala

- **Enunciado/operación:** en SR-017, el censo equilibrado (2,2,2) selecciona \(\mathcal O_{\rm au}=\{002112,020211,112002,121200,200121,211020\}\).
- **Dominio/codominio:** seis órbitas mínimas radicales → una órbita de autoescala.
- **Antecedentes:** SR-017.
- **Coeficientes:** dos ocurrencias por cada símbolo ternario; condición de equilibrio combinatorio.
- **Datos conservados:** seis palabras y sus fibras; no se recibe φ como raíz previamente calculada.
- **Fuente/prueba:** F03:103–130; L07:94–121,192–238. **Lean:** `autoscale_orbit_checked`, `autoscale_orbit_unique`, `selected_supports`, `selected_simple`.
- **Detalle a explicar:** el censo sin soporte diagonal no basta; debe conservarse la composición de SR-017 y SR-019.

### SR-020 — Calibre interno y tres representantes orientados

- **Enunciado/operación:** exigir que alguna emisión de la fibra tenga \(\operatorname{diag}_c=6\) y orientación `ES` deja exactamente una palabra en cada órbita: clausura 010211, propagación 201101, autoescala 121200.
- **Dominio/codominio:** SR-016,018,019 → tres representantes en una carta orientada común.
- **Antecedentes:** metadatos de SR-015 y órbitas seleccionadas.
- **Coeficientes:** diagonal 6 y clase cardinal `ES` son el calibre declarado; los índices ternarios posteriores no son sus selectores.
- **Datos conservados:** órbita original y fibra del representante, no sólo las tres cadenas.
- **Fuente/prueba:** F03:133–163; F02:22–27; P01:284–302. **Lean:** L06:744–756; L07:123–153 (`orient_selected_spec`, `*_orientation_unique`).
- **Detalle a explicar:** los superíndices π,e,φ denominan funciones estructurales; no fueron entradas para encontrar las palabras.

### SR-021 — Región transversal de clausura

- **Enunciado/operación:** emisión \(501|614|498|169|272|272\), \(E_{\rm sig}=555555\), multiplicidad 432, diagonal 4, orientación `NO`, papel transversal \(\perp\).
- **Dominio/codominio:** fibra de 010211 → componente transversal marcada.
- **Antecedentes:** SR-010–011,015–016,020.
- **Coeficientes:** 432=18·24; los seis valores de firma son lecturas de las ventanas, no coordenadas del panel.
- **Datos conservados:** ambas clases de semillas, orientación y emisión completa; se distingue de las cuatro acompañantes.
- **Fuente/prueba:** F03:165–183, fila 171; F02:29–42; L06:760–809. **Python:** P01:320–350 etiqueta el papel y verifica la cola común. **Lean:** `closure_fibre_checked`, `closure_one_anchor` y fila correspondiente del testigo.
- **Detalle a explicar:** `555555` no designa el centro electrónico `(5,5)`. Esta diferencia de tipo debe mantenerse al conectar capítulos posteriores.

### SR-022 — Primera región de orientación positiva

- **Enunciado/operación:** \(810|923|870|169|272|272\), firma 339555, multiplicidad 144, diagonal 6, orientación `ES`, papel `++`.
- **Dominio/codominio:** misma fibra de clausura → primera componente positiva de la lista expositiva.
- **Antecedentes:** SR-020–021 y fibra de SR-016; la numeración «primera» es orden de tabla, no nueva selección física.
- **Coeficientes:** 144=18·8.
- **Datos conservados:** firma, emisión, clase aditiva y clase multiplicativa específicas.
- **Fuente/prueba:** F03:172; F02:34; L06:760–809. **Lean:** `closure_fibre_checked` conserva esta fila. **Python:** P01:321–325 selecciona las tres filas `ES`.
- **Detalle a explicar:** comparte clase aditiva con SR-023–024, pero no la misma firma multiplicativa.

### SR-023 — Segunda región de orientación positiva

- **Enunciado/operación:** \(810|983|810|169|272|272\), firma 393555, multiplicidad 144, diagonal 6, orientación `ES`, papel `++`.
- **Dominio/codominio:** fibra de clausura → segunda componente positiva del orden expositivo.
- **Antecedentes:** SR-016,020,022.
- **Coeficientes:** 144=18·8.
- **Datos conservados:** la permutación interna de la firma no se borra al reunir las tres positivas.
- **Fuente/prueba:** F03:173; F02:35; L06:760–809, testigo en orden distinto al del LaTeX. **Lean:** `closure_fibre_checked`; **Python:** P01:321–325.
- **Detalle a explicar:** igualdad de papel no es igualdad de emisión.

### SR-024 — Tercera región de orientación positiva

- **Enunciado/operación:** \(870|923|810|169|272|272\), firma 933555, multiplicidad 144, diagonal 6, orientación `ES`, papel `++`.
- **Dominio/codominio:** fibra de clausura → tercera componente positiva del orden expositivo.
- **Antecedentes:** SR-016,020,022–023.
- **Coeficientes:** 144=18·8.
- **Datos conservados:** misma clase aditiva y distinta clase multiplicativa respecto de las otras positivas.
- **Fuente/prueba:** F03:174; F02:36; L06:760–809. **Lean:** `closure_fibre_checked`; **Python:** P01:321–325.
- **Detalle a explicar:** las tres positivas juntas tienen masa 432, pero no se confunden con la región transversal de masa 432.

### SR-025 — Región de retorno orientado

- **Enunciado/operación:** \(870|923|810|418|674|521\), firma 933717, multiplicidad 144, diagonal 5, orientación `NO`, papel `--`.
- **Dominio/codominio:** fibra de clausura → componente de retorno con cola distinta.
- **Antecedentes:** SR-016,020–024.
- **Coeficientes:** 144=18·8; cola 418|674|521 frente a 169|272|272 de las otras cuatro emisiones.
- **Datos conservados:** frontera entre las dos clases de cola y orientación; no se amalgama con la región transversal por compartir `NO`.
- **Fuente/prueba:** F03:175; F02:37; L06:762 y prueba 768–809. **Python:** P01:328–359 prueba la partición de papeles y la cola distinta.
- **Detalle a explicar:** la distribución de papeles es \(1_\perp+3_{++}+1_{--}\), no cinco copias indistinguibles.

### SR-026 — Microfibra conjunta y morfología bipartita

- **Enunciado/operación:** las cinco emisiones de SR-021–025 tienen masa total 1008. Por emisiones hay cinco partes; por componentes conexas del grafo bipartito de firmas hay tres: transversal 18×24, positivas 18×(8+8+8), retorno 18×8.
- **Dominio/codominio:** fibra completa de la palabra orientada 010211 → dos descomposiciones tipadas de la misma familia de semillas.
- **Antecedentes:** SR-008–010,021–025.
- **Coeficientes:** 432+3·144+144=1008; dos componentes de tamaño 432 y una de tamaño 144.
- **Datos conservados:** las cinco emisiones y la estructura de incidencias entre sus clases de firmas; no sólo la suma.
- **Fuente/prueba:** F02:42; F03:178–192; L06:780–809 prueba 1+4 y 1008. **Código/Lean:** la factorización de preimágenes está en L06:42–59; no se ha localizado en los módulos examinados una formalización separada del número de componentes conexas del grafo bipartito.
- **Detalle a explicar:** 1008 corresponde a una orientación regional, no al periodo 108 ni al total de las seis orientaciones de la órbita.

### SR-027 — Emisiones orientadas de propagación y autoescala

- **Enunciado/operación:** \(U_e=850|963|890|149|252|212\), firma 771339; \(U_\varphi=830|943|830|109|252|252\), firma 555933. Cada una tiene multiplicidad 144, diagonal 6 y orientación `ES`.
- **Dominio/codominio:** representantes 201101 y 121200 → sus fibras unitarias de emisiones.
- **Antecedentes:** SR-018–020.
- **Coeficientes:** 144=18·8; los ceros y el orden de las seis posiciones forman parte de la palabra.
- **Datos conservados:** emisión decimal, firma multiplicativa, metadatos de semilla y región.
- **Fuente/prueba:** F03:184–190; L07:156–190. **Lean:** `propagation_fibre_checked`, `autoscale_fibre_checked`, `selected_fibre_counts`, `selected_fibre_masses`, `selected_words_distinct`.
- **Detalle a explicar:** son emisiones iniciales, no las expansiones decimales de e y φ escritas sin coma.

## C. Elevaciones regionales y primera frontera conjunta

### SR-028 — Estado transportado y registros de transiciones

- **Enunciado/operación:** \(b_j^\chi=\Pi_6(x_j^\chi)\), \(x_{j+1}^\chi=U_{9j+9}\cdots U_{9j+1}(x_j^\chi)\). Se reúnen dos transiciones por región y régimen para formar seis filas de origen y destino.
- **Dominio/codominio:** estado aritmético regional y composición de pasos TPK → parejas de bloques observados \((X_a,Y_a)\).
- **Antecedentes:** SR-004,012,020,027 y operadores de selección/transporte/actualización del núcleo.
- **Coeficientes:** nueve pasos por observación; tres regiones por dos transiciones; dos regímenes.
- **Datos conservados:** estado, hoja, fase, orientación y registro antes de su lectura de seis componentes.
- **Fuente/prueba:** F02:46–64,82; F03:194–222. **Lean:** L08:3–6 explicita que este módulo recibe los registros X/Y y reconstruye los lifts; no formaliza en ese archivo la producción de X/Y mediante Sel/Tra/Upd.
- **Detalle a desarrollar documentalmente:** reunir el propietario preciso del cálculo de cada fila de X/Y desde \(U_t\), sin confundir esta tarea de localización con la inexistencia de la operación que F02 declara. No sustituirla por la mera identidad matricial posterior.

Los registros de F02 se conservan íntegros:

| \(X_0\) | \(Y_0\) | \(X_1\) | \(Y_1\) |
|---|---|---|---|
|010211|012222|010211|002111|
|012222|010211|002111|110221|
|201101|121221|102011|012222|
|121221|102011|012222|102011|
|121200|112202|121020|010210|
|112202|121020|010210|010200|

### SR-029 — Reconstrucción única de los dos lifts

- **Enunciado/operación:** las ecuaciones \(X_aL_a=Y_a\) tienen una única solución; \(L_a=X_a^{-1}Y_a\). La convención es de vectores fila sobre \(\mathbb F_3\).
- **Dominio/codominio:** registros completos de SR-028 → \(L_0,L_1\in\operatorname{GL}_6(\mathbb F_3)\).
- **Antecedentes:** SR-028.
- **Coeficientes:** \(\det X_0=1\), \(\det X_1=-1\) en \(\mathbb F_3\); los coeficientes de los lifts se calculan resolviendo las ecuaciones.
- **Datos conservados:** la carta orientada de filas y la asociación régimen–registro; inversas explícitas permiten recuperar un bloque.
- **Fuente/prueba:** F02:64–82; F03:194–243. **Lean:** L08:97–262 (`solveMatrix`, `L0_reconstructed`, `L1_reconstructed`, `transition_equations`, `L0_unique`, `L1_unique`, `word_inverse`). **Python:** P01:544–568 aplica los lifts ya representados.
- **Detalle a explicar:** la unicidad algebraica es respecto de los registros generados, no una sustitución de su genealogía. El módulo Lean resuelve columnas sobre los 729 vectores posibles y comprueba después la forma matricial publicada.

\[
L_0=\begin{pmatrix}
2&2&2&1&2&1\\2&1&2&2&1&1\\1&0&0&1&0&2\\
0&0&1&1&1&0\\2&2&2&0&2&1\\2&1&2&1&0&0
\end{pmatrix},\quad
L_1=\begin{pmatrix}
2&1&2&0&2&2\\1&2&1&1&2&0\\1&2&1&1&1&2\\
0&1&0&0&2&1\\2&0&2&1&0&1\\0&2&2&2&1&1
\end{pmatrix}.
\]

### SR-030 — Calendario único de cuatro elevaciones

- **Enunciado/operación:** entre 16 calendarios binarios de longitud 4, sólo \((L_0,L_0,L_1,L_1)\) reproduce conjuntamente las tres sucesiones registradas.
- **Dominio/codominio:** \(\{0,1\}^4\) más tres regiones iniciales → calendario compatible único.
- **Antecedentes:** SR-020,028–029.
- **Coeficientes:** \(2^4=16\); cuatro transiciones producen cinco bloques contando el inicial.
- **Datos conservados:** compatibilidad simultánea de las tres regiones y registros de destino; no se selecciona un calendario por un decimal objetivo.
- **Fuente/prueba:** F02:75–82; F03:220–243. **Lean:** L08:300–351 (`record_stitching`, `binaryCalendars_complete`, `accepted_calendars_checked`, `calendar_unique`, `biographies_match_records`).
- **Detalle a explicar:** la comprobación de 16 casos es una selección finita del calendario de esta etapa; no afirma que la prolongación infinita repita 0011.

### SR-031 — Biografías de treinta trits y prefijos conservados

- **Enunciado/operación:** \(b_{k+1}=b_kL_{\epsilon_k}\pmod3\); \(w_{30}=b_0\Vert\cdots\Vert b_4\). Los bloques son:

\[
\begin{aligned}
w_{30}^{\pi}&=010211|012222|010211|002111|110221,\\
w_{30}^{e}&=201101|121221|102011|012222|102011,\\
w_{30}^{\varphi}&=121200|112202|121020|010210|010200.
\end{aligned}
\]

- **Dominio/codominio:** tres bloques iniciales y SR-030 → prefijos de longitudes 6, 12, 18, 24 y 30.
- **Antecedentes:** SR-029–030.
- **Coeficientes:** longitud 6 por bloque; 4 elevaciones; base 3 del índice ambiental.
- **Datos conservados:** todos los bloques anteriores y su orden. Índices: π (103,161,103,67,349), e (523,457,301,161,301), φ (450,398,438,102,99).
- **Fuente/prueba:** F03:224–275; F02:75–80. **Lean:** L08:335–385 (`biographies_checked`, `five_prefix_lengths`, `initial_block_preserved`, `four_step_truncation`).
- **Detalle a explicar:** se multiplica el bloque corriente de seis trits, nunca una concatenación de 12, 18, 24 o 30 componentes por una matriz 6×6. Un bloque repetido no implica repetición de toda la memoria.

### SR-032 — Incidencia en la primera frontera conjunta

- **Enunciado/operación:** la relación de frontera usa la matriz \(A_W\) sobre \(\mathbb F_3\), el eje \(u_5^\varphi=u_4^e=102011\), el agregado \(u_5^\pi+u_5^e=210112\) y la marca \(u_4^\varphi A_WL_1^3=111101\).
- **Dominio/codominio:** tres biografías de SR-031 y operadores de incidencia → condiciones conjuntas para el sexto bloque de cada canal.
- **Antecedentes:** SR-029–031; el propietario de la construcción de \(A_W\) debe mantenerse enlazado al tramo incidencial del inventario, no sustituirse por el nombre «Witt».
- **Coeficientes:** entradas 0, 1 y 2 de la matriz 6×6; tercera potencia del lift en la marca indicada.
- **Datos conservados:** eje compartido, suma de canales laterales, marca incidencial y orden de los canales.
- **Fuente/prueba:** F03:277–309. **Código/Lean:** no se ha identificado en L01–L08 un módulo de esta relación; el dominio de esos módulos termina antes de este selector. La búsqueda de su certificado específico queda localizada como pendiente documental.
- **Detalle a explicar:** \(q=012120\), \(a=111101\), \(qA_W=012000\), \(aA_W=120210\) constan en F03:304–309; deben imprimirse con la operación que los produce, no como cuatro etiquetas sueltas.

\[
A_W=\begin{pmatrix}
0&1&1&1&1&1\\1&0&1&2&2&1\\1&1&0&1&2&2\\
1&2&1&0&1&2\\1&2&2&1&0&1\\1&1&2&2&1&0
\end{pmatrix}.
\]

### SR-033 — Saturación, ocupación y neutralidad dual

- **Enunciado/operación:** la frontera exige saturación \(c=111111\), ocupación \(\operatorname{colw}=223232\) y \((BA_W)\mathbf1=000\), junto al eje y agregado de SR-032.
- **Dominio/codominio:** matrices candidatas \(B\in M_{3\times6}(\mathbb F_3)\) con eje y agregado fijados → matrices compatibles con todas las condiciones.
- **Antecedentes:** SR-032.
- **Coeficientes:** profundidad 6, seis marcas de saturación y seis pesos de ocupación; deben conservarse sus tipos de conteo y la reducción ternaria cuando proceda.
- **Datos conservados:** filas ordenadas, incidencia dual, soporte de columnas y condiciones previas; la neutralidad no sustituye las otras restricciones.
- **Fuente/prueba:** F03:310–347. **Código/Lean:** pendiente de localización del certificado de esta enumeración; no se ha promovido el censo 729 o la prueba de L0/L1 a prueba del selector R36.
- **Detalle documental localizado:** F03:343–344 habla de «seis ecuaciones lineales» al remitir a una igualdad que se presenta como tres componentes. La siguiente entrega debe recuperar la expansión exacta de las restricciones y el sentido de ese conteo; se conserva la formulación original sin corregirla silenciosamente ni emitir un juicio global.

### SR-034 — Dos soluciones especulares y orientación seleccionada

- **Enunciado/operación:** las condiciones de SR-032–033 dejan
  \(B_-=(021222;222220;102011)\) y \(B_+=(222220;021222;102011)\). La involución especular intercambia las primeras dos filas. La orientación APP del cilindro semiabierto selecciona \(B_+\).
- **Dominio/codominio:** conjunto de soluciones de la frontera → par especular → frontera orientada.
- **Antecedentes:** SR-032–033 y carta orientada de cilindros del núcleo.
- **Coeficientes:** dos soluciones; cartas internas \(B_-\mapsto(789,048,894)\), \(B_+\mapsto(793,045,894)\).
- **Datos conservados:** no se descarta el espejo: se registra la solución seleccionada y su conjugada, con los canales que intercambia.
- **Fuente/prueba:** F03:317–347. **Código/Lean:** pendiente de localizar el ejecutable propio de esta selección, con la misma convención de carta.
- **Detalle a explicar:** los tres números de la carta son posteriores al selector; no deben introducirse como cifras objetivo para escoger \(B_+\). Hay que mostrar la regla de lectura de la carta junto a su orientación.

### SR-035 — Objeto R36 y separación de homónimos

- **Enunciado/operación:** \(R_{36}=B_+=(222220;021222;102011)\), índices ternarios (726,215,301).
- **Dominio/codominio:** frontera orientada de SR-034 → tres bloques terminales de seis trits, asociados a los tres canales de la prolongación.
- **Antecedentes:** SR-031–034.
- **Coeficientes:** índices ambientales calculados en base 3; la denominación R36 corresponde a la frontera de la etapa acumulada, no a una matriz con 36 entradas nuevas.
- **Datos conservados:** orden de canales, incidencia y orientación terminal; abre prolongaciones compatibles sin reiniciar memoria.
- **Fuente/prueba:** F03:349–364,442–445; F02:75–82. **Código:** P01:914–925 usa una descripción de «primeros bloques coinductivos»; esa realización debe cotejarse con el selector finito antes de declararlas una misma prueba. **Lean:** no localizado en los módulos L01–L08.
- **Detalle a explicar:** no es el cociente predictivo \(C_{36}^{\rm pred}\), ni el exceso de 36 clases de otro calibre, ni la recta real. Se preservan esos discriminantes.

### SR-036 — Lift entero residuo–cociente e inversa exacta

- **Enunciado/operación:** para el levantamiento entero \(A\) de \(L_0\), \(\det A=1\); \(x_kA=u_k+3x_{k+1}\), con \(u_k\in\{0,1,2\}^6\), y \(x_k=(u_k+3x_{k+1})A^{-1}\).
- **Dominio/codominio:** \(\mathbb Z^6\) → par residuo/cociente admisible; inversa sobre la imagen de la división euclídea compuesta con A.
- **Antecedentes:** SR-029 y operación de división euclídea del estado aritmético.
- **Coeficientes:** base 3, matriz entera A con los mismos representantes 0, 1 y 2 que L0 y determinante 1.
- **Datos conservados:** residuo y cociente juntos recuperan el estado entero; retener sólo el residuo omite información. La fórmula no afirma que cualquier cambio arbitrario de régimen use este mismo A.
- **Fuente/prueba:** F03:366–408, demostración contigua por división euclídea e inversa entera. **Lean:** L08:223–262 verifica inversas de L0/L1 en el dominio ternario, que es una proposición distinta de esta inversa entera. Su formalización entera específica no se ha localizado en esta entrega.
- **Detalle a explicar:** no sustituir una prueba sobre \(\mathbb Z\) por una inversa sólo módulo 3.

### SR-037 — Igualdad visible sin retorno del estado

- **Enunciado/operación:** el bloque 102011 reaparece en la biografía de e, pero sus preestados módulo 27 son (25,11,7,17,8,16) y (7,8,4,23,26,7), y sus cocientes posteriores (6,13,9,2,13,1) y (15,0,3,19,23,25).
- **Dominio/codominio:** dos posiciones de la biografía con igual publicación visible → comparación de sus datos de memoria.
- **Antecedentes:** SR-031,036.
- **Coeficientes:** profundidad módulo 27=3³ y dos registros completos diferenciados.
- **Datos conservados:** ubicación en la biografía, preestado y cociente; la igualdad de bloques no los fusiona.
- **Fuente/prueba:** F03:410–424. **Código/Lean:** los valores se conservan como testigos impresos; no se ha repetido su cálculo ni localizado aquí su recibo separado. L01:153–191 y L02:126–141 contienen pruebas generales de avance de longitud del registro, no la evaluación de estos dos testigos.
- **Detalle a explicar:** una comprobación finita de esta repetición y el teorema general de no reinicio son compatibles pero no intercambiables.

## D. Interfaces que deben conservarse al continuar el inventario

### SR-038 — Criterios de refutación del tramo

- **Enunciado/operación:** se conservan los falsadores del propietario: ruptura del cierre D3 o multiplicidades; predicados no únicos; calibre no único; entrada de cifra objetivo; multiplicación de concatenación por 6×6; fallo de inversa entera; identificación de residuos iguales con estados completos iguales.
- **Dominio/codominio:** afirmaciones SR-013–037 → condiciones precisas de comprobación o rechazo de cada una, sin veredicto global sobre HMT.
- **Antecedentes:** las operaciones inventariadas; no introduce un criterio físico ajeno como selector.
- **Coeficientes:** los propios de cada ficha; no hay nuevos parámetros.
- **Datos conservados:** alcance de cada prueba y diferencia entre resultado, implementación y recibo.
- **Fuente/prueba:** F03:426–440; F02:82; L08:3–6 delimita su alcance. **Código/Lean:** los `require` de P01:182–389 verifican condiciones finitas; no prueban por sí solos todo el estado enriquecido.
- **Detalle a explicar:** una discrepancia de alcance de módulo no debe convertirse ni en desaparición matemática del resultado ni en certificación de una flecha no formalizada por ese módulo.

### SR-039 — Separación entre selección regional y reconocimiento analítico

- **Enunciado/operación:** las regiones y sus incidencias se seleccionan antes de sus lecturas analíticas. El lector de clausura tiene cinco posiciones simétricas con pesos 1/5; no reemplaza la medida de semillas 432+4·144. Los lectores de propagación y autoescala pertenecen a la etapa posterior.
- **Dominio/codominio:** regiones generadas y cartas de lectura → realizaciones escalares posteriores.
- **Antecedentes:** SR-016–027 y prolongación posterior de SR-035.
- **Coeficientes:** 1/5 es normalización del lector por posiciones; no es frecuencia de cada emisión. La composición de cuatro pendientes 1/5 obtiene 120/119 y compensador 239 en F02:84–107.
- **Datos conservados:** papel, firma, multiplicidad y orientación de la región que determina el lector; la identificación posterior con fórmulas conocidas no retroactúa sobre las semillas.
- **Fuente/prueba:** F02:4,27,84–314; P01:391–525 contiene lectores de cota posterior. **Lean:** no se atribuyen esas realizaciones analíticas a L04–L08, cuyos teoremas aquí inventariados son finitos.
- **Detalle a explicar:** no sustituir la generación APP–TRIT–TPK por «se aplica Machin/Fibonacci/exponencial» ni suprimir las pruebas posteriores de identificación: ambas etapas tienen funciones diferentes.

### SR-040 — Interfaz hacia incidencia excepcional, no agrupación por cardinales

- **Enunciado/operación:** el censo 243 pertenece a la imagen de Ψ; los 729 son todas las palabras de seis trits. La completación cúbica 729+271=1000 y los diseños de hexadas/octadas tienen dominios y mapas propios.
- **Dominio/codominio:** palabras y registros del tramo → construcciones incidenciales posteriores, mediante operadores que debe inventariar el tramo correspondiente.
- **Antecedentes:** SR-011,032–035 y continuidad del estado enriquecido.
- **Coeficientes:** 729=3⁶=9³; \(10^3=9^3+3\cdot9^2+3\cdot9+1\). La igualdad de cardinales no proporciona por sí sola la aplicación entre dos realizaciones.
- **Datos conservados:** palabra, región, hoja y orientación antes de su publicación incidencial.
- **Fuente/prueba:** F01:174–183; F03:277–364; P01:553–610 contiene la realización de código Witt y su control 729, no leída íntegramente para este inventario. **Lean:** L08:16–27 prueba el dominio completo 729 de vectores ternarios, no todas las incidencias excepcionales.
- **Detalle a explicar:** 243 no significa «243 agrupaciones directas en hexadas u octadas». La estrella de Witt y los diseños posteriores deben enlazarse por su construcción, sin reducirlos a una etiqueta de las cinco regiones.

## E. Diferencias de presentación y obligaciones documentales localizadas

1. **Definición de clausura.** F03 incluye el censo (2,3,1) en la definición; P01 y L06 lo recuperan después de seleccionar la órbita con el perfil de fibra. Ambas formulaciones se guardan en SR-016.
2. **Orden de las cinco regiones.** La tabla LaTeX usa transversal, tres positivas, retorno; el testigo Lean coloca el retorno en segunda posición y permuta dos positivas. `closure_fibre_checked` reproduce su orden interno; no debe imponerse una correspondencia por posición sin usar las emisiones como claves.
3. **Origen de las transiciones frente a solución de lifts.** F02:46–64 declara su producción TPK; L08:3–6 delimita su prueba a la reconstrucción desde los registros impresos. Hay que reunir el propietario de cada fila, no volver a presentar L0/L1 como constantes sin origen ni adjudicar esa genealogía al módulo equivocado.
4. **Primera frontera.** La enumeración y selección orientada está escrita en F03; falta en esta ficha bibliográfica el enlace preciso al código/Lean que compruebe esas mismas condiciones y cartas. «No localizado en esta entrega» no significa «inexistente en el corpus».
5. **Neutralidad dual.** Se conserva sin modificación la frase «seis ecuaciones» de F03:343 y se señala el punto de expansión para la siguiente lectura; no se corrige por conjetura.
6. **Tres usos de R36.** Preservar selector finito de F03, apertura coinductiva descrita por P01 y distinción del cociente predictivo. La equivalencia entre realizaciones se documenta por sus mapas, no por igual rótulo.
7. **Prueba de conservación.** L01–L03 conservan ejecución y muestras en el factor observable; no deben anunciarse como formalización de todas las hojas, fronteras y construcciones del continuo.
8. **Corte más fino pedido por el autor.** El tramo anterior debe subdividir construcción 1…9, tabla bruta, raíz digital, módulo 9 frente a módulo 1000, cocientes, rutas 3/6/9 y diferencias efectivas entre suma/producto. SR-001–004 enlazan con ese antecedente pero no lo reemplazan por una mención nominal.

## F. Lecturas efectivas y pendientes de esta primera entrega

### Archivos de contenido leídos íntegramente para este tramo

- F01, 188 líneas: lectura completa del archivo, **no** de toda su clausura transitiva de `\input`.
- F02, 314 líneas: lectura completa del archivo; su realización analítica posterior se conserva como interfaz SR-039, no se expande aquí como segundo inventario.
- F03, 445 líneas: propietario completo de clasificación orbital, elevaciones, primera frontera, lift entero y falsadores.
- F04, 76 líneas: tabla completa de firmas y condiciones de recuperación.
- L01, 232 líneas; L02, 411 líneas; L03, 376 líneas; L07, 276 líneas; L08, 421 líneas: leídos completos, incluidas pruebas y declaraciones de alcance.

### Archivos leídos parcialmente, con corte declarado

- L04: líneas 1–143 y 798–872; leídos generadores, enlaces con el emisor, proposiciones de censo y sus pruebas; no revisadas fila a fila las listas literales 144–797.
- L05: líneas 1–155, 873–944 y 990–1080; leídas acción, equivariancia, cierre, clasificación del cociente y pruebas; no revisadas íntegramente las tablas literales de emisiones/palabras/representantes ni el bloque final de `#print axioms`.
- L06: líneas 1–200 y 672–810; leídas construcción de metadatos, tablas 18/26 de metadatos, factor de semillas, selección y cinco regiones; no revisadas íntegramente las 468 filas del testigo 201–671 ni la lista final de impresiones de axiomas.
- P01: se han leído las definiciones de Ψ/acción y la función completa `select_structural_orbits`, líneas 182–389; también se consultaron anteriormente lectores y prolongación en cortes puntuales. Este inventario **no declara una lectura completa del archivo** ni una nueva ejecución.
- D01: identificado como entrada de P01; no se han leído de nuevo sus 468 objetos completos en esta entrega. La procedencia del censo se documenta además por la generación Lean, que no toma ese JSON como entrada.

### Pendientes de lectura/integración, no afirmaciones de ausencia

- Propietario completo del algoritmo `Sel/Tra/Upd→X0,Y0,X1,Y1`, con los estados que producen cada fila.
- Certificado exacto de las restricciones de R36, definición desarrollada de q/a/saturación/ocupación, regla de las cartas (789,048,894)/(793,045,894) y selección semiabierta.
- Formalización entera del lift Hensel de F03 y recibos de los dos preestados del canal e.
- Comparación de contenido/huellas entre los módulos L01–L08 leídos y las copias más recientes de entrega; comprobación del recibo de compilación asociado a la copia finalmente escogida.
- Lectura integral de las tablas literales omitidas en L04–L06 si se requiere inventario de cada una de las 468 emisiones y de las 43 órbitas, no sólo sus tipos y selecciones.
- Descomposición en subfichas del lector analítico de cada región, la continuación G9 y el puente incidencial completo Paley–Witt, que pertenecen a entregas siguientes.
- Comprobación de todos los `\input` necesarios antes de presentar F01/F02 como secciones autosuficientes fuera del artículo.

## G. Controles efectuados y lo que no certifican

Durante este trabajo se ejecutaron las autocomprobaciones del núcleo formal permanente y de causalidad de constantes, con salidas `PASS_NUCLEO_FORMAL_HMT_PERMANENTE` y `PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY`. Esos controles ayudan a conservar el orden de trabajo; no son una recompilación de los módulos Lean ni una nueva prueba de R36.

Las habilidades de núcleo formal, HMT-first, continuidad, causalidad de constantes y conexión nonádica han guiado la separación de dominios, la preservación de las cinco regiones y el orden **selección regional → transporte → lectura → reconocimiento posterior**. No se han editado los PDF, las fuentes LaTeX, el catálogo ni los módulos Lean. Sólo se crea este inventario sucesor.
