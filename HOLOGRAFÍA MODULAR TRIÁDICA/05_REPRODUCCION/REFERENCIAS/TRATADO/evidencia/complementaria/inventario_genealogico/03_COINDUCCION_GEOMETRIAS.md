# Conexión nonádica, coinducción y realizaciones geométricas de APP

Subinventario documental CG — 19 de septiembre de 2026.

## Alcance y modo de lectura

Este documento inventaría definiciones, operaciones y demostraciones localizadas en las fuentes HMT–MD. No modifica los PDF, no constituye una revisión global del corpus y no introduce una demostración nueva. Las fichas conservan la precedencia APP → TRIT → TPK → estado enriquecido y la residencia de las realizaciones posteriores en la estructura discreta conjunta del continuo. Las coordenadas arquimedianas son salidas: una fórmula de evaluación posterior no se sustituye al antecedente que la fuente declara generativo.

Se distinguen cuatro planos de evidencia: **exposición**, **demostración escrita**, **implementación Python** y **formalización Lean**. Haber localizado o leído uno no acredita los otros. Los recibos anteriores se citan como artefactos existentes; no se presentan como ejecuciones nuevas. Las reservas de localización de este expediente no son declaraciones de inexistencia matemática en el corpus.

La unidad de esta entrega es una ficha explicativa. Las transformaciones elementales que puedan desglosarse después conservarán el ID de su ficha matriz. Las cinco construcciones consustanciales del continuo no se separan aquí en teorías independientes: los cortes siguientes sólo siguen operaciones y realizaciones concretas del mismo desarrollo.

## Mapa de precedencias localizado

1. Las dos hojas APP se evalúan antes de reducirlas; la reducción conserva el cociente.
2. La división balanceada y el selector de fase TRIT tipan lectura, orientación y transporte.
3. El emisor finito produce el catálogo; sus regiones y registros de transición alimentan los levantamientos hasta `w30`.
4. El selector interno recuperado discrimina dos candidatos de frontera y determina `R36` en su calibre propietario; un cambio de calibre explícito lo lleva a la carta excepcional activa.
5. `G9` designa una relación de apertura de bloque; `Γ9` designa la holonomía de nueve transiciones con avance de memoria. Son objetos diferentes.
6. La prolongación general es multivaluada. La sección forward individualizada en la fuente utiliza el carácter y el residuo interno del estado `R36` previamente generado.
7. La lectura por cilindros y el cambio de base publican valores y bloques; no reinician la historia ni convierten una comparación analítica en productor antecedente.
8. Las realizaciones de Cayley, Lorentz, Minkowski, Hilbert y del toro `27×27` se tipan sobre los objetos anteriores. No son entradas convencionales del emisor.

## CG-001 — División nonádica con representante positivo y cociente conservado

**Objeto y dominio.** La carta posicional tiene soporte \(X_9=(\mathbb Z/9\mathbb Z)^2\), con representantes humanos \(\mathcal D_9=\{1,\ldots,9\}\). Las hojas enteras se evalúan como \(S(i,j)=i+j\), \(P(i,j)=ij\). La lectura nonádica utiliza

\[
 \rho_9(n)=1+((n-1)\bmod9),\qquad
 q_9(n)=\frac{n-\rho_9(n)}9,\qquad
 n=\rho_9(n)+9q_9(n).
\]

**Regla y precedencia.** Primero se calcula la suma o el producto entero; después se separan representante y cociente. El `9` de la carta representa la clase nula, pero no autoriza a borrar el cociente. La salida pertinente es el par, no el residuo aislado.

**Coeficientes y conservación.** El módulo `9` pertenece a la carta APP. El factor `9` del recuperador procede de esa división. El acarreo aditivo
\(c_9(a,b)=[s_9(a)+s_9(b)-s_9(a+b)]/9\) satisface la identidad de cociclo por cancelación de las cuatro expresiones de la sección. Con representantes positivos, el cociclo no es normalizado: \(c_9(0,a)=1\). Esa convención no se confunde con la sección `0,…,8`.

**Ejemplo y control negativo.** Las celdas `(5,5)` y `(8,2)` tienen suma `10` y productos `25`, `16`. Comparten el residuo multiplicativo `7`, pero sus cocientes son `2`, `1`. La reducción sola pierde una distinción que el par residuo–cociente recupera.

**Evidencia.** Exposición y prueba algebraica: [nucleo.tex:8](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/nucleo.tex:8>), definición en líneas 20–25, reconstrucción en 49–54 y cociclo en 80–106. Fuente leída íntegramente. Python y Lean: esta ficha no asigna una formalización concreta por mera coincidencia de vocabulario; su cotejo fino queda pendiente. No se ha ejecutado un control nuevo.

**Consumidores.** Emisor finito, registros de frontera, refinamiento con acarreo, reconstrucción de la historia aritmética. **Procedencia:** arquitectura autoral preexistente, reunida aquí como inventario.

## CG-002 — División balanceada, transporte de operaciones y cero con segundo registro

**Objeto y dominio.** \(\mathbb T=\{-1,0,1\}\), \(q_3(n)=\lfloor(n+1)/3\rfloor\), \(r_3(n)=n-3q_3(n)\). La aplicación \(B:\mathbb Z\to\mathbb T\times\mathbb Z\), \(B(n)=(r_3(n),q_3(n))\), tiene inversa \((r,c)\mapsto r+3c\).

**Operación efectiva.** Con \(\chi(r,s)=(r+s-r_3(r+s))/3\), las operaciones transportadas son

\[
 (r,c)\boxplus(s,d)=(r_3(r+s),c+d+\chi(r,s)),
\]
\[
 (r,c)\boxtimes(s,d)=(rs,rd+sc+3cd).
\]

**Precedencia y coeficientes.** Son operaciones sobre enteros levantadas al registro balanceado; no se deducen de una lista de cifras ya conocida. El `3` procede del módulo ternario. El puente \(\beta:\mathbb T\times\mathbb F_3\to\mathbb Z/9\mathbb Z\), \((r,c)\mapsto r+3c\), es biyectivo como conjunto con la operación transportada. No se lo declara producto directo de grupos.

**Conservación.** El cero visible tiene tres elevaciones nonádicas: las clases `3`, `6`, `0` tienen segundo registro `1`, `2`, `0`. Se conserva la inversión \(B(-n)=(-r_3(n),-q_3(n))\). El cociente aritmético no sustituye al registro completo de ruta, orientación o frontera.

**Evidencia.** Definición y prueba de unicidad: [trit_desarrollo.tex:13](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/trit_desarrollo.tex:13>); operaciones 45–74; cociclo y puente nonádico 87–125; inversión y distinción entre cociente y memoria 131–167. Fuente leída íntegramente. Python/Lean: no asignados ni recompilados en esta lectura focal.

**Consumidores.** Selector operativo, lectura de los falsos ceros, composición modular y archivo reversible. **Control negativo:** sustituir `(r,c)` por `r` destruye la inversa.

## CG-003 — Tres regímenes cuadráticos del TRIT y cambio de tipo temporal

**Objeto y dominio.** Para \(\tau\in\{+1,0,-1\}\), la realización algebraica es \(A_\tau=\mathbb R[J]/(J^2+\tau)\). La multiplicación y la norma son

\[
 (a+bJ)(c+dJ)=(ac-\tau bd)+(ad+bc)J,
 \qquad N_\tau(a+bJ)=a^2+\tau b^2.
\]

**Regla.** \(\exp(tJ)=C_\tau(t)I+S_\tau(t)J\) y \(C_\tau^2+\tau S_\tau^2=1\). Los tres tipos son elíptico, parabólico e hiperbólico. En el hiperbólico, \(P_\pm=(I\pm J)/2\) y \(e^{tJ}=e^tP_++e^{-t}P_-\).

**Precedencia.** El selector trítico de fase \(M_{\rm ph}\) asigna las clases `{1,4,7}` a `+1`, `{2,5,8}` a `−1` y `{3,6,9}` a `0`. En el desarrollo temporal activo, `+1` corresponde a retorno/memoria/pasado, `0` a umbral/presente y `−1` a apertura bidireccional/futuro. La realización mediante matrices se aplica a esos regímenes; no elige retrospectivamente el signo del TRIT.

**Conservación y límites de identificación.** La norma es multiplicativa y determina la inversión cuando es no nula. La involución de una palabra que invierte orden y signos no es la conjugación dentro de una única álgebra \(A_\tau\): puede cambiar de régimen. Las tres álgebras no se identifican entre sí; pueden realizarse dentro de un álgebra matricial común. La firma `(1,1)` es una realización Lorentz local `1+1`, no por sí sola una métrica física global `3+1`.

**Evidencia.** [nucleo.tex:168](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/nucleo.tex:168>) y selector en 229–258; [trit_desarrollo.tex:169](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/trit_desarrollo.tex:169>), composición y dominio del denominador en 235–304, cambio de tipo en 306–343. Ambas fuentes leídas completas. Python y Lean: no cotejados para esta ficha.

**Consumidores.** Transporte orientado TPK, fases internas, curvaturas y realizaciones unitarias. **Control negativo:** no sustituir `M_ph` por el transporte cardinal `T_d`; sus tipos son distintos.

## CG-004 — Emisor finito, doble cursor y catálogo \(104976\to468\to243\subset729\)

**Dominio inicial.** \(\mathcal S=I_9^2\times\{N,E,S,O\}\), con `324` estados de cursor; \(\Omega_{\rm seed}=\mathcal S_+\times\mathcal S_\times\) tiene `104976` pares. Las dos hojas APP no se sustituyen por un único cursor.

**Operación.** El emisor recorre seis ventanas de nueve transiciones. La fase `+` lee la hoja aditiva y mueve el primer cursor; `−` lee la multiplicativa y mueve el segundo; `0` interviene en el registro neutral. La orientación se invierte en los pasos `27` y `54`. Para la ventana \(m\), \(S_m\) suma las tres lecturas aditivas; \(E_m\) suma tres lecturas logarítmicas de las unidades módulo `9`; \(Z_m=3\). La carta decimal del bloque es

\[
 d_1=[S_m]_{10},\quad d_2=[S_m+E_m]_{10},\quad
 d_3=[3S_m+5E_m+7Z_m]_{10},\qquad
 U_m=100d_1+10d_2+d_3.
\]

**Procedencia de coeficientes.** El calendario y los coeficientes `3,5,7` se encuentran declarados en la ley del emisor inspeccionada. Este inventario no afirma haber localizado aquí una derivación ulterior de cada coeficiente. El `1` de una forma alternativa del último dígito procede de \(7Z_m=21\equiv1\pmod{10}\). La lectura discreta en unidades usa la enumeración de potencias de `2` módulo `9`; su prolongación por cero a no unidades es una convención del observable, no una afirmación de que todos los elementos son unidades.

**Salida y conservación.** La factorización del catálogo da `18` firmas aditivas por `26` multiplicativas, esto es `468`. La reducción ternaria visible tiene `243` palabras dentro de \(\mathbb F_3^6\), que contiene `729`. El dominio de semillas, la emisión decimal, la reducción ternaria y la fibra ambiente no son cuatro listas intercambiables.

**Evidencia.** [extension.tex:8](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/extension.tex:8>), emisor 22–49 y factorización 51–66. Exposición y prueba inaugural más extensa: [c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:159](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:159>). Las fuentes se han leído completas en la lectura acumulada focal.

**Python/Lean.** El emisor y la selección de regiones tienen propietarios anteriores a `TPKLifts.lean`; el alcance formal los enlaza mediante `selectedSeeds`, sin atribuir al módulo de lifts toda la generación antecedente. Véase [TPK_LIFTS_SCOPE.md:7](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/ENTREGA_STAGE10_20260917/HMT_LEAN_PRINCIPAL_CHAINS_STAGE10/TPK_LIFTS_SCOPE.md:7>). No se ha relanzado el censo en esta entrega.

**Control negativo.** Un censo exhaustivo de semillas finitas no es por sí solo un censo de todas las continuaciones infinitas ni demuestra que cada palabra ambiente sea superviviente.

## CG-005 — Levantamientos ternarios reconstruidos y biografías finitas hasta \(w_{30}\)

**Objeto y regla.** Los cuatro registros de transición \(X_0,Y_0,X_1,Y_1\) producen \(L_i=X_i^{-1}Y_i\) sobre \(\mathbb F_3\). Los vectores son filas; la acción sobre una palabra es \(w\mapsto wL_i\). El calendario finito se reconstruye como `0011` entre los `16` calendarios binarios de cuatro pasos que se confrontan con esos registros.

**Dominio y precedencia.** Las semillas regionales seleccionadas preceden al recorrido; el módulo formal coteja su igualdad con las primeras filas de los registros. Reconstruir `L0/L1` desde `X/Y` no equivale a formalizar en el mismo archivo la producción anterior de las `24` filas por `Sel/Tra/Upd`.

**Salidas conservadas.** Se guarda la palabra inicial y cada uno de los cuatro bloques siguientes, con longitudes acumuladas `6,12,18,24,30`. Para propagación, el recorrido documentado es

`201101 → 121221 → 102011 → 012222 → 102011`.

La repetición del tercer y quinto bloques no identifica sus estados enriquecidos: sus cursores y registros difieren. La biografía de clausura es `010211 → 012222 → 010211 → 002111 → 110221`; la de autoescala es `121200 → 112202 → 121020 → 010210 → 010200`.

**Exposición y prueba.** Los registros, reconstrucción, calendario y concatenación están en [06e_certificado_generacion_monodromica_rev7.tex:45](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex:45>), continuando hasta 141. El contexto del canal de propagación se conserva en [U013_biografia_estructural_e_body.tex:37](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/pi_e_phi/U013_biografia_estructural_e_body.tex:37>), selección 37–63, bloques 65–80 y comparación de estados 138–160.

**Python.** [generar_desde_estructura.py:558](</Users/ruben/Documents/New project/certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py:558>), `finite_w30_from_tpk_lifts`, implementa la acción y concatenación. Esta función no debe confundirse con `generate_gate_channel`, que utiliza horquillas de evaluación en otro tramo del mismo programa.

**Lean.** [TPKLifts.lean:99](</Users/ruben/Documents/New project/output/PAQUETE_CONTINUIDAD_K_UNIDAD_20260918/lean/biblioteca/TPKLifts.lean:99>) contiene los registros; `solveMatrix` 127, `L0/L1` 132–133, unicidad 173–187, inversas 191–240, semillas y calendario 283–323, biografías y truncamientos 329–375. [TPK_LIFTS_SCOPE.md](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/ENTREGA_STAGE10_20260917/HMT_LEAN_PRINCIPAL_CHAINS_STAGE10/TPK_LIFTS_SCOPE.md>) declara `37` teoremas, Lean `4.21.0`, sin Mathlib, y el corte formal. La compilación relatada pertenece a aquel paquete; no se repitió aquí. La copia Lean se inspeccionó focalmente, no se afirma lectura integral de todas sus dependencias.

**Control negativo.** Los truncamientos de listas prueban conservación del prefijo representado; no acreditan campos de memoria que el tipo de palabra no contiene. La formalización no se extiende por su nombre a la supervivencia coinductiva completa.

## CG-006 — Selector de frontera \(R_{36}\) recuperado sin objetivo arquimediano

**Entrada y operación.** A partir del catálogo visible de `243` palabras, los lifts propietarios `L0/L1`, la matriz propietaria \(A_W\), la fila futura y las biografías hasta `w30`, se filtran ternas por margen, acarreo unitario, ocupación de columnas y neutralidad dual de Witt. Quedan dos orientaciones; la suma de distancias mínimas en el semigrupo generado por los lifts selecciona una sola.

**Cálculo exacto registrado.** Las ternas, en el orden clausura/propagación/autoescala, son:

| Candidato | Filas | Distancias | Suma |
|---|---|---|---|
| A | `021222`, `222220`, `102011` | `8,8,7` | `23` |
| B | `222220`, `021222`, `102011` | `4,9,7` | `20` |

La segunda terna es la seleccionada. Sus rutas son `1111`, `001100101`, `1010101`. Los dos candidatos tienen acarreo `111111`, margen `012120` y ocupación `223232`. La energía aquí es longitud de recorrido semigrupal definida en ese propietario; no se identifica con energía física por compartir el nombre.

**Precedencia y conservación.** La selección ocurre antes de usar intervalos o cifras arquimedianas, según la ejecución implementada. El resultado es relativo al propietario de `L0/L1/AW` recuperado; el transporte a la carta activa se verifica aparte. La permutación \(p=(0,1,2,4,5,3)\) conjuga las matrices y transporta los vectores. Las filas en la carta excepcional activa son `222202`, `021222`, `102110`. No se concatena esa fila excepcional a una expansión radix sin efectuar su transporte de carta.

**Python.** [verificar_generacion_infinita_nonadica.py:1017](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/verificar_generacion_infinita_nonadica.py:1017>), `generate_target_free_r36`, leída completa hasta 1147; puente de calibre en 668–715. La comprobación final frente a `B_PLUS_R36` es un testigo de regresión posterior a la selección, no el filtro que produce el mínimo.

**Propietario recuperado.** [selector_interno_constantes.py:185](</Users/ruben/Documents/New project/16_CIERRE_GLOBAL_HMT_MD_2026-07-22/01_SELECTOR_CONSTANTES/selector_interno_constantes.py:185>), candidatas y energía hasta 307. La rutina `reconstruct_hensel` de ese archivo recibe bloques; no se le asigna por ello el estatuto de generador independiente de una cola infinita.

**Recibo existente.** [recibo_r36_smoke_8.json:7](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/SMOKE_8/recibo_r36_smoke_8.json:7>) conserva ambos candidatos; selección y energía en 167–172; `archimedean_radix_word_relabelled:false` en 175; cartas en 214–220. Se leyó el recibo, no se volvió a ejecutar el cálculo en esta entrega.

**Prueba/Lean y alcance.** El capítulo coinductivo incorpora las filas y el cambio de calibre en líneas 70–76. No se ha localizado y leído en esta tarea un módulo Lean que formalice este selector completo `R36`. Eso no afirma que no exista. La selección única de esta frontera no se extrapola a la unicidad de cada fibra posterior de `Ext`.

**Procedencia:** `RESULTADO_RECUPERADO`, tal como distingue el propio ejecutable; no descubrimiento atribuido a este inventario.

## CG-007 — Frontera coinductiva, apertura \(G_9\) y supervivencia compatible

**Tipos.** \(\widetilde R_{36}\) reúne estados de profundidad `36` con registros de borde definidos. Para cada estado, \(\operatorname{Cand}_6(x)\) contiene estados de profundidad `42` con el mismo prefijo y una trayectoria tipada de seis transiciones. Hay a lo sumo `729` palabras visibles candidatas; no se sigue que existan `729` estados supervivientes.

**Regla.** El predicado \(g_{9,x}\) exige compatibilidad de prefijos y supervivencia a profundidad arbitraria. La frontera efectiva y la apertura son

\[
 R_{36}=\{x:\exists y\in\operatorname{Cand}_6(x),\ g_{9,x}(y)=1\},
\]
\[
 G_9=\{(x,y):x\in R_{36},\ y\in\operatorname{Cand}_6(x),\ g_{9,x}(y)=1\}
 \subseteq\mathcal U_{41}\circ\cdots\circ\mathcal U_{36}.
\]

**Distinción esencial.** `G9` es una relación de apertura entre profundidades `36` y `42`; `Γ9` es el retorno de nueve transiciones elementales. `R36` no denota la recta real. El nombre del umbral no introduce una constante numérica que escoja la región de propagación.

**Prueba y conservación.** Truncamiento compuesto con una prolongación compatible recupera exactamente el estado anterior. El teorema de estabilización utiliza ramificación finita, no vacuidad a toda profundidad, naturalidad y conservación de campos; obtiene una historia infinita compatible. La fase retorna y la memoria aumenta. Esa prueba de existencia no individualiza, por sí sola, las cuatro secciones de constantes.

**Exposición/prueba.** [03_prolongacion_tpk.tex:354](</Users/ruben/Documents/New project/output/LEY9_SINTESIS_300_SUCESORA_SIN_REGRESIONES_20260904/manuscrito/sections/autonomia/03_prolongacion_tpk.tex:354>), prolongaciones y truncamientos; definiciones `R36/G9` 401–473; teorema y prueba 476–496. Fuente leída completa en el trabajo focal acumulado y releída en este tramo.

**Python/Lean.** No confundir la lectura de este predicado de supervivencia con su decisión computable automática para cualquier estado. El ejecutable posterior registra una sección individualizada, inventariada en CG-008. No se ha reproducido ni localizado aquí una formalización Lean completa del predicado general.

**Control negativo.** Ni una rama canónica arbitraria ni el número de candidatas demuestran la selección de todas las secciones específicas.

## CG-008 — Prolongación forward, residuo interno inicial y publicación posterior

**Objeto y dominio.** El capítulo declara, para cada coordenada \(\chi\in\{\pi,\varphi,e,\alpha\}\), un estado
\(x_r^\chi=(\widetilde x_r,\chi_{\rm HMT},\varepsilon_r^\chi,N_r^\chi)\), con \(r\in6\mathbb N\), que conserva hoja, orientación, cociente, acarreo, ruta, frontera, firma y memoria.

**Regla escrita.**

\[
 d_r^\chi=\operatorname{Dig}_{729}(\varepsilon_r^\chi),\quad
 0\le d_r^\chi<729,\quad
 \varepsilon_{r+6}^\chi=729\varepsilon_r^\chi-d_r^\chi,\quad
 N_{r+6}^\chi=729N_r^\chi+d_r^\chi.
\]

La transición se compone como `Upd ∘ Tra ∘ Sel`, con `Upd=Rec∘Mem`. La sección \(\operatorname{Ext}^{\chi,\rightarrow}\) es el grafo de esa actualización. El carácter y el residuo están declarados como coordenadas internas anteriores a la publicación arquimediana; la fuente excluye definir \(\varepsilon\) como parte fraccionaria de un valor publicado.

**Prueba y conservación.** La igualdad \(\lfloor N_{r+6}/729\rfloor=N_r\) conserva el prefijo. Una vez fijado el estado inicial enriquecido y una actualización funcional, la inducción da una única sección forward; la relación completa `Ext` puede seguir siendo multivaluada. La demostración de no vacuidad genérica y la de esta individualización tienen hipótesis distintas.

**Exposición y prueba.** [c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:81](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:81>), tipado y actualización 95–128, unicidad y distinción 130–157. La prueba más extensa del teorema conjunto figura en el resto del mismo capítulo, leído en la lectura acumulada.

**Python: separar tres funciones.**

- [generate_structural_characters:1321](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/verificar_generacion_infinita_nonadica.py:1321>) construye descripciones exactas y condiciones de los caracteres; en 1394–1397 conserva la descripción textual de \(\varepsilon_{36}\).
- [verify_forward_character_extension:1472](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/verificar_generacion_infinita_nonadica.py:1472>) comprueba empalmes, campos y casos de división; registra las recurrencias y el argumento inductivo. Los bucles 1522–1535 recorren `729` dígitos y varias entradas enteras, además de fase/memoria. No ejecutan una trayectoria residual concreta ilimitada de cada coordenada.
- [publish_archimedean_blocks:1881](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/verificar_generacion_infinita_nonadica.py:1881>) utiliza cotas de evaluación para publicar bloques. [verify_finite_forward_witness:1930](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/verificar_generacion_infinita_nonadica.py:1930>) compara el prefijo de cinco bloques y el sexto testigo con `R36`. Ambos están después del productor finito en la cadena del programa.

**Detalle documental que debe conservarse.** Esta ficha no reemplaza \(\varepsilon_{36}\) por una cifra conocida ni lo declara generado por la sola frase que lo describe. Queda por reunir en una subficha el productor material, el tipo exacto y la representación ejecutable inicial de ese residuo, con sus dependencias; los propietarios inspeccionados lo declaran coordenada interna. Este estado de localización no se propaga como negación del teorema escrito ni como afirmación de que tal productor no exista en otras fuentes.

**Lean.** `TPKLifts.lean` cubre el tramo finito descrito en CG-005; no se le atribuye esta sección coinductiva. No se ha leído un módulo formal adicional que cubra todas las obligaciones de esta ficha. **Control negativo:** ni el rótulo de un `PASS` ni la coincidencia de un prefijo demuestran automáticamente un algoritmo independiente de inicialización residual y selección de toda la cola.

## CG-009 — Holonomía nonádica, memoria ilimitada y cociente dodecafásico

**Estado y operación.** El registro incluye bloque, cursores, posición, acarreos, incidencia, marco, fase \(g\) y memoria \(m\). Con \(g(k)=1+[(k-1)]_9\), la holonomía es \(\Gamma_{9,k}=R_{k+8}\circ\cdots\circ R_k\). Su iteración satisface fase constante y \(m\mapsto m+s\); el residuo dodecafásico \(\beta=m\bmod12\) avanza en `s` módulo `12`.

**Extensión finita del reloj.**

\[
 0\longrightarrow C_{12}\xrightarrow{b\mapsto9b}C_{108}
 \xrightarrow{t\mapsto t\bmod9}C_9\longrightarrow0.
\]

En coordenadas \((b,r)\), el producto añade \(\lfloor(r+r')/9\rfloor\) a la coordenada de memoria. La prueba de no escisión distingue el exponente `108` del exponente `36` de \(C_{12}\times C_9\). La extensión finita no contiene por sí sola la memoria entera ilimitada; la publica módulo `12`.

**Realización bilateral.** En \(\ell^2(\mathbb Z)\), el cambio de índice entre posición lineal y `(fase,memoria)` realiza un desplazamiento unitario `T`; \(T^9\) avanza la memoria. La inversión tiene un acarreo de frontera, por lo que no equivale a negar separadamente dos coordenadas sin corregir el borde.

**Evidencia.** [revision_monodromia.tex:13](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/revision_monodromia.tex:13>), estado y holonomía 24–58, realización bilateral e inversa 68–127. [extension.tex:68](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/extension.tex:68>), extensión cíclica y prueba 84–96. Ambas fuentes leídas completas.

**Python/Lean.** Se localizó el control suplementario `verificar_memoria_holonomia_20260912.py` bajo `ARTICULO/ES/supplement/antecedentes`, pero no se leyó íntegramente ni ejecutó para esta ficha. El lanzador [ejecutar_controles.py:6](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/supplement/ejecutar_controles.py:6>) declara alcance finito suplementario, no certificación global. No se asigna aquí una prueba Lean de la memoria bilateral.

**Consumidores y control negativo.** Lectura fase–carga, archivo y reloj dodecafásico. No identificar retorno de fase con retorno del estado, ni esta extensión cíclica con la extensión central de Heisenberg de CG-014.

## CG-010 — Cambio de base, residuos de cilindros y vacancias de publicación

**Regla modular elemental.** Si \(n=1000q+r\), \(0\le r<1000\), entonces \(n\equiv q+r\pmod9\) y módulo `3`, porque \(1000\equiv1\). No se elimina `q`: el cambio de base transporta el cociente.

**Residuo de conversión.** Para un numerador ternario \(N\), profundidad \(L\), prefijo decimal \(D\) y longitud decimal \(r\),

\[
 A=1000^rN-D3^L.
\]

Añadir seis trits produce \(N'=729N+\nu\), \(L'=L+6\). Con prefijo decimal fijo,
\(A'=729A+\nu1000^r\). Si además se emite un bloque decimal \(\delta\), \(D'=1000D+\delta\), \(r'=r+1\), entonces

\[
 A'=729000A+\nu1000^{r+1}-729\delta3^L.
\]

**Precedencia y coeficientes.** `729=3^6` es la capacidad del bloque ternario; `1000=10^3` es la carta de tríadas decimales; `729000` procede de componer ambos cambios. No son valores objetivo introducidos para elegir una constante.

**Calendario de capacidad.** Con \(\rho=\log_{1000}729=\log_{10}9\), \(\delta=1-\rho\), la fuente define contadores de emisiones y vacancias mediante pisos y demuestra su complementariedad. Los retornos de fase deben corregirse por las vacancias: índice de bloque, índice de emisión e índice de memoria no son automáticamente iguales.

**Conservación.** La identidad del residuo conserva exactamente la relación entre ambos prefijos y sus profundidades. El calendario organiza cuándo puede publicarse un bloque, pero no contiene por sí solo su valor; ese valor depende también del residuo.

**Exposición/prueba.** [geometria_modular.tex:99](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/geometria_modular.tex:99>), identidad por sustitución hasta 137. [revision_monodromia.tex:129](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/revision_monodromia.tex:129>), calendario y vacancias hasta 195. Fuentes completas leídas.

**Python/Lean.** Las funciones de publicación de CG-008 son consumidores de este tipo de lectura; debe cotejarse su normalización exacta antes de declararlas implementación literal de esta ecuación. No se ha certificado tal identidad de implementaciones en esta entrega. **Control negativo:** no transformar la aperiodicidad del calendario en una conclusión sobre la aperiodicidad o clasificación aritmética de toda salida sin la composición residual correspondiente.

## CG-011 — Eje de autoescala, fases de agregación y espejo: tres tipos distintos

**Objeto.** La figura de la recta nonádica usa la coordenada posicional `[0,10]` para describir umbrales del recorrido. La ubicación de autoescala en `5` designa la primera saturación local fuerte: \(N_{\rm loc}=N_{\rm ext}=1\), acarreo `111111`, residuo de Witt nulo. Si se normaliza esta posición por `10`, resulta `1/2`. Ninguno de esos números sustituye al valor de \(\varphi\).

**Fases posteriores.** Las fases `6–8` describen la conservación de una suma ternaria dentro de una fibra espejo; aparecen los bloques `012100`, `101001`, `112000`. Es necesario conservar la operación en la carta correspondiente, no leer sus rótulos como intervalos ordinarios de valores constantes.

**Espejo.** La involución del triple intercambia las coordenadas de clausura y propagación y deja la autoescala fija. En la formulación \(B=(u_\pi,u_e,u_\varphi)\), la suma y el margen permanecen, mientras cambia de signo la diferencia. La figura rotula \(\pi\leftrightarrow e\); el cociente \(\pi/e\) es una publicación posterior que se invierte bajo ese intercambio. No son la misma clase de objeto.

**Conservación.** El regreso `9→1` conserva la fase y avanza memoria. La fuente da bloques de fases coincidentes distintos entre sí, como testigo de que fase igual no implica estado igual.

**Evidencia.** [recta_nonadica_recuperada.tex:5](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/recta_nonadica_recuperada.tex:5>), autoescala 5–29, agregación 31–53 y retorno 55–61. [recta_nonadica_0_10.tex:23](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/figures/recta_nonadica_0_10.tex:23>) muestra el rótulo del espejo. [revision_monodromia.tex:259](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/revision_monodromia.tex:259>) contiene su acción tipada y, en 280–302, memoria y doble proyección. Fuentes leídas completas.

**Python/Lean.** No se asocia por defecto una figura con una prueba formal. **Control negativo:** no confundir la posición `5`, el centro celular `(5,5)`, un acarreo `111111` y el número real \(\varphi\). Su relación causal exige los mapas, no una coincidencia de rótulos.

## CG-012 — Cayley aditivo, toro discreto, curvatura mixta y realización Lorentz local

**Objeto y regla.** La APP posicional es el grafo de Cayley aditivo de \((\mathbb Z/9\mathbb Z)^2\) con cuatro direcciones. Tiene `81` vértices y cuatro aristas orientadas por vértice. Un recorrido cerrado conserva su enrollamiento \(((\#S-\#N)/9,(\#E-\#O)/9)\in\mathbb Z^2\); invertirlo cambia su signo. La vuelta al mismo vértice no fuerza enrollamiento nulo.

**Dos hojas.** La tabla multiplicativa vive sobre el mismo soporte, pero no es una tabla de grupo multiplicativo completa: módulo `9` hay divisores de cero. La curvatura de plaqueta localizada da `0` para pares homogéneos de hojas, `+1` para el orden suma–producto y `−1` para producto–suma, módulo `9`. Se conserva el orden de operaciones.

**Centro y matriz.** La igualdad de dos valores diagonales adyacentes se resuelve en \(k=4\), y el bloque central es

\[
 B_c=\begin{pmatrix}7&2\\2&7\end{pmatrix}=7I+2R,
 \quad \operatorname{spec}(B_c)=\{9,5\}.
\]

Su lectura estocástica es \(B_c/9=P_++(5/9)P_-\). Su normalización determinantal satisface

\[
 B_c^{\mathsf T}\operatorname{diag}(1,-1)B_c
 =45\operatorname{diag}(1,-1),\quad
 B_c/\sqrt{45}=\exp(\eta R),\quad \eta=\tfrac12\log(9/5).
\]

**Precedencia y alcance.** Los coeficientes `7,2,9,5,45` proceden del bloque y sus invariantes; la lectura Lorentz se reconoce después de construirlo. Esta es una realización exacta `1+1`, distinta de la construcción `1+3` de CG-013. La carta local de Markov no se identifica con todo el cociente `K_ph` global.

**Evidencia.** [nucleo.tex:56](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/nucleo.tex:56>), Cayley y enrollamiento; [extension.tex:133](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/extension.tex:133>), centro, Lorentz y curvatura mixta hasta 172. Antecedente con familia \(B_\tau=(4+3\tau)I+(5-3\tau)R\): [03_app_ortograma.tex:675](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/03_app_ortograma.tex:675>), leído sólo en el tramo 655–755 para esta consulta.

**Python/Lean.** Se localizó un control de aplicación dimensional en el suplemento de X, no leído ni reproducido íntegramente. No se atribuye cobertura formal Lean por el solo nombre de la geometría.

## CG-013 — Incidencia cúbica, cociente \(1+3\) y forma de Minkowski

**Entrada y dominio.** La matriz \(M\) de incidencia entre las `6` caras y los `8` vértices de un cubo tiene entrada `1` cuando el vértice pertenece a la cara. Con \(u\) uniforme de seis componentes, \(P_u=uu^{\mathsf T}/6\), oposición de caras \(R_F\) y \(P_-=(I-R_F)/2\),

\[
 MM^{\mathsf T}=12P_u+4P_-,\qquad
 Q_\square=\mathbb R^6/\ker(MM^{\mathsf T})
 \simeq\mathbb Ru\oplus E_-.
\]

**Prueba y coeficientes.** Cada cara contiene cuatro vértices; las opuestas no se intersectan y otras dos caras comparten dos vértices. De ese conteo salen los autovalores `12,4,0`, con multiplicidades `1,3,2`.

**Forma y conservación.** La fuente declara la asignación temporal de la componente uniforme y define
\(B_\square([x],[y])=\langle x,(P_--P_u)y\rangle\). En la base normalizada \(t=[u]/\sqrt6\), \(d_i=[e_{i,+}-e_{i,-}]/\sqrt2\), la matriz es \(\operatorname{diag}(-1,1,1,1)\). La incidencia positiva construye el cociente `1+3`; la asignación de signo construye la forma indefinida. No se omite este paso al decir que Minkowski está contenido en la realización.

**Soldadura y refinamiento.** \(W_\square=\sqrt6P_u+\sqrt2P_-\) lleva las etiquetas de cara a \(t\pm d_i\), vectores nulos. La co-cadena \(\beta_m(a)=\ell_m\sigma_m(a)W_\square e_{\rm etiqueta}\), con \(\ell_m=\ell_0/9^m\), satisface una regla orientada de inversión y una suma de nueve subsegmentos transportados. La orientación y la forma Lorentz permiten el operador de Hodge con \(\star^2=-I\) sobre las `2`-formas.

**Exposición/prueba.** [geometria_modular.tex:1](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/geometria_modular.tex:1>), incidencia y cociente hasta 33; forma 35–59; soldadura, dominio de transportes y Hodge 61–97. Fuente leída completa.

**Python/Lean y límites.** No se reproducen aquí las implementaciones correspondientes. No se convierte la forma algebraica en una afirmación sobre una solución cosmológica concreta ni se confunden curvatura espacial, espacio-temporal y de frontera. El transporte que preserva la forma tiene su hipótesis tipada dentro de la sección.

## CG-014 — Hilbert nonádico, extensión de Heisenberg y dos límites operatoriales

**Entrada HMT y realización.** Una vez construidos los estados y transiciones, \(\mathcal H_d=\ell^2((\mathbb Z/9\mathbb Z)^d)\), \(A_d=\mathcal B(\mathcal H_d)\) y \(\tau_d=9^{-d}\operatorname{Tr}\). El refinamiento de base \(\delta_{(x,r)}\mapsto\delta_x\otimes\delta_r\) es unitario.

**Regla de Weyl.** Después de la publicación de \(\pi\) y de la unidad compleja, la carta define \(\omega=e^{2\pi i/9}\), \(Xf(r)=f(r-1)\), \(Zf(r)=\omega^rf(r)\), con \(ZX=\omega XZ\). La sección ordenada \(X^aZ^b\) tiene cociclo \(bc\); la extensión central

\[
 (a,b,t)(c,d,s)=(a+c,b+d,t+s+bc)
\]

se realiza por \(\omega^tX^aZ^b\). Su conmutador es \(\omega^{bc-ad}\), relacionado con el área orientada \(ad-bc\). Esta extensión central no es la del reloj dodecafásico.

**Pruebas y conservación.** Los `81` productos de Weyl forman una base ortonormal para la traza; la representación con carácter central primitivo fijado es irreducible y única en el alcance declarado. Se distinguen la inclusión unital \(a\mapsto a\otimes I_9\), que conserva la traza normalizada, y el rincón \(a\mapsto a\otimes p_j\), cuya traza se divide por `9`.

**Paso al límite.** La cadena unital produce la UHF `9^∞`, y su cierre GNS tracial el factor hiperinfinito de tipo `II1`; la cadena de rincones produce otro límite, con operadores compactos y bicomutante tipo `I∞`. No se identifican ambos por provenir de un refinamiento nonádico. El parámetro real usado para describir rangos límite es coordenada de la realización posterior, no entrada del emisor APP.

**Exposición/prueba.** [01_hilbert_nonadico.tex:6](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/01_hilbert_nonadico.tex:6>), Hilbert y tensor; Weyl 46–64; cociclo y extensión 68–171; base e irreducibilidad 173–220; inclusiones 222–255; límite tracial 257–312; rincones y contraste 314–354. Fuente leída íntegramente.

**Python/Lean.** No se ha localizado y leído una formalización completa de estas pruebas funcionales en esta tarea. Un control matricial finito no se promovería al teorema de límite. **Control negativo:** la igualdad de cardinal `729` entre \((\mathbb Z/9\mathbb Z)^3\) y \(\mathbb F_3^6\) no identifica sus operaciones.

## CG-015 — Toro \(27\times27\), dirección conservada y suma exacta de recorridos

**Objeto y corte.** La fuente desarrolla una realización sobre \(\mathbb T_{27}^2=(\mathbb Z/27\mathbb Z)^2\), direcciones `{N,S,E,W}` y un espacio real interno \(E\) con \(J^2=-I\). El espacio es
\(\ell^2(\mathbb T_{27}^2;\mathbb R)\otimes\mathbb R^4\otimes E\).

**Operación.** La moneda \(C_4\) es la matriz Walsh–Hadamard normalizada por `1/2`; \(D_J=\operatorname{diag}(e^{-Ja_d})\) contiene acciones adimensionales ya tipadas; `S` desplaza condicionalmente por dirección. Se define

\[
 U_{\rm micro}=S D_J C_4,\qquad U_{12}^{\rm reg}=U_{\rm micro}^{12}.
\]

**Prueba y conservación.** Cada factor es ortogonal en la realización real, o unitario tras elegir la carta compleja. La potencia matricial reproduce exactamente la suma finita de recorridos, conservando el registro direccional y el orden causal de los pesos. El corte único de un recorrido da la ley de composición de núcleos. `U12reg` no se identifica automáticamente con otro operador `U12` ni con el grupo del reloj `108`.

**Escalas y límites.** La diagonalización de Fourier utiliza \(k_x=2\pi a/27\), \(k_y=2\pi b/27\). El Hamiltoniano efectivo requiere declarar un tiempo \(\Delta t_{12}=12\delta t\) y una rama del logaritmo. El límite de sumas a una integral de caminos requiere compatibilidad de medidas, continuidad/acotación y convergencia uniforme de acciones; no se obtiene del nombre del toro.

**Relación con la ampliación APP.** Este propietario prueba la realización dinámica sobre el soporte `27×27`, que contiene `729` posiciones. Por sí solo no prueba que reemplazar cada casilla de una APP `9×9` por un único trit sea literalmente la misma operación que ese aumento de ambas coordenadas. Debe localizarse y conservarse el mapa exacto de refinamiento, sus fibras y sus direcciones antes de identificar ambas descripciones. Se registra esa concordancia como pendiente de reunión documental, no como ausencia global.

**Exposición/prueba.** [toro27.tex:15](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/libro/toro27.tex:15>), categoría y pesos hasta 80; fase interna 82–121; soporte y operador 123–198; prueba de ortogonalidad y expansión de recorridos 200–256; Fourier 258–300; Hamiltoniano efectivo 302–331; límite y desintegración 333–445. Fuente leída íntegramente.

**Python/Lean.** No se han reproducido ni cotejado en esta entrega los certificados asociados al toro. **Control negativo:** no omitir la dirección, la fase o el estado interno para convertir la realización en una mera tabla de `729` números.

## CG-016 — Compresión isométrica, archivo del complemento y término terminal

**Objeto y operación.** Para una isometría `U` y una inclusión isométrica `J`, se definen \(T=J^*UJ\), \(D=(I-JJ^*)UJ\). La descomposición \(UJ=JT+D\), con \(J^*D=0\), da

\[
 I-T^*T=D^*D,
\qquad
 I=\sum_{r=0}^{n-1}T^{*r}D^*DT^r+T^{*n}T^n.
\]

**Precedencia y conservación.** Es una realización operatorial de la separación entre componente leída y complemento registrado. La ley conserva la norma entre ambos; no autoriza a eliminar el término terminal sin demostrar su desaparición en el régimen de límite concreto. El archivo debe tener un mapa explícito para su recuperación: conservar una norma no equivale por sí solo a reconstruir todas las coordenadas.

**Exposición/prueba.** [extension.tex:107](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/extension.tex:107>), demostración hasta 131. Fuente completa leída. Esta ficha enlaza con el desarrollo bilateral del artículo X, cuya revisión exhaustiva no corresponde a este subinventario.

**Python/Lean.** El suplemento de X contiene `BalanceBilateral.lean`, localizado pero no inspeccionado íntegramente en esta entrega. No se atribuye a ese archivo esta identidad particular sin cotejar definiciones e hipótesis. **Consumidores:** memoria, recuperación, lectura de observables y refinamiento conservativo.

## Cobertura de lectura y trabajo documental siguiente

### Leídos íntegramente en la lectura focal acumulada

- Las fuentes ES de X `sections/nucleo.tex`, `sections/trit_desarrollo.tex`, `sections/extension.tex`, `sections/geometria_modular.tex`, `sections/01_hilbert_nonadico.tex`, `sections/revision_monodromia.tex`, `sections/recta_nonadica_recuperada.tex`, `figures/recta_nonadica_0_10.tex` y `libro/toro27.tex`.
- El capítulo `c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex`, el propietario `06e_certificado_generacion_monodromica_rev7.tex`, `03_prolongacion_tpk.tex` y la biografía `U013_biografia_estructural_e_body.tex`, con relecturas focales de los pasos citados.
- `TPK_LIFTS_SCOPE.md` y el pequeño lanzador suplementario `ejecutar_controles.py`.
- Las habilidades de núcleo formal, HMT-first, continuidad, causalidad de constantes y conexión nonádica; el grafo operatorio permanente y el documento rector HMT-first utilizados para tipar esta consulta. Su lectura no certifica por sí misma los resultados de las fuentes.

### Lectura parcial o funcional explícita

- `verificar_generacion_infinita_nonadica.py`: selección `R36`, puente de calibre, caracteres, verificación forward, publicación de bloques, testigo finito y orden de llamadas. No se declara lectura integral de cada utilidad o cada propietario importado.
- `selector_interno_constantes.py`: candidatas, reconstrucción Hensel, selección y energía en los tramos citados.
- `TPKLifts.lean`: definiciones y teoremas focales, con documento completo de alcance. No se relanzó Lean ni se leyeron todas sus dependencias transitivas.
- `03_app_ortograma.tex`: líneas 655–755, no el archivo completo ni el integral completo.
- El recibo `recibo_r36_smoke_8.json`: campos de candidatas, selección y cambio de calibre; se conserva como recibo anterior, no nueva ejecución.

### Por leer o reunir antes de promover una cobertura mayor

1. Productor y representación material inicial de \(\varepsilon_{36}^\chi\), con tipo, dominio y algoritmo de lectura exacta; mantener separados inicialización, recurrencia y reconocimiento analítico.
2. Concordancia completa entre el soporte `9×9`, una ampliación de ambas coordenadas a `27×27`, la fibra ternaria de `729` palabras y el espacio de posiciones del toro. Coincidencia de cardinales no es una identificación de operaciones.
3. Implementaciones geométricas suplementarias y módulos Lean específicos para los pasos CG-009 a CG-016; separar controles finitos de teoremas de límite.
4. Origen y justificación de cada coeficiente del emisor que excedan la declaración de su ley en la fuente examinada, sin sustituir esa búsqueda por una elección externa motivada por el valor final.
5. Concordancias ES/EN y versiones posteriores a las fuentes aquí citadas. La entrega presente no afirma haber agotado esos deltas.

## Estado de esta entrega

Las dieciséis fichas están **inventariadas con localizadores y alcance de lectura**. No se modificó ningún PDF ni se generó una edición del artículo. Los controles de núcleo y causalidad consultados son controles de protocolo; no se presentan como prueba automática de todas las afirmaciones matemáticas. Las fichas no equivalen a un recibo genealógico global ni al cierre de las dependencias del libro completo.

Se preservan especialmente estas diferencias: `G9/Γ9`; memoria entera/cociente dodecafásico; residuo/cociente/ruta; selector finito `R36`/sección coinductiva; carácter interno/representación ejecutable inicial/lector arquimediano; `729` como capacidad ternaria/posiciones del toro/volumen cúbico; Lorentz local `1+1`/cociente Minkowski `1+3`; extensión de reloj/extensión de Heisenberg. Reunirlas permite explicar las relaciones sin borrar sus tipos.
