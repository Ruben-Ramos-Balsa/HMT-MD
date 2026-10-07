# Deformaciones espaciales, cotransporte de espín y límite quiral

Pruebas focales nuevas del 29 de septiembre de 2026. Se conservan las
fuentes selladas y las notas anteriores. El resultado es una realización
espacial covariante con límite sobre un núcleo común; no identifica un
cambio de coordenadas con una deformación normal de geometría dinámica.

## 1. Datos recibidos y alcance de la construcción

Se reutiliza la genealogía material de
[RECIBO_GENEALOGIA.json](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/RECIBO_GENEALOGIA.json>):
APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta
del continuo. Las dos hojas, residuos, cocientes, orientación, ruta,
acarreo, frontera y memoria preceden a los lectores utilizados aquí.
Las cinco construcciones del continuo siguen siendo consustanciales.
El retorno de fase no reinicia la memoria. No se sustituyen esos datos
por una métrica o una constante convencional elegida retrospectivamente.

Esta nota parte del transporte geométrico ya realizado y construye su
prolongación espacial. Los propietarios efectivos son:

- [VIII, 30d: realización geométrica](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30d_realizacion_geometrica.tex>), ecuaciones de soldadura y holonomía realizada, representación espinorial y tres curvaturas.
- [VIII, 33: acción espinorial](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex>), `vii:eq:clifford-material-explicito`, `vii:eq:adjunto-conexion-espinorial`, `vii:eq:accion-dirac-material`: módulo de Clifford, conexión y acción material de primer orden.
- [X: Hamiltonianos de curvatura](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/X_ES/sections/hamiltonianos_curvatura.tex>), `eq:hc-pauli`, `eq:hc-dirac`, `thm:hc-dirac-square`: construcción de las matrices a partir de los canales graduados y realización espacial libre; adjunto transportado con el producto interno.
- [TRIT_CURVATURAS_Y_DEFORMACIONES.md](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/TRIT_CURVATURAS_Y_DEFORMACIONES.md>), §4: variación de la normal y corchete de deformaciones de una pantalla.
- [LEGENDRE_PCH_Y_RELOJ_PARAMETRIZADO.md](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/LEGENDRE_PCH_Y_RELOJ_PARAMETRIZADO.md>), §§2–3: cargo Noether, Legendre de la misma acción y restricciones con Gauss y borde.
- [CONMUTADOR_ESPACIAL_ESPINORIAL.md](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/CONMUTADOR_ESPACIAL_ESPINORIAL.md>): cálculo del conmutador de lapsos de primer orden, término de espín y dominio de la conexión intrínseca con contorsión ya eliminada.

La geometría espacial empleada a continuación es una hoja suave compacta,
orientada y sin borde, de dimensión tres, con métrica riemanniana g y
estructura de espín σ recibidas de una carta no degenerada. La normal
temporal se conserva junto con ella. Las constantes de acción y velocidad
son las secciones ya generadas. Compactitud, suavidad y ausencia de borde
son hipótesis de esta realización, no propiedades inferidas para todas
las pantallas del corpus.

## 2. El transporte es entre fibras geométricas, no dentro de una métrica fija

Sea φ un difeomorfismo orientado suave. Pónganse

\[
 g'=\phi_*g=(\phi^{-1})^*g,\quad
 \sigma'=\phi_*\sigma,\quad A'=\phi_*A.
 \tag{1}
\]

La aplicación φ es una isometría de (Σ,g) a (Σ,g'). Su levantamiento
de espín \(\widetilde\phi\) transporta el módulo espinorial recibido
y la normal. Cuando se exige σ'=σ, sólo se consideran los
difeomorfismos que preservan esa estructura de espín y sus lifts.
La composición usa pares (φ,\(\widetilde\phi\)); no se eligen sus
signos independientemente en cada producto.

Sea \(S_{g,\sigma}=S_{L,g}\oplus S_{R,g}\) el módulo de espín 1+3
restringido a la hoja, de rango complejo cuatro. Con los fibrados
materiales hermíticos de rango finito realmente recibidos, definimos
\(\mathscr E_{g,A}=(S_{L,g}\otimes E_L)\oplus(S_{R,g}\otimes E_R)\).
No se añade un compañero derecho a una representación que sólo tenga
canal izquierdo. Definimos

\[
 \mathscr H_{g,A}=L^2(\Sigma,\mathscr E_{g,A};d\mathrm{vol}_g),
 \quad
 (U_\phi\psi)(y)=\widetilde\phi_{x}\psi(x),\quad x=\phi^{-1}(y).
 \tag{2}
\]

El lift incluye el transporte del fibrado interno. Es unitario punto
a punto, y \(\phi^*d\mathrm{vol}_{g'}=d\mathrm{vol}_g\); por tanto
Uφ es unitario **entre** las dos fibras (2). Sobre semidensidades,
la misma operación, escrita respecto de densidades coordenadas, lleva
el factor

\[
 |\det D\phi^{-1}(y)|^{1/2}.
 \tag{3}
\]

No se añade ese factor una segunda vez si ya se integra con la medida
geométrica transportada. Las composiciones satisfacen
\(U_{\phi_2}U_{\phi_1}=U_{\phi_2\phi_1}\) con sus fibras y lifts
correspondientes. Se obtiene un campo de espacios de Hilbert sobre
geometrías, estructuras de espín y conexiones, con transporte unitario.
No se ha supuesto una medida sobre el espacio infinito-dimensional de
todas las métricas para formar un Hilbert global distinto.

### Quiralidad del módulo espaciotemporal

En dimensión espacial tres no hay un operador de quiralidad de un
módulo de espín irreducible de rango dos. Aquí se conserva la graduación
\(\Gamma_5\) del módulo espaciotemporal de rango cuatro recibido,
restringido a la hoja con normal y orientación. En la representación
de X se puede tomar

\[
 \alpha^j=\sigma_1\otimes\sigma_j,\qquad
 \beta=\sigma_3\otimes I_2,\qquad
 \Gamma_5=\sigma_1\otimes I_2.
 \tag{4}
\]

Entonces \([\Gamma_5,\alpha^j]=0\) y
\(\{\Gamma_5,\beta\}=0\). El lift orientado preserva el producto
de Clifford de volumen y la normal, de modo que

\[
 U_\phi\Gamma_{5,g}=\Gamma_{5,g'}U_\phi,
 \qquad U_\phi P_{L/R,g}=P_{L/R,g'}U_\phi.
 \tag{5}
\]

La quiralidad se cotransporta; no se congela una matriz de coordenadas
mientras se transforma sólo una parte del marco.

## 3. Operador espacial y naturalidad exacta

La conexión recibida, reducida a la hoja, se combina con una conexión
interna hermítica que preserva los fibrados izquierdo y derecho. Sea
\(\nabla^A\) la conexión compatible con Clifford. En esta realización
intrínseca, define

\[
 D_{g,A}=-i\hbar c\,\alpha^j\nabla^A_j,
 \qquad \operatorname{Dom}D_{g,A}=H^1(\Sigma,\mathscr E_{g,A}).
 \tag{6}
\]

Es el cinético de primer orden, no el bloque de segundo orden D_T*WD_T.
En la hoja cerrada suave, (6) es simétrico elíptico y autoadjunto: la
integración por partes usa compatibilidad de conexión y medida; la
estimación elíptica de primer orden da
\(\|u\|_{H^1}\le C(\|Du\|+\|u\|)\); si un vector está en el
dominio del adjunto, la regularidad elíptica distribucional lo sitúa en
H¹. Así coinciden los dominios. Su resolvente es compacto por la
inclusión compacta H¹→L². Las secciones suaves son un núcleo de grafo.

Esta construcción prolonga sobre una hoja curva la representación y
conexión explícitas de los propietarios. No declara que todo término
extrínseco de una foliación física esté incluido en (6).

**Teorema 1 — naturalidad espacial.** Con los datos transportados en
(1),

\[
 \nabla^{A'}_{d\phi X}(U_\phi\psi)=U_\phi\nabla^A_X\psi,
 \quad D_{g',A'}U_\phi=U_\phi D_{g,A},
 \quad U_\phi H^s_g=H^s_{g'}.
 \tag{7}
\]

En particular, las igualdades de operadores incluyen sus dominios.

**Prueba.** El pushforward de la conexión de Levi–Civita es torsión
cero y compatible con g', luego es la conexión de Levi–Civita de g'
por unicidad. Su lift de espín y la conexión interna transportada
satisfacen la primera fórmula. La naturalidad de Clifford transforma
\(\alpha_g(\xi)\) en
\(\alpha_{g'}((\phi^{-1})^*\xi)\), y su contracción con la derivada
da la segunda. El cambio de variables conserva las normas geométricas
de derivadas; la versión con cartas usa normas Sobolev equivalentes.
La clausura sobre H¹ da la igualdad de operadores autoadjuntos. ∎

La conexión preserva Γ5 y las α conmutan con ella, por lo que
\([D,\Gamma_5]=0\) con dominio invariante. Si se añade un potencial
suave hermítico V, acotado en esta hoja, se obtiene

\[
 H=D+V,\quad \operatorname{Dom}H=H^1,
 \qquad V'=U_\phi VU_\phi^*,\quad H'=U_\phi HU_\phi^*.
 \tag{8}
\]

La autoadjunción sigue por perturbación acotada. Un término de Yukawa
puede mezclar L/R: (5) y la covariancia de (8) no implican
\([H,\Gamma_5]=0\). Con \(V=mc^2\beta\), ese conmutador es no
nulo para m≠0. Se preserva la estructura quiral de representación, no
una carga axial que la interacción no conserve.

La misma prueba sirve para una forma cerrada acotada inferiormente q
ya construida sobre su dominio Q: si
\(Q'=U_\phi Q\) y
\(q'(U_\phi u,U_\phi v)=q(u,v)\), la unicidad del operador asociado
da \(H'=U_\phi HU_\phi^*\). Esto permite cotransportar las formas
interactuantes recibidas con todos sus campos y medidas. No convierte
por sí solo un producto de campos singular sin regulador en una forma
cerrada del continuo espacial.

## 4. Un regulador espacial que conserva el transporte y la graduación

Definamos el corte espectral del cinético recibido:

Se trata de una **realización reguladora añadida en esta prueba**,
posterior a los datos recibidos; no se afirma que P_R sea el propio
refinamiento nonádico del productor TPK. Ambos reguladores conservan
sus dominios y mapas. Identificarlos requeriría demostrar un
entrelazador entre sus espacios, formas y límites, no sólo comprobar
que ambos convergen o que ambos preservan una graduación.

\[
 P_R=\mathbf1_{[0,R^2]}(D^2),\qquad \mathscr H_R=P_R\mathscr H.
 \tag{9}
\]

Aquí R tiene las unidades de D. La compactitud del resolvente implica
dimensión finita de \(\mathscr H_R\), y sus vectores son suaves.
El corte es espacial y no local en posiciones; no se afirma que sea
simultáneamente un operador reticular ultralocal. Por cálculo espectral,

\[
 [P_R,\Gamma_5]=[P_R,D]=0,\qquad
 P'_R U_\phi=U_\phi P_R.
 \tag{10}
\]

Así no se obtiene la quiralidad seleccionando modos después de comparar
sus masas. Se conservan las dos graduaciones y sus multiplicidades
recibidas, sin inferir un modelo físico nuevo de los modos del corte.

**Teorema 2 — retirada de este corte.** Para H de (8), sea
\(H_R=P_RHP_R\) sobre \(\mathscr H_R\), extendido por cero en su
complemento. Entonces H_R es autoadjunto y

\[
 H_R\longrightarrow H\quad\text{en resolvente fuerte},\qquad
 e^{-itH_R/\hbar}\psi\longrightarrow e^{-itH/\hbar}\psi.
 \tag{11}
\]

La segunda convergencia es uniforme en intervalos compactos de t para
cada ψ. Además, el corte y el límite satisfacen exactamente (7)–(10)
para cada difeomorfismo con lift declarado.

**Prueba.** Para \(\psi\in C^\infty\), el cálculo espectral y las
estimaciones elípticas dan \(P_R\psi\to\psi\) en H^s para todo s.
De aquí \(H_R\psi\to H\psi\) en L². Fijado z no real,

\[
 (H_R-z)^{-1}(H-z)\psi-\psi
 =(H_R-z)^{-1}(H-H_R)\psi\longrightarrow0.
 \tag{12}
\]

Las resolventes tienen cota \(|\operatorname{Im}z|^{-1}\), y
\((H-z)C^\infty\) es denso por ser C∞ un núcleo de H. (12) prueba
la convergencia fuerte de resolventes. Su cálculo espectral, con
aproximación por ventanas compactas y control uniforme de las colas
para cada vector fijo, da la convergencia de grupos en (11). Las
identidades (7) y (10) conjugan cada paso del argumento. ∎

Este teorema retira el regulador espacial de este operador de primer
orden y de sus potenciales suaves acotados. No equivale a retirar
simultáneamente el corte ultravioleta de todas las interacciones de
campos Higgs, gauge y torsión cuártica. Es un resultado adicional
compatible con esas construcciones, con un dominio específico.

La memoria de profundidad arbitraria no tiene por qué cortarse para
aplicar esta prueba: para una suma ortogonal de fibras completas
\(\bigoplus_{\mathfrak h}\mathscr H_{g_{\mathfrak h},A_{\mathfrak h}}\),
se aplican H_R y H fibra a fibra con sus dominios de suma directa.
La cota común de resolvente \(|\operatorname{Im}z|^{-1}\) y la
convergencia en cada fibra dan convergencia fuerte en la suma por
aproximación con soporte finito. En este caso P_R conserva toda la
memoria y **no es de rango finito global**: sólo corta los modos
espaciales de cada fibra. Esta extensión no presupone una medida
continua de historias ni convierte sus permutaciones discretas en
un grupo fuertemente continuo. Un término que mezcle fibras debe
transportarse dentro del mismo operador; su límite no se deduce de
ignorar esa mezcla.

## 5. Lapsos espaciales y conmutadores en el núcleo común

Sea A_N un operador diferencial de primer orden con coeficientes suaves,
por ejemplo \(A_N=\tfrac12(NH+HN)\) con N suave real. Para N,M
fijos y \(\psi\in H^2\), se cumple

\[
 [P_RA_NP_R,P_RA_MP_R]\psi
 \longrightarrow[A_N,A_M]\psi\quad\text{en L}^2.
 \tag{13}
\]

**Prueba.** Los P_R son uniformemente acotados en H^s, utilizando la
norma espectral de \((1+D^2)^{s/2}\), equivalente a la norma Sobolev.
Por tanto \(P_RA_MP_R\psi\to A_M\psi\) en H¹, ya que
\(A_M:H^2\to H^1\) es continuo. Aplicar
\(A_N:H^1\to L^2\) y después P_R demuestra la convergencia del
primer producto; el segundo es idéntico. ∎

El núcleo C∞ es común a cualquier colección finita de lapsos suaves.
Para productos de más factores se aumenta el orden Sobolev; en C∞
se pueden pasar productos y Jacobi con la misma prueba. Esto no
afirma que los espacios espectrales finitos sean invariantes bajo
cualquier lapse ni que el límite sea uniforme sobre todos los lapsos.

La identidad de compresión exacta es

\[
 \begin{aligned}
 &[P_RA_NP_R,P_RA_MP_R]-P_R[A_N,A_M]P_R\\
 &\qquad=P_RA_M(1-P_R)A_NP_R-P_RA_N(1-P_R)A_MP_R.
 \end{aligned}
 \tag{14}
\]

Es fuga por el corte espacial. (13) controla su acción en el núcleo,
no su norma operatoria en todos los modos de borde del corte.

### Naturalidad de los términos geométricos de la hipersuperficie

Sean \(N'=N\circ\phi^{-1}\), \(M'=M\circ\phi^{-1}\). El vector
que aparece en el corchete normal de la pantalla cumple

\[
 v_g(N,M)=g^{-1}(N\,dM-M\,dN),\qquad
 \phi_*v_g(N,M)=v_{g'}(N',M').
 \tag{15}
\]

La identidad se prueba aplicando el transporte de g^{-1} a cada
uno-forma. El término vertical de espín satisface asimismo

\[
 U_\phi[\alpha_g(dN),\alpha_g(dM)]U_\phi^*
 =[\alpha_{g'}(dN'),\alpha_{g'}(dM')].
 \tag{16}
\]

Por tanto un conmutador de lapsos de primer orden que cierre como
transporte tangencial más rotación Clifford conserva sus dos términos
bajo (1), (13). Si se emplea la forma
\(H=-ia\alpha^j\nabla_j+B\), con
\(\{B,\alpha(\xi)\}=0\), la identidad local correspondiente es

\[
 [A_N,A_M]=-a^2\left(
 \nabla_{v_g(N,M)}+\tfrac12\operatorname{div}_g v_g(N,M)
 +\tfrac14[\alpha(dN),\alpha(dM)]\right).
 \tag{17}
\]

Su evaluación y su alcance normal se mantienen separados de la
covariancia demostrada aquí. En concreto, (17) no es por sí sola el
álgebra cuántica completa de una métrica dinámica: (15) transporta la
métrica; no calcula las variaciones canónicas de todas sus variables.

Para Gauss interna, la covariancia natural es
\(U_\phi R(u)U_\phi^*=R(u\circ\phi^{-1})\), con la conexión también
transportada. Lleva el subespacio que satisface las restricciones
recibidas al correspondiente subespacio transformado. No se inventa
un promedio de Haar sobre el grupo infinito-dimensional de funciones
gauge lisas para justificar este paso.

La segunda cuantización exterior \(\Gamma_-(U_\phi)\) preserva CAR
y la graduación en cada sector de partículas. Sobre el núcleo de
partícula finita con factores suaves,
\([d\Gamma(A_N),d\Gamma(A_M)]=d\Gamma([A_N,A_M])\), y (13) pasa
sector por sector. Es la Fock no polarizada de los canales, no una
prueba de implementabilidad de toda transformación en una representación
con mar de Dirac renormalizado ni una cancelación automática de anomalías
quirales de una teoría de campos interactuante.

### Defecto de compatibilidad entre embeddings

En una trivialización unitaria común de un campo de Hilbert sobre
embeddings, sea H_N el generador **total** de una deformación N:
incluye la conexión de marco y densidad, no sólo su expresión material
a métrica fija. Sobre un núcleo común donde existan las derivadas,
definamos \(\mathcal D_N=\delta_N+(i/\hbar)H_N\). La curvatura es
la identidad verificable

\[
 \begin{aligned}
 [\mathcal D_N,\mathcal D_M]-\mathcal D_{[N,M]}
 &=\frac{i}{\hbar}\mathcal F_{N,M},\\
 \mathcal F_{N,M}
 &=\delta_NH_M-\delta_MH_N-H_{[N,M]}
   +\frac{i}{\hbar}[H_N,H_M].
 \end{aligned}
 \tag{21}
\]

Aquí [N,M] denota el corchete de los campos de deformación sobre
embeddings; para dos normales contiene el vector tangencial (15),
con el signo de normal de la nota TRIT. Expandir las dos derivadas
prueba (21). La trivialización unitaria transforma la conexión completa
y su curvatura por conjugación. Si se mantiene una conexión de marco
separada, su curvatura y sus derivadas covariantes deben añadirse a
la misma fórmula.

La identidad (17) calcula el último término de (21) para el operador
intrínseco fijado. No calcula por ello \(\delta_NH_M\): varían el
marco, la métrica, la normal y los datos materiales cotransportados.
La condición \(\mathcal F_{N,M}=0\), o su reducción por las
restricciones verticales de la acción, es una igualdad que se evalúa;
no se impone como definición de transporte para proclamar compatibilidad.
La prueba de límite (13) pasa el término de conmutador; para pasar
(21) completo deben converger además sus derivadas de forma en el
mismo núcleo. Esto localiza exactamente la diferencia entre el
resultado de esta nota y una evolución independiente de la elección
física de hipersuperficie.

## 6. Tres controles que fijan qué significa «arbitrario»

**Métrica congelada.** Incluso para un escalar plano,
\(p_X=-i\hbar(X\partial_x+X'/2)\) y
\(H=-\hbar^2\partial_x^2/(2m)\) cumplen

\[
 [p_X,H]= -\frac{i\hbar^3}{2m}
 (2X'\partial_x^2+2X''\partial_x+X'''/2).
 \tag{18}
\]

No se anula para un campo X arbitrario. Congelar g mientras sólo se
transporta ψ no convierte un cambio de coordenadas en una simetría del
Hamiltoniano de esa métrica. (7) evita ese error cotransportando g.

**Estructura de espín fija.** En un toro de tres dimensiones, una
estructura con condiciones de vuelta (periódica, antiperiódica,
periódica) se transforma bajo una rotación de 90° del plano xy en
(antiperiódica, periódica, periódica). La rotación tiene determinante
positivo, pero no actúa sobre la misma estructura de espín sin
transportarla. Una inversión espacial de orientación, además, puede
intercambiar Γ5 con −Γ5. «Arbitrario» se refiere a todos los
difeomorfismos orientados con el lift y los datos transportados, no a
omitir esos datos.

**Corte espectral y uniformidad.** En S¹, con unidades de control
\(\hbar=1\), sea \(D=-i\partial_x\) y
\(L_k=e^{ikx}(D+k/2)\). Sobre \(e_n=e^{inx}\),

\[
 L_ke_n=(n+k/2)e_{n+k},\qquad
 [L_k,L_l]=(l-k)L_{k+l}.
 \tag{19}
\]

Para \(P_R=\mathbf1_{|n|\le R}\), lapsos N=cos x, M=sin x y el
modo e_R, el defecto de (14) tiene norma

\[
 \frac12(R+1/2)^2.
 \tag{20}
\]

Crece con R, aunque desaparece sobre cada polinomio trigonométrico
fijo cuando el corte contiene todos sus modos intermedios. Más aún,
si los lapsos cambian con el regulador,
\(N_R=\cos((2R+1)x)\), \(M_R=\sin((2R+1)x)\), ambos generadores
comprimidos son cero, mientras el conmutador completo sobre e_1 es
\(-i(2R+1)e_1\). No existe convergencia uniforme sobre lapsos con
derivadas arbitrariamente crecientes. Estos defectos son de compresión;
no son una anomalía quiral.

## 7. Resultado cerrado en este dominio

Quedan construidos: el transporte espacial de semidensidades y
espinores entre geometrías, la naturalidad del cinético de primer
orden y de Γ5, un corte espacial finito exactamente covariante y
graduado, su límite de operadores, y el paso de los conmutadores de
lapsos suaves al límite sobre el núcleo común. La covariancia abarca
todas las deformaciones tangenciales orientadas con spin lift y datos
cotransportados de la carta declarada.

La variación normal física de la geometría pertenece a la acción PCH
y su Legendre, no a un cambio de coordenadas de (2). Para identificar
con ella un operador realizado, se aplica el cuadrado variacional y
su defecto explícito de la nota Legendre. Esta distinción no degrada
los transportes recibidos ni declara ausencia matemática en el corpus;
evita adjudicar a la prueba de naturalidad un contenido diferente.

El [verificador asociado](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/verificar_deformaciones_espaciales.py>) utiliza aritmética racional gaussiana para las
identidades de Clifford y los defectos Fourier (19)–(20). No sustituye
las pruebas de dominio, elipticidad ni límite de esta nota.
