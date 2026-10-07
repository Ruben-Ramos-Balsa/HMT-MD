# Composición matemática de los sectores electromagnético, electrodébil, cromático y gravitatorio HMT–MD

## 0. Objeto y alcance

Esta nota reúne composiciones explícitas y sus pruebas. No modifica los manuscritos. El resultado probado es la confluencia de lectores electrodébiles, constitutivos y gravitatorios, junto con una representación conjunta color–mezcla y su transporte geométrico condicionado. La composición no es meramente clásica: incluye operadores sobre estados, dinámica espectral Yang–Mills y su relación con la evolución de Schrödinger. La realización variacional es una parte de ese conjunto, no una clasificación del conjunto entero. La cuestión adicional es demostrar la compatibilidad conjunta de todos sus operadores sobre el mismo estado y durante su refinamiento; la suma de acciones no sustituye esa demostración.

La procedencia es APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. En APP se conservan simultáneamente suma, producto, cociente y residuo de las entradas 1,…,9 en sus dos orientaciones. TRIT conserva régimen y orientación. TPK compone selección, transporte y memoria mediante U_t; la holonomía Γ₉ precede a su publicación reducida K_ph. La prolongación w6→w12→w18→w24→w30→R36→G9 conserva las fibras completas: vuelve la fase y avanza la memoria. Las cinco construcciones del continuo permanecen conjuntas; los sectores físicos de esta nota son realizaciones posteriores, no una partición de aquellas construcciones.

Las coordenadas π, φ, e y α y las secciones de acción recibidas son salidas internas de esa genealogía. Las dos vías de α se conservan en sus propietarios. Los valores externos no seleccionan rutas ni coeficientes. Los mapas inversos que siguen comprueban una salida ya generada; no sustituyen su generación. Como reconocimiento convencional posterior se emplean el cálculo espectral, las representaciones de calibre y la formulación variacional.

## 1. Antecedente angular y respuesta del vacío

Se recibe la sección angular HMT en la cámara x>y>0, con x=50πα/9. Sean R una involución autoadjunta marcada y P±=(I±R)/2, de rango uno en la realización bicapa:

\[
q_+=e^{-x-y},\quad q_-=e^{-x+y},\quad
T=q_+P_++q_-P_-,\quad D=q_+q_-=e^{-2x}.
\]

La incidencia hexada–octada conserva 90=6·C(6,2) y 120=8·C(6,2). Su respuesta es

\[
\mathcal V=(I-T^{90})(I-T^{120})^{-1},\qquad
f(s)=\frac{1+s+s^2}{1+s+s^2+s^3},\quad s_\pm=q_\pm^{30}.
\]

En efecto, V(I+S+S²+S³)=I+S+S², con S=T³⁰; la inversa existe porque 0<q±<1. Por cálculo espectral,

\[
r_\pm=f(s_\pm),\quad
\widehat\varepsilon=r_+^2,\quad
\widehat\mu=r_-^2,\quad
\widehat Z=r_-/r_+,\quad
\widehat c=(r_+r_-)^{-1}.
\]

Así με=c⁻² y μ/ε=Z² en la normalización interna. La realización dimensional conserva las rectas de acción, carga y velocidad, y no identifica sin conversión las coordenadas normalizadas con valores SI.

## 2. Eliminación de los canales entre vacío, calibre e Higgs

En la realización electrodébil de árbol y a escala común, el propietario fija

\[
g^2=\frac{4\pi\alpha}{1-D},\qquad
g'^2=\frac{4\pi\alpha}{D},\qquad
\lambda_H=\frac{g^2}{8}e^{6x+10y/3}.
\]

**Proposición 1.** Definiendo

\[
D=\frac{g^2}{g^2+g'^2},\qquad
\Xi=\frac{8D^3\lambda_H}{g^2},
\]

se recuperan exactamente

\[
x=-\tfrac12\log D,\quad y=\tfrac3{10}\log\Xi,\quad
q_\pm=\sqrt D\,\Xi^{\mp3/10},\quad
s_\pm=D^{15}\Xi^{\mp9}.
\]

El dominio de la cámara es 0<D<1 y 1<Xi<D⁻⁵ᐟ³. Sobre él,

\[
\boxed{\widehat\varepsilon=f(D^{15}\Xi^{-9})^2,\quad
\widehat\mu=f(D^{15}\Xi^{9})^2,\quad
\widehat Z=\frac{f(D^{15}\Xi^9)}{f(D^{15}\Xi^{-9})}.}
\]

**Prueba.** D³=e⁻⁶ˣ cancela el término 6x en λH, de modo que Xi=e¹⁰ʸᐟ³. Elevar q± a 30 produce los exponentes 15 y ∓9. Sustituir en la respuesta espectral prueba las tres identidades. La condición 0<y<x equivale al dominio anunciado. □

La sección generada conserva además

\[
\alpha=\frac{g^2g'^2}{4\pi(g^2+g'^2)}
=-\frac9{100\pi}\log D,
\qquad
\frac1{g^2}+\frac1{g'^2}=\frac1{4\pi\alpha}.
\]

La segunda expresión de α usa x=50πα/9; no vale para una terna arbitraria de acoplamientos fuera de esa sección.

## 3. Del mismo par espectral a Barbero–Immirzi y a la respuesta gravitatoria

Sea el funcional de retorno del corpus

\[
H(s)=\frac{12s^3}{1-s^9}-\frac{s^4}{1-s^{12}}
-\frac{(\log s)^2}{20\pi},\quad 0<s<1.
\]

**Proposición 2.** La composición del lector constitutivo y el de incidencia da

\[
\boxed{\gamma=H(D^{15}\Xi^9)-H(D^{15}\Xi^{-9}).}
\]

**Prueba.** El propietario demuestra γ=H(s−)−H(s+). La proposición 1 sustituye sus argumentos conservando las etiquetas. El término logarítmico produce [(log s+)²−(log s−)²]/(20π)=180xy/π, exactamente el término angular de γ. Los dos términos racionales conservan el retorno 12S90−S120. □

En la realización radial especificada por el corpus se reciben c>0, la sección reducida de acción ℏ=ℏret>0 y L*>0, y se tiene

\[
L_\alpha=\frac{5759}{23040}\alpha^{16}L_*,\qquad
G=\frac{c^3L_\alpha^2}{\hbar},\qquad
\kappa=\frac{8\pi G}{c^4}=\frac{8\pi L_\alpha^2}{\hbar c}.
\]

Por sustitución, la acción geométrica y la amplitud espinorial existentes se escriben

\[
S_{\rm geom}=\frac{\hbar}{16\pi L_\alpha^2}
\int\Sigma_{IJ}\wedge(\star+\gamma^{-1}I)F^{IJ}
-\frac{\Lambda\hbar}{8\pi L_\alpha^2}\int\mathrm{vol}_e,
\]

\[
\boxed{s_0[\rho,V_c]=\frac{3\pi c\hbar L_\alpha^2}{2}
\frac{\gamma^2}{1+\gamma^2}
\frac{\operatorname{Tr}(\rho\widehat{\mathscr Q}_{sp})}{V_c^2}.}
\]

Se mantienen cotetrada no degenerada, estructura de espín, γ≠0, constantes en la carta y condiciones de frontera del problema variacional. La sustitución utiliza κc²ℏ²=(8πLα²/(ℏc))c²ℏ²; de ahí el coeficiente 3πcℏLα²/2. No se deduce que el estado ρ o el volumen Vc queden determinados sólo por (g,g′,λH).

En el sector de ocupación tres del propietario, Qsp=4I. Para ρ de traza uno en ese sector, su contribución es positiva y se conserva por las evoluciones unitarias que preservan el sector. No se atribuye esa positividad a cualquier estado material.

### 3.1. Enlace espectral fuerte–gravitatorio mediante las hojas

El propietario Yang–Mills utiliza el lector areal–volumétrico procedente del calendario TPK. Su matriz F_av=[[0,1],[1,1]], con las dos hojas distinguidas, da la medida de Parry μvol=φ²/(1+φ²) y el lector regional π/φ². Recibe una unidad longitudinal ℓ0>0 y fija

\[
\kappa_{av}=\frac{\mu_{vol}}{\ell_0}\left(\frac{\pi}{\varphi^2}-1\right)
=\frac{\pi-\varphi^2}{(1+\varphi^2)\ell_0},\qquad
\Delta_E=3\hbar c\kappa_{av},\qquad
m_{gap}=\frac{3\hbar}{c}\kappa_{av}.
\]

El semigrupo del propietario conserva q_m=exp(−3a_mκav), a_m=9a_(m+1), de modo que q_(m+1)^9=q_m. Estos q_m no son los dos canales q±. La brecha se refiere al sector colectivo gauge-invariante, no a una masa elemental del gluón.

**Corolario de composición espectral–gravitatoria.** En la misma sección de acción y velocidad, el reconocimiento posterior de la masa de Planck mP=√(ℏc/G) y la realización radial del apartado 3 dan

\[
m_P=\frac{\hbar}{cL_\alpha},\qquad
\boxed{\frac{m_{gap}}{m_P}
=3\frac{L_\alpha}{\ell_0}
\frac{\pi-\varphi^2}{1+\varphi^2}
=\frac{5759}{7680}\frac{L_*}{\ell_0}\alpha^{16}
\frac{\pi-\varphi^2}{1+\varphi^2}.}
\]

**Prueba.** Sustituir G=c³Lα²/ℏ en la raíz positiva da mP=ℏ/(cLα). Dividir el m_gap anterior por esa expresión cancela ℏ/c. Sustituir Lα=(5759/23040)α¹⁶L* y multiplicar por 3 prueba la última igualdad. □

No se identifica ℓ0 con Lα ni con L*: su razón permanece explícita. El corolario compone las dos realizaciones y sus escalas; no selecciona por sí solo una coordenatización metrológica nueva ni iguala sus Hamiltonianos. La identificación del gap con el sector físico y el paso al límite son antecedentes del propietario Yang–Mills, no se vuelven a demostrar mediante esta división.

## 4. Ensamblaje exacto de color y mezcla débil

El corpus obtiene el espacio cromático desde el residuo ternario y sus operadores de Weyl; distingue la coordenada de sabor de la de color. La realización monoidal fuerte declarada permite trabajar sobre

\[
\mathcal H_q=(\mathbb C^3_u\oplus\mathbb C^3_d)\otimes\mathbb C^3_{col}.
\]

Se recibe V=VCKM unitario. En base de masas, sean

\[
J_+^{m}=\begin{pmatrix}0&V\\0&0\end{pmatrix}\otimes I_3,
\quad J_-^{m}=(J_+^{m})^\dagger,
\quad J_3=\frac12\begin{pmatrix}I_3&0\\0&-I_3\end{pmatrix}\otimes I_3,
\quad C_a=I_6\otimes t_a.
\]

**Proposición 3.** Para los generadores cromáticos ta,

\[
[J_+,J_-]=2J_3,\quad [J_3,J_\pm]=\pm J_\pm,
\quad [J_i,C_a]=0.
\]

**Prueba.** J+J− tiene bloque superior VV†=I, y J−J+ tiene bloque inferior V†V=I. La resta produce 2J3. El producto con la diagonal J3 prueba las otras dos identidades. Los operadores de color actúan sobre el segundo factor tensorial, por lo que conmutan con todos los bloques del primero. □

Para no introducir CKM dos veces, el cambio de base se realiza simultáneamente sobre corrientes y masas:

\[
W=\operatorname{diag}(I_3,V)\otimes I_3,\quad
M_m=\operatorname{diag}(D_u,D_d)\otimes I_3,
\]
\[
J_+^w=WJ_+^mW^\dagger=\begin{pmatrix}0&I_3\\0&0\end{pmatrix}\otimes I_3,
\quad M_w=WM_mW^\dagger
=\operatorname{diag}(D_u,VD_dV^\dagger)\otimes I_3.
\]

En ambas bases [M,Ca]=0; en general [M,J±]≠0. Por tanto, la compatibilidad color–mezcla no afirma una simetría débil no rota del operador de masa.

El enlace con carga se expresa, al recibir las etiquetas de carga del catálogo, por Q/e=J3+I/6 en el doblete quark izquierdo. Entonces [Q/e,J±]=±J± y [Q,Ca]=0. Es una composición del lector de carga recibido, no una nueva derivación de sus etiquetas.

La dinámica cromática anterior permanece la del propietario Yang–Mills: S_m,gs=P_m^(F²)/(4gs²), μ_m,gs=Z⁻¹exp(−S_m,gs)μ_m,0 y H_m,gs=3κav Σb(I−E_b^gs), con acción, medida y refinamiento compatibles. gs y κav conservan sus definiciones propias: κav no es la κ gravitatoria y aquí no se inventa una igualdad entre ellas.

## 5. Composición geométrica: qué queda demostrado al acoplar

Sobre una misma realización geométrica y un fibrado interno unitario vectorial Eint, la conexión tensorial es

\[
\nabla^{tot}=\nabla^{spin}\otimes I+I\otimes\nabla^{int},
\quad
F_{tot}=F_{spin}\otimes I+I\otimes F_{int}.
\]

**Proposición 4.** Esta conexión preserva la acción de Clifford si las dos conexiones son compatibles con las métricas respectivas. La corriente de espín derivada de la acción de Dirac conserva la fórmula del propietario con suma sobre los índices internos.

**Prueba.** Por Leibniz, los términos cruzados de la curvatura se cancelan: las matrices de los dos factores conmutan y las formas de grado uno anticonmutan. Además [γI⊗I,I⊗Aint]=0, de donde la compatibilidad Clifford. La variación respecto de ω no modifica Aint y produce el mismo anticonmutador Clifford, contraído ahora con el emparejamiento interno. □

Para el sector electrodébil quiral se conserva S_L⊗E_L ⊕ S_R⊗E_R. No se reemplaza por un acoplamiento vectorial. Un mapa de masa obtenido de Higgs debe satisfacer la equivariancia Y(g·H)ρ_R(g)=ρ_L(g)Y(H), junto con su adjunto. Esta identidad es la condición del término material: no se deduce de la sola existencia de un espectro de masas.

Si una acción material común S_m sobre esa misma geometría satisface esas condiciones de representación, sus corrientes son sus derivadas, no corrientes elegidas independientemente. La variación de Sgeom+Sm da entonces las ecuaciones existentes:

\[
D_\omega[(\star+\gamma^{-1}I)\Sigma]=\kappa c\,\sigma,
\quad
G_{\mu\nu}+\Lambda g_{\mu\nu}
=\kappa(T_{\mu\nu}^{LC}+U_{\mu\nu}^{spin}),
\quad
\nabla_{LC}^{\mu}(T_{\mu\nu}^{LC}+U_{\mu\nu}^{spin})=0.
\]

La conservación requiere las ecuaciones materiales y la covariancia de esa acción concreta. La realización Einstein–Schrödinger exige además un dominio común preservado y el cierre de las restricciones sin anomalía; reunir las expresiones variacionales no demuestra por sí solo esa compatibilidad operatoria. Esta precisión se refiere a ese enlace concreto, no a una separación del estado HMT en una construcción clásica y otra cuántica.

### 5.1. Construcción explícita del término quiral para el sector quark

La condición anterior puede resolverse algebraicamente en una realización concreta. Recibidas las cargas del catálogo, usamos las representaciones izquierda y derecha

\[
E_L=\mathbb C^2\otimes\mathbb C^3_f\otimes\mathbb C^3_{col},\qquad
E_R=(\mathbb C^3_u\oplus\mathbb C^3_d)\otimes\mathbb C^3_{col},
\]

con YL=I/6, YRu=2I/3, YRd=−I/3. Para que la representación global de U(1) sea unívoca, se usan pesos enteros y=6Y: yL=1, yRu=4, yRd=−2; el coeficiente de la conexión es g′/6. La notación Y y g′ equivalente se entiende al nivel de álgebra de Lie.

Sea H un doblete escalar de peso yH=3 y sea H̃=iσ₂H̄, de peso −3. Esta elección es la realización Higgs explícita del presente ensamblaje, no una nueva generación HMT de hipercargas. Con v>0 de la realización de árbol, definimos los mapas de sabor posteriores a la evaluación de masas:

\[
Y_u=\frac{\sqrt2}{v}D_u,\qquad
Y_d=\frac{\sqrt2}{v}VD_dV^\dagger,\qquad
\mathsf Y(H)=\bigl[\widetilde H\otimes Y_u,\ H\otimes Y_d\bigr]\otimes I_{col}.
\]

**Proposición 5.** Este mapa satisface la equivariancia quiral

\[
\mathsf Y(gH)\rho_R(g)=\rho_L(g)\mathsf Y(H),
\]

y en H0=(0,v/√2) produce exactamente el operador de masa en la base débil del apartado 4.

**Prueba.** Para U∈SU(2), H̃ transforma como UH̃ porque iσ₂Ū=Uiσ₂. Los pesos enteros de las dos columnas después de actuar sobre ER son −3+4=1 y 3−2=1, el peso de EL. Los mapas Yu,Yd actúan sólo en sabor y el factor identidad entrelaza color. Esto demuestra la equivariancia para SU(2)×SU(3)×U(1). En H0 se tiene H̃0=(v/√2,0), luego Y(H0)=diag(Du,VDdV†)⊗Icol. □

Las conexiones son separadamente

\[
\begin{aligned}
\nabla_L&=\nabla^{spin}_L-i g\,W^aJ_a-i g'B Y_L-i g_s C^at_a,\\
\nabla_R&=\nabla^{spin}_R-i g'B Y_R-i g_s C^at_a.
\end{aligned}
\]

Aquí se conserva la base débil o se transporta todo simultáneamente por W. El término de Yukawa −(q̄L Y(H)qR+h.c.) es invariante por la proposición 5. Las curvaturas de B,W,C y la cinética covariante de H completan una acción material clásica común. En una carta de unidades ℏ=c=1, su forma es

\[
\begin{split}
S_{tot}={}&S_{geom}+\int\mathrm{vol}_e\Bigl[
-\tfrac14F_{B,\mu\nu}F_B^{\mu\nu}
-\tfrac14\sum_aF_{W,\mu\nu}^{a}F_W^{a,\mu\nu}
-\tfrac14\sum_aF_{C,\mu\nu}^{a}F_C^{a,\mu\nu}\\
&\quad -(\nabla_\mu H)^\dagger\nabla^\mu H-V(H)
 +\mathcal L_{Weyl}(q_L,\nabla_L)+\mathcal L_{Weyl}(q_R,\nabla_R)
-\bigl(\bar q_L\mathsf Y(H)q_R+\mathrm{h.c.}\bigr)\Bigr].
\end{split}
\]

Se usa la firma (−,+,+,+), curvaturas con sus acoplamientos incluidos, contracciones cromática y débil normalizadas por sus componentes, y cinéticas de Weyl con el adjunto de la realización espinorial del corpus. Esta elección de unidades no elimina la sección de acción ni su procedencia: Sgeom conserva G=Lα² en esa carta y se restituye su expresión dimensional del apartado 3 al cambiarla.

La acción es una realización clásica conjunta explícita: los campos de calibre actúan sobre la misma materia y la misma geometría, y los tensores que gravitan son las variaciones de esa acción. La invariancia del término de materia no se ha supuesto por tener las cuatro etiquetas: se ha probado mediante la equivariancia. Su ecuación métrica utiliza el tensor total y su ecuación de torsión la corriente espinorial de esa misma acción.

El g_s>0 conserva aquí el parámetro del propietario Yang–Mills; esta composición no calcula una selección numérica nueva de ese acoplamiento. El sector quark aislado tampoco es una teoría cuántica electrodébil libre de anomalías: el cierre cuántico requiere el contenido completo, incluidos los leptones, y sus controles. El paso desde Yang–Mills en R4 a su versión cuántica interactuante con geometría dinámica no se prueba mediante esta acción clásica.

## 6. Refinamiento y pruebas de no promoción

Para la amplificación Tm=T⊗I_(9^m), τm=Tr/(2·9^m), Rm=R⊗I, se recuperan D=exp(2τm(log Tm)) y e²ʸ=exp(−2τm(Rm log Tm)). Las trazas normalizadas son −x y −y. El cálculo funcional conserva la respuesta V y H(s±); por tanto, las composiciones de los apartados 1–3 son invariantes en esta torre. La representación de 4 se amplifica por identidad y conserva sus conmutadores exactamente. Este argumento no prueba por sí solo los límites de una teoría de campos acoplada en espacio-tiempo curvo.

Los falsadores precisos son: perder las etiquetas permuta ε y μ y cambia γ de signo; sustituir la traza normalizada por el determinante ampliado cambia D por D^(9^m); perder la unitariedad de V rompe [J+,J−]=2J3; transportar sólo masas o sólo corrientes duplica o elimina indebidamente V; una acción material no covariante no satisface automáticamente el balance gravitatorio; una representación quiral no puede sustituirse por la vectorial del apartado 5.

El reconocimiento convencional posterior conserva la diferencia entre una identidad de lectores, una representación conjunta y la dinámica cuántica completa: ninguna de ellas sustituye a las otras.

## 7. Procedencia y conclusión

Los apartados 1–3 reúnen resultados previos y realizan sus sustituciones contiguas. El apartado 4 explicita una composición representacional con prueba de bloques y cambio de base; no reclama prioridad matemática. El apartado 5 prueba la regla de acoplamiento vectorial; el apartado 5.1 construye y prueba la equivariancia quiral del sector quark y escribe una realización variacional común. Esta formalización no se atribuye como cita literal de los propietarios anteriores.

Queda demostrada aquí una composición exacta de los lectores de vacío, electrodébiles y gravitatorios y una compatibilidad operatoria color–mezcla. No se ha demostrado en esta nota que todos los sectores cuánticos acoplados satisfagan conjuntamente existencia, renormalización, cancelación de anomalías y comparación experimental. Tampoco se ha vuelto a verificar íntegramente el teorema Yang–Mills del propietario. El comprobador adjunto prueba identidades racionales finitas y hace controles numéricos de sustitución; no certifica una unificación física completa.

### Propietarios consultados

- Vacío: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/III_ES/manuscrito/sections/04_respuesta_constitutiva.tex`, respuesta, inversión y refinamiento.
- Barbero: mismo III_ES, `manuscrito/sections/06_pell_barbero.tex`, líneas 195–354.
- Higgs/calibre: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VII_ES/manuscrito/ampliacion_composicion/higgs.tex`, íntegro, especialmente reconstrucción y confluencia.
- Escala electrónica: mismo VII_ES, `manuscrito/ampliacion_composicion/electroweak.tex`, íntegro.
- Color/sabor: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VI_ES/sections/08_familias_y_compuestos.tex`, líneas 317–402.
- Composición monoidal: `/Users/ruben/Documents/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/04ab_postulados_cuanticos_genealogicos_rev2.tex`, líneas 304–382; condiciones conservadas.
- Color: mismo integral, `sections/md/06e_color_qutrit_gauge_finito.tex`.
- Dinámica fuerte: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/X_ES/sections/ym_complete.tex`, líneas 469–744 y 1620–1695; uso focal, no revisión de todas las dependencias.
- Escala fuerte: mismo X_ES, `sections/ym_scale.tex`, íntegro; `sections/hamiltonianos_curvatura.tex`, líneas 547–620, inmersión modal y compatibilidad de refinamiento.
- Gravedad: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex`, ecuaciones variacionales; `33_corriente_espinorial_y_densidad.tex`, acción/corriente; `90_conclusiones.tex`, restitución radial y amplitud.
- Einstein–Schrödinger: `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex`, íntegro.

El resolutor global conserva un corte histórico de 2084 páginas; para esta composición se usa el integral autoral de 2249 y los propietarios especializados citados, no el corte antiguo como sustituto de ellos.
