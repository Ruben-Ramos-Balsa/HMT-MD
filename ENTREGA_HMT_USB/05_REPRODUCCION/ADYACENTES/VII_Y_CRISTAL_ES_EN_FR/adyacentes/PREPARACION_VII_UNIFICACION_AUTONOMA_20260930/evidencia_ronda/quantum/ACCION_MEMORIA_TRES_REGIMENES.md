# Acción, memoria y evolución en los tres regímenes TRIT

## 1. Base recuperada y punto de aplicación

APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo es el origen de los operadores utilizados. Se conservan conjuntamente las cinco construcciones del continuo, las hojas y el registro de retorno. Las secciones de acción y las constantes se reciben como salidas internas anteriores. El reconocimiento convencional posterior consiste aquí en representar y componer esos transportes en un espacio de funciones; no se introducen valores experimentales para seleccionar el generador.

El propietario actual `X_ES/sections/hamiltonianos_curvatura.tex`, dentro de `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes`, demuestra:

- los generadores nativos `J_τ²=−τI`, τ=+1,0,−1, a partir del ciclo de aumento, el nilpotente y la incidencia areal–volumétrica;
- el cambio de marco simpléctico que los lleva a los representantes cuadráticos, conservando su orientación;
- el Hamiltoniano de marco variable y la carga `I_mem=s−18g`;
- la realización espinorial del operador de masa recibido, sin identificar la masa con su mero histograma.

La representación geométrica `VIII_ES/manuscrito/30d_realizacion_geometrica.tex`, §§3, realiza `[P_a^(τ),P_b^(τ)]=−τJ_ab` y la curvatura de Cartan correspondiente. El signo de un generador cuadrático, el de la curvatura de una superficie espacial y el de la curvatura cuatridimensional conservan sus tipos: no se intercambian por compartir tres valores.

`II_ES/sections/gravedad_rigidez_20260926.tex`, desde «Escalas de Planck y especialización del carácter unitario», fija la dependencia conjunta de masa, longitud, energía, G y sección de acción. La continuación presente añade las pruebas operatorias siguientes. La interpretación de pasado, presente y futuro procede de `VIII_ES/manuscrito/sections/temporalidad_trit.tex`: antecedente conservado, actualización y prolongación; no son tres relojes físicos independientes.

## 2. Cuantización exacta del transporte trítico de marco variable

En la realización de una fibra canónica recibida se toman `Qf(x)=xf(x)` y `Pf(x)=−iℏ f'(x)` sobre el dominio común `S(R)`. ℏ>0 es la sección generada. Se usa la carta canónica normalizada en la que Q y P tienen dimensión de raíz de acción, η es adimensional y ω tiene dimensión de frecuencia. Esto fija las unidades de la realización sin seleccionar ninguna constante. Sean

\[
A=Q^2/2,\quad B=(QP+PQ)/2,\quad C=P^2/2.
\]

Las relaciones canónicas dan exactamente

\[
[A,B]=2i\hbar A,\qquad [B,C]=2i\hbar C,\qquad[A,C]=i\hbar B.
\tag{1}
\]

No hay un término de ordenamiento adicional: el producto mixto está simetrizado. Esto puede comprobarse expandiendo cada conmutador y usando `[Q,P]=iℏI`.

Para τ∈{+1,0,−1}, η(t) real C¹ y ω(t)>0 continua, definimos

\[
I_{\tau,\eta}=\tau e^{-\eta}A+e^\eta C,\qquad
H_{\tau,\eta}(t)=\omega(t)I_{\tau,\eta(t)}+\frac{\dot\eta(t)}2 B.
\tag{2}
\]

Es la realización simétrica del Hamiltoniano ya obtenido en el propietario, incluido su término de conexión. De (1),

\[
\partial_tI_{\tau,\eta}+\frac{i}{\hbar}[H_{\tau,\eta},I_{\tau,\eta}]=0
\tag{3}
\]

en S(R): la derivada explícita es `dotη(−τe^−ηA+e^ηC)` y el conmutador aporta su opuesto.

**Teorema 1.** El propagador exacto es

\[
U_\tau(t,s)=S_{\eta(t)}\exp\!\left[-\frac{i}{\hbar}
(\tau A+C)\int_s^t\omega(u)\,du\right]S_{\eta(s)}^*,
\quad
(S_\eta f)(x)=e^{-\eta/4}f(e^{-\eta/2}x).
\tag{4}
\]

Es unitario para todo tiempo para el que estén definidos η y la integral, conserva S(R), satisface composición de propagadores y transporta el invariante (3).

**Prueba.** El cambio de variable en la integral L² demuestra que S_η es unitario. Su conjugación da `S_ηQS_η*=e^−η/2Q`, `S_ηPS_η*=e^η/2P`, y `iℏ dotS_η S_η*=dotη B/2`. Derivar (4) sobre S(R) produce exactamente (2). El generador `A+C` es el oscilador autoadjunto; C es el multiplicador autoadjunto de momento cuadrado tras Fourier. Para `C−A`, una rotación simpléctica de ángulo π/4 lo transforma en `(Q'P'+P'Q')/2`, generador del grupo unitario de dilataciones. Sus cierres autoadjuntos y propagadores son por tanto explícitos. Estas transformaciones metaplécticas conservan S(R). La cancelación de los factores S_η y la aditividad de la integral prueban la ley de composición. La conjugación de I o, equivalentemente, (3), prueba la conservación. ∎

En τ=−1 la energía cuadrática no es semidefinida, pero su evolución sigue siendo unitaria. Confundir autoadjunción con positividad excluiría incorrectamente el régimen hiperbólico. En cambio, pasar de un τ a otro no es conjugar sus generadores: sus cuadrados son distintos. El calendario efectivo se compone mediante sus operadores en orden, conservando en la historia dónde cambia el régimen.

## 3. Profundidad arbitraria y control de las aproximaciones temporales

La profundidad arbitraria del productor HMT se conserva; no se deduce de unas pruebas numéricas. Para su realización temporal cuadrática se puede demostrar además un resultado de límite, no sólo una composición finita.

Sea τ(t) cualquier función medible con valores −1,0,+1, sea η absolutamente continua y acotada en cada intervalo compacto, y sea ω integrable en dichos intervalos. El generador matricial del transporte completo es

\[
K(t)=\omega(t)
\begin{pmatrix}0&e^{\eta(t)}\\-\tau(t)e^{-\eta(t)}&0\end{pmatrix}
+\frac{\dot\eta(t)}2\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
\tag{5}
\]

No se exige periodicidad ni un número finito de cambios de τ. K pertenece a `L¹_loc` y al álgebra simpléctica. Su solución fundamental S(t,s) existe por la serie de integrales iteradas y satisface

\[
\|S(t,s)\|\le \exp\int_{\min(s,t)}^{\max(s,t)}\|K(u)\|du,\qquad S^T\Omega S=\Omega.
\tag{6}
\]

La serie converge porque su término de orden n está acotado por `∥K∥₁^n/n!`. La derivada de `S^TΩS` se anula casi en todas partes, lo que prueba la segunda identidad.

Para aproximaciones temporales K_n por tramos en particiones nonádicas, elegidas de modo que `∥K_n−K∥₁→0`, la fórmula de variación da

\[
\sup_{s\le t\le T}\|S_n(t,s)-S(t,s)\|
\le e^{\|K_n\|_1+\|K\|_1}\|K_n-K\|_1\longrightarrow0.
\tag{7}
\]

Una construcción explícita de tales aproximaciones es la media de K en cada celda de la partición. Es una aproximación del operador temporal ya construido, no una sustitución del selector ternario ni una modificación de su historia. La densidad de funciones por tramos y la contractividad de la media en L¹ prueban la convergencia requerida.

El camino simpléctico parte de la identidad y determina un único levantamiento metapléctico continuo con ese origen. Su representación unitaria en L² da U(t,s). La convergencia uniforme de caminos de (7), conservando el levantamiento, implica `U_n(t,s)f→U(t,s)f` fuertemente, para cada f y uniformemente en compactos temporales. Se prueba localmente en cartas del recubrimiento y se concatenan finitas cartas sobre cada camino compacto; la continuidad fuerte de la representación termina el argumento.

Así quedan cubiertas historias temporales aperiódicas y profundidad de aproximación arbitraria en esta realización. Las condiciones de integrabilidad pertenecen a la parametrización temporal, no restringen el número de dígitos del productor. Una profundidad simbólica ilimitada no autoriza por sí sola una parametrización singular para la que la integral de (5) diverja: son objetos diferentes y aquí se ha dado la construcción temporal que evita ese salto.

El invariante (3) tenía τ fijo. Si cambia el régimen, no se declara conservada su misma expresión instantánea: un salto aporta `ΔI=Δτ e^−η A`. El invariante global de la historia es `J(t)=U(t,s)I_{τ(s),η(s)}U(t,s)*`, con dominio transportado `U(t,s)D(I_{τ(s),η(s)})`. Satisface `U(t,s)*J(t)U(t,s)=I_{τ(s),η(s)}`. Así la composición conserva el observable transportado y la memoria del cambio de régimen, en lugar de borrar ese cambio identificando indebidamente los tres generadores.

## 4. La memoria permanece como operador, no sólo como relato

El propietario recibe el retorno adimensional `(g,s)↦(g+4,s+72)` y construye `I_mem=s−18g`. Para no confundirlo con las unidades de §2, se declara su transducción: una escala de acción recibida a_*>0 da Q_m=g y P_m=a_*s. La representación canónica es Q_m f(x)=xf(x), P_m f(x)=−iℏ f'(x), con x adimensional. Así,

\[
\widehat I_{\rm mem}=P_m-18a_*Q_m,\quad
\widehat H_{\rm mem}=\widehat I_{\rm mem}^2/(2a_*),\quad
\widehat H_{\rm ret}=4\widehat I_{\rm mem}.
\tag{8}
\]

Los generadores de (8) tienen dimensión de acción y actúan respecto del parámetro adimensional u; no se confunde u con tiempo físico. Si la carta recibida proporciona un reloj t_*>0 y t=t_*u, los Hamiltonianos de energía correspondientes son H_mem/t_* y H_ret/t_*.

La transformación de fase `Wf(x)=exp(i9a_*x²/ℏ)f(x)` satisface `WP_mW*=P_m−18a_*Q_m`. Por tanto los tres operadores de (8) se construyen por conjugación de P_m, P_m²/(2a_*) y 4P_m; sus cierres y dominios autoadjuntos quedan fijados. Conmutan fuertemente porque son funciones del mismo operador autoadjunto.

El propagador de retorno produce en Heisenberg

\[
U_{\rm ret}(u)^* Q_m U_{\rm ret}(u)=Q_m+4uI,\qquad
U_{\rm ret}(u)^* P_m U_{\rm ret}(u)=P_m+72a_*uI.
\tag{9}
\]

La prueba es el conmutador con 4(P_m−18a_*Q_m); la segunda derivada es cero porque el primero es escalar. Al dividir P_m por a_* se recupera exactamente s→s+72u. En particular, cada retorno conserva I_mem y aumenta ambas coordenadas. Tener una carga conservada no significa que el estado o su historia estén inmóviles. La fase W incorpora el término de frontera `a_*d(9g²)` de la acción transducida; no se borra al hacer el cambio canónico.

## 5. Acción y gravedad: covarianza exacta de la evolución y de la restricción

La fuente de rigidez demuestra, para el carácter positivo Y,

\[
L=\frac{5759}{23040}\alpha^{16}L_*,\quad
H_a=\frac{\hbar_ac}{L}Y,\quad M_a=\frac{\hbar_a}{cL}Y,
\quad R=LY,\quad\Lambda=LY^{-1},\quad
G_a=\frac{c^3L^2}{\hbar_a}.
\tag{10}
\]

Si dos secciones de acción tienen razón positiva ρ, manteniendo L,c,Y, se sigue

\[
H_b=\rho H_a,\quad M_b=\rho M_a,\quad G_b=G_a/\rho,
\qquad\frac{H_b}{\hbar_b}=\frac{H_a}{\hbar_a}=\frac cL Y.
\tag{11}
\]

**Proposición 2.** Sobre los mismos dominios espectrales, las dos secciones inducen exactamente el mismo grupo unitario `exp(−it cY/L)`, el mismo radio y la misma longitud recíproca. Si el tensor material completo se transporta con `T_b=ρT_a`, el producto fuente `G_b T_b=G_a T_a` y, por tanto, la restricción geométrica Einstein–Schrödinger se conservan también.

**Prueba.** Sustitución en (10), cálculo funcional y multiplicación de las dos reglas de escala. El término de torsión debe pertenecer a la misma acción y sección; no puede cambiarse independientemente. ∎

No se supone que un cambio de la razón interna `R_act=ℏ_pre/ℏ_ret` deje fijo Y: el operador másico `M_β=R_act^{B_M/2}M_0R_act^{B_M/2}` registra precisamente esa dependencia. La proposición compara secciones con el mismo carácter o una reescala simultánea de ambas acciones, no modifica selectivamente ese cociente.

En una normalización de campos donde la acción total es `S_a=ℏ_a S_0`, con longitud y coeficientes adimensionales fijados, su variación métrica da `T_a=ℏ_a T_0` y el supuesto de la proposición se obtiene de la misma acción. La acción geométrica posee el prefactor `c³/G_a=ℏ_a/L²`, por lo que entra en esa composición. Esto explica por qué la ecuación de la acción y la de G enlazan la evolución con su respuesta geométrica; no son simples números comparados al final.

La propiedad conserva un cierre operatorio si éste está demostrado, pero no elimina un defecto por cambio de escala. Para restricciones C que se escalen como la acción,

\[
\Delta_{ab}=[C_a,C_b]-i\hbar f_{ab}^{\ \ c}C_c
\quad\Longrightarrow\quad
\Delta'_{ab}=\rho^2\Delta_{ab}.
\tag{12}
\]

Por ello la prueba del cierre tiene que utilizar los transportes y restricciones efectivos, además de (10). (12) es un falsador algebraico concreto contra atribuir a una sustitución escalar el efecto de demostrar un conmutador. No niega el origen HMT de ninguna constante.

## 6. Composición con geometría, materia y dimensión

La lectura conjunta conserva tres afirmaciones diferentes: la evolución unitaria de los tres regímenes (4)–(7); la memoria activa con carga conservada (8)–(9); y la covarianza acción–masa–gravedad (10)–(11). Se componen con los transportes de Cartan y la variación de normal de pantalla desarrollados en `TRIT_CURVATURAS_Y_DEFORMACIONES.md`, y con el carácter másico sobre historias completas en `LIMITE_MATERIA_MEMORIA.md`.

Estos resultados amplían de manera efectiva la prueba más allá del corte finito anterior. Ninguna de las identidades identifica, por sí sola, un generador afín de retorno con un Hamiltoniano, ni un cambio de rango con una equivalencia unitaria sobre espacios de distinta dimensión. El complemento conservado en memoria y el transporte de los dominios se mantienen en la composición.
