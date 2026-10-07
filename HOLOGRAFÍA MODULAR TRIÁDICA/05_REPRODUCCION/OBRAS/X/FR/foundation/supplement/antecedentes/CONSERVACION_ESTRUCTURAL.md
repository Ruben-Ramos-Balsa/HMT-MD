# Conservación de observables y memoria bajo refinamiento nonádico

Investigación fundacional HMT–MD, 11 de septiembre de 2026.

## 1. Objeto y procedencia de la construcción

La construcción parte de las dos hojas operatorias de APP. Para las marcas tipadas \(i,j\in\{1,\ldots,9\}\), la evaluación aditiva y multiplicativa conserva la descomposición entera \(n=\rho_9(n)+9q_9(n)\), con \(\rho_9(n)\in\{1,\ldots,9\}\). La orientación TRIT discrimina los residuos mediante \(0\mapsto0,1\mapsto+1,2\mapsto-1\) y conserva el acarreo de la división ternaria. El TPK compone selección, transporte y actualización, \(U_t=\operatorname{Upd}_t\circ\operatorname{Tra}_t\circ\operatorname{Sel}_t\). Sus prolongaciones conservan las hojas, la orientación, el residuo, el cociente, el acarreo, la ruta y la frontera, y actualizan la memoria.

La holonomía nonádica \(\Gamma_9\) actúa sobre ese estado enriquecido. En la coordenada de vueltas y fase,

\[
(w,r)\longmapsto\bigl(w+\lfloor(r+1)/9\rfloor,\ (r+1)\bmod9\bigr).
\]

La vuelta de fase incrementa el registro entero. El desarrollo \(w_6\to w_{12}\to w_{18}\to w_{24}\to w_{30}\to R_{36}\to G_9\) pertenece a esta prolongación. Las construcciones espectral, solenoidal, de calibre, cohomológica y determinantal son realizaciones correlativas de la misma estructura discreta del continuo. Sus mapas de refinamiento proceden de las mismas emisiones y de sus relaciones, como desarrolla [Refinamiento y conservación de medida](REFINAMIENTO.md).

Las realizaciones lineales utilizadas a continuación se aplican a transportes así obtenidos. Las coordenadas \(\pi_{\rm HMT},\varphi_{\rm HMT},e_{\rm HMT},\alpha_{\rm HMT}\), el registro dodecafásico \(K\) y las escalas de acción pertenecen a sus etapas de generación y lectura: son salidas, con sus operadores y orden constructivo propio. Los espacios de Hilbert y el teorema espectral intervienen como lenguaje de realización y demostración posterior.

**Procedencia.** El balance de compresión y expresión, la conservación de formas sesquilineales y la distinción entre fase y memoria están en el corpus. Este desarrollo reúne esas pruebas, obtiene explícitamente el sector terminal de la compresión nonádica, formula su covariancia por transporte de carta y los conecta con el refinamiento, la incidencia y la acción. Las ideas de conservación de unidad y memoria son arquitectura autoral preexistente. La prioridad global de estas formulaciones adicionales no se atribuye aquí.

## 2. Balance de un observable conservado

Sean \(\mathcal H,\mathcal K\) las realizaciones de un espacio de lectura y de su extensión enriquecida. Sean \(J:\mathcal H\to\mathcal K\) una isometría, \(P=JJ^*\), \(U:\mathcal K\to\mathcal K\) un transporte acotado y \(\widetilde A\) un observable acotado autoadjunto. Supóngase

\[
U^*\widetilde A U=\widetilde A,\qquad [\widetilde A,P]=0.
\]

Definimos

\[
A=J^*\widetilde A J,\qquad T=J^*UJ,
\qquad \eta=(I-P)UJ.
\]

**Proposición 1.** La carga se descompone exactamente entre lectura y complemento:

\[
\boxed{A=T^*AT+\eta^*\widetilde A\eta.}\tag{1}
\]

**Demostración.** La identidad \(UJ=JT+\eta\) es una descomposición ortogonal. Al expandir \(J^*U^*\widetilde A UJ\), los términos cruzados son cero porque \(\widetilde A\) reduce los subespacios \(P\mathcal K\) y \((I-P)\mathcal K\). El término izquierdo es \(A\); los dos términos diagonales son los de (1). Esto prueba también la identidad de las formas sesquilineales para dos estados distintos. Si \(\widetilde A\geq0\), ambos sumandos son positivos. Para \(\widetilde A=I\), la hipótesis de conservación es \(U^*U=I\). ∎

Si la lectura mezcla sectores del observable, el balance conserva adicionalmente

\[
T^*J^*\widetilde A\eta+\eta^*\widetilde A JT.
\]

Estos términos representan la interferencia entre las dos residencias de la carga. La condición de reducción escrita arriba garantiza su anulación para toda la descomposición. En realizaciones particulares pueden anularse también por otras razones, por ejemplo cuando \(\eta=0\).

## 3. Especialización a la conexión nonádica

Sea \(C\) la realización unitaria del transporte de memoria sobre \(\mathcal H\). En \(\mathcal H^9\), el transporte de las nueve fases y su inclusión uniforme son

\[
S_C(v_0,\ldots,v_8)=(Cv_8,v_0,\ldots,v_7),
\qquad Jv=\tfrac13(v,\ldots,v).
\]

El factor \(1/3\) resulta de la normalización de nueve copias. La compresión y su complemento son

\[
T=\frac{8I+C}{9},\qquad
\eta v=\frac1{27}\bigl(8(C-I)v,-(C-I)v,\ldots,-(C-I)v\bigr).
\]

Si \(A=A^*\) es acotado y \([A,C]=0\), el observable \(\widetilde A=I_9\otimes A\) satisface las hipótesis de la proposición 1. Por tanto,

\[
\boxed{A=T^*AT+\frac8{81}(I-C)^*A(I-C).}\tag{2}
\]

Los coeficientes proceden del reparto entre las nueve componentes: \(8^2+8=72\), dividido por \(27^2\), da \(8/81\). La identidad es el balance sesquilineal ya documentado en el artículo espectral, expresado aquí para un observable general.

La iteración telescópica proporciona, para cada \(N\geq1\),

\[
A=T^{*N}AT^N+
\sum_{j=0}^{N-1}T^{*j}\eta^*\widetilde A\eta T^j.\tag{3}
\]

Para \(A=I\), la aplicación

\[
V_Nv=(T^Nv,\eta v,\eta Tv,\ldots,\eta T^{N-1}v)
\]

es isométrica. El paso \(N\to N+1\) descompone exclusivamente el terminal \(T^Nv\) en su nueva lectura y complemento; mantiene todos los registros previos. Así, la conservación se verifica a cualquier profundidad.

**Distinción de operaciones.** Se cumple \(S_C^9=I_9\otimes C\). La iteración \(T^N\) describe compresiones sucesivas con almacenamiento de sus complementos. El transporte enriquecido sin compresiones intermedias es \(S_C^N\). Ambas operaciones tienen dominios definidos y funciones diferentes; la prueba conserva esa distinción.

## 4. Sector terminal y registro a profundidad ilimitada

Sea \(P_{\rm fix}\) la proyección ortogonal sobre \(\ker(I-C)\).

**Teorema 2.** Para todo transporte unitario \(C\), la compresión nonádica satisface

\[
\underset{N\to\infty}{\operatorname{s-lim}}T^N=P_{\rm fix},\qquad
\boxed{I=P_{\rm fix}+\sum_{j=0}^{\infty}T^{*j}\eta^*\eta T^j.}\tag{4}
\]

La serie converge en la topología fuerte. Para cada observable acotado autoadjunto \(A\) que conmuta con \(C\), se obtiene además

\[
\boxed{A=P_{\rm fix}AP_{\rm fix}
+\sum_{j=0}^{\infty}T^{*j}\eta^*(I_9\otimes A)\eta T^j.}\tag{5}
\]

**Demostración.** En la representación espectral del operador unitario \(C\), la compresión corresponde a \(t(z)=(8+z)/9\). Sobre el círculo unitario,

\[
|t(z)|^2=1-\frac8{81}|1-z|^2.
\]

Por tanto \(t(z)^N\to0\) para \(z\ne1\), y \(t(1)^N=1\). La convergencia dominada respecto de cada medida espectral vectorial prueba \(T^N\to P_{\rm fix}\) fuertemente. El mismo argumento vale para \(T^{*N}\). Como \(A\) es acotado, \(T^{*N}AT^N\to P_{\rm fix}AP_{\rm fix}\) fuertemente. El límite de (3) da (5), y su especialización \(A=I\) da (4). ∎

En particular,

\[
V_\infty v=(P_{\rm fix}v,\eta v,\eta Tv,\eta T^2v,\ldots)
\]

es una isometría. Conserva el producto interior completo, además de la norma.

**Corolario 2.1: memoria bilateral.** Para el desplazamiento \(Ce_n=e_{n+1}\) en \(\ell^2(\mathbb Z)\), \(P_{\rm fix}=0\): una sucesión fija sería constante y su única realización cuadrado-sumable es cero. En consecuencia, toda la norma inicial se distribuye en el registro de complementos. Esto precisa el comportamiento ilimitado de la realización bilateral de memoria presente en el corpus.

**Corolario 2.2: calendario finito.** En un ciclo de \(d\) posiciones, la sucesión uniforme determina un subespacio fijo unidimensional. Ese sector permanece como terminal y el complemento acumula el resto. El calendario finito y el registro bilateral poseen, por tanto, terminales diferentes.

En el caso bilateral, la convergencia fuerte puede coexistir con \(\|T^N\|=1\) para todo \(N\). La demostración no supone una tasa uniforme de contracción. También distingue esta compresión del modo \((5/9)C\), cuya contracción geométrica es uniforme y está estudiada separadamente en las fuentes.

## 5. Conservación de simetría y transporte de carta

Sea \(R\) unitario y definamos \(C'=RCR^*\), \(A'=RAR^*\). La fórmula explícita de la compresión da

\[
T(C')R=RT(C),\qquad
\eta(C')R=R^{\oplus9}\eta(C).\tag{6}
\]

**Demostración.** La primera igualdad se obtiene distribuyendo \((8I+RCR^*)R/9\). La segunda resulta de \((C'-I)R=R(C-I)\) en cada una de las nueve componentes de \(\eta\). ∎

La iteración de (6) entrelaza los registros finitos. Además, \(P_{\rm fix}(C')=RP_{\rm fix}(C)R^*\), por transporte del núcleo de \(I-C\), de modo que también queda entrelazado el registro ilimitado. Así, el balance de observables es covariante cuando se transportan conjuntamente la carta, el operador y el observable. Las simetrías que conmutan con \(C\) actúan además en una misma carta fija. Esta distinción permite incorporar las transformaciones excepcionales con sus marcos, banderas y orientaciones efectivamente transportados.

La composición concreta recuperada en el artículo IV usa la matriz de Hadamard del registro, \(H_{12}^2=4I\), y la incidencia \(\mathcal I\) de las doce posiciones en las 132 hexadas:

\[
J_H=H_{12}/2,\qquad
\mathcal I^*\mathcal I=36I+30\mathbf1\mathbf1^*,\qquad
U_W=\mathcal I/6\big|_{\mathbf1^\perp}.
\]

Ambos operadores normalizados son isométricos en los dominios indicados. La composición \(B=U_WJ_H\) sobre \(W=J_H(\mathbf1^\perp)\) conserva productos interiores y entrelaza la representación transportada de \(M_{12}\) con la acción en las hexadas. El registro entero \(K\) conserva, además, la inversión integral \(H_{12}/4\) sobre su red de congruencias; esa inversión y la normalización isométrica tienen funciones distintas. [La demostración, la prolongación APP–Witt–Leech y sus dominios están desarrollados aquí](EXCEPCIONAL.md).

En esta composición, la conservación de incidencia tiene un contenido operatorio concreto. Su extensión por otros transportes usa (6) y los entrelazadores efectivos de las fuentes, respetando sus grupos y dominios respectivos.

### Transporte íntegro de las doce coordenadas de K

La separación del subespacio centrado puede completarse manteniendo también su media. Sean \(P_0=I-\mathbf1\mathbf1^*/12\), \(\mu(k)=\mathbf1^*k/12\) y

\[
F(k)=\left(\mu(k),\frac16\mathcal I P_0k\right)\in\mathbb R\oplus E_{\rm inc}.
\]

Equipamos el codominio con \(\|(\mu,y)\|^2=12|\mu|^2+\|y\|^2\). El Gram de incidencia demuestra

\[
\|F(k)\|^2=\|k\|^2,\qquad
\boxed{F^{-1}(\mu,y)=\mu\mathbf1+\frac16P_0\mathcal I^*y.}\tag{6a}
\]

En efecto, \(\mathcal I^*\mathcal I P_0=36P_0\), de modo que la fórmula inversa recupera \(P_0k\), y el primer término recupera su media. La acción de \(M_{12}\) es trivial sobre la media y permuta las hexadas; por ello \(F\) es equivariante. Componer \(FJ_H\) transporta las coordenadas firmadas normalizadas. Así se conservan las doce coordenadas del registro, no sólo su parte centrada. El dominio de esta reconstrucción es el registro dodecafásico; la memoria completa de la historia mantiene sus otras coordenadas y su prolongación.

### Especialización al operador excepcional de orden tres

El integral construye el operador ortogonal \(g_c\) sobre la realización del vecino de Leech, mediante las doce fibras APP–Witt de tipo \(A_2\), y demuestra \(g_c^3=I\) y \(\ker(I-g_c)=0\). Su construcción, entrelazamiento y preservación reticular están localizados en [EXCEPCIONAL.md, §4](EXCEPCIONAL.md).

Construimos ahora, como composición operatoria de esa salida con la carta de nueve fases,

\[
T_3=\frac{8I+g_c}{9},\qquad
\eta_3=(I-JJ^*)S_{g_c}J.
\]

**Corolario 2.3.** Esta composición satisface

\[
\boxed{T_3^*T_3=\frac{19}{27}I,\qquad
\eta_3^*\eta_3=\frac8{27}I,\qquad
\|T_3^Nv\|^2=\left(\frac{19}{27}\right)^N\|v\|^2.}\tag{6b}
\]

**Demostración.** El vector \((I+g_c+g_c^2)v\) es fijo por \(g_c\); la ausencia de vectores fijos implica \(I+g_c+g_c^2=0\). Como \(g_c^*=g_c^2\), tenemos \(g_c+g_c^*=-I\). Sustituyendo,

\[
T_3^*T_3=\frac{65I+8(g_c+g_c^*)}{81}
=\frac{57}{81}I=\frac{19}{27}I.
\]

El balance (2) con \(A=I\) da el segundo coeficiente. La aplicación reiterada de la igualdad de normas da la potencia para todo \(N\). ∎

El registro ilimitado es isométrico y su terminal tiende a cero con la tasa explícita de (6b). Aquí la estructura excepcional determina los dos coeficientes complementarios; ambos proceden de la relación polinómica de \(g_c\) y de las nueve fases. Esta es una composición matemática desarrollada en esta investigación. Su definición no identifica \(g_c\) con \(\Gamma_9\), ni afirma que \(S_{g_c}\) sea el operador temporal canónico del TPK: conserva la distinción entre prolongación excepcional y holonomía temporal mientras las compone explícitamente.

## 6. Refinamiento de historias y compatibilidad de los balances

Para las historias enriquecidas de profundidad \(n\), sea \(p_h(\varepsilon)\) la probabilidad de una extensión superviviente, normalizada por \(\sum_\varepsilon p_h(\varepsilon)=1\). El refinamiento canónico sobre las bases de historias es

\[
R_n\delta_h=\sum_{\varepsilon\in\operatorname{Out}(h)}
\sqrt{p_h(\varepsilon)}\,\delta_{h\varepsilon}.
\]

Las extensiones de historias diferentes tienen prefijos diferentes y soportes disjuntos. Por ello \(R_n^*R_n=I\). Esta es la realización isométrica de la consistencia proyectiva de la medida: los coeficientes proceden de los pesos de supervivencia ya construidos.

Para transportar (1) entre profundidades, se conservan conjuntamente las inclusiones, las proyecciones, los transportes y los observables. Con isometrías de refinamiento \(R_n,\widetilde R_n\), los cuadrados necesarios son

\[
J_{n+1}R_n=\widetilde R_nJ_n,\quad
P_{n+1}\widetilde R_n=\widetilde R_nP_n,\quad
U_{n+1}\widetilde R_n=\widetilde R_nU_n,\quad
\widetilde A_{n+1}\widetilde R_n=\widetilde R_n\widetilde A_n.
\]

Estos cuadrados implican \(T_{n+1}R_n=R_nT_n\) y \(\eta_{n+1}R_n=\widetilde R_n\eta_n\). Con cotas uniformes, las identidades pasan al límite inductivo de las realizaciones. Las historias, en cambio, forman el sistema proyectivo de prefijos; las direcciones contrarias de ambos tipos de mapas quedan diferenciadas. [Se incluyen las pruebas de medida, Gram y paso al límite](REFINAMIENTO.md).

## 7. Especialización variacional: acción y orientación

La acción elíptica del artículo II proporciona una especialización física del principio, con parámetros ya construidos en sus etapas HMT. En sus coordenadas canónicas,

\[
H_\eta(Q,P)=\frac{\omega}{2}
\left(e^{-\eta}Q^2+e^\eta P^2\right),\qquad
I_\eta=H_\eta/\omega.
\]

La transformación canónica \(Q=e^{\eta/2}q\), \(P=e^{-\eta/2}p\) convierte \(I_\eta\) en \((q^2+p^2)/2\). Las rotaciones de \((q,p)\), transportadas a \((Q,P)\), constituyen una simetría continua. Para el lagrangiano \(L=P\dot Q-\omega I_\eta\), su carga de Noether es \(I_\eta\). En el contorno de la fuente \(I_\eta=\hbar\), la acción orientada es \(\oint P\,dQ=2\pi\hbar=h\), con la orientación de la órbita hamiltoniana. La prueba distingue la transformación simpléctica y la antisimpléctica: pueden conservar la misma energía y actuar con signos diferentes sobre la acción orientada. [Desarrollo variacional y reloj generado](ACCION.md).

### Actualización de la forma y término de conexión

La matriz de forma \(M_\eta=\operatorname{diag}(e^{\eta/2},e^{-\eta/2})\) permite desarrollar un transporte entre elipses con parámetros diferentes. Fijamos \(J_2=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\) y \(R(\theta)=\exp(-\theta J_2)\), la rotación hamiltoniana en el plano \((q,p)\). El transporte

\[
z'=M_{\eta'}R(\delta\theta)M_\eta^{-1}z,
\qquad z=(Q,P)^\mathsf T,
\]

es simpléctico y satisface exactamente \(I_{\eta'}(z')=I_\eta(z)\). La prueba consiste en llevar ambos estados a sus coordenadas normalizadas y usar la conservación de \(q^2+p^2\) por la rotación. Conserva la acción mientras cambia la forma.

Para una realización diferenciable \(\eta(t)\), con avance angular \(\dot\theta=\omega\), la diferenciación de ese transporte produce

\[
\dot Q=\omega e^\eta P+\tfrac12\dot\eta Q,\qquad
\dot P=-\omega e^{-\eta}Q-\tfrac12\dot\eta P.
\]

Su generador hamiltoniano, obtenido de estas dos ecuaciones, es

\[
\boxed{H_{\rm trans}=\omega I_\eta+\frac{\dot\eta}{2}QP.}\tag{7}
\]

El segundo sumando es el término de conexión de la forma variable. Con la convención \(\{f,g\}=\partial_Qf\partial_Pg-\partial_Pf\partial_Qg\),

\[
\partial_tI_\eta=\frac{\dot\eta}{2}(-e^{-\eta}Q^2+e^\eta P^2),
\quad
\left\{I_\eta,\frac{\dot\eta}{2}QP\right\}
=\frac{\dot\eta}{2}(e^{-\eta}Q^2-e^\eta P^2).
\]

Ambas contribuciones se cancelan y \(dI_\eta/dt=0\). Para el transporte prescrito, (7) es único salvo una función del tiempo. La realización diferenciable es una especialización declarada del transporte entre formas; el resultado discreto anterior vale directamente entre dos parámetros generados. La actualización TPK específica conserva su propia regla para seleccionar esos parámetros y sus tiempos.

Así se obtiene una conexión precisa: un observable conservado por la dinámica completa se distribuye entre lectura y memoria mediante (1). Cuando ese observable es el generador de una simetría continua de la acción construida, la cantidad distribuida es una carga de Noether. La norma, la carga de una simetría y el funcional energético quedan relacionados por sus operadores específicos.

Una especialización acotada efectiva se obtiene del calendario de 108 estados del integral. Su Hamiltoniano realizado es \(H_{\rm clk}=\hbar\omega_0N_{108}\), con \(N_{108}=\sum_{k=0}^{107}kP_k\) y \(P_k\) sus proyectores de Fourier. La acción del reloj tiene carga \(\hbar\langle\psi,N_{108}\psi\rangle=E_{\rm clk}/\omega_0\). Los transportes y las inclusiones que satisfacen las hipótesis de (1) distribuyen esa carga entre lectura y complemento. Aquí todos los operadores son finitos y acotados. La acción elíptica de (7) se ha probado en su realización clásica simpléctica; una cuantización con observables no acotados conserva, además, sus condiciones de dominio propias.

## 8. Resultado de conjunto y dirección fundacional

La unidad conservada adquiere tres expresiones compatibles: masa total de las extensiones supervivientes, producto interior del registro completo y carga del observable transportado. El refinamiento determina sus mapas; la holonomía nonádica determina el reparto; la incidencia conserva las representaciones en sus dominios; la acción permite reconocer las correspondientes cargas dinámicas. La orientación y la memoria pertenecen materialmente a estas identidades.

El resultado explícito adicional de esta investigación es el teorema 2: identifica el terminal de la compresión nonádica a profundidad ilimitada y prueba la conservación completa de observables en el registro. Las proposiciones de covariancia, refinamiento e incidencia permiten componer ese resultado con las realizaciones del corpus sin sustituir el estado por una única coordenada numérica.

La propuesta fundacional resultante es estudiar la conservación sobre el sistema de transportes y sus realizaciones correlativas, y después sus expresiones variacionales y metrológicas. El orden expositivo parte del generador, continúa con los mapas que conservan estructura y obtiene de ellos sus lecturas. El electrón, las vacancias y los restantes sectores aportan especializaciones mediante sus mapas ya construidos, no mediante analogías nominales.

## Fuentes de las pruebas y alcance

- Integral de 2.249 páginas, fuente `sections/hmt/06e_certificado_generacion_monodromica_rev7.tex`, especialmente las identidades de compresión, expresión y actualización de memoria; propietarios exactos en los desarrollos asociados.
- Artículo espectral REV04, [transporte_y_momentos.tex](../REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/PRIMOS_Y_ZETA_COMPLETO/ampliacion/transporte_y_momentos.tex), §§Compresión uniforme, Registro de vueltas y Conservación de la forma aritmética: antecedente de (1)–(3).
- Artículo IV REV04: `sections/registro_k.tex` y `sections/excepcional.tex`; cadenas y dominios transcritos en [EXCEPCIONAL.md](EXCEPCIONAL.md).
- [REFINAMIENTO.md](REFINAMIENTO.md): fuentes del estado, medida y construcción correlativa del integral; prueba de naturalidad de los balances.
- [ACCION.md](ACCION.md): fuentes del oscilador, forma canónica y reloj; demostraciones de las cargas y orientación.
- Emmy Noether, *Invariante Variationsprobleme* (1918), [traducción del artículo original](https://arxiv.org/html/physics/0503066v3): comparación posterior con las simetrías continuas de la acción. Las acciones de grupos finitos se tratan mediante sus entrelazadores, distintos de las hipótesis del teorema variacional.

El archivo `verificar_balances_exactos.py` acompaña las demostraciones con controles racionales finitos y casos negativos. El teorema de límite está probado arriba mediante convergencia espectral; su validez no se infiere de ejecutar un número finito de iteraciones. Los PDF anteriores permanecen intactos. Este desarrollo constituye investigación matemática focal, no una nueva certificación empírica global de todas las interpretaciones físicas del corpus.
