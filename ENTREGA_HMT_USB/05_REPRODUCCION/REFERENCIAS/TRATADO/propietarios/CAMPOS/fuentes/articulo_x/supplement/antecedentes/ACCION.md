# Acción, transporte de memoria y conservación variacional HMT–MD

Fecha: 11 de septiembre de 2026. Nota de desarrollo; no modifica publicaciones.

## 1. Premisas y fuentes

Se reciben el estado enriquecido APP–TRIT–TPK y sus lecturas de acción, forma y reloj ya construidas. APP conserva hojas suma/producto, residuo y cociente; TRIT fija régimen y orientación; TPK transporta acarreo, ruta, frontera y memoria. La realización variacional sucede a esa construcción y recibe sus salidas. Una carga particular no sustituye el registro completo ni disgrega la estructura discreta conjunta del continuo.

El resultado es una formalización de la conservación evolutiva mediante tres identidades: una carga radional de Noether, un transporte canónico entre formas sucesivas y una descomposición de carga entre lectura y memoria. El Hamiltoniano elíptico, la acción del reloj y el balance material–espín son RESULTADO_RECUPERADO. La prueba reunida y el término de conexión de §3 son FORMALIZACION_NUEVA respecto de los propietarios leídos; no se atribuye novedad histórica a los métodos generales de Noether.

### Localizadores exactos

**I. Integral activo de 2.249 páginas.** Prefijo de fuente:

/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/

- sections/md/11d_regimenes_cuadraticos_lector_temporal.tex:134: espacio de 108 estados, desplazamiento, Hamiltoniano; :208: acción CLK4–CLK5 y ecuación variacional.
- sucesor_102/radion_52/snippets/c52_06_03_oscilador_lc.tex:6: realización LC, forma, reloj, acción; :64: conjugación y evolución bidireccional.
- sucesor_102/radion_52/c52_12_conservacion_evolutiva.tex:115: balance visible, memoria, radial, vacancias, radiación y retorno; :234: monodromía y memoria; :274: unidad radional y acción de fase.

**II. Artículo de acción y Barbero.** Prefijo:

/Users/ruben/Documents/New project/output/APERTURAS_PAPER_RESTAURADAS_20260911_REV03/II_BARBERO_CKM_ACCION/

- manuscrito/sections/05_accion.tex:7: cociente determinantal; :96: lectores; :136: secciones de acción anterior/posterior al retorno.
- manuscrito/sections/07b_geometria_elipse.tex:10: procedencia APP–TRIT–TPK; :81: ley areal; :112: signo de recorrido; :216: realización LC.
- manuscrito/sections/07c_covarianza_accion.tex:19: matriz de forma; :138: transformación canónica; :180: Hamiltoniano elíptico.
- fuentes/propietarios_II/D04/FORMA_ELIPTICA_RADIO_MODULAR_ACCION_ORIENTADA.md:3: forma y reciprocidad; :76: matrices de transporte; :95: acción orientada; :125: cambio de sección.

**VII. Artículo de gravitación.** Prefijo:

/Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/VII_GRAVITACION/manuscrito/

- 31_corriente_y_respuesta_cartan.tex:355: fuentes variacionales y balance covariante total.
- 60_tensor_residual_y_balance.tex:38: residual; :116: separación de traza e intercambio.

El origen de cada parámetro permanece explícito: \(A,C^*,\hbar\) son salidas de los propietarios II; \(108\) pertenece al calendario; \(t_0>0\) pertenece a la realización temporal declarada. No se escoge una energía, una masa ni una constante convencional objetivo. La prueba utiliza estas salidas legítimas como datos de su etapa posterior.

## 2. La acción radional es una carga de Noether

Se fija una sección positiva de acción \(\hbar\), el par angular \(A,C^*\) en una misma unidad, \(A\ne0\), \(|C^*/A|<1\), y

\[
\eta=\operatorname{artanh}(C^*/A).
\]

El plano realizado \(\mathcal P_\eta\) tiene coordenadas \((Q,P)\), ambas de dimensión raíz de acción, con

\[
\lambda=P\,dQ,\qquad \Omega=dQ\wedge dP=-d\lambda.
\]

Los propietarios I y II ya dan

\[
\mathcal I_\eta(Q,P)=\frac12(e^{-\eta}Q^2+e^\eta P^2),
\qquad H_\eta=\omega\mathcal I_\eta,\qquad \omega>0.
\tag{1}
\]

La elipse HMT es \(\mathcal I_\eta=\hbar\). Su área es \(2\pi\hbar\); \(\mathcal I_\eta\) tiene dimensión de acción y \(H_\eta\) de energía. Definimos las matrices ya realizadas

\[
M_\eta=\operatorname{diag}(e^{\eta/2},e^{-\eta/2}),\quad
J_2=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
R_\eta(\varepsilon)=M_\eta e^{-\varepsilon J_2}M_\eta^{-1}.
\tag{2}
\]

**Proposición 1.** El grupo \(R_\eta\) es una simetría canónica de la acción

\[
\mathscr S_\eta[z]=\int_{t_a}^{t_b}
\left(P\dot Q-\omega\mathcal I_\eta(Q,P)\right)dt
\tag{3}
\]

y su carga de Noether es \(\mathcal I_\eta\).

**Prueba.** El determinante de \(M_\eta\) es uno y \(M_\eta^{\mathsf T}J_2M_\eta=J_2\). Además,
\(\mathcal I_\eta(M_\eta y)=\|y\|^2/2\), invariante bajo \(e^{-\varepsilon J_2}\).
El generador

\[
X_\eta=e^\eta P\,\partial_Q-e^{-\eta}Q\,\partial_P
\]

satisface \(\iota_{X_\eta}\Omega=d\mathcal I_\eta\). Por la fórmula de Cartan,

\[
\mathcal L_{X_\eta}\lambda=dF_\eta,\qquad
F_\eta=\lambda(X_\eta)-\mathcal I_\eta=e^\eta P^2-\mathcal I_\eta.
\]

Como \(X_\eta H_\eta=0\), la variación de la densidad de acción es \(dF_\eta/dt\). Su carga es

\[
\frac{\partial L}{\partial\dot Q}X_\eta Q-F_\eta
=Pe^\eta P-F_\eta=\mathcal I_\eta.
\]

Las ecuaciones \(\dot Q=\omega e^\eta P\), \(\dot P=-\omega e^{-\eta}Q\) verifican directamente \(d\mathcal I_\eta/dt=0\). \(\square\)

La parametrización positiva del propietario es \(Q=a_S\cos\theta\), \(P=b_S\sin\theta\). Estas ecuaciones le asignan \(\dot\theta=-\omega\). Por tanto, en una vuelta recorrida según el flujo dinámico, \(\oint P\,dQ=2\pi\mathcal I_\eta\); con \(\theta\) creciente, la integral es \(-2\pi\mathcal I_\eta\). Es la distinción de orientación escrita en II, 07b. En el contorno radional, el módulo es \(h=2\pi\hbar\).

## 3. Cambio de forma: transporte y conexión determinados

Para dos formas ya publicadas \(\eta,\eta'\) y un avance de fase \(\vartheta\), se define

\[
\mathcal T_{\eta',\eta}^{\vartheta}:\mathcal P_\eta\to\mathcal P_{\eta'},
\qquad
\mathcal T_{\eta',\eta}^{\vartheta}
=M_{\eta'}e^{-\vartheta J_2}M_\eta^{-1}.
\tag{4}
\]

**Proposición 2.** Este transporte es simpléctico y cumple

\[
\mathcal I_{\eta'}(\mathcal T_{\eta',\eta}^{\vartheta}z)
=\mathcal I_\eta(z),\qquad
\mathcal T_{\eta'',\eta'}^{\vartheta_2}
\mathcal T_{\eta',\eta}^{\vartheta_1}
=\mathcal T_{\eta'',\eta}^{\vartheta_1+\vartheta_2}.
\tag{5}
\]

**Prueba.** Todos los factores son simplécticos. La primera igualdad se reduce a la invariancia de \(\|y\|^2/2\) bajo una rotación. En la segunda se cancelan las matrices contiguas \(M_{\eta'}^{-1}M_{\eta'}\) y se suman las fases. \(\square\)

La fórmula recibe las formas y los avances del lector; no selecciona sus valores. La lista completa de transiciones puede retenerse junto con el transporte compuesto: dos listas que den el mismo mapa compuesto no se identifican como historias.

**Proposición 3.** Una realización diferenciable \(\eta(t),\vartheta(t)\in C^1\), con \(\dot\vartheta=\omega(t)\), del transporte (4) tiene generador

\[
\boxed{
H_{\rm tr}(Q,P,t)=
\omega(t)\mathcal I_{\eta(t)}(Q,P)
+\frac{\dot\eta(t)}2 QP.}
\tag{6}
\]

Este generador conserva \(\mathcal I_{\eta(t)}(z(t))\).

**Prueba.** Al derivar
\(z(t)=M_{\eta(t)}e^{-\vartheta(t)J_2}y_0\) se obtiene

\[
\dot Q=\omega e^\eta P+\frac{\dot\eta}2Q,\qquad
\dot P=-\omega e^{-\eta}Q-\frac{\dot\eta}2P.
\]

Son las ecuaciones de Hamilton de (6). El término de conexión realiza exactamente \(\dot M_\eta M_\eta^{-1}z\), y su Hamiltoniano queda determinado salvo una función exclusiva de \(t\). En efecto,

\[
\begin{aligned}
\frac{d\mathcal I_\eta}{dt}
&=\frac{\dot\eta}{2}(-e^{-\eta}Q^2+e^\eta P^2)
+\left\{\mathcal I_\eta,\frac{\dot\eta}{2}QP\right\}\\
&=\frac{\dot\eta}{2}(-e^{-\eta}Q^2+e^\eta P^2)
+\frac{\dot\eta}{2}(e^{-\eta}Q^2-e^\eta P^2)=0.
\end{aligned}
\tag{7}
\]

Equivalentemente, \(Q=e^{\eta/2}q\), \(P=e^{-\eta/2}p\) dan

\[
P\dot Q-H_{\rm tr}
=p\dot q-\frac{\omega(t)}2(q^2+p^2).
\tag{8}
\]

La simetría de rotación y su carga se transportan exactamente. \(\square\)

Aquí se ha derivado el término de conexión del transporte, no de una fuerza externa. El Hamiltoniano LC de forma fija conserva \(\mathcal I_\eta\). Durante una deformación, omitir el segundo término de (6) deja sin cancelar el primer término de (7). La conservación variacional exige transportar también la forma canónica.

La proposición determina el generador de la interpolación declarada; no asigna una interpolación física única a toda historia TPK. La identidad discreta (4)–(5) funciona sin interpolación.

## 4. Orientación y frontera de la acción

Los propietarios distinguen \(S(Q,P)=(P,Q)\) y \(J_2(Q,P)=(-P,Q)\). Ambos intercambian la forma \(\eta\leftrightarrow-\eta\), pero

\[
S^*\Omega=-\Omega,\quad J_2^*\Omega=\Omega,\qquad
S^*\lambda=-\lambda+d(PQ),\quad
J_2^*\lambda=\lambda-d(PQ).
\tag{9}
\]

Asimismo,

\[
S R_\eta(\varepsilon)S^{-1}=R_{-\eta}(-\varepsilon),\qquad
J_2R_\eta(\varepsilon)J_2^{-1}=R_{-\eta}(\varepsilon).
\tag{10}
\]

Se comprueban usando \(SM_\eta=M_{-\eta}S\), \(J_2M_\eta=M_{-\eta}J_2\), \(SJ_2S^{-1}=-J_2\). Para una curva abierta orientada \(z:[a,b]\to\mathcal P_\eta\),

\[
\int_{J_2z}\lambda=\int_z\lambda-[PQ]_a^b,\qquad
\int_{Sz}\lambda=-\int_z\lambda+[PQ]_a^b.
\tag{11}
\]

Los términos de frontera se anulan en un ciclo y se cancelan al concatenar extremos compatibles. La energía cuadrática por sí sola no determina estos signos ni esos términos.

La monodromía nonádica registra retorno de fase y \(q_{\rm mem}\mapsto q_{\rm mem}+1\). La constancia de una carga no obliga al contador a permanecer fijo. En la realización elíptica, una vuelta conserva \(\mathcal I_\eta\) mientras incrementa la integral acumulada orientada en \(2\pi\mathcal I_\eta\). Carga, acción integrada, fase y registro tienen tipos distintos. No se identifica aquí una vuelta angular con cualquier ciclo TPK sin especificar su lector.

## 5. Noether del reloj y balance visible–memoria

### 5.1. Una carga de acción explícita del reloj

El integral realiza el calendario sobre \(\mathcal H_{\rm clk}=\mathbb C^{108}\), con proyectores Fourier \(P_k=|\widetilde k\rangle\langle\widetilde k|\), y determina

\[
N_{108}=\sum_{k=0}^{107}kP_k,\quad
H_{\rm clk}=\hbar\omega_0N_{108},\quad
\omega_0=\frac{2\pi}{108t_0}.
\tag{12}
\]

Su propagador durante \(t_0\) es el desplazamiento de una celda. La acción CLK4–CLK5 ya escrita es

\[
\mathscr S[\psi]=\int
\left[\frac{i\hbar}{2}
(\langle\psi,\dot\psi\rangle-\langle\dot\psi,\psi\rangle)
-\langle\psi,H_{\rm clk}\psi\rangle\right]dt.
\tag{13}
\]

El producto es antilineal en la primera variable. La ecuación es \(i\hbar\dot\psi=H_{\rm clk}\psi\).

**Proposición 4.** Para \(B=B^*\) con \([B,H_{\rm clk}]=0\), la simetría \(\psi\mapsto e^{-i\varepsilon B}\psi\) tiene carga

\[
\mathcal Q_B(\psi)=\hbar\langle\psi,B\psi\rangle.
\tag{14}
\]

**Prueba.** Al localizar el parámetro, \(\delta\psi=-i\varepsilon(t)B\psi\), se obtiene
\(\delta L=\hbar\dot\varepsilon\langle\psi,B\psi\rangle\).
La integración por partes en las ecuaciones variacionales da \(d\mathcal Q_B/dt=0\). Directamente,

\[
\frac{d}{dt}\langle\psi,B\psi\rangle
=\frac{i}{\hbar}\langle\psi,[H_{\rm clk},B]\psi\rangle=0.
\]

Con \(B=I\) se conserva norma; con \(B=N_{108}\) la carga es la acción \(E_{\rm clk}/\omega_0\). \(\square\)

La forma simpléctica del espacio real subyacente es
\(\Omega_{\rm clk}(u,v)=2\hbar\operatorname{Im}\langle u,v\rangle\);
su uno-forma es
\(\Theta_\psi(v)=-\hbar\operatorname{Im}\langle\psi,v\rangle\),
con \(\Omega_{\rm clk}=-d\Theta\).

### 5.2. Balance exacto de carga

Sean \(\mathcal H,\mathcal K\) espacios hermíticos finitos, \(J:\mathcal H\to\mathcal K\) isometría, \(U\) unitario sobre \(\mathcal K\), y

\[
\Pi=JJ^*,\quad T=J^*UJ,\quad
\eta_{\rm mem}=(I-\Pi)UJ.
\tag{15}
\]

El operador \(\eta_{\rm mem}\) es distinto del parámetro escalar \(\eta\).

**Proposición 5.** Si

\[
\widetilde B=\widetilde B^*,\quad U^*\widetilde BU=\widetilde B,
\quad [\widetilde B,\Pi]=0,\quad B=J^*\widetilde BJ,
\tag{16}
\]

entonces

\[
B=T^*BT+\eta_{\rm mem}^*\widetilde B\eta_{\rm mem},
\qquad
\mathcal Q_B(\psi)=
\mathcal Q_B(T\psi)+\mathcal Q_{\widetilde B}(\eta_{\rm mem}\psi).
\tag{17}
\]

**Prueba.** Se expande \(UJ\psi=JT\psi+\eta_{\rm mem}\psi\) en
\(J^*U^*\widetilde BUJ=J^*\widetilde BJ\).
La conmutación con \(\Pi\) anula los términos cruzados. Evaluar la identidad operatoria y multiplicar por \(\hbar\) da el balance de acción. \(\square\)

Por iteración,

\[
\mathcal Q_B(\psi)=\mathcal Q_B(T^n\psi)
+\sum_{j=0}^{n-1}\mathcal Q_{\widetilde B}
(\eta_{\rm mem}T^j\psi).
\tag{18}
\]

Esta suma registra complementos sucesivos de la dinámica comprimida. La dinámica completa tiene otra fórmula exacta, con \(z_n=U^nJ\psi\):

\[
\mathcal Q_B(\psi)=
\mathcal Q_B(J^*z_n)+
\mathcal Q_{\widetilde B}((I-\Pi)z_n).
\tag{19}
\]

No se identifica \(T^n\) con \(J^*U^nJ\) sin otra propiedad: el estado completo puede reabsorber memoria. Si \(B,\widetilde B\ge0\), todos los sumandos de (18) son no negativos; para cargas firmadas permanece la igualdad, sin esa interpretación de positividad.

Si \(U\) es propagador de una acción como (13), la conmutación de \(\widetilde B\) con su Hamiltoniano aporta la conservación de Noether. La condición de reducción por \(\Pi\) especifica las lecturas que separan carga sin términos de interferencia.

Sin imponer (16), la identidad general conserva los términos adicionales:

\[
\begin{aligned}
&\mathcal Q_B(T\psi)+\mathcal Q_{\widetilde B}(\eta_{\rm mem}\psi)
+2\hbar\operatorname{Re}
\langle JT\psi,\widetilde B\eta_{\rm mem}\psi\rangle\\
&=\mathcal Q_B(\psi)+
\hbar\langle\psi,J^*(U^*\widetilde BU-\widetilde B)J\psi\rangle.
\end{aligned}
\tag{20}
\]

La carga física requiere su lector, por ejemplo \(N_{108}\); una identidad de normas corresponde a \(B=I\). Tampoco se identifica automáticamente el término de memoria con \(\hbar_{\rm pre}-\hbar_{\rm ret}\): esas secciones mantienen el lector de retorno del artículo II.

## 6. Balance covariante recuperado en VII

VII deriva después de eliminar variacionalmente la contorsión

\[
\mathcal T_{\mu\nu}
=T^{\rm phys,LC}_{\mu\nu}+U^{\rm phys,spin}_{\mu\nu},
\qquad
\mathring\nabla^\mu\mathcal T_{\mu\nu}=0.
\tag{21}
\]

Su dominio es la carta HMT–MD realizada, con los acoplamientos mantenidos constantes durante la variación. Para un campo de Killing \(\xi\),

\[
j^\mu_\xi=\mathcal T^{\mu\nu}\xi_\nu,\qquad
\mathring\nabla_\mu j^\mu_\xi=0.
\tag{22}
\]

La prueba usa (21), la simetría de \(\mathcal T\) y la antisimetría de \(\mathring\nabla_\mu\xi_\nu\). Al integrar, la diferencia entre cargas de las hipersuperficies es el flujo por la frontera lateral.

La conservación pertenece al tensor total; cada componente puede intercambiar carga. El propietario 60 determina explícitamente \(\mathcal J^{\rm tr}_\nu=\partial_\nu\operatorname{tr}_g(T^{\rm res})/4\) y los balances opuestos de traza y parte de traza nula. Esto se recupera como instancia covariante del criterio de balance conjunto, no como nueva ecuación gravitatoria.

## 7. Conclusión y alcance preciso

El aporte decisivo es (6): la actualización de forma exige un término de conexión determinado por el transporte canónico. Con él, la acción radional se conserva aun cuando cambia su distribución entre coordenadas. (17) proporciona la separación exacta de una carga de Noether entre lectura y memoria; (19) distingue el estado completo de la reiteración de la lectura comprimida.

La arquitectura autoral de acción, fase, memoria y autoconservación recibe así un desarrollo variacional verificable. No se igualan una carga constante, una memoria creciente y una integral acumulada. Tampoco se atribuye al mero retorno de fase una invariancia del estado completo.

Los controles de continuidad ejecutados conservaron sus resultados de no regresión; su índice automatizado todavía identifica el testigo histórico 2084. La autoridad de lectura de esta nota permaneció en la selección autoral 2249 y los artículos II/VII indicados. Ningún PASS se usa como prueba de las proposiciones nuevas, cuyas demostraciones están escritas aquí. No se ha modificado publicación alguna ni generado un PDF.
