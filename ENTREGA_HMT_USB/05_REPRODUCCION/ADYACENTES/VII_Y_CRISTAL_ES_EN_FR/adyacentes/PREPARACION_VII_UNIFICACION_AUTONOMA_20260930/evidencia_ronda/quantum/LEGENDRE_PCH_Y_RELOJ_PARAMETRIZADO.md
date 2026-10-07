# Momento de deformación, Legendre PCH y parametrización del reloj interactuante

Composición y pruebas focales nuevas, 29 de septiembre de 2026. Esta nota
no modifica los resultados anteriores ni cambia sus hipótesis. Distingue
el cargo normal de una acción covariante, el momento compensador de su
parametrización y los generadores unitarios de cambios de coordenada.

## 1. Datos recibidos y punto de corte causal

Se reutiliza la genealogía material de
[RECIBO_GENEALOGIA.json](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/RECIBO_GENEALOGIA.json>): APP produce las dos
hojas con residuos y cocientes; TRIT conserva régimen y orientación; el
TPK transporta el estado enriquecido con ruta, frontera, acarreo, hoja y
memoria. La conexión nonádica conjunta prolonga ese mismo estado, sin
reiniciarlo al retornar la fase. La estructura discreta conjunta del
continuo y sus cinco construcciones consustanciales no se separan aquí.

El corte de esta nota es posterior: utiliza la realización geométrica de
esos transportes y los lectores de acción ya generados. No selecciona sus
coeficientes mediante la teoría convencional. La transformación de
Legendre, la corriente de Noether y la suspensión son lenguajes de
realización y prueba posteriores, no generadores de constantes.

Propietarios efectivos:

- [Composición corriente–conexión, 30c](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30c_composicion_corriente_conexion.tex>): variación del transporte de pantalla y su corriente, con pesos y acción de marco conservados.
- [Realización geométrica, 30d](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30d_realizacion_geometrica.tex>): cotetrada no degenerada y conexión; igualdad declarada entre las holonomías realizadas y los transportes TPK; hojas de curvatura y representación espinorial.
- [Respuesta Cartan–Holst, 31](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex>), etiquetas `vii:eq:accion-cartan-holst`, `vii:eq:corriente-variacional`, `vii:eq:ecuacion-cartan-holst`: normalización de la acción y eliminación algebraica de contorsión para materia afín en ella.
- [Legendre y Einstein–Schrödinger, 11p](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex>): acción covariante y Hamiltoniano restringido de la misma realización; dominio y ordenamiento de la prolongación cuántica.
- [SUSPENSION_RELOJ_INTERACTUANTE.md](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/SUSPENSION_RELOJ_INTERACTUANTE.md>), teoremas 1–4: operador autoadjunto completo de reloj interactuante, retorno activo de memoria, Gauss y límite fuerte de lectores. Se aplica el resultado de esa nota, no un logaritmo escogido para el retorno.

Los coeficientes \(\hbar,c,\kappa,\gamma,\Lambda\) se reciben de sus
lectores y de la carta común; permanecen fijos en la variación de 31.
No se vuelven a calibrar. Esta nota aporta dos pruebas, no una nueva
derivación del catálogo de constantes ni una auditoría del corpus.

## 2. El cargo normal procede de la misma acción

Trabajamos en la carta cuatro-dimensional no degenerada de 30d y 31,
con una foliación espaciotemporal, una hipersuperficie espacial \(\Sigma\)
y normal unitaria \(n\). Se retienen las condiciones de borde del
problema variacional. Para exponer la igualdad sin cargo de borde se
puede tomar \(\Sigma\) cerrada o lapsos de soporte interior.

Escribamos

\[
 a=\frac1{2\kappa c},\quad b=\frac1{\kappa c}=2a,\qquad
 B_{IJ}=(\mathsf P_\gamma\Sigma)_{IJ},\quad
 \Sigma^{IJ}=e^I\wedge e^J,
 \quad \mathsf P_\gamma=\star+\gamma^{-1}I.
 \tag{1}
\]

La acción recibida es

\[
 S=\int_M L,\qquad
 L=aB_{IJ}\wedge F^{IJ}-b\Lambda\operatorname{vol}_e+L_m.
 \tag{2}
\]

Aquí \(L_m\) es la acción material covariante que realmente se varía;
no se deduce su identidad con otro Hamiltoniano sólo de su nombre.
Incluye sus conexiones internas y, cuando corresponde, sus campos
espinoriales. Definimos \(\eta_I=\iota_{E_I}\operatorname{vol}_e\),
\(\delta_eL_m=\delta e^I\wedge\tau_I+\mathrm d(\cdots)\) y usamos
la convención de 31,
\(\delta_\omega L_m=-\tfrac12\delta\omega^{IJ}\wedge\sigma_{IJ}
+\mathrm d(\cdots)\). La variación geométrica da

\[
 \theta_{\rm geom}(\delta)=aB_{IJ}\wedge\delta\omega^{IJ},
 \quad
 \mathcal E_I=2a e^J\wedge(\mathsf P_\gamma F)_{IJ}
              -b\Lambda\eta_I+\tau_I,
 \quad
 \mathcal E^\omega_{IJ}=aD_\omega B_{IJ}-\tfrac12\sigma_{IJ}.
 \tag{3}
\]

En particular, \(\mathcal E^\omega=0\) reproduce exactamente
\(D_\omega B=\kappa c\sigma\). El potencial simpléctico espacial
es \(\Theta_{\rm geom}=\int_\Sigma\theta_{\rm geom}\). Si se usan
componentes con \(B=\tfrac12B_{ab}\,dx^a\wedge dx^b\), el momento es

\[
 \Pi^a{}_{IJ}=\frac a2\epsilon^{abc}B_{bc,IJ}
             =\frac1{4\kappa c}\epsilon^{abc}B_{bc,IJ}.
 \tag{4}
\]

La escritura en formas (3) fija la normalización antes de escoger si se
suman todos los pares antisimétricos o sólo los independientes.

**Proposición 1 — identidad Noether–Legendre.** En el sistema canónico
obtenido de (2), el generador de una deformación \(\xi\) es el cargo
normal/tangencial de las restricciones de esa misma acción, más sus
transformaciones verticales y su cargo de borde. Para
\(\xi=Nn\), en el cociente de Gauss y con borde nulo, es precisamente
la restricción normal \(\mathcal C[N]\), no un momento de una acción
externa introducido por analogía.

**Prueba geométrica explícita.** Pónganse
\(u^I=\iota_\xi e^I\), \(\lambda^{IJ}=\iota_\xi\omega^{IJ}\).
La identidad
\(\mathcal L_\xi\omega=\iota_\xi F+D_\omega\lambda\) da

\[
 \begin{aligned}
 j_\xi^{\rm geom}
 &=\theta_{\rm geom}(\mathcal L_\xi\omega)-\iota_\xi L_{\rm geom}\\
 &=\mathrm d\bigl(aB_{IJ}\lambda^{IJ}\bigr)
   -a(D_\omega B_{IJ})\lambda^{IJ}
   -2a u^Ie^J\wedge(\mathsf P_\gamma F)_{IJ}
   +b\Lambda u^I\eta_I.
 \end{aligned}
 \tag{5}
\]

No se ha impuesto la ecuación métrica en (5). Los términos materiales
se calculan con el potencial \(\theta_m\) de la misma variación. Para
materia covariante de primer orden, la descomposición canónica de
\(\mathcal L_\xi\) en transporte y rotación vertical añade las
contribuciones a \(\mathcal E_I,\mathcal E^\omega\), las restricciones
de Gauss internas y el cargo material de borde. Si el sistema utiliza
restricciones primarias de segunda clase, esta afirmación se entiende
sobre su superficie o después de la reducción de Dirac; no se omiten
esas restricciones para hacer invertible una Legendre degenerada.

Puede comprobarse la misma igualdad sin una identificación nominal de
cargos. Descomponer
\(\omega=\omega_0dt+\underline\omega\) da
\(F_{0a}=\dot\omega_a-D_a\omega_0\). El término cinético es
\(a\int_\Sigma B\wedge\dot{\underline\omega}\), y la integración
por partes del segundo término deja \(+a\omega_0D B\) y el borde.
Escribir \(e_0=Nn+N^ae_a\), y efectuar la misma Legendre en los
campos materiales, produce

\[
 S=\int dt\left[
 \Theta_{\rm red}(\dot z)
 -\mathcal C[N]-\mathcal V[N^a]-\mathcal G_{\rm L}[\omega_0]
 -\mathcal G_{\rm int}[A_0]\right]+S_{\partial}.
 \tag{6}
\]

Las convenciones de signos en (6) son
\(\mathcal C_I=-\iota_\Sigma^*\mathcal E_I\),
\(\mathcal G_{{\rm L},IJ}=-\iota_\Sigma^*\mathcal E^\omega_{IJ}\),
y \(\mathcal C[N]=\int_\Sigma Nn^I\mathcal C_I\), después de expresar
velocidades materiales en momentos y conservar las primarias.
Por (5) y la Legendre material, el cargo total satisface, en esa
superficie canónica,

\[
 \int_\Sigma j_\xi
 =\mathcal C[u]+\mathcal G_{\rm L}[\iota_\xi\omega]
   +\mathcal G_{\rm int}[\iota_\xi A]
   +\int_{\partial\Sigma}Q_\xi.
 \tag{7}
\]

En (7), \(\mathcal C[u]=\int_\Sigma u^I\mathcal C_I\) incluye
las componentes normal y tangencial. El término geométrico de
\(Q_\xi\) es \(aB_{IJ}\lambda^{IJ}\). El convenio de lift de los
campos espinoriales puede redistribuir la transformación vertical y
el cargo, pero no eliminar ambos sin pasar al cociente y tratar el
borde. En ese cociente, (7) da la afirmación. ∎

La proposición prolonga la equivalencia variacional afirmada en 11p
mediante una identidad calculable. No afirma que una igualdad de
holonomías en 30d pruebe por sí sola una igualdad de formas simplécticas
entre todas las realizaciones posibles de pantalla.

### Torsión reducida una sola vez

Distinguimos la contorsión \(\mathfrak k\) del operador de reloj
\(\mathbb K\). En el dominio afín de 31, su ecuación algebraica tiene
la solución única \(\mathfrak k_*\), y la interacción inducida es
\(-\tfrac14\mathfrak k_*\wedge\sigma\). Si
\(L_{\rm red}=L|_{\mathfrak k_*}\), la regla de la cadena contiene

\[
 \delta L_{\rm red}
 =\left.\delta L\right|_{\mathfrak k_*}
  +\left.\frac{\partial L}{\partial\mathfrak k}\right|_{\mathfrak k_*}
       \delta\mathfrak k_*,
 \qquad
 \left.\frac{\partial L}{\partial\mathfrak k}\right|_{\mathfrak k_*}=0.
 \tag{8}
\]

Por tanto las ecuaciones y la forma presimpléctica se transportan al
reducido, conservando los términos de borde. Si se elimina una
divergencia al escribir la acción de Levi–Civita, se conserva también
su modificación del potencial. En una carta efectiva de primer orden,
(8) es la igualdad usual de momentos de Legendre por sustitución
estacionaria. No se conserva a la vez una contorsión independiente y
su interacción cuártica ya eliminada. Si otro término de la acción
depende de \(\mathfrak k\), su derivada pertenece a la ecuación
estacionaria antes de usar (8).

## 3. Momento de parametrización: el signo no es opcional

Sea \((\mathcal P,\Omega=-\mathrm d\Theta)\) el espacio canónico
reducido de un sistema recibido, y \(h\) su Hamiltoniano en una carta
de reloj. La reparametrización de la misma acción es

\[
 S_{\rm par}[z,r]=\int
 \left[\Theta(z)(z')-h(z)r'\right]d\lambda.
 \tag{9}
\]

\(r\) es la lectura del mismo reloj y \(\lambda\) una etiqueta
arbitraria; no se introduce un cuarto tiempo físico. Legendre da

\[
 p_r=-h,\qquad C=p_r+h=0.
 \tag{10}
\]

La restricción (10) elimina el par añadido como redundancia de
parametrización. Análogamente, al parametrizar una foliación mediante
su embedding \(X\), el momento cotangente
\(J_N=\langle P_X,Nn\rangle\) cumple
\(J_N+\mathcal C[N]=0\), con los términos verticales y de borde de
(7) si no se han reducido. El momento del embedding es el compensador
**opuesto** al cargo físico normal de (7). Confundir esos dos momentos
produciría el signo equivocado aunque ambos se llamaran deformación.

Esta afirmación usa la parametrización de la acción (6), no una
identificación arbitraria entre dos funciones con el mismo símbolo.
No basta, sin embargo, parametrizar un Hamiltoniano distinto para
concluir que éste era la restricción PCH de (6).

## 4. Realización cuántica exacta del reloj interactuante

Sea \(\mathbb K=\mathbb K^*\) el operador de
`SUSPENSION_RELOJ_INTERACTUANTE.md`, sobre su espacio \(\mathscr K\).
Ese operador incorpora el retorno unitario de historias completas y
la interacción local en el orden allí probado. Sus hipótesis no
incluyen que el retorno preserve separadamente el dominio de la
energía local. El período de aquella suspensión se sigue llamando
\(T\), y su fase interna \(s\). Aquí \(r\) parametriza su evolución;
es una redundancia de representación, eliminada por la restricción,
no otra fase independiente añadida a la física.

En \(\mathscr H_{\rm par}=L^2(\mathbb R_r,dr;\mathscr K)\), defínanse

\[
 (Wf)(r)=e^{-ir\mathbb K/\hbar}f(r),\qquad
 C=W(-i\hbar\partial_r)W^*,\qquad
 \operatorname{Dom}C=W H^1(\mathbb R;\mathscr K).
 \tag{11}
\]

**Teorema 2 — restricción de reloj sin elección de logaritmo.**
\(C\) es autoadjunto. Sobre la intersección regular actúa como
\(C=-i\hbar\partial_r+\mathbb K\). Sus soluciones generalizadas
son exactamente la evolución del reloj interactuante,

\[
 \Psi(r)=e^{-ir\mathbb K/\hbar}\psi_0.
 \tag{12}
\]

El espacio físico, con producto dado por los datos \(\psi_0\), es
\(\mathscr K\); no se ha añadido un grado físico de libertad.

**Prueba.** El grupo de \(\mathbb K\) es fuertemente continuo y
unitario, luego W es una multiplicación unitaria. (11) transporta el
dominio del operador autoadjunto de traslación. Derivar
\(e^{ir\mathbb K/\hbar}\Psi(r)\) en el dominio regular demuestra la
expresión diferencial. Por conjugación, \(C\Psi=0\) equivale a
\(\partial_r(W^*\Psi)=0\), que da (12). En todo \(\mathbb R\), una
solución no nula tiene norma constante y no pertenece a
\(\mathscr H_{\rm par}\). En consecuencia el núcleo L² de C es cero;
las soluciones físicas son generalizadas y su norma se fija en una
sección del reloj. No se presenta una evaluación puntual arbitraria
de clases L² como operador acotado. ∎

La acción de Schrödinger parametrizada, en curvas suficientemente
regulares del dominio de \(\mathbb K\), es

\[
 \int d\lambda\left[
 \frac{i\hbar}{2}\bigl(\langle\psi,\psi'\rangle
                  -\langle\psi',\psi\rangle\bigr)
 -r'\langle\psi,\mathbb K\psi\rangle\right].
 \tag{13}
\]

Su ecuación \(i\hbar\psi'=r'\mathbb K\psi\) recupera (12) donde
\(r'\ne0\). Por tanto (11) no sólo renombra un operador: es la
restricción diferencial de la parametrización de esa misma evolución.
Se usa el dominio exacto (11), no la falsa igualdad general
\(\operatorname{Dom}C=\operatorname{Dom}\partial_r\cap
L^2(\operatorname{Dom}\mathbb K)\).

### Álgebra de semidensidades y cambio de lapse

Para \(N\in C_c^\infty(\mathbb R;\mathbb R)\), el campo
\(N(r)\partial_r\) es completo. Su flujo actúa unitariamente sobre
semidensidades. El generador autoadjunto es el cierre de

\[
 p_N=-i\hbar\left(N\partial_r+\frac12N'\right),\qquad
 C_N=Wp_NW^*.
 \tag{14}
\]

El dominio exacto es \(W\operatorname{Dom}p_N\). Un núcleo común
denso e invariante para los cálculos es

\[
 \mathscr D=W\left(C_c^\infty(\mathbb R)\odot\mathscr K_{\rm fin}\right),
 \qquad
 \mathscr K_{\rm fin}=\bigcup_{R>0}\mathbf1_{[-R,R]}(\mathbb K)\mathscr K.
 \tag{15}
\]

La esencial autoadjunción de \(p_N\) también se ve directamente:
las soluciones de deficiencia se transportan a lo largo del flujo
completo como semidensidades con un factor exponencial real. Su norma
constante bajo el transporte unitario obliga a que una solución L²
de cualquiera de los dos signos sea nula. El dominio suave compacto
es un núcleo por regularización local y corte a lo largo de ese flujo.

En \(\mathscr D\),

\[
 C_N=\tfrac12(NC+CN)
 =-i\hbar(N\partial_r+N'/2)+N\mathbb K,
 \qquad
 [C_N,C_M]=-i\hbar C_{NM'-MN'}.
 \tag{16}
\]

En efecto, si \(L_N=N\partial_r+N'/2\), el coeficiente de
\(\partial_r^2\) en \([L_N,L_M]\) se cancela, el de
\(\partial_r\) es \(NM'-MN'\), y el de orden cero es su derivada
dividida por dos. Conjugar por W prueba (16), incluido el factor y
el signo. Jacobi se conserva exactamente en el dominio común; no
procede de comprobar sólo una matriz finita.

**Distinción necesaria.** Los \(C_N\) son generadores unitarios de
reparametrización sobre semidensidades. No se imponen todos como
restricciones simultáneas sobre la misma representación. De hecho,

\[
 C\Psi=0\quad\Longrightarrow\quad
 C_N\Psi=-\frac{i\hbar}{2}N'\Psi.
 \tag{17}
\]

Imponer todos los \(C_N\Psi=0\) mataría incluso las soluciones no
nulas correctas de (12). El cierre algebraico no autoriza ese paso.

Para un cambio de lapse **positivo**, tómese ahora N suave con
\(0<n_-\le N(r)\le n_+<\infty\), y derivadas regulares. Sea
\(y(r)=\int_0^rN(u)^{-1}du\). Es una coordenada global y
\(U_N f(y)=N(r(y))^{1/2}f(r(y))\) es unitario de L²(dr) a L²(dy).
Así \(p_N=U_N^{-1}(-i\hbar\partial_y)U_N\) y

\[
 C_N=N^{1/2} C N^{1/2},\qquad
 \operatorname{Dom}C_N=WU_N^{-1}H^1(\mathbb R_y;\mathscr K).
 \tag{18}
\]

La igualdad de la primera fórmula se entiende con el dominio
transportado de la segunda. Las soluciones generalizadas son

\[
 \Psi_N(r)=N(r)^{-1/2}e^{-ir\mathbb K/\hbar}\psi_0.
 \tag{19}
\]

Esto demuestra la equivalencia por el peso de semidensidad; no afirma
igualdad literal de núcleos para todos los lapsos. En la realización
escalar ponderada \(L^2(dr/N)\), el operador unitariamente equivalente
es \(NC\), y sus soluciones son (12). El cambio de medida y el cambio
de densidad deben transportarse juntos.

Si una representación interna de Gauss conmuta fuertemente con
\(\mathbb K\), conmuta con W, preserva (11), (15), (18) y reduce
todos estos operadores. Así se conservan las restricciones internas
ya probadas para el reloj suspendido. (16) trata lapsos del único
reloj, no la familia completa de lapsos espaciales independientes.

## 5. Cuadrado variacional exacto y alcance

Las secciones 2–3 prueban el cuadrado de la **misma acción PCH**:
variación → cargo de deformación → Legendre → restricción. La sección
4 prueba el cuadrado de la **misma evolución interactuante**:
suspensión autoadjunta → parametrización → restricción de reloj →
evolución y cambio de densidad. No se igualan ambos Hamiltonianos
por cambiarles el nombre.

Para verificar una identificación concreta entre las dos realizaciones,
sea \(\mathcal R\) el mapa sobre los espacios canónicos reducidos,
con \(\iota_{X_h}\Omega=\mathrm dh\). Defínanse

\[
 \Delta\Omega=\mathcal R^*\Omega_P-\Omega_H,\quad
 \Delta C_N=\mathcal R^*C_P[N]-C_H[N],\quad
 \Delta X_N=X_{P,N}\circ\mathcal R-T\mathcal R\,X_{H,N}.
 \tag{20}
\]

Entonces, como identidad de uno-formas,

\[
 \boxed{\mathrm d\Delta C_N
 =\iota_{X_{H,N}}\Delta\Omega
 +\mathcal R^*(\iota_{\Delta X_N}\Omega_P).}
 \tag{21}
\]

En el último término se evalúa la contracción por el vector a lo largo
de \(\mathcal R\). La prueba es simplemente tirar hacia atrás
\(\mathrm dC_P[N]=\iota_{X_{P,N}}\Omega_P\) y restar la ecuación H.
Si el transporte conserva la forma simpléctica y el campo de
deformación, (21) da \(\mathrm d\Delta C_N=0\); fijar el mismo
borde y una constante de referencia en cada componente conectada
da la igualdad de cargos, ahora demostrada y no postulada.

En una realización cuántica con mapa I y dominio común, el defecto
verificable correspondiente es
\(\Delta_N=C_N^P I-I C_N^H\), y se cumple exactamente

\[
 [C_N^P,C_M^P]I-I[C_N^H,C_M^H]
 =C_N^P\Delta_M-C_M^P\Delta_N
  +\Delta_NC_M^H-\Delta_MC_N^H.
 \tag{22}
\]

Esto localiza el transporte que debe evaluarse para un lapse espacial
concreto, sin negar el transporte TPK ya construido ni afirmar una
ausencia en el corpus. La realización de (11) descarga completamente
este cuadrado para el reloj único porque W es el entrelazador explícito.
No sustituye \(N(x)\) por \(N(r)\) cuando se pide la deformación
normal independiente de cada punto de una hipersuperficie.

Como control negativo de representación: en \(\ell^2(X)\) con medida
de conteo, una permutación continua pretendida
\(V(t)\delta_x=\delta_{\phi_t(x)}\) no es fuertemente continua si
\(\phi_t(x)\ne x\) para tiempos arbitrariamente pequeños, pues la
distancia es \(\sqrt2\). La suspensión utilizada en (11) evita
precisamente ese salto: construye otro portador continuo con frontera
unitaria y conserva la monodromía discreta; no renombra una permutación
discreta como flujo continuo.

## 6. Control focal

[verificar_legendre_reloj.py](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/verificar_legendre_reloj.py>) comprueba mediante aritmética racional
gaussiana el conmutador diferencial (16), la cancelación de los
términos en \(\mathbb K^2\), el signo de (17) y el peso
de (18). Son identidades locales sobre jets polinomiales, prolongables
con funciones de corte; los polinomios de prueba no se presentan como
dominios autoadjuntos. Las pruebas de dominio, de torsión reducida y de
Noether–Legendre están arriba, no en el recuento de controles.
