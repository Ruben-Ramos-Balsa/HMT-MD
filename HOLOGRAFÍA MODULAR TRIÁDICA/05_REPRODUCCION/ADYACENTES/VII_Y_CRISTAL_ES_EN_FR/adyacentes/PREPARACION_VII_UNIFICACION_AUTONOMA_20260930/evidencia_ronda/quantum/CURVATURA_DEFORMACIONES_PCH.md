# Curvatura de deformaciones: variación de corriente, marco y operador de Dirac

Prueba focal nueva, 29 de septiembre de 2026. Se calcula la conexión de
evolución entre hipersuperficies del operador espinorial de la acción
recibida. No se define un Hamiltoniano como un puro cambio de marco
para obtener después curvatura cero por definición: primero se deriva
el generador a partir de la ecuación y de su corriente conservada.

## 1. Procedencia y alcance exacto

Se conserva el antecedente APP → TRIT → TPK → estado enriquecido →
estructura discreta conjunta del continuo, con sus hojas, orientación,
residuos, cocientes, ruta, frontera, acarreo y memoria. Se reutiliza el
[recibo genealógico](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/RECIBO_GENEALOGIA.json>).
El operador se realiza después de esos datos; las secciones de acción
y velocidad recibidas no son parámetros calibrados en esta prueba.

Los propietarios materiales utilizados, sin modificar sus fuentes, son:

- [VIII/30d](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30d_realizacion_geometrica.tex>), soldadura y realización de holonomías: coframe, conexión y lift de espín del transporte TPK.
- [VIII/33](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex>), `vii:eq:clifford-material-explicito`, `vii:eq:adjunto-conexion-espinorial`, `vii:eq:accion-dirac-material`, líneas 50–119: representación, conexión y acción espinorial de primer orden. Las líneas 171–221 separan la interacción cuártica de torsión obtenida por eliminación.
- [VIII/31](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex>), `vii:prop:fuente-metrica-balance`, líneas 401–452: balance de la fuente total y su identidad de Noether sobre las ecuaciones materiales.
- [11p, Legendre PCH y Einstein–Schrödinger](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex>): equivalencia variacional de la misma acción y realización cuántica con dominio y cierre tipados.
- [CONMUTADOR_ESPACIAL_ESPINORIAL.md](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/CONMUTADOR_ESPACIAL_ESPINORIAL.md>): conmutador a geometría fija y término adicional de un potencial general.
- [DEFORMACIONES_ESPACIALES_Y_QUIRALIDAD.md](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/DEFORMACIONES_ESPACIALES_Y_QUIRALIDAD.md>): naturalidad de las fibras, dominios y límites sobre núcleo suave.

El teorema que sigue realiza el **operador de Dirac lineal completo en
los campos geométricos y materiales suaves declarados**. Admite masa,
mezcla/Yukawa y conexiones internas con potencial temporal, no sólo
el cinético libre. Esos campos son coeficientes del problema lineal.
No representa como un potencial lineal la interacción cuártica de
corriente ni convierte los coeficientes geométricos en operadores de
una métrica cuántica dinámica. Esa diferencia queda localizada en §7.

## 2. Corriente y operador en una carta espaciotemporal

La acción espinorial simétrica de VIII/33, en una carta temporal y una
trivialización de espín, tiene una ecuación de primer orden de la forma

\[
 i\hbar\partial_t\psi=L(t)\psi,
 \qquad L=-i\hbar A^i(t,x)\partial_i+B(t,x).
 \tag{1}
\]

La densidad positiva y el flujo de la corriente de esa acción se escriben

\[
 \rho=\psi^\dagger K\psi,\qquad
 j^i=\psi^\dagger J^i\psi,\qquad
 J^i=KA^i=(J^i)^\dagger,\qquad K=K^\dagger>0.
 \tag{2}
\]

Aquí K contiene el producto de corriente y la densidad coordenada; no
es el registro dodecafásico K ni el Hamiltoniano de reloj llamado 𝕂
en otras notas. El espín, el
coframe y las conexiones de la acción determinan A, B y K. Derivar
(2) usando (1) prueba que la conservación local es exactamente

\[
 \boxed{\dot K+\partial_iJ^i
       +\frac{i}{\hbar}(B^\dagger K-KB)=0.}
 \tag{3}
\]

En un marco plano normalizado, K=I, A^i=cα^i y B=V=V†, luego (3)
es inmediata para cualquier potencial matricial hermítico V(t,x).
Incluye los bloques de masa/Yukawa hermíticos y un potencial gauge
temporal: no se exige \(\{V,\alpha^i\}=0\).

Para una geometría curva, (3) es la forma coordenada de la corriente
covariante conservada del mismo Dirac, con la densidad de volumen
incluida. Los términos de conexión, normal y volumen no se suprimen.
Las hipótesis de realidad/hermiticidad de la acción y de su conexión
son las que garantizan esa corriente. Si una realización material no
satisface (3), no se le aplica silenciosamente el teorema.

## 3. Restricción a una gráfica y generador obtenido de la ecuación

Sea \(X_f(x)=(f(x),x)\) una hipersuperficie espacial de Cauchy en
esa carta. Para una solución de (1), póngase
\(u_f(x)=\psi(f(x),x)\). El flujo a través de la gráfica da

\[
 Q_f=K_f-J_f^i\partial_i f>0,\qquad
 \|u_f\|_f^2=\int u_f^\dagger Q_f u_f\,dx.
 \tag{4}
\]

El subíndice f significa evaluación en t=f(x), antes de aplicar la
derivada espacial a u. Suponemos positividad uniforme en la familia
de gráficas considerada. En Minkowski esto es
\(Q_f=I-c\alpha(df)\), con \(c|df|<1\). En una familia compacta
uniformemente espacial hay cotas positivas comunes de Q y Q⁻¹.

La regla de la cadena \(\partial_i u_f=(\partial_i\psi)_f+
f_i(\partial_t\psi)_f\), sustituida en (1), produce

\[
 i\hbar(\partial_t\psi)_f
 =(I-A_f^if_i)^{-1}L_f u_f
 =Q_f^{-1}T_f u_f,
 \qquad T_f=K_f(-i\hbar A_f^i\partial_i+B_f).
 \tag{5}
\]

Tomemos \(S_f=Q_f^{1/2}\), \(R_f=S_f^{-1}\), y la semidensidad
normalizada \(v_f=S_fu_f\) en el espacio fijo L²(dx). Para una
variación vertical de gráfica \(\delta_M f=M\), (5) da el generador
**derivado**, con todos sus términos:

\[
 \boxed{\mathcal H_M(f)
 =M R_fT_fR_f+i\hbar S_MR_f,\qquad
 S_M=\delta_M S_f,\qquad
 i\hbar\delta_M v_f=\mathcal H_M(f)v_f.}
 \tag{6}
\]

El segundo término no es opcional. No se obtiene congelando la
métrica ni aplicando sólo la regla \(H_M=MH\) a cada superficie.
Surge al normalizar la corriente de la acción sobre esa superficie.

### Simetría y términos de densidad

Definamos \(q_0=\dot K_f-\dot J_f^if_i\). Las derivadas son

\[
 Q_M=Mq_0-J_f^i\partial_iM,\qquad
 S_fS_M+S_MS_f=Q_M.
 \tag{7}
\]

La segunda es una ecuación de Sylvester con solución hermítica única
porque S es positivo. De (3), recordando
\(\partial_i(J_f^i)=(\partial_iJ^i)_f+\dot J_f^if_i\), se obtiene

\[
 T_f-T_f^\dagger=-i\hbar q_0.
 \tag{8}
\]

Por tanto la diferencia entre el primer término de (6) y su adjunto
es \(-i\hbar R_fQ_MR_f\). La diferencia para el segundo es
\(i\hbar(S_MR_f+R_fS_M)=i\hbar R_fQ_MR_f\). Se cancelan
exactamente. Así (6) es simétrico sobre el núcleo suave, incluso
cuando los términos separados no lo sean.

## 4. Cálculo explícito de las variaciones y de la curvatura

Las siguientes expresiones permiten calcular los términos de variación
sin introducir un transporte plano por definición:

\[
 \begin{aligned}
 Q_N&=N(\dot K_f-\dot J_f^if_i)-J_f^i\partial_iN,\\
 S_N&=\int_0^\infty e^{-sS_f}Q_Ne^{-sS_f}\,ds,\\
 R_N&=-R_fS_NR_f,\\
 Q_{NM}&=NM(\ddot K_f-\ddot J_f^if_i)
       -\dot J_f^i(N\partial_iM+M\partial_iN),\\
 S_fS_{NM}+S_{NM}S_f&=Q_{NM}-S_NS_M-S_MS_N.
 \end{aligned}
 \tag{9}
\]

En particular \(S_{NM}=S_{MN}\). Con todos los factores en su orden,

\[
 \begin{aligned}
 \delta_N\mathcal H_M
 ={}&M(R_NT_fR_f+R_f(N\dot T_f)R_f+R_fT_fR_N)\\
 &+i\hbar(S_{NM}R_f+S_MR_N),\\
 \delta_N\mathcal H_M-\delta_M\mathcal H_N
 ={}&M(R_NT_fR_f+R_fT_fR_N)
       -N(R_MT_fR_f+R_fT_fR_M)\\
 &+i\hbar(S_MR_N-S_NR_M).
 \end{aligned}
 \tag{10}
\]

El término \(NM\dot T_f\) y la segunda derivada S_NM se cancelan
en la antisimetrización, pero no sus términos de primer orden. (9)–(10)
son válidas para métrica y potencial dependientes de t y x.

### Evaluación no homogénea en una hoja plana

Sea \(L_0=-i\hbar c\alpha^i\partial_i+V(t,x)\), con V hermítico
general. En f=0, \(S=R=I\). Escribamos
\(a_N=\alpha(dN)\),
\(v=N\operatorname{grad}M-M\operatorname{grad}N\),

\[
 \mathcal T_{NM}=\nabla_v+\tfrac12\operatorname{div}v
                     +\tfrac14[a_N,a_M],\qquad
 \mathcal W_V=N\{V,a_M\}-M\{V,a_N\}.
 \tag{11}
\]

Se tiene \(S_N=-ca_N/2\), \(R_N=ca_N/2\) y
\(S_{NM}=-c^2\{a_N,a_M\}/8\). Sustituir en (6) y (10) da

\[
 \boxed{\mathcal H_M(0)=\tfrac12(ML_0+L_0M),}
 \tag{12}
\]

\[
 \boxed{\delta_N\mathcal H_M-\delta_M\mathcal H_N
       =i\hbar c^2\mathcal T_{NM}-\tfrac c2\mathcal W_V.}
 \tag{13}
\]

La prueba usa
\(\{L_0,a_N\}=-i\hbar c(2\nabla_{\mathrm{grad}N}+\Delta N)
+\{V,a_N\}\). El conmutador del operador (12), calculado sin
descartar V, es

\[
 [\mathcal H_N,\mathcal H_M]
 =-\hbar^2c^2\mathcal T_{NM}
  -\frac{i\hbar c}{2}\mathcal W_V.
 \tag{14}
\]

Las deformaciones verticales de gráfica con N,M fijos conmutan. Por
(13)–(14),

\[
 \boxed{\mathcal F_{NM}
 =\delta_N\mathcal H_M-\delta_M\mathcal H_N
   +\frac{i}{\hbar}[\mathcal H_N,\mathcal H_M]=0.}
 \tag{15}
\]

Los gradientes de lapsos arbitrarios y la rotación espinorial se
cancelan por separado. También se cancela el término del potencial
temporal que era un falsador del conmutador aislado. La variación de
V con t contribuye simétricamente como NM·dot V y no altera (15).
Así se ha calculado el término que no contenía el conmutador a
geometría congelada.

## 5. Gráficas generales: prueba de integrabilidad y dominios

**Teorema.** Considérese el problema lineal (1) derivado de la acción,
con corriente (2)–(3), coeficientes suaves, y una región globalmente
hiperbólica con superficies de Cauchy compactas sin borde. Para una
familia suave de gráficas de Cauchy uniformemente espaciales, el
operador (6) determina una evolución unitaria de sus datos, preserva
H¹ y el núcleo suave, y satisface (15) en toda gráfica de la familia,
no sólo en f=0.

**Prueba.** El problema de Dirac es simétrico hiperbólico. En cada
intervalo compacto de la familia, Q y Q⁻¹ y los coeficientes necesarios
están acotados. La identidad (3) da la estimación L² sin pérdida.
Conmutar derivadas espaciales hasta orden s y usar la simetría del
símbolo principal da
\(\partial_\lambda\|v\|_{H^s}^2\le C_s\|v\|_{H^s}^2\).
Regularizar espacialmente, resolver los problemas regularizados y
usar estas cotas produce el propagador; la misma estimación para la
diferencia da unicidad. Se obtiene invariancia de cada H^s y del
núcleo C∞; el argumento inverso da un propagador invertible.

La corriente mixta, obtenida polarizando (2), también se conserva.
Aplicar Stokes entre dos gráficas prueba que restringir la **misma
solución** a ambas conserva su producto. Sea \(\mathcal R_f\) la
restricción normalizada por S_f desde una superficie de referencia.
Por el problema de Cauchy, es sobreyectiva y unitaria. La regla de la
cadena y (5) ya han demostrado, antes de usar su cociclo,

\[
 i\hbar\delta_M\mathcal R_f=\mathcal H_M(f)\mathcal R_f.
 \tag{16}
\]

La dependencia suave respecto de f se obtiene diferenciando el mismo
problema hiperbólico, con pérdida controlada de una derivada por
variación. En C∞ se pueden intercambiar dos variaciones. Aplicar
\([\delta_N,\delta_M]=0\) a (16) produce
\(-i\mathcal F_{NM}\mathcal R_f/\hbar=0\). La sobreyectividad y la
invariancia del núcleo implican \(\mathcal F_{NM}=0\). No se definió
H por este resultado: H fue obtenido en (5)–(6), su variación está
calculada en (9)–(10), y (16) lo identifica con la misma ecuación. ∎

La expresión (6) actúa continuamente H¹→L². Si M se anula, no es
necesariamente elíptica y no se identifica su dominio autoadjunto
máximo con H¹. El teorema usa el propagador simétrico hiperbólico y
su núcleo común, no esa falsa igualdad de dominios. Cuando M está
separado de cero y el símbolo espacial de Dirac es elíptico, su
realización congelada tiene el dominio H¹ habitual. Para una hoja
no compacta o con borde se necesitan las hipótesis de soporte/cotas
y el flujo de borde del problema de Cauchy; no se omiten por cambiar
el signo del régimen trítico.

El argumento curvo no introduce nuevas ecuaciones físicas. Utiliza la
ecuación espinorial y su corriente de la acción recibida, en un dominio
globalmente hiperbólico declarado. La acción fuente no implica que toda
geometría o toda elección global de borde satisfaga ese dominio.

## 6. Normales físicas, cambios de marco y graduación quiral

Los vectores verticales \(N\partial_t\) de las gráficas no son los
campos normales \(Nn_X\) sobre embeddings parametrizados. En el
segundo caso varían la normal y la parametrización espacial; su
corchete contiene el desplazamiento tangencial de la nota TRIT.

Para un embedding espacial orientado X, la restricción de una solución
y su corriente define la misma aplicación \(\mathcal R_X\), ahora
con el lift de espín y la densidad de X. En un marco unitario suave,
sea H_N el generador obtenido por la regla de la cadena de esa
restricción, incluyendo sus componentes tangencial, normal y de
marco. Repetir la última línea de la prueba con
\([\delta_N,\delta_M]=\delta_{[N,M]}\) da

\[
 \boxed{\delta_NH_M-\delta_MH_N-H_{[N,M]}
              +\frac{i}{\hbar}[H_N,H_M]=0.}
 \tag{17}
\]

En una descomposición horizontal que deja la rotación de espín o el
calibre como componente vertical separada, (17) se expresa módulo
esa acción vertical y su restricción de Gauss. No se borra el cargo
tangencial ni se toma una normal congelada para obtener (17).
Un cambio unitario de marco \(v'_X=U_Xv_X\) modifica

\[
 H'_N=U_XH_NU_X^*+i\hbar(\delta_NU_X)U_X^*,
 \qquad \mathcal F'_{NM}=U_X\mathcal F_{NM}U_X^*.
 \tag{18}
\]

Esta es la conexión total de la misma evolución, no sólo la conjugación
de un Hamiltoniano congelado. Los lifts se componen con su signo;
una posible holonomía global de spin no se elimina mediante una
elección independiente de signos en cada paso.

La densidad de corriente y los cambios de marco propios preservan la
graduación Γ5 del módulo espaciotemporal. En el caso plano, Q_f y S_f
conmutan con Γ5 porque las α lo hacen; por naturalidad ocurre lo
mismo en los marcos correspondientes. Una masa o Yukawa puede mezclar
L/R. La prueba de (15) y (17) conserva esa mezcla completa, no supone
conservación de carga axial ni añade representaciones derechas.

La elevación al espacio exterior también tiene una identidad explícita.
Sobre el Fock exterior con vacío de cero partículas, la unitaria de Cauchy U
se eleva por Γ₋(U)=⊕_n ∧ⁿU. En el núcleo de número finito de partículas y
factores suaves, el generador es dΓ(H_N), sus variaciones son
dΓ(δ_NH_M) y [dΓ(H_N),dΓ(H_M)]=dΓ([H_N,H_M]). Así la curvatura
elevada es dΓ(F_NM)=0, sin desechar los bloques de mezcla. Tensorizar
esta realización con identidades permite compararla con otras fibras
en un espacio común. Este resultado usa esa representación exterior:
no afirma implementabilidad en un vacío polarizado de energía negativa
ni construye por sí solo el acoplamiento cuántico con la geometría.

Para el límite espacial se puede fijar en esta carta un corte espectral
P_R del cinético de una superficie de referencia. Entonces δ_NP_R=0.
Los operadores (6), (10) tienen orden uno con coeficientes suaves, y
los productos de (14) tienen orden a lo sumo dos. La convergencia de
P_R en H^s, demostrada en la nota de deformaciones, da para N,M,f
fijos y ψ suave

\[
 \mathcal F^{(R)}_{NM}\psi
 =\frac{i}{\hbar}\left(
 [P_RH_NP_R,P_RH_MP_R]-P_R[H_N,H_M]P_R\right)\psi
 \longrightarrow0.
 \tag{22}
\]

Las derivadas de (10) también pasan al límite H¹→L² sobre ese núcleo;
no se ha controlado solamente el conmutador congelado. El corte puede
preservar la graduación Γ5 del cinético de referencia aunque el
Yukawa mezcle L/R. No se afirma que la curvatura del corte finito sea
cero ni que (22) sea uniforme sobre lapsos arbitrariamente oscilantes.

Un corte espectral **móvil** P_R(f) puede saltar al cruzar un autovalor
el umbral. No se le atribuye diferenciabilidad por la sola suavidad de
la métrica: deben incluirse sus variaciones/segundas formas, o usarse
un regulador suave con los controles correspondientes. Tampoco se
identifica el regulador espectral añadido con el refinamiento nonádico
del productor. Así se separa el límite probado en una carta común de
una afirmación distinta sobre todas las familias móviles de cortes.

### Límite conjunto de precisión de lectores y corte espacial graduado

Sea m el índice de precisión de las **salidas ya generadas** HMT,
no una entrada elegida por comparación física. Mantengamos la carta,
el coframe suave, los campos materiales externos y sus espacios
quirales. Sus lecturas aproximantes \(\hbar_m,c_m,V_m\) y los
coeficientes A_m,B_m,K_m se obtienen mediante las mismas fórmulas
suaves de esas salidas. Se conservan denominadores separados de cero,
\(\hbar_m\ge\hbar_*>0\), y positividad uniforme \(Q_{m,f}\ge q_*I\)
en la familia de gráficas. Suponemos convergencia de los coeficientes
en C^k con las cotas de derivadas que utiliza cada estimación.

Cada conexión se reconstruye de **su propia corriente** por (3)–(10):
no se combina el Hamiltoniano de una precisión con el producto interno
de otra. En consecuencia,
\(\mathcal F^{(m)}_{NM}=0\) para cada m. La ecuación de Sylvester
tiene inversa uniformemente acotada por \(1/(2\sqrt{q_*})\); sus
derivadas sucesivas muestran que S_m,R_m y los coeficientes de H_m
heredan las cotas y convergencias indicadas.

Tomemos un mismo P_R espectral de referencia que conmuta con Γ5 y es
independiente de f y m. Para \(\psi\in H^{2+r}\), r>0 entero, el
resto espectral cumple
\(\|(I-P_R)u\|_{H^s}\le C(1+R^2)^{-r/2}\|u\|_{H^{s+r}}\),
usando unidades fijas del operador de referencia. El primer orden de
H_{m,N}, con normas H^{s+1}→H^s uniformes en m, da

\[
 \boxed{\|\mathcal F^{(m,R)}_{NM}\psi\|_{L^2}
 \le \frac{C_{N,M,r}}{\hbar_*}(1+R^2)^{-r/2}
                         \|\psi\|_{H^{2+r}}.}
 \tag{23}
\]

**Prueba de la cota.** Por (22) y la identidad de compresión, el
defecto es la diferencia de
\(P_RH_{m,M}(I-P_R)H_{m,N}P_R\) y el término intercambiado,
multiplicada por i/ℏ_m. Acotar el primer H de H¹ a L², aplicar el
resto espectral de H^{1+r} a H¹, y acotar el segundo H de H^{2+r}
a H^{1+r} prueba (23). La cota de P_R en las normas espectrales es
uno; la equivalencia con Sobolev sólo altera C. La convergencia
suave y la positividad uniforme hacen independiente de m esa
constante. ∎

Así, para cualquier diagonal \(m_j\to\infty\), \(R_j\to\infty\),

\[
 \mathcal F^{(m_j,R_j)}_{NM}\psi\longrightarrow0,
 \qquad P_{R_j}H_{m_j,N}P_{R_j}\psi\longrightarrow H_N\psi,
 \quad \psi\in C^\infty.
 \tag{24}
\]

La segunda afirmación suma el error de coeficientes H_m−H y los
errores espectrales de orden uno; las variaciones (10) tienen la
misma convergencia. Se trata de un límite conjunto real de precisión
y espacial, graduado por el mismo Γ5, con Yukawa retenido. No exige
que el Hamiltoniano masivo conmute con Γ5. Conserva asimismo la
distinción entre este regulador añadido y el refinamiento nonádico,
y no constituye un límite de una interacción cuártica de campos que
no figure como operador lineal de (1).

## 7. Ward PCH y el residuo mínimo del operador total

La identidad de Noether del propietario VIII/31 no es sólo una
conservación separada del Dirac libre: conserva la fuente métrica
total, incluida la contribución de la torsión eliminada. Antes de
eliminar la conexión, escribamos la variación como
\(\delta L=\delta e^I\wedge\mathcal E_I+
\delta\omega^{IJ}\wedge\mathcal E^\omega_{IJ}
+\delta A\wedge\mathcal E_A+\delta\Psi\,\mathcal E_\Psi+
\mathrm d\theta\), con adjuntos incluidos. Para una difeomorfía
covariantizada,

\[
 \delta_\xi e^I=D(\iota_\xi e^I)+\iota_\xi T^I,
 \quad\delta_\xi\omega=\iota_\xi F,\quad
 \delta_\xi A=\iota_\xi F_A,\quad
 \delta_\xi\Psi=\iota_\xi D\Psi.
 \tag{19}
\]

La invariancia de la misma acción e integración por partes de
\(D(\iota_\xi e)\) dan la identidad Ward clásica integrada

\[
 \int\left[-(\iota_\xi e^I)D\mathcal E_I
 +(\iota_\xi T^I)\wedge\mathcal E_I
 +(\iota_\xi F^{IJ})\wedge\mathcal E^\omega_{IJ}
 +(\iota_\xi F_A)\wedge\mathcal E_A
 +(\iota_\xi D\Psi)\mathcal E_\Psi+\mathrm{adj.}\right]=0.
 \tag{20}
\]

Se toman variaciones de soporte interior o los cargos de borde de la
acción. Al imponer las ecuaciones, (20) da el balance de VIII/31 y
la propagación de las restricciones clásicas. La eliminación algebraica
de contorsión conserva (20), pues su término de regla de la cadena se
anula por estacionariedad; no se suma la contorsión independiente a
su interacción cuártica ya reducida.

La prueba lineal anterior descarga efectivamente la parte de evolución
espinorial en una geometría y campos dados. Para el **operador total**,
escribamos en el mismo dominio y representación
\(H_N^{\rm tot}=H_N^D+\mathcal V_N\), donde \(H_N^D\) es el
operador identificado por (5)–(6), y \(\mathcal V_N\) conserva los
momentos geométricos y las interacciones cuánticas restantes que
efectivamente tenga esa realización. Sin suprimir términos, el residuo
exacto es

\[
 \boxed{\begin{aligned}
 \mathcal F^{\rm tot}_{NM}={}&
 \delta_N\mathcal V_M-\delta_M\mathcal V_N-\mathcal V_{[N,M]}\\
 &+\frac{i}{\hbar}\bigl(
 [H_N^D,\mathcal V_M]+[\mathcal V_N,H_M^D]
 +[\mathcal V_N,\mathcal V_M]\bigr).
 \end{aligned}}
 \tag{21}
\]

(21) utiliza la cancelación demostrada, no una conjetura sobre la parte
Dirac. La identidad clásica (20) no convierte automáticamente esos
productos operatorios y sus dominios en una Ward cuántica sin términos
de contacto. Para anular (21) en la realización total deben calcularse
sus operadores reales; sustituir \(\mathcal V_N=0\) cambiaría el
problema. Esta fórmula es la diferencia precisa que queda entre el
resultado probado aquí y el cierre cuántico completo solicitado, no
una declaración de inexistencia de ese cierre en el corpus.

## 8. Certificado focal

[verificar_curvatura_deformaciones_pch.py](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/verificar_curvatura_deformaciones_pch.py>) calcula en aritmética
racional gaussiana los dos lados de (13)–(15) con lapsos no homogéneos,
masa variable y potencial hermítico que no anticomuta con Clifford.
Comprueba por separado que omitir la variación de S deja un defecto
no nulo. La prueba para gráficas generales, dominios y métrica curva
es la anterior; no se reemplaza por los ejemplos del certificado.
