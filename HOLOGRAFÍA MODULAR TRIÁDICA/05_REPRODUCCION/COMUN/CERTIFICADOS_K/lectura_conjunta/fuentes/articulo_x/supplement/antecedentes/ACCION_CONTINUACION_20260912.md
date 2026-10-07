# Conservación de acción entre formas variables y regímenes tríticos

Continuación matemática, 12 de septiembre de 2026. Los desarrollos precedentes y los PDF permanecen íntegros.

## 1. Construcción recibida y fuentes

APP produce las hojas aditiva y multiplicativa con residuo y cociente; TRIT orienta la emisión y conserva acarreo; TPK selecciona, transporta y actualiza su registro. El estado enriquecido y las cinco operaciones correlativas de su estructura discreta constituyen la base común. Se heredan sus pruebas y mapas de [REFINAMIENTO.md](REFINAMIENTO.md), §§2–7. Las coordenadas numéricas, las formas y los parámetros de acción son lecturas posteriores de ese estado.

La presente construcción compone dos resultados previos: el transporte canónico entre formas del artículo II y el balance de nueve fases. El cambio de forma sucede dentro del balance, manteniendo la orientación y la memoria. Después se obtiene una versión alternante común a los tres regímenes de la identidad de Euler extendida.

Fuentes efectivamente utilizadas:

- [Artículo II, covarianza de la acción](</Users/ruben/Documents/New project/output/APERTURAS_PAPER_RESTAURADAS_20260911_REV03/II_BARBERO_CKM_ACCION/manuscrito/sections/07c_covarianza_accion.tex:19>): forma, transformación canónica y Hamiltoniano; líneas 19, 138 y 180.
- [Artículo II, geometría elíptica](</Users/ruben/Documents/New project/output/APERTURAS_PAPER_RESTAURADAS_20260911_REV03/II_BARBERO_CKM_ACCION/manuscrito/sections/07b_geometria_elipse.tex:81>): ley areal y orientación.
- [Integral, tres generadores y Euler extendido](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/09b_algebras_cuadraticas.tex:289>): operadores concretos, invariantes y exponenciales, líneas 289–520.
- [Integral, factor común y tres regímenes](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/radion_52/snippets/c52_07_01_tres_regimenes.tex:8>): factor \(e^{-x}\), giro, umbral y apertura; parámetros angulares al final del fragmento.
- [Carta nonádica y defecto](</Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/PRIMOS_Y_ZETA_COMPLETO/ampliacion/transporte_y_momentos.tex:55>): composición de nueve fases, proyección y defecto de costura.
- [ACCION.md](ACCION.md), §§2–3: demostración de la carga de Noether y del término de conexión; [CONSERVACION_ESTRUCTURAL.md](CONSERVACION_ESTRUCTURAL.md), §§2–7: balance precedente y alcance analítico.

Procedencia: formas, regímenes, orientación y memoria son resultados recuperados del corpus. Las composiciones y pruebas reunidas aquí son `FORMALIZACION_NUEVA` respecto de este expediente. Su prioridad histórica global permanece sin atribuir.

## 2. Balance entre dos formas de acción

Las salidas angulares \(A,C^*\), en una misma unidad, determinan la forma \(\eta=\operatorname{artanh}(C^*/A)\) sobre el dominio \(A\ne0\), \(|C^*/A|<1\). Recibidas dos formas sucesivas \(\eta_n,\eta_{n+1}\), definimos

\[
M_n=\operatorname{diag}(e^{\eta_n/2},e^{-\eta_n/2}),\qquad
G_n=M_n^{-\mathsf T}M_n^{-1},\qquad
I_n(z)=\tfrac12z^\mathsf TG_nz.
\]

Aquí \(z=(Q,P)^\mathsf T\), con ambas coordenadas de dimensión raíz de acción. La escala \(\hbar\), cuando fija el contorno \(I_n=\hbar\), es la salida de acción previamente construida; no interviene como objetivo de ajuste.

Sea \(R_n\) la rotación canónica del avance angular \(\theta_n\). El transporte sin avance angular y el transporte con dicho avance son, respectivamente,

\[
B_n=M_{n+1}M_n^{-1},\qquad
C_n=M_{n+1}R_nM_n^{-1}.
\tag{1}
\]

Ambos van de la carta \(n\) a la carta \(n+1\). Definimos la lectura comprimida y su registro complementario normalizado:

\[
T_n=\frac{8B_n+C_n}{9},\qquad
D_n=\frac{\sqrt8}{9}(C_n-B_n).
\tag{2}
\]

El operador \(D_n\) es una realización isométricamente normalizada del único patrón de diferencias entre las nueve fases. El registro de nueve componentes es \((8z,-z,\ldots,-z)/27\), con \(z=(C_n-B_n)v\); la suma de sus productos interiores da el mismo factor \(8/81\). Se mantiene el registro de nueve fases cuando las etiquetas individuales intervienen en otros lectores.

**Teorema 1.** Se conserva la acción entre lectura y memoria:

\[
\boxed{G_n=T_n^\mathsf TG_{n+1}T_n+D_n^\mathsf TG_{n+1}D_n.}
\tag{3}
\]

**Prueba.** La normalización de las cartas da
\(B_n^\mathsf TG_{n+1}B_n=G_n=C_n^\mathsf TG_{n+1}C_n\).
Al expandir (2), las contribuciones cruzadas tienen coeficientes \(+8\) y \(-8\). Los coeficientes diagonales restantes son \(72\) para \(B_n\) y \(9\) para \(C_n\), divididos por \(81\). La suma es \(G_n\). ∎

Con \(z_{n+1}=T_nz_n\), \(m_n=D_nz_n\), la forma escalar es

\[
\boxed{I_n(z_n)=I_{n+1}(z_{n+1})+I_{n+1}(m_n).}
\tag{4}
\]

La suma telescópica, reteniendo cada memoria en la carta donde fue emitida, da

\[
I_0(z_0)=I_N(z_N)+\sum_{n=0}^{N-1}I_{n+1}(m_n).
\tag{5}
\]

El transporte \(B_n\) es material en esta composición: sustituirlo por la identidad cuando las formas difieren altera los dominios y puede romper (3).

## 3. Ley exacta de acumulación con fase variable

En coordenadas normalizadas \(y_n=M_n^{-1}z_n\), la lectura es
\(y_{n+1}=(8I+R_n)y_n/9\). Para una rotación plana,

\[
\left(\frac{8I+R_n}{9}\right)^\mathsf T
\left(\frac{8I+R_n}{9}\right)=r_n I,\qquad
r_n=1-\frac{32}{81}\sin^2(\theta_n/2).
\tag{6}
\]

Por tanto,

\[
I_N(z_N)=I_0(z_0)\prod_{n=0}^{N-1}r_n.
\tag{7}
\]

**Teorema 2.** Para \(I_0(z_0)>0\), el terminal tiende a cero exactamente cuando

\[
\sum_{n\ge0}\sin^2(\theta_n/2)=+\infty.
\tag{8}
\]

**Prueba.** Sea \(c=32/81\) y \(u_n=\sin^2(\theta_n/2)\in[0,1]\). Se cumple
\(cu_n\leq-\log(1-cu_n)\leq cu_n/(1-c)\), por integración de \(1/(1-s)\) entre cero y \(cu_n\). La suma de estos logaritmos diverge exactamente cuando diverge \(\sum u_n\). Aplicando el logaritmo al producto de (7), se obtiene la equivalencia. ∎

Se conserva (5) en ambos casos. Una sucesión de avances angulares puede dejar un terminal positivo o transferir toda la acción al registro, según la suma (8). El cambio de forma por sí solo conserva la acción; la dispersión angular determina su reparto en esta realización. Las fases \(\theta_n\) deben proceder del lector concreto de la trayectoria: la prueba no selecciona retrospectivamente una sucesión para imponer un resultado.

## 4. Euler extendido y área orientada común

Los generadores concretos del integral son

\[
J_{+1}=(2C_{A_2}+I)/\sqrt3,\qquad
J_0=N,\qquad
J_{-1}=(2F_{\rm av}^2-3I)/\sqrt5.
\]

En sus cartas bidimensionales tienen traza cero y satisfacen
\(J_\tau^2=-\tau I\). El Coxeter procede del antecedente APP, el nilpotente del transporte de umbral y \(F_{\rm av}\) del descenso de modos TPK. Las funciones exponenciales constituyen la realización analítica posterior:

\[
E_\tau(t)=\exp(tJ_\tau)=c_\tau(t)I+s_\tau(t)J_\tau,
\]

donde \((c_\tau,s_\tau)\) son \((\cos,\sin)\), \((1,t)\) y \((\cosh,\sinh)\), respectivamente. La traza cero da determinante uno. Con

\[
\Omega=\begin{pmatrix}0&1\\-1&0\end{pmatrix},
\]

se obtiene \(E_\tau^\mathsf T\Omega E_\tau=\Omega\). En cartas variables se toma
\(C_n=M_{n+1}E_{\tau_n}(t_n)M_n^{-1}\) y el mismo \(B_n\) de (1).

**Teorema 3.** Los tres regímenes satisfacen

\[
\boxed{\Omega=T_n^\mathsf T\Omega T_n+D_n^\mathsf T\Omega D_n,}
\tag{9}
\]

con \(T_n,D_n\) de (2).

**Prueba.** En dimensión dos, \(L^\mathsf T\Omega L=(\det L)\Omega\). Los determinantes de \(M_n\), \(B_n\) y \(C_n\) son uno. La expansión usada en (3), aplicada a la forma alternante, demuestra (9). ∎

En una carta fija, los dos determinantes son

\[
\det T_\tau=\frac{65+16c_\tau(t)}{81},\qquad
\det D_\tau=\frac{16(1-c_\tau(t))}{81}.
\tag{10}
\]

Esto resulta de \(\det(aI+C)=a^2+a\operatorname{tr}C+\det C\) y \(\operatorname{tr}E_\tau=2c_\tau\). Su suma es uno. En los representantes \(C_{A_2}\), \(I+N\), \(F_{\rm av}^2\), los pares son \((19/27,8/27)\), \((1,0)\), \((89/81,-8/81)\).

El régimen parabólico puede producir una memoria no nula de rango uno con área cero. El hiperbólico conserva área orientada mediante un complemento de signo opuesto. El elíptico permite además el balance positivo de acción de §2. La forma alternante común y las formas métricas de cada régimen mantienen sus tipos respectivos.

### Acción integrada y orientación

Sea \(\gamma\) una curva cerrada a trozos \(C^1\) en el plano canónico. Para cualquier matriz real \(L\) de orden dos,

\[
\oint_{L\gamma}P\,dQ=(\det L)\oint_\gamma P\,dQ.
\]

En efecto, al escribir \(Q'=aQ+bP\), \(P'=cQ+dP\), las integrales de \(Q\,dQ\) y \(P\,dP\) son cero, y \(\oint Q\,dP=-\oint P\,dQ\). Queda el coeficiente \(ad-bc\). Aplicando (10),

\[
\boxed{\oint_\gamma P\,dQ
=\oint_{T_n\gamma}P\,dQ+\oint_{D_n\gamma}P\,dQ.}
\tag{11}
\]

Los signos son los de las curvas transportadas. La identidad se conserva para los tres regímenes y para cambios de forma con determinante uno.

## 5. El factor común del lector exponencial

El propietario radional contiene también \(e^{-x}\exp(-yJ_\tau)\). Se conserva ese factor cuando actúa en el lector. Sea

\[
C_n=e^{-x_n}M_{n+1}E_{\tau_n}(t_n)M_n^{-1}.
\]

Ahora \(C_n^\mathsf T\Omega C_n=e^{-2x_n}\Omega\). La misma expansión da

\[
T_n^\mathsf T\Omega T_n+D_n^\mathsf T\Omega D_n
=\frac{8+e^{-2x_n}}9\Omega.
\tag{12}
\]

Para \(x_n\geq0\), definimos un registro complementario de escala

\[
D_{{\rm esc},n}=\frac{\sqrt{1-e^{-2x_n}}}{3}B_n.
\]

Entonces la identidad completa es

\[
\Omega=T_n^\mathsf T\Omega T_n+D_n^\mathsf T\Omega D_n
+D_{{\rm esc},n}^\mathsf T\Omega D_{{\rm esc},n}.
\tag{13}
\]

Es una composición definida aquí para representar explícitamente el defecto de escala del lector. Su coeficiente procede de (12). No se atribuye a este registro por su nombre una identidad con otro sector físico del corpus; se conserva el mapa para que esa comparación pueda hacerse con sus propietarios.

## 6. Refinamiento de acción sobre las emisiones completas

Para cada prefijo enriquecido \(h\), sea \(M_h\) su carta y \(G_h=M_h^{-\mathsf T}M_h^{-1}\). Para cada emisión superviviente \(\epsilon\), sea \(R_\epsilon\) una rotación realizada y

\[
U_\epsilon=M_{h\epsilon}R_\epsilon M_h^{-1},\qquad
(\mathscr U z)_{h\epsilon}=\sqrt{p_h(\epsilon)}U_\epsilon z_h.
\]

Los pesos proceden de la medida de emisiones de la construcción común; \(\sum_\epsilon p_h(\epsilon)=1\), con multiplicidades preservadas. De \(U_\epsilon^\mathsf TG_{h\epsilon}U_\epsilon=G_h\) se sigue

\[
\sum_{h,\epsilon}I_{h\epsilon}((\mathscr U z)_{h\epsilon})
=\sum_h I_h(z_h).
\tag{14}
\]

La prueba suma primero los pesos de los descendientes de un padre. En una trayectoria, los factores \(M_h^{-1}M_h\) intermedios se cancelan, y las rotaciones se componen en el orden registrado. Esto conserva las etiquetas y la memoria sin mezclar hijos de padres distintos. La forma alternante en suma directa satisface la misma identidad de transporte para los tres regímenes simplécticos, sustituyendo \(R_\epsilon\) por \(E_{\tau_\epsilon}(t_\epsilon)\).

Las completaciones métricas se toman con \(\sum_h z_h^\mathsf TG_hz_h\), de modo que estos mapas son isométricos. Identificar además esa norma con una suma directa euclídea fija requiere cotas uniformes de \(M_h\) y \(M_h^{-1}\); esa identificación adicional no se utiliza en (14).

## 7. Resultado y conservación del alcance

La continuación integra tres hechos demostrados: la acción se distribuye exactamente mientras cambia la forma; las fases controlan la ley de acumulación mediante (6)–(8); y los tres regímenes de Euler comparten el balance de área orientada (9), incluso al variar el régimen en la secuencia. El factor común exponencial tiene su defecto y su registro explícitos en (12)–(13). Los refinamientos conservan las mismas identidades sobre las emisiones generadas.

La conservación positiva, la conservación alternante y la conservación de operadores en el registro tienen demostraciones y dominios propios. Su composición conserva esta información en el mismo desarrollo, sin imponer una métrica positiva única a los tres regímenes ni identificar cifras, registros y estados completos.

El verificador `verificar_continuacion_exacta_20260912.py` contiene ejemplos racionales exactos de los tres regímenes, la forma variable y un control que detecta la omisión de su transporte. Las pruebas de este texto, y no el censo de esos ejemplos, establecen las identidades generales.
