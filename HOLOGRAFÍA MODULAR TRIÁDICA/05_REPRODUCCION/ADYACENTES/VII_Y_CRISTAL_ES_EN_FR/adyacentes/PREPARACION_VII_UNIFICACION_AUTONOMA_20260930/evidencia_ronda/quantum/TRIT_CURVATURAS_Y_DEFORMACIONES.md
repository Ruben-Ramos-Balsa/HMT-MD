# Tres curvaturas, deformaciones de pantalla y memoria a profundidad arbitraria

Formalización focal nueva, 29 de septiembre de 2026. Esta nota se añade a las
anteriores; no modifica fuentes ni convierte un control documental en prueba.

## 1. Propietarios y tipos que se conservan

La cadena efectiva recibida es APP → TRIT → TPK → estado enriquecido →
estructura discreta conjunta del continuo. APP conserva las dos hojas y los
datos de cociente y acarreo; TRIT discrimina el régimen y la orientación; TPK
compone selección, transporte y actualización sin reiniciar la memoria al
retornar la fase. Los transportes y la soldadura de pantalla de esta nota son
salidas de esa cadena. No se eligen a partir de una geometría objetivo.

Propietarios activos focales, bajo
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`:

- `VIII_ES/manuscrito/30d_realizacion_geometrica.tex`, líneas 16–57 y 125–170: soldadura, realización de rutas, holonomía y tres conexiones de Cartan.
- `VIII_ES/manuscrito/30c_composicion_corriente_conexion.tex`, líneas 28–79, 122–166 y 187–237: diferencial completo de transportes invertibles y corriente del mismo funcional de memoria.
- `VIII_ES/fuentes_conservadas/02_dinamica_tres_hojas.tex`: primer jet nilpotente, memoria por Schur y energía de corona.
- `X_ES/sections/hamiltonianos_curvatura.tex`, líneas 25–105, 138–231 y 234–271: generadores nativos, cambio de marco, carga del registro y curvaturas métricas.

Propietarios del integral de 3988 páginas, conservados en
`/Users/ruben/Documents/New project/output/TRATADO_GENERATIVO_HMT_MD_20260919/REV03/source/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/`:

- `manuscrito/ampliacion_20260919/propietarios/X_RECIPROCIDAD/nuclear__06.tex`, líneas 5–50 y 293–355: composición afín de memoria, transición entre regímenes y refinamiento arbitrario.
- `colaboracion/partes_i_ii/source/canonical/corredor/02_pantalla_accion.tex`, «Módulo de canales y rango dimensional» y «Estado dimensional y transporte simultáneo»: pantalla como cociente, rango y morfismos que conservan relaciones.

Se preserva una distinción crucial: el símbolo `H` en el primer propietario
integral designa el **retorno afín** \(m\mapsto Cm+\kappa\), no el
Hamiltoniano de Schrödinger. En esta nota se escribe \(\mathsf A\) para
ese retorno y \(\mathbb H\) para un Hamiltoniano cuántico. La masa como
lectura de memoria conserva sus lectores previos; la carga del registro que
aparece aquí no se identifica por su nombre con una masa física.

## 2. Las tres realizaciones no son tres nombres del mismo generador

Los operadores nativos recuperados satisfacen

\[
J_+=\frac{2C+I}{\sqrt3},\quad J_0=N,\quad
J_-=\frac{2F_{\rm av}^{2}-3I}{\sqrt5},\qquad J_\tau^2=-\tau I.
\]

La orientación temporal del lector es retorno/memoria para \(+1\), umbral
variacional para \(0\) y apertura para \(-1\). El parámetro de cada
realización debe conservarse: esto no introduce tres tiempos externos
independientes. La identidad dual \(\epsilon^2=0\) publica el primer jet
de la acción; no es por sí misma una evolución unitaria finita.

Si \(BJ_\tau=J_{\tau'}B\) y \(B\) es invertible, elevar al cuadrado da
\((\tau-\tau')B=0\). Por tanto una transición de régimen no puede
presentarse como conjugación de esos generadores con \(\tau\ne\tau'\).
El propietario sí construye composiciones entre sus fibras mediante enlaces
simplécticos y conservación de los complementos de memoria.

En dimensión geométrica \(d\), con métrica interna
\(\eta=\operatorname{diag}(-1,1,\ldots,1)\), ponemos

\[
(J_{ab})^c{}_d=\delta_a^c\eta_{bd}-\delta_b^c\eta_{ad},\qquad
P_a^{(\tau)}=
\begin{pmatrix}0&e_a\\-\tau\eta_{a\bullet}&0\end{pmatrix}.
\tag{1}
\]

Los \(J_{ab}\) se incluyen en el bloque superior izquierdo de tamaño
\(d\). Multiplicar estas matrices prueba

\[
[J_{ab},P_c]=\eta_{bc}P_a-\eta_{ac}P_b,\qquad
[P_a,P_b]=-\tau J_{ab}.
\tag{2}
\]

Con \(d=4\), las hojas no nulas preservan la forma
\(\operatorname{diag}(\eta,\tau)\): son las realizaciones de de Sitter
para \(\tau=+1\) y anti-de Sitter para \(\tau=-1\); \(\tau=0\) da
el grupo afín de Poincaré. Para una realización de Cartan plana y torsión
nula, \(F_\omega^{ab}=\tau\ell^{-2}e^a\wedge e^b\). El signo del
término cosmológico queda así fijado por la convención del propietario.
No se confunde con el signo de un Hamiltoniano cuadrático ni con la firma
normal de una hipersuperficie.

## 3. El conmutador sale de la variación del transporte realizado

La igualdad de holonomías del propietario 30d realiza las rutas TPK mediante
\(\mathcal A_\tau=\frac12\omega^{ab}J_{ab}+\ell^{-1}e^aP_a^{(\tau)}\).
Con \(D=d+\rho(\mathcal A_\tau)\), el transporte satisface
\(\dot U=-\rho(\mathcal A_\tau(\dot\gamma))U\).

La variación de una ruta \(\gamma\) por un campo \(\xi\) es

\[
\delta_\xi U_\gamma
=-A(\xi_f)U_\gamma+U_\gamma A(\xi_i)
-\int U_{f,t}F(\xi,\dot\gamma)U_{t,i}\,dt.
\tag{3}
\]

Aquí \(A=\rho(\mathcal A_\tau)\), \(F=dA+A\wedge A\). Se obtiene
diferenciando la ecuación de transporte, integrando por partes el término
\(A(\delta\dot\gamma)\) y conservando el orden de los factores. La
curvatura mide el defecto de las dos deformaciones sucesivas del mismo
transporte, no un campo agregado después.

Para una sección suave y campos \(\xi,\eta\), expandir las derivadas da

\[
\boxed{[D_\xi,D_\eta]=D_{[\xi,\eta]}+F(\xi,\eta).}\tag{4}
\]

La realización trítica aporta de forma efectiva

\[
\mathcal F_\tau=\tfrac12(F_\omega^{ab}-\tau\ell^{-2}e^a\wedge e^b)J_{ab}
+\ell^{-1}T^aP_a^{(\tau)}.
\tag{5}
\]

Así se conservan curvatura y torsión en el conmutador. Si la contorsión se ha
eliminado variacionalmente en una carta efectiva, se utiliza su conexión
reducida y su término inducido; no se mantiene simultáneamente una contorsión
independiente en (5) y la energía de su eliminación.

**Teorema 1 (álgebra covariante con todos sus términos).** Para pares
\((\xi,\lambda)\), con \(\lambda\) una sección del álgebra interna
representada, definimos \(\mathscr D_{\xi,\lambda}=D_\xi+\rho(\lambda)\).
Entonces

\[
[\mathscr D_{\xi,\lambda},\mathscr D_{\eta,\mu}]
=\mathscr D_{[\xi,\eta],\nu},\quad
\nu=D_\xi^{\rm ad}\mu-D_\eta^{\rm ad}\lambda
+[\lambda,\mu]+\mathcal F_\tau(\xi,\eta).
\tag{6}
\]

**Prueba.** (4) calcula los términos con dos derivadas. La regla de Leibniz
calcula los dos términos mixtos y el último producto da
\(\rho([\lambda,\mu])\). La suma es (6). El jacobiador vertical restante
es la evaluación de \(D\mathcal F_\tau\), que se anula por Bianchi; el
horizontal es el jacobiador de campos vectoriales. También puede comprobarse
directamente por la asociatividad de los operadores sobre su dominio suave
común. ∎

Se pueden usar coeficientes suaves arbitrarios, incluidos lapsos de soporte
compacto. No se exige que sean constantes ni que el transporte sea abeliano.
Para \(\tau\) constante, (5) es la curvatura de ese régimen. Si se hace
variar \(\tau\) suavemente, la derivada de las matrices (1) también
contribuye a \(d\mathcal A\); omitirla no conserva (4). Ese cálculo vive
en el álgebra matricial ambiente: en \(\tau=0\),
\(\partial_\tau P_a\) tiene un bloque inferior que no pertenece al sector
de traslaciones afines. No se declara cerrado ese término adicional dentro
de una única álgebra de Cartan de tipo fijo. Las transiciones
discretas entre hojas se componen con sus enlaces, como en §5, y no se
simulan mediante una conjugación inexistente.

## 4. Lapsos normales arbitrarios: variar la normal de la pantalla

En una carta suave no degenerada, sea \(X:\Sigma\to M\) una pantalla
embebida, \(e_i=\partial_iX\), \(q_{ij}=g(e_i,e_j)\), y \(n\) su
normal unitaria con \(g(n,n)=\varepsilon\in\{+1,-1\}\). La métrica
ambiente se mantiene fija en esta variación cinemática; los campos de la
realización y sus cambios de marco siguen siendo los recibidos de 30d.

Definimos el campo en el espacio de embeddings
\(\mathfrak X_N[X]=Nn_X\), para un lapso suave \(N\) fijado como función
de las coordenadas de \(\Sigma\). Derivar
\(g(n,e_i)=0\) y \(g(n,n)=\varepsilon\), usando la conexión métrica de
Levi–Civita de \(g\), produce

\[
\delta_Nn=-\varepsilon q^{ij}(\partial_jN)e_i.
\tag{7}
\]

La torsión de una conexión material separada no altera esta derivación de la
normal métrica. Si se escribe con otra conexión, deben conservarse sus
términos de torsión en lugar de identificarlas silenciosamente.

**Teorema 2 (deformaciones normales).** Con el corchete de campos definido
por \([X,Y]=DY\cdot X-DX\cdot Y\),

\[
\boxed{[\mathfrak X_N,\mathfrak X_M][X]
=\varepsilon\,dX\!\left(q^{ij}(N\partial_jM-M\partial_jN)\partial_i\right).}
\tag{8}
\]

**Prueba.** Los lapsos están fijados en las coordenadas de la pantalla, por
lo que el corchete aplicado a \(X\) es
\(M\delta_Nn-N\delta_Mn\). Sustituir (7) da (8). La normal y \(q\)
son funciones del embedding; no se congelan al iterar el cálculo. Jacobi
se conserva porque se trata de campos sobre ese espacio de configuraciones,
no de un álgebra con \(q^{ij}\) artificialmente constante. ∎

En la convención simpléctica del propietario,
\(\iota_{X_H}\omega=dH\), el momento cotangente de un campo
\(\mathfrak X\) es \(J_{\mathfrak X}=p(\mathfrak X)\) y satisface
\(\{J_{\mathfrak X},J_{\mathfrak Y}\}=-J_{[\mathfrak X,\mathfrak Y]}\).
Por tanto (8) da

\[
\{J_N,J_M\}=-\varepsilon J_{q^{ij}(N\partial_jM-M\partial_jN)\partial_i}.
\tag{9}
\]

Para una normal temporal lorentziana \(\varepsilon=-1\), aparece el signo
positivo usual del generador tangencial. \(\varepsilon\) y \(\tau\)
no son el mismo parámetro: (8) vale en las tres curvaturas tríticas dentro
de sus cartas no degeneradas.

El levantamiento covariante conserva además los términos verticales de (6).
No se sustituyen todos los cambios de pantalla por una traslación interna
\(NP_a\) con normal fija: ésta omitiría (7) y perdería los gradientes
espaciales de los lapsos.

## 5. Profundidad arbitraria, retorno afín y cambio de régimen

El propietario integral entrega, para cada emisión,

\[
\mathsf A_\epsilon(m)=C_\epsilon m+\kappa_\epsilon,\quad
\kappa_{\epsilon_2\epsilon_1}
=\kappa_{\epsilon_2}+C_{\epsilon_2}\kappa_{\epsilon_1}.
\]

Su representación homogénea es

\[
\widetilde A_\epsilon=
\begin{pmatrix}C_\epsilon&\kappa_\epsilon\\0&1\end{pmatrix}.
\]

Si \(pC'=Cp\) y \(p\kappa'=\kappa\), entonces
\(\widetilde p\widetilde A'=\widetilde A\widetilde p\), con
\(\widetilde p=\operatorname{diag}(p,1)\). Multiplicar en el orden de la
ruta demuestra el mismo cuadrado para cualquier número finito de emisiones,
sin cota prefijada de profundidad. La familia compatible de todos los prefijos
conserva el registro completo; no se sustituye por un entero infinito.

Esta prueba entrelaza **retornos afines**. No demuestra por homonimia
\(p\mathbb H'=\mathbb Hp\) para el Hamiltoniano cuántico total. Ese
cuadrado requiere su propia forma, dominio o resolvente, tratados en las
otras notas.

Para el paso entre fibras de distinto régimen se conservan los mapas
simplécticos \(B_k\), \(E_k=e^{t_kJ_{\tau_k}}\), y las lecturas

\[
T_k=B_k(8I+E_k)/9,\qquad
D_k=B_k\sqrt8(E_k-I)/9.
\]

El balance demostrado en el propietario es

\[
\Omega_0=P_N^*\Omega_NP_N+
\sum_{k=0}^{N-1}(D_kP_k)^*\Omega_{k+1}(D_kP_k),\quad
P_{k+1}=T_kP_k.
\tag{10}
\]

El terminal y todos los complementos permanecen. La identidad es simpléctica
y no presupone una norma positiva en los tres regímenes. Puede usarse para
cualquier secuencia finita de hojas; no requiere
\(B_kJ_{\tau_k}=J_{\tau_{k+1}}B_k\).

**Composición nueva con el álgebra covariante.** Para mapas de fibra
\(F:E'\to E\), la condición correcta para transportar (6) es

\[
dF+AF-FA'=0,\qquad F\rho'(\lambda')=\rho(\lambda)F.
\tag{11}
\]

Entonces \(FD'\psi'=D(F\psi')\), y aplicar dos veces da
\(F\mathcal F'=\mathcal FF\). Se conserva el corchete (6) y, por
consiguiente, su Jacobi. Esto no exige que las etiquetas \(\tau_k\) sean
conjugadas: usa la conexión y los enlaces reales de la ruta completa. Los
cuadrados de retorno afín proporcionan la parte de memoria de (11) en toda
profundidad; la realización diferencial de la parte geométrica conserva su
condición de holonomía propia, no se obtiene solamente de una igualdad de
rangos.

## 6. Cambio de dimensión de pantalla sin perder el corchete

La dimensión del propietario es
\(d_\Sigma=\dim(M/\mathcal R)\), no una etiqueta insertada en una
métrica. Un transporte \(F\) lleva relaciones a relaciones y por ello
induce \(\bar F:M/\mathcal R\to M'/\mathcal R'\). Puede ser rectangular
o cambiar rango; no se trata como un cambio de marco invertible.

Si los operadores \(A,B\) conservan las relaciones y los cuadrados
\(\bar FA=A'\bar F\), \(\bar FB=B'\bar F\) se cumplen, entonces

\[
\boxed{\bar F[A,B]=[A',B']\bar F.}\tag{12}
\]

Multiplicar los cuadrados prueba la igualdad, sin requerir inyectividad ni
igualdad de dimensiones. Si no se cumplen exactamente, su defecto también
queda calculado. Para \(\Delta_A=\bar FA-A'\bar F\),

\[
\Delta_{[A,B]}=A'\Delta_B-B'\Delta_A+\Delta_AB-\Delta_BA.
\tag{13}
\]

Esta identidad permite comprobar si las relaciones y la memoria conservadas
son suficientes antes de comprimir. Conservar el complemento completo,
según (10), evita presentar un defecto de proyección como un defecto del
álgebra completa.

El cálculo de normales (7)–(9) utiliza una pantalla de rango constante y
métrica inducida no degenerada. En un salto de rango se compone por (12).
Un lapso desciende al cociente únicamente si no distingue estados
identificados por ese cociente. Las direcciones retiradas pueden permanecer
en el archivo completo; no se exige que sus lapsos se conviertan en una
función unívoca del dato reducido cuando no lo son.

## 7. Acción efectiva, generadores y alcance de la representación cuántica

El funcional de memoria ya compuesto es
\(E=\langle r,Wr\rangle\), \(r_a=f_t-U_af_s\), y su eliminación
interior conserva \(E_{\rm eff}=z^*R^{-1}z\), con
\(z=b-U_\gamma a\) y \(R=BW^{-1}B^*\). Para cambios invertibles de
marco \(f'=Vf\), \(r'=Er\), el peso se transporta como
\(W'=E^{-*}WE^{-1}\). Así la acción es exactamente la misma, incluidos
los regímenes no unitarios del TRIT.

Su diferencial, ya dado por el propietario, es

\[
\delta E=-2\operatorname{Re}\sum_a\langle(Wr)_a,
\delta U_af_{s(a)}\rangle+\langle r,\delta Wr\rangle
+\hbox{variaciones de campo}.
\tag{14}
\]

Insertar (3) produce las respuestas a deformaciones de ruta, con curvatura,
extremos y memoria. Aplicar dos variaciones y restar conserva (6): omitir
sus términos de marco o de peso cambiaría la propia acción. Las cargas
cotangentes que implementan una simetría de este funcional tienen el
corchete (9) y sus análogos de marco, siempre que el resto de la acción
reciba la misma transformación.

En una configuración suave **finidimensional** \(Q\), el levantamiento
cuántico sobre semidensidades es explícito:

\[
\widehat J_X=-i\hbar\mathcal L_X^{1/2},\qquad
\mathcal L_X^{1/2}=X^a\partial_a+\tfrac12\partial_aX^a.
\]

En \(C_c^\infty(Q)\) se verifica

\[
[\widehat J_X,\widehat J_Y]=-i\hbar\widehat J_{[X,Y]}.
\tag{15}
\]

El término de divergencia conserva el producto de semidensidades. Para un
flujo completo, su pullback unitario define por Stone un generador
autoadjunto cuya acción sobre ese dominio es la expresión anterior, con la
orientación temporal correspondiente. La prueba es local en coordenadas y
las semidensidades hacen compatible el cambio de cartas. No se ha introducido
un determinante fermiónico ni una afirmación sobre anomalías quirales.

El espacio completo de embeddings y campos gravitatorios no es una
configuración finidimensional con medida de Lebesgue canónica. Allí (8) es
una identidad geométrica exacta de derivaciones, pero (15) no autoriza a
inventar un producto de Hilbert ni un dominio común de restricciones. Tampoco
identifica por sí misma \(J_N\), momento cinemático de embeddings, con la
restricción dinámica obtenida de la acción PCH reducida y del Hamiltoniano
acoplado. Esta nota calcula el generador geométrico y su corchete para hacer
esa comparación, sin definirlo retrospectivamente como el lado izquierdo.

## 8. Falsadores focales y resultado

Tres falsadores concretos delimitan la construcción:

1. Con normal congelada, dos deformaciones \(Nn,Mn\) de una pantalla plana
   darían conmutador cero. Para \(N(s)=s^2,M(s)=s^3\), (8), con normal
   temporal lorentziana, da desplazamiento tangencial \(-s^4\partial_s\):
   la normal debe variar como (7).
2. En \(D_x=\partial_x\), \(D_y=\partial_y+xJ\), el conmutador es
   multiplicación por \(J\). Quitar la curvatura de (4) predice
   incorrectamente cero.
3. Para \(X_\lambda(s,t)=(s,\lambda t,0)\),
   \(q=\operatorname{diag}(1,\lambda^2)\). Un lapso dependiente de \(t\)
   no desciende al colapso \(\lambda=0\); su gradiente contiene
   \(\lambda^{-2}\partial_tN\). No puede conservarse mediante un cambio
   de base invertible de la pantalla reducida. Debe conservarse esa dirección
   en la memoria completa o restringirse al lapso que sí desciende.

Resultado demostrado: álgebra covariante trítica completa con Bianchi/Jacobi,
conmutador de lapsos normales arbitrarios dentro de cada carta no degenerada,
naturalidad de ese corchete por mapas de pantalla compatibles y composición
del registro afín a profundidad arbitraria sin imponer conjugación entre
regímenes. Se da además una representación cuántica exacta de los generadores
geométricos en las configuraciones finidimensionales indicadas. No se
identifica un retorno afín, un lector de memoria o un momento cinemático con
el Hamiltoniano cuántico total por compartir una letra o una dimensión.

El script `verificar_trit_curvaturas_deformaciones.py` contrasta las relaciones
matriciales de las tres hojas, el balance de memoria en una ruta de regímenes
mezclados, el retorno afín y los falsadores de normal congelada y reducción de
rango. No sustituye las demostraciones para lapsos suaves arbitrarios,
profundidades sin cota prefijada o dominios de operadores no acotados.
