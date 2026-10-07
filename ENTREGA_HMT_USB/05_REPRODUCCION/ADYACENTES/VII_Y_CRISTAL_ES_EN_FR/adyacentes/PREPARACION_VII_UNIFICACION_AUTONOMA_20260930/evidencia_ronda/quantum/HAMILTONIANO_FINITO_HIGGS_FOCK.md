# Acoplamiento finito Higgs–Fock sobre el transporte común HMT

29 de septiembre de 2026. Construcción focal nueva por composición de propietarios; las fuentes anteriores permanecen intactas.

## 1. Punto de partida y propietarios

Desde APP–TRIT–TPK se toman las rutas, hojas y estados enriquecidos supervivientes que determinan el corte finito. Se conserva su residencia en la estructura discreta conjunta del continuo, con las cinco construcciones correlacionadas. La conexión nonádica conjunta y la memoria no se sustituyen por un recorrido independiente de puertas. El corte fija una celularización orientada compatible con esas rutas y conserva el transporte de su frontera. El objeto a componer es su realización de holonomía, no un conjunto de matrices escogidas por ajuste numérico.

Los ingredientes usados son:

- Holonomía y geometría: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30d_realizacion_geometrica.tex`, líneas 16–58. La pantalla y su soldadura producen `e_m=J_scr,m β_m`; la realización conserva `Hol_A(R_C(γ))=ρ_C(Hol_TPK(γ))`, concatenación, inversión y subdivisión. Conserva el levantamiento de espín por separado del vectorial.
- Color: `/Users/ruben/Documents/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/06e_color_qutrit_gauge_finito.tex`, §§ «Par de Weyl» y «Conexión y acción». La carta residual produce el qutrit y la forma real SU(3); las holonomías transforman por los marcos de los extremos.
- Dinámica gauge: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/X_ES/sections/ym_complete.tex`, líneas 383–458 y 659–665. El Hamiltoniano, sus expectativas condicionales, la reducción física y los refinamientos se transportan conjuntamente. Se recibe ese operador; no se lo reemplaza por un Hamiltoniano externo de nombre parecido.
- Fock: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/V_ES/sections/30_fock_gibbs.tex`, líneas 14–126; y `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VI_ES/sections/13_fock_pauli_composicion.tex`, líneas 413–535. Se reciben la paridad, CAR, el funtor exterior y las identidades de transporte con el adjunto explícito.
- Materia y mezcla: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VI_ES/sections/08_familias_y_compuestos.tex`, líneas 181–402; carga en `11_apendices_catalogo.tex`, líneas 297–319. Sabor, color, multisección, registro y representación no se identifican entre sí.
- Higgs y parámetros recibidos: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VII_ES/manuscrito/ampliacion_composicion/higgs.tex` y `electroweak.tex`, junto con la composición explícita ya reunida en `../INTEGRACION_MATEMATICA.md`, §5.1.

La presente construcción amplía el acoplamiento de esos ingredientes. No afirma que las fórmulas siguientes sean citas literales de un único capítulo anterior. Los coeficientes de acción, los acoplamientos, masas, matrices de mezcla y datos métricos que intervienen son lectores recibidos en sus cartas declaradas; el desarrollo no usa valores objetivo para elegirlos. Las masas pequeñas empleadas por el comprobador son fixtures algebraicos para falsar errores de composición, no evaluaciones físicas HMT.

## 2. Espacio común y transformación gauge

Sea `K=(V,E,F)` el corte celular y sea `G=SU(3)×SU(2)×U(1)`, con pesos enteros `y=6Y`. Se utiliza la representación de materia recibida y explicitada en la nota de anomalías, no un nuevo catálogo de representaciones. Las holonomías actúan en cada bloque por su representación correspondiente.

Para presentar el Hamiltoniano se elige la realización espacial de producto positivo de una partícula. La elección incluye su normal temporal y su levantamiento de espín. Una matriz de Spin(3,1) no es, en general, unitaria respecto del producto euclídeo: no se convierte en transporte unitario por llamarla holonomía. El bloque geométrico común conserva esa distinción y transporta el producto de las fibras junto con el marco. Esta carta Hamiltoniana no modifica la genealogía del estado.

La fibra fermiónica finita es

\[
\mathfrak h_F=\bigoplus_{v\in V}
(S_{L,v}\otimes E_L\ \oplus\ S_{R,v}\otimes E_R),
\qquad \mathcal F_F=\bigwedge\mathfrak h_F.
\]

El doblete Higgs vive en `C²` por vértice. Sea `X_B` la realización de holonomías, datos geométricos y campos escalares del mismo corte. Sobre el espacio bosónico `H_B` se recibe la medida gauge-invariante correspondiente y el bloque cinético común `H_0^HMT`. La extensión actúa en `H_B⊗F_F`, antes de introducir el corte espectral auxiliar. La geometría puede ser operatoria dentro de `H_B`: no se exige congelarla para definir esta composición.

Para `g∈G^V`, la representación conjunta es

\[
(\mathscr R(g)\Psi)(x)=\Gamma(\rho(g))\Psi(g^{-1}x).
\]

Por tanto, la transformación del Higgs, de cada enlace y de los modos fermiónicos ocurre a la vez. Sobre un enlace orientado,

\[
T_e(x):\mathfrak h_{F,s(e)}\to\mathfrak h_{F,t(e)},\qquad
T_e(gx)=\rho_{t(e)}(g)T_e(x)\rho_{s(e)}(g)^{-1}.
\]

`T_e` conserva el levantamiento de espín y la representación interna de la holonomía TPK. El operador de diferencia covariante y las contracciones métricas recibidas mantienen esta ley. La composición de dichos operadores pertenece al bloque geométrico-materia desarrollado conjuntamente; no se infiere un operador de Weyl de primer orden sólo de que exista un Laplaciano positivo `D_T* W D_T`.

## 3. Operador de Yukawa recibido y variable

En la base débil de tipo arriba,

\[
Y_u=\sqrt2D_u/v,\qquad Y_d=\sqrt2VD_dV^\dagger/v,
\qquad \widetilde H=i\sigma_2\bar H,
\]
\[
\mathsf Y_q(H)=
[\widetilde H\otimes Y_u,\ H\otimes Y_d]\otimes I_{\rm col}.
\]

El mismo cambio de base se aplica a corrientes y masas; no se introduce `V` otra vez en un bloque ya transformado. Para leptones se emplea `H⊗Y_e`, y, si la realización contiene singletes neutrínicos derechos, `\widetilde H⊗Y_ν`. Su presencia y su naturaleza no se deducen sólo de neutralidad eléctrica.

La identidad fundamental, probada por los pesos y la pseudorrealidad del doblete, es

\[
\mathsf Y(gH)\rho_R(g)=\rho_L(g)\mathsf Y(H).
\tag{1}
\]

En la fibra de una partícula se forma el bloque hermítico

\[
h_Y(H)=\begin{pmatrix}0&\mathsf Y(H)\\
\mathsf Y(H)^\dagger&0\end{pmatrix}.
\]

La interacción sobre Fock es la multiplicación operatoria

\[
(\widehat H_Y\Psi)(x)=
d\Gamma(h_Y(H(x)))\Psi(x)
=\sum_{v,a,b}
c_{L,v,a}^\dagger\mathsf Y(H_v(x))_{ab}c_{R,v,b}\Psi(x)
 +\mathrm{h.c.}
\tag{2}
\]

La dependencia del operador fermiónico respecto del campo Higgs es una interacción: no es una suma de Hamiltonianos independientes. Evaluar `H` en su sección de vacío recupera el operador de masa, pero hacerlo antes de comprobar la transformación gauge elimina información que (1) necesita.

**Lema de covariancia.** `R(g) H_Y R(g)⁻¹=H_Y` en su dominio algebraico común.

**Prueba.** La acción bosónica transforma la función coeficiente en `Y(g⁻¹H)`, mientras la segunda cuantización conjuga sus índices por `ρ_L(g)` y `ρ_R(g)†`. La combinación es `ρ_L(g)Y(g⁻¹H)ρ_R(g)†=Y(H)` por (1). Lo mismo vale para el adjunto. La suma finita sobre modos conserva la identidad. □

El escalar de Higgs y su cinética se realizan con las mismas contracciones espaciales. En una carta de coordenadas reales normalizadas por `H=(φ₁+iφ₂,φ₃+iφ₄)/√2`, el bloque de momento contiene la expresión canónica `−ℏ²Δ_φ/(2w_v)`, donde `w_v>0` es el peso volumétrico recibido, junto con lapse y las normalizaciones de esa carta. La diferencia entre vértices es `ρ_H(U_e)H_s−H_t`; su norma se contrae con los pesos positivos de la pantalla. El propietario fija `V(H)=−μ_H²|H|²+λ_H|H|⁴`. En su sección de mínimo, `μ_H²=λ_H v²`, de modo que

\[
w_vV(H_v)=w_v\lambda_H(|H_v|^2-v^2/2)^2-w_v\lambda_Hv^4/4.
\]

Se conserva el último término: al acoplar geometría, restarlo no es una mera renormalización de un escalar fijo y afecta a la densidad de vacío. Las fórmulas recibidas son `g²=4πα/(1−D)`, `λ_H=(g²/8)exp(6x+10y/3)` y `v=2E_W^angle/g`, con `E_W^angle=E_e^β exp(94x−y/6)`. No se escogen `w_v`, `v`, `λ_H` o `ℏ` para producir una salida buscada.

Si esos coeficientes geométricos son operadores, sus productos y orden se fijan en el bloque común mediante la forma cuadrática simétrica, no multiplicando operadores no conmutativos como si fueran escalares. La construcción finita siguiente usa las matrices de esa forma ya ordenada.

## 4. Autoadjunción y reducción física en un corte finito

Sea `P_N` un proyector ortogonal de rango finito cuyo rango está en el dominio algebraico común y que conmuta con `R(g)`. Una elección explícita en la realización de enlaces y escalares conserva bloques completos de Peter–Weyl y todos los multipletes de oscilador de un mismo número total. El corte de geometría se realiza con su transporte de marcos, como en el bloque común. Retener un componente de un doblete y descartar el otro no cumple esta condición.

Sea `H_base` la forma hermítica gauge-invariante que reúne el transporte, la dinámica geométrica y de calibre y los términos escalares anteriores. Definimos

\[
\mathbb H_N=P_N(H_{\rm base}+\widehat H_Y)P_N
\quad\hbox{sobre}\quad\mathscr H_N=\operatorname{Ran}P_N.
\tag{3}
\]

La composición concreta con el desarrollo paralelo `ACOPLAMIENTO_GRAVITATORIO_MEMORIA_20260929.md` se obtiene tomando

\[
H_{\rm base}=H_{\rm clk}^{\mu}+\hbar cK_{\rm gauge}
+d\Gamma(D_T^*WD_T)+H_{H,\rm cin}+V_H.
\tag{3a}
\]

Se mantienen sus fibras de medida `μ_x`, el transporte unitario `A_x` y la dependencia de `D_T` y `W` en el registro geométrico. El reloj puede mezclar esos registros. El término Yukawa de (2) actúa sobre la misma Fock y las mismas fibras, ahora ampliadas por el campo escalar: no se reemplaza la geometría cuántica por un número al hacer (3a). El bloque de respuesta de segundo orden conserva su identidad y no se presenta como el cinético Weyl.

**Teorema finito.** (3) es autoadjunto y acotado inferiormente, genera una evolución unitaria para todo tiempo y admite reducción gauge exacta. Con

\[
\Pi_N=\int_{G^V}\mathscr R_N(g)\,dg,
\]

se cumplen `Π_N²=Π_N=Π_N†`, `[Π_N,H_N]=0`, y la restricción `H_N^phys=H_N|RanΠ_N` es autoadjunta. Además,

\[
e^{-it\mathbb H_N/\hbar}\Pi_N
=\Pi_Ne^{-it\mathbb H_N/\hbar}.
\tag{4}
\]

**Prueba.** La forma base es hermítica por su construcción y (2) contiene cada término y su adjunto. Su matriz comprimida es hermítica en dimensión finita, por lo que tiene un espectro real finito, cota inferior y cálculo funcional unitario. La invariancia de la forma y `[P_N,R(g)]=0` implican `[H_N,R_N(g)]=0`. Invariancia de Haar e inversión del grupo dan idempotencia y autoadjunción de `Π_N`. Integrar el conmutador demuestra la reducción, y el cálculo funcional da (4). □

La constante inferior no se confunde con positividad de cada término de interacción. En el sistema finito puede sumarse un múltiplo de la identidad sin alterar los conmutadores; esa operación algebraica no autoriza a eliminar un término proporcional al volumen geométrico ni deriva una escala física nueva. La existencia de un singlete no vacío puede acreditarse conservando en el corte las funciones bosónicas invariantes y el vacío exterior. La prueba de su existencia no afirma que ese singlete sea el estado físico de menor energía.

La reducción exacta no se obtiene promediando un Hamiltoniano defectuoso a posteriori: procede de (1), del transporte de enlaces y del corte que conserva los multipletes. Tampoco la demostración finita identifica automáticamente todas las restricciones gravitatorias de la realización Einstein–Schrödinger; conserva el operador y las restricciones efectivamente compuestas.

### Positividad temporal finita del sistema interactuante

La autoadjunción anterior permite una afirmación cuántica adicional para el álgebra **par** de observables gauge invariantes del mismo sistema. Sean `0<t₁<⋯<t_k<T`,

\[
B_F=e^{-(T-t_k)H_N^{\rm phys}}A_k
e^{-(t_k-t_{k-1})H_N^{\rm phys}}\cdots A_1e^{-t_1H_N^{\rm phys}},
\quad Z_{2T}=\operatorname{Tr}e^{-2TH_N^{\rm phys}}>0.
\]

La reflexión de una historia invierte el orden y toma adjuntos. El núcleo térmico reflejado es

\[
K(F_i,F_j)=Z_{2T}^{-1}\operatorname{Tr}(B_{F_i}^\dagger B_{F_j}).
\]

**Proposición.** Este núcleo es positivo semidefinido para cualquier corte finito construido arriba, incluida su interacción Yukawa.

**Prueba.** Para `z_i` complejos,
`Σ conjugado(z_i)K(F_i,F_j)z_j=Z⁻¹ Tr(B†B)≥0`, con `B=Σ z_jB_Fj`. Todos los operadores son matrices finitas; la traza y la composición están definidas. □

Así queda construida positividad de reflexión **temporal finita** en la realización operatoria común. No es una medida euclídea continua ni afirma positividad de un determinante quiral. La restricción al álgebra par evita sustituir la reflexión graduada de campos fermiónicos impares por la reflexión bosónica ordinaria. El resultado es compatible con la reducción gauge ya demostrada, porque se calcula en su espacio físico.

## 5. Condiciones exactas de refinamiento con interacción

Los propietarios de Fock demuestran, para un transporte isométrico `J`,

\[
\Gamma(J)c^\dagger(f)=c^\dagger(Jf)\Gamma(J),\qquad
c(Jf)\Gamma(J)=\Gamma(J)c(f).
\]

Para una mera contracción, la segunda identidad conserva `J*`; no se elimina ese adjunto. La functorialidad por sí sola no prueba el transporte de un Hamiltoniano nuevo.

Si `h'J=Jh`, entonces

\[
d\Gamma(h')\Gamma(J)=\Gamma(J)d\Gamma(h).
\tag{5}
\]

**Prueba.** En el grado `n`, cada sumando de `dΓ(h')=Σ_j h'_j` se aplica a `J⊗n`. La identidad de una partícula reemplaza `h'J` por `Jh` en ese factor; sumar y restringir al sector exterior prueba (5). □

Para el bloque de Yukawa, (5) exige los dos cuadrados

\[
Y'J_R=J_LY,\qquad Y'^\dagger J_L=J_RY^\dagger,
\tag{6}
\]

además del transporte de los coeficientes bosónicos y su dominio. El primer cuadrado solo no garantiza el segundo si aparecen modos nuevos: un modo derecho fino exterior a `Ran J_R` puede ser enviado por `Y'` a `Ran J_L`.

Un transporte total `I_B⊗Γ(J)` que satisfaga (6), conserve los enlaces y entrelace la forma base preserva el Hamiltoniano completo por suma. Es un criterio efectivo: cada bloque mixto y su adjunto se comprueban. Los propietarios de Fock aseguran la elevación una vez verificadas estas identidades de los bloques; no publican por ello una prueba automática de (6) para toda interacción que se añada. Para eliminación de modos en lugar de invariancia exacta, se conserva el mecanismo de Schur y memoria del bloque común, sin sustituirlo por `J*H'J=H` como si implicara (5).

## 6. Control quiral bajo refinamiento

La cancelación de anomalías de la representación y la ausencia de duplicaciones fermiónicas son pruebas diferentes. En una realización periódica con derivada central libre,

\[
D_a(p)=\frac{i}{a}\sum_{j=1}^d\gamma_j\sin(ap_j),
\qquad
D_a(p)^\dagger D_a(p)=a^{-2}\sum_j\sin^2(ap_j)I.
\]

Todos los vértices `ap_j∈{0,π}` anulan el símbolo: hay `2^d` ceros. El Hamiltoniano espacial correspondiente tiene ocho conos candidatos en dimensión tres; la formulación euclídea ingenua tiene dieciséis en dimensión cuatro. La cancelación de los coeficientes de anomalía no elimina ninguno de esos ceros.

Este control no afirma que el transporte HMT sea ese retículo periódico: muestra qué falla si se lo reemplaza por esa realización sin una prueba adicional. El [teorema de Nielsen–Ninomiya](https://doi.org/10.1016/0370-2693(81)91026-1) tiene hipótesis concretas; una generación aperiódica no lo contradice por su nombre ni demuestra automáticamente el espectro deseado. Se debe analizar el operador y sus refinamientos efectivos. La [relación de Ginsparg–Wilson](https://doi.org/10.1103/PhysRevD.25.2649) ilustra una realización diferente de la simetría quiral, pero no se la declara ya construida por haberla citado.

Para el corte finito de (3), autoadjunción, covariancia y reducción están demostradas. Una afirmación sobre el límite quiral debe conservar el índice, la multiplicidad de modos bajos, los dominios, la localización y los mapas de refinamiento del operador específico. No se promueve el conteo finito de anomalías a una demostración de ese límite.

## 7. Comprobación material

`verificar_acoplamiento_finito.py` ejecuta 26 controles con biblioteca estándar:

- covariancia quark y leptónica bajo transformaciones simultáneas no triviales;
- recuperación del bloque de masas CKM en una única base coherente;
- interacción finita bosón–fermión que conserva la carga total pero modifica sus ocupaciones separadas;
- autoadjunción y reducción a un sector de carga con interacción no nula;
- positividad del núcleo temporal reflejado en ese sector interactuante;
- controles negativos al congelar indebidamente Higgs, retirar el adjunto, eliminar el operador cargado o cortar un multiplete;
- ceros del símbolo central en una a cuatro dimensiones.

Las comparaciones de grupos usan tolerancia `10⁻¹⁰`; el máximo residuo positivo observado es menor que `4·10⁻¹⁵`. Las pruebas simbólicas anteriores no dependen de esa tolerancia. Las masas y ángulos del test son fixtures arbitrarios para ejercer un enunciado válido para cualquier lector que cumpla las condiciones; no son nuevas entradas de la generación HMT ni predicciones metrológicas.

## 8. Inserción efectiva de la corriente espinorial y la torsión

### 8.1. Revisión del reloj entre fibras de medida

El desarrollo `ACOPLAMIENTO_GRAVITATORIO_MEMORIA_20260929.md` usa
`dμ_x=Z_x⁻¹exp(−S_x)dμ₀` y
`A_x f=√Z_x exp(S_x/2)f`. Su fórmula es correcta como aplicación
`L²(μ₀)→L²(μ_x)`: sustituir en la integral prueba `||A_xf||²_μx=||f||²_μ0`.
El adjunto de Hilbert es `A_x*=A_x⁻¹`, con los dos productos escalares
distintos. No se lo sustituye por la traspuesta conjugada euclídea de una
tabla de sus valores. En coordenadas finitas, la identidad correcta es
`A†W_xA=W₀`, y el reloj transportado satisface `H†W=W H`.

Como `S_x` y `Z_x` son gauge-invariantes, `A_x` entrelaza la acción
gauge; por tanto, transportar con `A=⊕_x A_x` el reloj que mezcla
registros geométricos conserva la reducción interna. La dependencia
geométrica de la medida no obliga a convertir la geometría en fondo fijo.
Los operadores locales de corriente que siguen actúan punto a punto en
`x`; la multiplicación escalar `A_x` transporta también su realización.

### 8.2. Corriente total, no suma de interacciones aisladas

El propietario es
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex`,
líneas 121–221, 229–354 y 360–476. Se leyó su demostración, incluido el
orden normal. Para su acción espinorial afín en contorsión,

\[
\mathcal L_{\rm spin}^{\rm eff}
=C_\gamma q(B)\operatorname{vol}_e,
\qquad C_\gamma=\frac{3\kappa c\hbar^2}{16}
\frac{\gamma^2}{1+\gamma^2}.
\tag{7}
\]

La constante `κ` de (7) es la gravitatoria del propietario, no
`κ_av` del generador gauge. Los factores de acción y Barbero son los
lectores anteriores de la misma cadena.

Con las matrices de Clifford de dicho propietario y `A_D=−ig⁰`, las
cuatro matrices `M_abc=A_Dg^ag^bg^c`, ordenadas `012,013,023,123`, son

\[
(M_1,M_2,M_3,M_4)
=(iJ\otimes R,\ iJ\otimes Z,\ iI\otimes J,\ iZ\otimes J).
\]

Son hermíticas, de cuadrado identidad y conmutan con
`γ₅=ig⁰g¹g²g³`. Así, al conservar la realización quiral, se usan

\[
\widetilde M_a=
(M_a|_{S_L}\otimes I_{E_L})\oplus
(M_a|_{S_R}\otimes I_{E_R}),
\qquad \widehat B_a=d\Gamma(\widetilde M_a).
\]

No se impone la misma representación interna a izquierda y derecha.
La conmutación con `γ₅` hace bien definidas ambas restricciones, y
`[\widetilde M_a,ρ_L(g)⊕ρ_R(g)]=0`. La corriente suma las
especies y sus multiplicidades **antes** de eliminar la contorsión.
Con `s=(−1,−1,−1,+1)`, el operador resultante es

\[
\boxed{\widehat Q_{\rm tot}
=\sum_{a=1}^4s_a
\left[d\Gamma(\widetilde M_a)^2
-d\Gamma(\widetilde M_a^2)\right]
=\sum_as_a\widehat B_a^2+2\widehat N.}
\tag{8}
\]

El último paso utiliza `\widetilde M_a²=I` en el portador recibido.
El orden normal se refiere al vacío exterior declarado. La primera
fórmula sigue siendo válida aunque se trabaje en bloques sin esa
normalización de cuadrado.

Si las especies se descomponen como `B_a=Σ_f B_{a,f}`, (8) contiene
`2Σ_{f<g,a}s_a B_{a,f}B_{a,g}`, además de los términos individuales.
Descartar esos términos cruzados equivale a sustituir la eliminación
de una conexión común por varias conexiones independientes. La prueba
computacional de ocho modos detecta exactamente esa diferencia.

### 8.3. Hamiltoniano torsional común y prueba

En la celda homogénea del propietario, `V=a³V_c`, y la variación del
lapse da `E_spin=−c C_γ q/V`. La inserción operatoria con el mismo
orden es, por tanto,

\[
\boxed{H_{\rm tor}(x)
=-\sum_{v\in V}\frac{N_v(x)cC_\gamma(x)}{\mathcal V_v(x)}
\widehat Q_{{\rm tot},v}(x).}
\tag{9}
\]

Para varias celdas, (9) es la realización celular por modos locales
normalizados en sus volúmenes, sin identificarla con una interpolación
continua única. La carta exige volúmenes positivos. En un corte
geométrico finito no degenerado, sus inversos están acotados; lapse y
coeficientes conservan sus lectores. En la carta de registro estos
coeficientes son multiplicaciones reales. Aunque el reloj mezcle
registros distintos, cada bloque de (9) es hermítico.

**Proposición.** En esa carta, el operador

\[
\mathbb H_N^{\rm spin}
=P_N(H_{\rm base}^{\rm red}+\widehat H_Y+H_{\rm tor})P_N
\tag{10}
\]

es autoadjunto y conserva la reducción gauge de §4. En general, su
acoplamiento con el reloj geométrico no se anula.

**Prueba.** Cada `B_a` es hermítico y la sustracción normal de (8)
es hermítica; por ello `Q_tot` lo es. La representación interna
conmuta con cada `\widetilde M_a`; segunda cuantización y productos
preservan esa conmutación. La transformación de marco de espín
transporta conjuntamente sus componentes y su contracción. Los
coeficientes reales de (9) son gauge-invariantes. El mismo argumento
de compresión y promedio de Haar de §4 se aplica a (10). Finalmente,
si el reloj tiene un bloque no nulo entre `x` e `x'` y los operadores
`C_γ Q/V` de esos registros difieren, el conmutador con (9) tiene un
bloque no nulo. La geometría intercambia energía con este término,
sin alterar la invariancia gauge. □

`H_base^red` especifica la **carta efectiva después de eliminar la
contorsión del sector afín**. No se mantiene como grado independiente
el mismo acoplamiento lineal espín–contorsión cuya eliminación produjo
(7). Los transportes de los observables completos pueden reconstruirse
desde `ω=ω_LC+K_*[Σ_fσ_f]`, mediante la inversa del propietario;
el término de energía no se vuelve a contar por segunda vez.

Hay una distinción operacional concreta con el bloque de respuesta
`D_T*WD_T`: si se pretende incluirlo también como una dependencia
independiente de `K` **antes** de la eliminación, debe intervenir su
variación. Escribir el sector previo como

\[
\tfrac12\langle K,\mathcal A_eK\rangle
+\langle J_D,K\rangle+R(K)
\]

da la ecuación `A_eK+J_D+δR/δK=0`. La fórmula (7) corresponde al
problema afín de VIII/33; no equivale a omitir `δR/δK` de un problema
distinto. La composición (10) es la realización efectiva explícita,
con su base ya reducida, y no declara equivalencia con todas las
restricciones PCH. Si se elige conservar el problema no lineal de
extensión mínima, se usa su inversión propia y no se le injerta (7)
como una segunda eliminación.

No se sustituye el segundo momento por el cuadrado de la corriente
media: el propietario da un estado con todas las medias nulas y
`<Q_sp>=4`. Tampoco se deduce conservación de `<Q_tot>` de la sola
conservación del número. Su balance exacto en el sistema acoplado es
`d<Q_tot>/dt=(i/ℏ)<[H,Q_tot]>`, más cualquier dependencia explícita
del lector. El Hamiltoniano de (10) es válido sin imponer que ese
conmutador se anule.

### 8.4. Verificación independiente

`verificar_torsion_fock.py` pasó **34/34 controles**. Reconstruye las
matrices desde Clifford, comprueba quiralidad y hermiticidad, produce
la matriz exacta de seis estados con dos ocupaciones de VIII/33 y
recupera las restricciones `0,0,4I,8I` para ocupaciones `0,1,3,4`.
Verifica los términos cruzados de dos copias espinoriales, la
invariancia bajo mezcla interna, el acoplamiento no trivial a dos
volúmenes geométricos y el adjunto correcto entre dos medidas.

Los controles negativos fallan al omitir el orden normal, al separar
las corrientes antes de elevar al cuadrado o al usar el adjunto
euclídeo entre fibras de distinta medida. Estas comprobaciones no
repiten el cálculo previo de anomalías.
