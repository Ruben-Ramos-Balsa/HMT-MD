# Acción, escala de Bohr y cierre orbital

La relación entre acción, estructura fina y escala electrónica se entiende al conservar la secuencia de construcciones de HMT y Mecánica Dimensional. Las lecturas del estado APP–TRIT–TPK proporcionan primero las coordenadas que después intervienen en la respuesta electromagnética, en la acción y en la masa electrónica. La longitud de Bohr se obtiene componiendo esas salidas. Su valor observado no interviene para escoger la acción, la masa ni el acoplamiento.

La diferencia entre valor y estructura adquiere aquí un contenido preciso. La forma de una elipse de acción conserva la separación entre dos modos; su área conserva la acción; y el transductor electromagnético y la masa convierten esa acción en una longitud. Cada paso conserva una información distinta. La relación con Kepler y Sommerfeld aparece al escribir el movimiento central y la acción acumulada en sus ciclos, con sus condiciones de frontera.

## De la forma angular a la acción

Sean \(A\) y \(C^*\) las coordenadas angulares del corpus, en la misma carta y con \(0<C^*<A\). Sea \(R\) el operador que intercambia las hojas, con \(R^2=I\), donde \(I\) es la identidad. El operador positivo
\[
B_1=AI+C^*R
\]
tiene autovalores \(A+C^*\) y \(A-C^*\). La coordenada de forma
\[
\eta_{\mathrm{el}}=\frac12\log\frac{A+C^*}{A-C^*}
\]
registra su asimetría. El subíndice distingue esta coordenada geométrica de la coordenada de retorno utilizada en el refinamiento de acción.

Sea \(\hbar>0\) la sección de acción de retorno utilizada en esta exposición. Mecánica Dimensional lleva la forma anterior a los semiejes
\[
a_S=\sqrt{2\hbar\,e^{\eta_{\mathrm{el}}}},
\qquad
b_S=\sqrt{2\hbar\,e^{-\eta_{\mathrm{el}}}}.
\]
Por multiplicación y división,
\[
a_Sb_S=2\hbar,
\qquad
\frac{a_S}{b_S}=e^{\eta_{\mathrm{el}}}.
\]
La primera igualdad conserva acción y la segunda conserva forma. En esta carta simétrica ambos semiejes tienen dimensión de raíz de acción. Es la razón por la que su producto puede transportarse a una longitud mediante masa y velocidad, mientras un semieje aislado todavía no representa un radio espacial.

Para la parametrización \(Q(\theta)=a_S\cos\theta\), \(P(\theta)=b_S\sin\theta\), la orientación \(dQ\wedge dP\) fija el área barrida:
\[
\begin{aligned}
\mathcal A(\theta)
&=\frac12\int_0^\theta
\left(Q(t)P'(t)-P(t)Q'(t)\right)\,dt\\
&=\frac{a_Sb_S}{2}\int_0^\theta
(\cos^2t+\sin^2t)\,dt
=\hbar\theta.
\end{aligned}
\]
Una vuelta completa contiene \(2\pi\hbar=h\). La acción por unidad de fase y la acción por vuelta son dos lecturas de la misma identidad. Aquí \(\theta\) es el parámetro de fase de la elipse; no se confunde con el ángulo polar de cada punto de una elipse espacial.

La orientación también importa al pasar de área a integral de acción. Con el recorrido anterior, \(\oint P\,dQ=-2\pi\hbar\), mientras el área orientada es positiva. Invertir el recorrido invierte ese signo. La integral canónica de un movimiento orbital se escribirá con su propia orientación dinámica. Así se conserva la acción sin introducir un cambio de signo inadvertido.

## Cómo la acción determina la escala de Bohr

Denotemos por \(q_e\) la magnitud de la carga elemental, para distinguirla del número de Euler \(e\). Sean \(Z_{\mathrm{vac}}\) la impedancia del vacío y \(\varepsilon_{\mathrm{vac}}\) su permitividad en la sección constitutiva escogida. El corpus escribe
\[
q_e^2=\frac{4\pi\alpha_{\mathrm{HMT}}\hbar}{Z_{\mathrm{vac}}},
\qquad
Z_{\mathrm{vac}}c=\varepsilon_{\mathrm{vac}}^{-1}.
\]
La segunda igualdad y la primera producen, sin una nueva selección de coeficientes,
\[
\frac{q_e^2}{4\pi\varepsilon_{\mathrm{vac}}}
=\alpha_{\mathrm{HMT}}\hbar c.
\]
Por tanto, para dos cargas elementales opuestas, la parte eléctrica del potencial es
\[
V_C(r)=-\frac{\mathcal K_C}{r},
\qquad
\mathcal K_C=\alpha_{\mathrm{HMT}}\hbar c.
\]
El coeficiente \(\mathcal K_C\) tiene dimensión de energía multiplicada por longitud. Esta ecuación es el enlace efectivo entre la salida de estructura fina, la acción y la dinámica central. Recuperar \(\alpha_{\mathrm{HMT}}\) despejando esta igualdad sería una comprobación de compatibilidad del recorrido, no otra vía que generase la constante.

Consideremos primero el núcleo inmóvil y la masa electrónica \(m_e\), tomados en la misma sección que \(\hbar\). Para una órbita circular, la ecuación radial y el momento angular \(L_{\mathrm{orb}}\) dan
\[
\frac{m_ev^2}{r}=\frac{\mathcal K_C}{r^2},
\qquad
L_{\mathrm{orb}}=m_evr,
\qquad
r=\frac{L_{\mathrm{orb}}^2}{m_e\mathcal K_C}.
\]
La condición de acción circular \(L_{\mathrm{orb}}=\hbar\) proporciona
\[
a_B=\frac{\hbar^2}{m_e\mathcal K_C}
=\frac{\hbar}{m_ec\alpha_{\mathrm{HMT}}}
=\frac{a_Sb_S}{2m_ec\alpha_{\mathrm{HMT}}}.
\]
La última identidad es justamente el transporte de acción a longitud: la forma de la elipse aporta su producto areal; el acoplamiento fija la intensidad de la respuesta; la masa y la velocidad completan la conversión dimensional.

La misma sustitución conserva la estructura focal de la carta de acción. Si \(d_S\) es la separación entre sus focos,
\[
d_S^2=4(a_S^2-b_S^2)=16\hbar\sinh\eta_{\mathrm{el}},
\]
y, para \(\eta_{\mathrm{el}}>0\),
\[
a_B=\frac{d_S^2}
{16m_ec\alpha_{\mathrm{HMT}}\sinh\eta_{\mathrm{el}}}.
\]
Esta relación utiliza una separación focal cuadrática en una carta de acción, no identifica un foco con la órbita del electrón. En el límite circular \(\eta_{\mathrm{el}}=0\), se emplea la fórmula regular con \(a_Sb_S\), evitando el cociente de dos cantidades nulas.

Si se conserva el movimiento del núcleo, su masa \(M_N\) y la masa electrónica forman la masa reducida
\[
\mu=\frac{m_eM_N}{m_e+M_N}.
\]
El problema relativo tiene entonces la escala \(a_\mu=\hbar/(\mu c\alpha_{\mathrm{HMT}})\). El radio convencional \(a_B\) del atlas utiliza \(m_e\); el reemplazo por \(\mu\) pertenece al problema de dos cuerpos. Esta distinción precisa qué sistema se está describiendo.

## Por qué aparecen las leyes de Kepler

El primer paso del desarrollo central del corpus es una identidad de frontera. Sea un grafo con enlaces orientados en ambos sentidos y sea \(F(x,y)\) un flujo antisimétrico, \(F(y,x)=-F(x,y)\). Al sumar la divergencia sobre una región finita \(S\), cada enlace interior contribuye una vez con cada signo. Sólo permanece el flujo que cruza la frontera:
\[
\sum_{x\in S}\operatorname{div}F(x)
=\operatorname{Flux}_{\partial S}F.
\]
La conservación exterior procede de esta cancelación. Para el cascarón cúbico de radio entero \(R\), el número de enlaces de frontera es \(6(2R+1)^2\). Si \(\mathcal Q\) es el flujo total de la fuente, su reparto medio uniforme y la carta de radio efectivo
\[
4\pi r_{\mathrm{eff}}^2=6(2R+1)^2
\]
dan
\[
\overline F_R
=\frac{\mathcal Q}{6(2R+1)^2}
=\frac{\mathcal Q}{4\pi r_{\mathrm{eff}}^2}.
\]
La cancelación interior, la uniformidad radial y la carta métrica son pasos distintos. La realización isotrópica y el transductor eléctrico o gravitatorio identifican después este flujo con la respuesta central. Mantener esos pasos explícitos explica por qué aparece la potencia inversa del área.

En la realización continua central, \(\mathbf r\) es la posición relativa, \(r=\|\mathbf r\|>0\), \(\mathbf p\) es su momento y \(\mu>0\) la masa reducida. Para un coeficiente atractivo \(\mathcal K>0\), el Hamiltoniano y su ecuación de movimiento son
\[
H=\frac{\|\mathbf p\|^2}{2\mu}-\frac{\mathcal K}{r},
\qquad
\mu\ddot{\mathbf r}=-\frac{\mathcal K}{r^3}\mathbf r.
\]
En la realización eléctrica anterior, \(\mathcal K=\mathcal K_C\). En la gravitatoria de dos cuerpos, \(\mathcal K=Gm_1m_2\). El carácter central de la fuerza conserva el vector momento angular
\[
\mathbf L=\mu\,\mathbf r\times\dot{\mathbf r}.
\]
Cuando \(L_{\mathrm{orb}}=\|\mathbf L\|>0\), ese vector fija el plano del movimiento. Sea \(\psi\) su ángulo polar y sea \(u=1/r\). La conservación \(L_{\mathrm{orb}}=\mu r^2\dot\psi\) transforma la ecuación radial en la ecuación de Binet
\[
\frac{d^2u}{d\psi^2}+u
=\frac{\mu\mathcal K}{L_{\mathrm{orb}}^2}.
\]
Su solución es
\[
r(\psi)=\frac{p_{\mathrm{orb}}}
{1+\epsilon_{\mathrm{orb}}\cos(\psi-\psi_0)},
\qquad
p_{\mathrm{orb}}=\frac{L_{\mathrm{orb}}^2}{\mu\mathcal K}.
\]
Aquí \(\epsilon_{\mathrm{orb}}\) es la excentricidad orbital y \(\psi_0\) fija la dirección del periastro. La letra \(e\) queda reservada al número de Euler. Para energía negativa y movimiento no radial, \(0\leq\epsilon_{\mathrm{orb}}<1\): la trayectoria es una elipse, con la circunferencia como caso límite.

La segunda ley se sigue directamente de la conservación de \(L_{\mathrm{orb}}\):
\[
\frac{dA_{\mathrm{orb}}}{dt}
=\frac12r^2\dot\psi
=\frac{L_{\mathrm{orb}}}{2\mu}.
\]
Sean \(a\) y \(b=a\sqrt{1-\epsilon_{\mathrm{orb}}^2}\) sus semiejes espaciales. Como \(p_{\mathrm{orb}}=a(1-\epsilon_{\mathrm{orb}}^2)\), el período satisface
\[
T=\frac{2\pi ab\,\mu}{L_{\mathrm{orb}}},
\qquad
T^2=\frac{4\pi^2\mu}{\mathcal K}a^3.
\]
Así aparece la tercera ley. La elipse, el barrido areal uniforme y la relación entre período y semieje son consecuencias encadenadas de la ecuación central, no tres semejanzas geométricas independientes.

## Las acciones de la órbita elíptica

El paso de Sommerfeld consiste en leer los ciclos por la acción acumulada. Para hacer explícita esa lectura, en el plano orbital escribimos el Hamiltoniano anterior como
\[
H=\frac{p_r^2}{2\mu}
+\frac{L_{\mathrm{orb}}^2}{2\mu r^2}
-\frac{\mathcal K}{r}.
\]
El momento radial es \(p_r\), y la energía ligada \(E<0\) determina
\[
a=-\frac{\mathcal K}{2E},
\qquad
L_{\mathrm{orb}}^2=\mu\mathcal K a(1-\epsilon_{\mathrm{orb}}^2).
\]
En el dominio orbital ligado se cumple \(0<L_{\mathrm{orb}}^2\leq\mu\mathcal K a\), de modo que \(0\leq\epsilon_{\mathrm{orb}}<1\). La acción angular y la acción de una oscilación radial completa son
\[
J_\psi=2\pi L_{\mathrm{orb}},
\qquad
J_r=2\int_{r_-}^{r_+}
\sqrt{2\mu\left(E+\frac{\mathcal K}{r}\right)
-\frac{L_{\mathrm{orb}}^2}{r^2}}\,dr,
\]
con \(r_\pm=a(1\pm\epsilon_{\mathrm{orb}})\). Este cálculo desarrolla las integrales del problema central; no introduce otra constante.

La sustitución \(r=a(1-\epsilon_{\mathrm{orb}}\cos u)\), \(0\leq u\leq\pi\), produce
\[
J_r=2\sqrt{\mu\mathcal K a}
\int_0^\pi
\frac{\epsilon_{\mathrm{orb}}^2\sin^2u}
{1-\epsilon_{\mathrm{orb}}\cos u}\,du.
\]
El integrando se descompone exactamente como
\[
\frac{\epsilon_{\mathrm{orb}}^2\sin^2u}
{1-\epsilon_{\mathrm{orb}}\cos u}
=1+\epsilon_{\mathrm{orb}}\cos u
-\frac{1-\epsilon_{\mathrm{orb}}^2}
{1-\epsilon_{\mathrm{orb}}\cos u}.
\]
Además, la sustitución \(t=\tan(u/2)\) demuestra
\[
\int_0^\pi\frac{du}{1-\epsilon_{\mathrm{orb}}\cos u}
=2\int_0^\infty
\frac{dt}{(1-\epsilon_{\mathrm{orb}})
+(1+\epsilon_{\mathrm{orb}})t^2}
=\frac{\pi}{\sqrt{1-\epsilon_{\mathrm{orb}}^2}}.
\]
Por tanto,
\[
J_r=2\pi\left(\sqrt{\mu\mathcal K a}-L_{\mathrm{orb}}\right),
\qquad
J_r+J_\psi=2\pi\sqrt{\mu\mathcal K a}.
\]
La suma fija el tamaño de la órbita y su energía; el reparto entre acción radial y angular fija la excentricidad. En el límite circular \(J_r=0\). Para una órbita elíptica no circular ambas acciones quedan diferenciadas. Éste es un ejemplo concreto de cómo un valor total conserva menos información que su descomposición en ciclos.

## Sommerfeld: cierre de fase y memoria de la vuelta

Sea \(\gamma\) un ciclo orientado y \(J_\gamma=\oint_\gamma\mathbf p\cdot d\mathbf q\) su acción. Sea \(\varepsilon_\gamma\in\{+1,-1\}\) la holonomía de signo de la línea transportada: registra si la vuelta restituye la orientación de esa línea o la invierte. En la realización semiclásica escrita por el corpus, el cierre exige
\[
\varepsilon_\gamma
\exp\!\left(i\frac{J_\gamma}{\hbar}\right)=1.
\]
Con holonomía positiva, la acción pertenece a \(2\pi\hbar\mathbb Z\); con holonomía negativa, pertenece a \(2\pi\hbar(\mathbb Z+\tfrac12)\). El semientero procede de compensar el signo transportado. La condición registra la memoria de la vuelta, además de la acción acumulada.

En el sector de holonomía trivial y con la regla de acciones de Sommerfeld sin términos de Maslov añadidos, escribimos
\[
J_r=2\pi\hbar n_r,
\qquad
J_\psi=2\pi\hbar n_\psi,
\qquad
n=n_r+n_\psi,
\]
donde \(n_r\geq0\) y \(n_\psi>0\) son enteros de acción. La evaluación anterior da
\[
a=\frac{\hbar^2n^2}{\mu\mathcal K},
\qquad
E=-\frac{\mu\mathcal K^2}{2\hbar^2n^2},
\qquad
\epsilon_{\mathrm{orb}}^2=1-\frac{n_\psi^2}{n^2}.
\]
Al sustituir \(\mathcal K_C=\alpha_{\mathrm{HMT}}\hbar c\),
\[
a=n^2\frac{\hbar}{\mu c\alpha_{\mathrm{HMT}}},
\qquad
E=-\frac{\mu c^2\alpha_{\mathrm{HMT}}^2}{2n^2}.
\]
El caso circular \(n_r=0,n_\psi=1\), con núcleo inmóvil, recupera exactamente la escala \(a_B\) obtenida antes. La excentricidad depende del reparto de acciones, mientras el tamaño depende de su suma.

Este cálculo identifica con precisión el contenido utilizado de Sommerfeld: la condición sobre ciclos convierte la acción en una selección de órbitas del problema central. Los enteros de acción aquí empleados no se identifican automáticamente con todos los números cuánticos de un operador atómico tridimensional. La realización con espín, correcciones relativistas e índices de Maslov debe conservar sus propios operadores y condiciones, sin contar dos veces una misma fase. El resultado anterior es el del Hamiltoniano central no relativista y del cierre declarado.

## En qué sentido \(\alpha\) es un cierre de frontera

El cierre orbital utiliza \(\alpha_{\mathrm{HMT}}\) después de su generación. Su cierre generativo ocurre antes, en el registro dodecafásico del estado enriquecido. Esta diferencia permite conectar ambos desarrollos sin que la órbita seleccione retroactivamente la constante.

El registro firmado y el bloque terminal conservan lecturas distintas del mismo estado TPK. El transporte de las historias, la extracción de los canales \(90/120\) y la transformación armónica producen el registro firmado; la inversión integral de sus bloques de Hadamard determina el sello \(K\). En la ventana dodecafásica, sean \(P_m,E_m,\Phi_m\) los bloques en base mil de las tres coordenadas HMT ya generadas, \(K_m\) los bloques del sello, \(A_m\) los de la salida y \(c_m\) los acarreos. La ley es
\[
P_m+E_m-\Phi_m-K_m+c_{m+1}
=A_m+1000c_m,
\qquad 1\leq m\leq12.
\]
El extremo derecho fija \(c_{13}=0\); el extremo izquierdo del cierre publicado satisface \(c_1=0\). Al multiplicar por \(1000^{12-m}\) y sumar, los términos interiores de acarreo se cancelan. Si
\[
\iota(v)=\sum_{m=1}^{12}v_m1000^{12-m},
\]
se obtiene
\[
\iota(P)+\iota(E)-\iota(\Phi)-\iota(K)-\iota(A)
=1000^{12}c_1-c_{13}=0.
\]
La frontera decide cómo se cierra la lectura global de la cadena. El acarreo participa en cada paso y su contribución interior se reorganiza en los extremos. Ése es un sentido matemático explícito de cierre de borde: una identidad local transportada determina una identidad global con extremos controlados.

La operación se invierte, conservando sus datos:
\[
K_m=P_m+E_m-\Phi_m+c_{m+1}-A_m-1000c_m.
\]
La reversibilidad pertenece a esa fibra, con los canales y la frontera especificados. Sustituir la cadena con extremo por un ciclo periódico cambiaría el problema de acarreos. La memoria de retorno y la condición de extremo han de conservarse juntas.

La sección de las dos vías distingue esta lectura dodecafásica de la lectura analítica de vacancias. La segunda comienza por el núcleo
\[
\begin{aligned}
P_6(x)={}&2\pi_{\mathrm{HMT}}x-\frac74x^2
+\frac{x^3}{2\pi_{\mathrm{HMT}}}
+\frac{x^4}{20}-\frac{2x^5}{21}-\frac{x^6}{46},\\
P_9(x)={}&P_6(x)-\frac{x^7}{120}
+\frac{x^8}{45}+\frac{2x^9}{495},
\end{aligned}
\]
y por la ecuación \(P_9(x)=\log_{10}(10/9)\) en el intervalo \(0<x<10^{-2}\). Los coeficientes de la prolongación escrita conservan la semicorona de fase, el determinante \(45\) del bloque central y el rango transversal \(11\), con \(495=45\cdot11\). El cuerpo de las dos vías distingue el testigo de orden nueve del sistema completo de prolongaciones.

En ese cuerpo, la identidad completa se formula mediante la compatibilidad de los dos sistemas a cada profundidad: ambos determinan los mismos cilindros supervivientes \(C_N^\alpha\), y sus diámetros tienden a cero. El cierre no se define por un número fijo de cifras. La formulación es
\[
\alpha_A=\alpha_B=\alpha_{\mathrm{HMT}},
\]
con una lectura dodecafásica y otra analítica del mismo desarrollo genealógico. Al reutilizar esa formulación, deben acompañarla sus mapas de prolongación y sus condiciones de compatibilidad; una tabla decimal por sí sola no sustituye esas condiciones.

Las dos vías de \(\alpha\) no se identifican aquí con las acciones radial y angular de una órbita. La conexión demostrada en esta exposición es la composición posterior: la salida \(\alpha_{\mathrm{HMT}}\) entra en \(\mathcal K_C=\alpha_{\mathrm{HMT}}\hbar c\); ese coeficiente entra en la ecuación central; las acciones de sus ciclos y la holonomía fijan el cierre orbital. La frontera generativa, el coeficiente de interacción y el cierre del ciclo conservan así su orden y su función.

El conjunto da una explicación más precisa que la yuxtaposición de constantes. El mismo desarrollo coordina forma, acción, respuesta del vacío, intensidad eléctrica, masa y escala orbital. Kepler expresa las consecuencias de la dinámica central; Sommerfeld añade la lectura de sus ciclos por acción; Bohr aparece como una escala particular de esa composición. El producto \(a_Sb_S\) es el punto de enlace que permite seguir esa cadena sin confundir las geometrías ni borrar la memoria de sus construcciones.
